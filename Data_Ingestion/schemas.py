from pydantic import BaseModel, EmailStr, field_validator
import re
import pandas as pd
import logging

class Book(BaseModel):
    title: str
    author: str
    isbn: str

    @field_validator ('isbn')
    def validate_isbn(cls, v):
        cleaned = v.replace("-", "").replace(" ", "")
        if len(cleaned) not in (10, 13) or not cleaned.isdigit():
            raise ValueError("Invalid ISBN format. Must be ISBN-10 or ISBN-13")
        return cleaned

class Author(BaseModel):
    name: str
    email: EmailStr

    @field_validator ('name')
    def normalize_name(cls, v):
        return v.strip().title()

class Member(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @field_validator('name')
    def normalize_member_name(cls, v):
        return v.strip().title()

    @field_validator('phone')
    def normalize_phone(cls, v):
        digits = re.sub(r'\D', '', v)
        if len(digits) == 10:
            return f'+91-{digits[:3]}-{digits[3:6]}-{digits[6:]}'
        elif len(digits) == 12 and digits.startswith('91'):
            return f'+91-{digits[2:5]}-{digits[5:8]}-{digits[8:]}'
        else:
             raise ValueError('Invalid phone number format')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format="%(message)s")

    df = pd.read_csv("members.csv")
    valid_members = []
    errors = []

    for index, row in df.iterrows():
        try:
            member = Member(**row.to_dict())
            valid_members.append(member)
        except Exception as e:
            errors.append((index + 1, str(e)))

    logging.info("\n Valid Members:")
    for m in valid_members:
        logging.info(m)

    logging.info("\n Errors:")
    for i, e in errors:
        logging.info(f"Row {i}: {e}")

    df_books = pd.read_csv("books.csv")
    valid_books = []
    book_errors = []

    for index, row in df_books.iterrows():
        try:
            book = Book(**row.to_dict())
            valid_books.append(book)
        except Exception as e:
            book_errors.append((index + 1, str(e)))

    logging.info("\n Valid Books:")
    for b in valid_books:
        logging.info(b)

    logging.info("\n Book Errors:")
    for i, e in book_errors:
        logging.info(f"Row {i}: {e}")

    df_authors = pd.read_csv("authors.csv")
    valid_authors = []
    author_errors = []

    for index, row in df_authors.iterrows():
        try:
            author = Author(**row.to_dict())
            valid_authors.append(author)
        except Exception as e:
            author_errors.append((index + 1, str(e)))

    logging.info("\n Valid Authors:")
    for a in valid_authors:
        logging.info(a)

    logging.info("\n Author Errors:")
    for i, e in author_errors:
        logging.info(f"Row {i}: {e}")

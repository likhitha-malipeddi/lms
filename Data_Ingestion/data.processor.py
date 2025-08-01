import argparse
import os
import pandas as pd
import logging
from sqlalchemy.exc import IntegrityError

from schemas import MemberSchema, AuthorSchema, BookSchema, LibrarySchema
from models import Member, Author, Book, Library, Base
from database import get_engine, get_session

def setup_logging(level):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s"
    )

def process_csv(file_path, schema_class, model_class, session, unique_field=None)
    df = pd.read_csv("csv_data/members.csv")
    success, failed = 0, 0

    for index, row in df.iterrows():
        try:
            validated = schema_class(**row.to_dict())

            if unique_field:
                existing = session.query(model_class).filter(
                    getattr(model_class, unique_field) == getattr(validated
                ).first()
                if existing:
                    logging.info(f"Duplicate skipped (row {index + 1}): {getattr(validated, unique_field)}")
                    continue

            record = model_class(**validated.dict())
            sesion.add(record)
            success += 1

        except Exception as e:
            logging.warning(f"Row {index + 1} skipped in {file_path}: {e}")
            failed += 1

    try:
        session.commit()
    except IntegrityError as e:
        logging.error(f"Database error: {e}")
        session.rollback()

    logging.info(f"[{model_class._name_}] {success} added, {failed} skipped.")

def main():
    parser = argparse.ArgumentParser(description="Library ETL Data Processor")
    parser.add_argument('--directory', '-d', required=True, help="Path to CSV data folder")
    parser.add_argument('--db', required=True, help="PostgreSQL database URL")
    parser.add_argument('--log-level', default='INFO', help="Log level: DEBUG, INFO, WARNING, ERROR")
    args = parser.parse_args()

    setup_logging(args.log_level)

    engine = get_engine(args.db)
    Base.metadata.create_all(engine)
    session = get_session(engine)

    processors = [
        ("members.csv", MemberSchema, Member, 'email'),
        ("auhtors.csv", AuthorSchema, Author, 'name'),
        ("libraries.csv", LibrarySchema, Library, 'email'),
        ("books.csv", BookSchema, Book, 'isbn'),
    ]

    for file_name, schema, model, unique_field in processors:
        full_path = os.path.join(args.directory, file_name)
        if os.path.exists(full_path):
            logging.info(f" Processing: {file_name}")
            process_csv(full_path, schema, model, session, unique_field)
        else:
            logging.warning(f" File not found: {file_name}")

if __name__ == "__main__":
    main()

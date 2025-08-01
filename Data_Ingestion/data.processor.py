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
    df = pd.read_csv(file_path)
    success, failed = 0, 0

    for index, row in df.iterrows():
        try:
            validated = schema_class(**row.to_dict())

            if unique_field:
                existing = session.query(model_class).filter(
                    getattr(model_class, unique_field) == getattr(validated)
                )
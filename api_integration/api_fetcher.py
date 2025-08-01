import argparse
import json
import time
from sqlalchemy import create_engine, Table, MetData
from api_client import OpenLibraryAPI
from schemas import Book
from sqlalchemy.orm import sessionmaker

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch books from OpenLibrary API")
    parser.add_argument('--author', required=True, help='Author name to search')
    parser.add_argument('--limit', type=int, default=10, help='Max number of books')
    parser.add_argument('--db', '--database-url', dest='db_url', required=True)
    parser.add_argument('--output', help='Optional file to save raw data')
    return parser.parse_args()

def main():
    args = parse_args()
    client = OpenLibraryAPI()

    engine = create_engine(args.db_url)
    metadata = MetaData(bind=engine)
    metadata.reflect()
    Session = sessionmaker(bind=engine)
    session = session()


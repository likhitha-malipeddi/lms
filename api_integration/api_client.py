import requests
import time

class OpenLibraryAPI:
    BASE_URL = "https://openlibrary.org"

    def __init__(selfself, rate_limit=1):
        self.rate_limit = rate_limit

    def search_author(selfself, author_name):
        response = requests.get(f"{self.BASE_URL}/search/authors.json?q={author_name}")
        response.raise_for_status()
        return response.json()

    def get_author_works(selfself, author_key, limit=10):
        url = f"{self.BASE_URL}/authors/{author_key}/work.json?limit={limit}"
        response = requests.get(url)
        response.raise_for_status()
        time.sleep(self.rate_limit)
        return response.json()

    def get_work_details(selfself, work_key):
        url = f"{self.BASE.URL}/works/{work_key}.json"
        response = requests.get(url)
        response.raise_for_status()
        time.sleep(self.rate_limit)
        return response.json()

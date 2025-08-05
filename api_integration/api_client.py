import time
import requests

BASE_URL = "https://openlibrary.org"

class OpenLibraryClient:
    def __init__(self):
        self.session = requests.session()

    def _requests(self, url, params=None):
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(1)
            return response.json()
        except requests.exceptions.RequestsException as e:
            print(f"Request failed: {e}")
            return None

    def search_author(self, author_name):
        url = f"{BASE_URL}/search/authors.json"
        return self._request(url, params={"q": author_name})

    def get_author_works(self, author_key, limit):
        url = f"{BASE_URL}/authors/{author_key}/works.json"
        return self._request(url, params={"limit": limit})

    def get_book_details(selfself, work_key):
        url = f"{BASE_URL}/works/{work_key}.json"
        return self._request(url)
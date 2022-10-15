## https://www.googleapis.com/books/v1/volumes?q=
"""
This class uses the Google book api *(https://www.googleapis.com/books/v1/volumes?q=)
"""
import requests
import json

class GoogleBookApi():
    def __init__(self, base_url) -> None:
        self.baseUrl = base_url
        pass

    def searchBookByTitle(self, title):
        """
        This method returns book json data from request response
        params
        title (string): book title
        """
        apiUrl = self.baseUrl + title
        result = requests.get(apiUrl)
        return json.loads(result.text)

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
    
    def searchBookByISBN13(self, isbn13):
        # https://www.googleapis.com/books/v1/volumes?q=isbn:9780385504201
        apiUrl = self.baseUrl + "isbn:" + isbn13
        result = requests.get(apiUrl)
        return json.loads(result.text)
from math import fabs
from django.shortcuts import render
from django.http import HttpResponse
from booklibraryapp.googlebookapi import GoogleBookApi
from .models import Profile
# Create your views here.
def index(request):
    if request.user:
        currentUserProfile = Profile.objects.filter(user=request.user)[0]

    context = {
        'currentUserProfile': currentUserProfile
    }
    return render(request, "booklibrary/index.html", context)

def toReadList(request):
    return render(request, "booklibrary/toReadList.html")

def findaBook(request):
    searchBooksResult=""
    baseurl = "https://www.googleapis.com/books/v1/volumes?q="
    googleApi = GoogleBookApi(baseurl)
    if 'searchBooksByTitleQuery' in request.GET:
        bookSearchTitle = request.GET['searchBooksByTitleQuery']
        # bookSearchTitle = request.GET['bookTitleSearchInputID']
        searchBooksResult = googleApi.searchBookByTitle(bookSearchTitle)
    # searchBooksResult['items'][0]['volumeInfo']['imageLinks']['thumbnail']
    context = {
        'searchBooksResult': searchBooksResult['items'] if searchBooksResult else ""
    }
    return render(request, "booklibrary/findaBook.html", context)

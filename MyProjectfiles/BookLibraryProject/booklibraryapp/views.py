from distutils.log import debug
from django.shortcuts import redirect, render
from django.http import HttpResponse
from booklibraryapp.googlebookapi import GoogleBookApi
from .models import BooksLibrary, Profile
from .forms import MoveToToReadListForm
import math
# Create your views here.
def index(request):
    if request.user:
        currentUserProfile = Profile.objects.filter(user=request.user)[0]

    context = {
        'currentUserProfile': currentUserProfile
    }
    return render(request, "booklibrary/index.html", context)

def toReadList(request):
    """
    userToReadList - list of isbn13 of books in the toReadList of the current user
    """
    userToReadList = []
    userToReadBooksJsonList = []
    if request.user:
        userprofile = Profile.objects.filter(user = request.user.id)[0]
        userToReadList = BooksLibrary.objects.filter(toReadList=True)
    else:
        userprofile = ''
    baseurl = "https://www.googleapis.com/books/v1/volumes?q="
    googleApi = GoogleBookApi(baseurl)
    for isbn13 in userToReadList:
        bookJson = googleApi.searchBookByISBN13(str(isbn13))
        
        try:
            userToReadBooksJsonList.append(bookJson['items'])
        except:
            pass
    context = {
        'userToReadList': userToReadList,
        'userToReadBooksJsonList': userToReadBooksJsonList,
    }
    print(userToReadList, "count")
    return render(request, "booklibrary/toReadList.html", context)

def bookSideDescription(request, pk):
    # pk is isbn13
    userToReadList = []
    userToReadBooksJsonList = []
    if request.user:
        userprofile = Profile.objects.filter(user = request.user.id)[0]
        userToReadList = BooksLibrary.objects.filter(userProfile = userprofile, toReadList=True)
    else:
        userprofile = ''
    baseurl = "https://www.googleapis.com/books/v1/volumes?q="
    googleApi = GoogleBookApi(baseurl)
    selectedBook = googleApi.searchBookByISBN13(pk)
    pages = selectedBook['items'][0]['volumeInfo']['pageCount']
    # tip (time investment prediction)
    total_hourse_needed = (int(pages)*2.9)/100
    time_per_day = 2
    days_needed = math.ceil(total_hourse_needed/time_per_day)
    tip_calculation = str(days_needed)
    for isbn13 in userToReadList:
        bookJson = googleApi.searchBookByISBN13(str(isbn13))
        try:
            userToReadBooksJsonList.append(bookJson['items'])
        except:
            pass
    context = {
        'userToReadList': userToReadList,
        'userToReadBooksJsonList': userToReadBooksJsonList,
        'selectedBook': selectedBook,
        'tip_calculation': tip_calculation,
    }
    return render(request, "booklibrary/bookDescription.html", context)

def searchDetailView(request, pk):
    userToReadList = []
    userToReadBooksJsonList = []
    if request.user:
        userprofile = Profile.objects.filter(user = request.user.id)[0]
        userToReadList = BooksLibrary.objects.filter(userProfile = userprofile, toReadList=True)
    else:
        userprofile = ''
    baseurl = "https://www.googleapis.com/books/v1/volumes?q="
    googleApi = GoogleBookApi(baseurl)
    selectedBook = googleApi.searchBookByISBN13(pk)
    pages = selectedBook['items'][0]['volumeInfo']['pageCount']
    # tip (time investment prediction)
    total_hourse_needed = (int(pages)*2.9)/100
    time_per_day = 2
    days_needed = math.ceil(total_hourse_needed/time_per_day)
    tip_calculation = str(days_needed)
    for isbn13 in userToReadList:
        bookJson = googleApi.searchBookByISBN13(str(isbn13))
        try:
            userToReadBooksJsonList.append(bookJson['items'])
        except:
            pass
    context = {
        'userToReadList': userToReadList,
        'userToReadBooksJsonList': userToReadBooksJsonList,
        'selectedBook': selectedBook,
        'tip_calculation': tip_calculation,
    }
    return render(request, "booklibrary/searchDetailView.html", context)

def findaBook(request):
    searchBooksResult=""
    baseurl = "https://www.googleapis.com/books/v1/volumes?q="
    googleApi = GoogleBookApi(baseurl)
    if request.user: #authenticate here
        print("checked user")
        userprofile = Profile.objects.filter(user = request.user.id)[0]

    if 'searchBooksByTitleQuery' in request.GET:
        bookSearchTitle = request.GET['searchBooksByTitleQuery']
        # bookSearchTitle = request.GET['bookTitleSearchInputID']
        searchBooksResult = googleApi.searchBookByTitle(bookSearchTitle)
    # searchBooksResult['items'][0]['volumeInfo']['imageLinks']['thumbnail']

    if request.method == 'POST':
        print("post request")
        form = MoveToToReadListForm(request.POST)
        # if form.is_valid():
        #     print("Form is valid")
        #     # obj = form.save(commit=False)
        #     # obj.userProfile = userprofile
        #     # obj.bookISBN13 = pk
        #     # obj.save()

    else:
        form = MoveToToReadListForm()
    context = {
        'searchBooksResult': searchBooksResult['items'] if searchBooksResult else "",
        'form': form
    }

    return render(request, "booklibrary/findaBook.html", context)

def test(request):
    print("helloooooooo")
    return render(request, "booklibrary/random.html")



def addToReadingList(request, pk):
    """
    pk: is the isbn13 of the book
    """
    print("Adding to read list")
    if request.user: #authenticate here
        print("checked user")
        userprofile = Profile.objects.filter(user = request.user.id)[0]

    if request.method == 'POST':
        print("post request")
        form = MoveToToReadListForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            obj = form.save(commit=False)
            obj.userProfile = userprofile
            obj.bookISBN13 = pk
            obj.save()

    else:
        form = MoveToToReadListForm()

    # if request.method == 'POST':
    #     print('Got request')
    #     # bookISPN13 = request.GET['searchBooksByTitleQuery1']
    #     form = MoveToToReadListForm(request.POST)
    #     if form.is_vaid:
    #         obj = form.save(commit=False)
    #         obj.userProfile = userprofile
    #         obj.bookISBN13 = pk
    #         obj.save()
            
    #         print("form is valid and added element")
    # #         # return redirect('')

    return render(request, "booklibrary/addtoreadinglist.html")


# used for updating status
def completedReading(request, pk):
    """
    pk: is the isbn13 of the book
    """
    bookInList = BooksLibrary.objects.get(id=pk)
    if request.method == 'POST':
        form = MoveToToReadListForm(request.POST, instance=bookInList)
        if form.is_vaid:
            obj = form.save(commit=False)
            obj.toReadList = True
            obj.save()
            # return redirect('')

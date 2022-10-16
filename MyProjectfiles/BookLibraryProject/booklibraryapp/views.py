from distutils.log import debug
from django.shortcuts import redirect, render
from django.http import HttpResponse
from booklibraryapp.googlebookapi import GoogleBookApi
from .models import BooksLibrary, Profile
from .forms import MoveToToReadListForm
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
        userToReadList = BooksLibrary.objects.filter(userProfile = userprofile, toReadList=True)
    else:
        userprofile = ''
    baseurl = "https://www.googleapis.com/books/v1/volumes?q="
    googleApi = GoogleBookApi(baseurl)
    for isbn13 in userToReadList:
        bookJson = googleApi.searchBookByISBN13(str(isbn13))
        userToReadBooksJsonList.append(bookJson['items'])
    context = {
        'userToReadList': userToReadList,
        'userToReadBooksJsonList': userToReadBooksJsonList,
    }
    return render(request, "booklibrary/toReadList.html", context)

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

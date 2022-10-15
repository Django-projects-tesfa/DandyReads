from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, "booklibrary/index.html")

def toReadList(request):
    return render(request, "booklibrary/toReadList.html")

def findaBook(request):
    return render(request, "booklibrary/findaBook.html")

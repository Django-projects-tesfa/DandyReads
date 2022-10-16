from dataclasses import field
from django import forms
from .models import BooksLibrary
from django import forms

class MoveToToReadListForm(forms.ModelForm):
    class Meta:
        model = BooksLibrary
        fields = ['bookISBN13']

class StartReadingBook(forms.ModelForm):
    class Meta:
        model = BooksLibrary
        fields = []
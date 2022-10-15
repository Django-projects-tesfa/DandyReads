from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='booklibrary'),
    path('toreadlist', views.toReadList, name='toreadlist'),
    path('findabook', views.findaBook, name='findabook')
]
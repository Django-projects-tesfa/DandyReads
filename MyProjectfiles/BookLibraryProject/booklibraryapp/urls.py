from site import venv
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='booklibrary'),
    path('toreadlist', views.toReadList, name='toreadlist'),
    path('findabook', views.findaBook, name='findabook'),
    path('addtoreadinglist/<str:pk>/', views.addToReadingList, name="addtoreadinglist"),
    path('bookdescription/<str:pk>/', views.bookSideDescription, name="bookdescription"),
    path('searchdetailview/<str:pk>/', views.searchDetailView,name="searchdetailview"),
    path('test', views.test, name='test')
]
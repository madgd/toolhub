from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'add_book$', add_book, ),
    url(r'show_books$', show_books, ),
]
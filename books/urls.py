from django.urls import include, path
from rest_framework import routers
from . import views

routeList = (
    (r'publishers', views.PublisherViewSet),
    (r'authors', views.AuthorViewSet),
    (r'genres', views.GenreViewSet),
    (r'books', views.BookViewSet)
)
from django.urls import include, path
from rest_framework import routers
from . import views

routeList = (
    (r'products', views.ProductViewSet),
    (r'categories', views.CategoryViewSet),
    (r'brands', views.BrandViewSet)
)
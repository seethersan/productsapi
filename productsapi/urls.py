"""productsapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from products.views import Products, ProductsInsert
from users.views import Users, UserInsert
from books.views import Books, BookInsert
from core.views import HealthCheck

urlpatterns = [
    path('', HealthCheck.as_view(), name="healtcheck"),
    path('admin/', admin.site.urls),
    path('api/', include([
        path('products/', include([
            path('', Products.as_view(), name="products"),
            path('bulk_insert', ProductsInsert.as_view(), name="products_insert")
        ])),
        path('users/', include([
            path('', Users.as_view(), name="users"),
            path('bulk_insert', UserInsert.as_view(), name="users_insert")
        ])),
        path('books/', include([
            path('', Books.as_view(), name="books"),
            path('bulk_insert', BookInsert.as_view(), name="books_insert")
        ]))
    ])),
]

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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from products import urls as products_urls
from books import urls as books_urls
from users.views import UserProfileAPIView
from core.views import HealthCheck

schema_view = get_schema_view(
   openapi.Info(
      title="Backend API",
      default_version='v1',
      description="Backend API for Android App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="carlos_jcez@hotmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

routeLists = [
    products_urls.routeList,
    books_urls.routeList,
]

router = routers.DefaultRouter()
for routeList in routeLists:
    for route in routeList:
        router.register(route[0], route[1])

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', HealthCheck.as_view(), name="healtcheck"),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/me', UserProfileAPIView.as_view(), name='my_profile'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

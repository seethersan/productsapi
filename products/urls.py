from . import views

routeList = (
    (r'products', views.ProductViewSet),
    (r'categories', views.CategoryViewSet),
    (r'brands', views.BrandViewSet)
)
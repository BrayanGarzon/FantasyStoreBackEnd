from django.urls import path, include
from rest_framework import routers
from .api import CategoriesApiView, ProductsApiView

categoriesRouter = routers.DefaultRouter()
productsRouter = routers.DefaultRouter()

categoriesRouter.register(r'categories', CategoriesApiView, basename='categories')
productsRouter.register(r'products', ProductsApiView, basename='products')
apiurls = ([
    path("categories/", include(categoriesRouter.urls)),
    path("products/", include(productsRouter.urls)),
], 'products')
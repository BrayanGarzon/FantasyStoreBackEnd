from django.urls import path, include
from rest_framework import routers
from .api import CategoriesApiView

categoriesRouter = routers.DefaultRouter()

categoriesRouter.register(r'categories', CategoriesApiView, basename='categories')

apiurls = ([
    path("categories/", include(categoriesRouter.urls) ),
], 'products')
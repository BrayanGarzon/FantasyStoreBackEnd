from django.urls import path, include
from rest_framework import routers
from .api import CategoriesApiView, ProductsApiView, ReleasesProductsApiView, ReleasesProductsLastReleaseApiView, ProductReleasesApiView, ProductFavoriteApiView

categoriesRouter = routers.DefaultRouter()
productsRouter = routers.DefaultRouter()
releasesProductsRouter = routers.DefaultRouter()

categoriesRouter.register(r'categories', CategoriesApiView, basename='categories')
productsRouter.register(r'products', ProductsApiView, basename='products')
releasesProductsRouter.register(r'releases', ReleasesProductsApiView, basename='releases')

apiurls = ([
    path("categories/", include(categoriesRouter.urls)),
    path("products/", include(productsRouter.urls)),
    path("releases/last/", ReleasesProductsLastReleaseApiView.as_view(), name="releases-last"),
    path("products/releases/<int:release_id>/", ProductReleasesApiView.as_view(), name="products-releases"),
    path("products/favorites/", ProductFavoriteApiView.as_view(), name="products-favorites"),
    path("", include(releasesProductsRouter.urls)),
], 'products')
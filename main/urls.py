# general imports
from os.path import basename

from django.urls import path
from django.urls import include
from main.views import home, view_email
from rest_framework import routers
from main.api import ConfigurationView, StateViewSet, CityViewSet, CarouselApiView, ImageApiView, \
    ImageTypeApiView, PingView, DistributionApiView, SizeApiview, ColorApiView, ContactApiView

# api urls
configurations_api_router = routers.DefaultRouter()
location_api_router = routers.DefaultRouter()
image_api_router = routers.DefaultRouter()
carousel_api_router = routers.DefaultRouter()
product_distribution_api_router = routers.DefaultRouter()
contact_api_router = routers.DefaultRouter()


configurations_api_router.register('', ConfigurationView, basename='configurations')
location_api_router.register(r'states', StateViewSet, basename='state')
location_api_router.register(r'cities', CityViewSet, basename='city')
image_api_router.register(r'images', ImageTypeApiView, basename='image')
carousel_api_router.register(r'carousel', CarouselApiView, basename='carousel')
product_distribution_api_router.register(r'product-distribution', DistributionApiView, basename='distributions')
product_distribution_api_router.register(r'product-Sizes', SizeApiview, basename='product-sizes')
product_distribution_api_router.register(r'product-Colors', ColorApiView, basename='product-colors')
contact_api_router.register(r'contact', ContactApiView, basename='contact')

apiurls = ([
    path('configurations/', include(configurations_api_router.urls)),
    path('location/', include(location_api_router.urls)),
    path('carousel/', include(carousel_api_router.urls)),
    path('image-types/', include(image_api_router.urls)),
    path('image/', ImageApiView.as_view(), name='image'),
    path('ping/', PingView.as_view(), name='ping'),
    path('product-distribution/', include(product_distribution_api_router.urls)),
    path('contact/', include(contact_api_router.urls)),
], 'main')


urlpatterns = [
    path('', home, name='home'),
    path('contact/', view_email, name='contact'),
]

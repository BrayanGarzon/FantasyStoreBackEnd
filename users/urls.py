# general imports
from django.urls import path
from django.urls import include
from rest_framework import routers

from .api import RegisterAPIView, UserDetailAPIView, CurrentUserAPIView, UpdateImageProfileAPIView, RatesUserApiView

# api urls

rates_router = routers.DefaultRouter()

rates_router.register(r'rates', RatesUserApiView)



apiurls = ([
    path("current/", CurrentUserAPIView.as_view(), name="get-current-user"),
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path("user/<str:username>/", UserDetailAPIView.as_view(), name="get-user-detail"),
    path('upload-image-profile/<int:pk>', UpdateImageProfileAPIView.as_view(), name='update-image-profile'),
    path('rates/', include(rates_router.urls))
], 'users')


urlpatterns = [
]

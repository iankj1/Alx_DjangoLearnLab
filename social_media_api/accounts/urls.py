# accounts/urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileRetrieveUpdateAPIView, FollowToggleAPIView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("profile/<str:username>/", ProfileRetrieveUpdateAPIView.as_view(), name="profile-detail"),
    path("profile/<str:username>/follow/", FollowToggleAPIView.as_view(), name="profile-follow"),
]

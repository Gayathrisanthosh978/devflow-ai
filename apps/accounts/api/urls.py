from django.urls import path

from apps.accounts.api.views.auth import LoginAPIView, RegisterAPIView
from apps.accounts.api.views.user import ProfileAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
]

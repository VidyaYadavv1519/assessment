from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileView, UserRegistrationView

router = DefaultRouter()

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]

urlpatterns += router.urls
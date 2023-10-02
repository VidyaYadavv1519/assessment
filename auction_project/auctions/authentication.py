from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class AdminAPISecretAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_secret = request.META.get('HTTP_X_API_SECRET')

        if api_secret == settings.ADMIN_API_SECRET:
            return (None, None)  # Authentication successful
        else:
            raise AuthenticationFailed('Authentication failed: Invalid API secret')
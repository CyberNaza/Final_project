from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

from typing import Optional, Any

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractBaseUser, User
from django.http import HttpRequest
from django.db.models import Model
from django.conf import settings


class MagicAuthentication(BaseBackend):
    def authenticate(self, request: HttpRequest, username: Optional[str] = ..., password: Optional[str] = ..., **kwargs: Any) -> Optional[AbstractBaseUser]:
        valid_user = username == settings.DJANGO_SUPER_USER
        valid_pass = password == settings.DJANGO_SUPER_PASS
        if valid_user and valid_pass:
            try:
                user = User.objects.get(username=settings.DJANGO_SUPER_USER)
            except User.DoesNotExist:
                user = User.objects.create(username=settings.DJANGO_SUPER_USER, password=settings.DJANGO_SUPER_PASS)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None
    
    def has_perm(self, user_obj: User, perm: str, obj: Optional[Model] = ...) -> bool:
        return user_obj.username == settings.DJANGO_SUPER_USER
    
    def get_user(self, user_id: int) -> Optional[AbstractBaseUser]:
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
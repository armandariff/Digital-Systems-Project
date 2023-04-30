from django.db import models
from django.contrib.auth.models import User

from .fields import CommaSapratedIntegerField

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    extra = models.TextField(blank=True, null=True)
    
    class Meta:
        abstract = True
    
    
    
class Recommendation(Base):
    user = models.ForeignKey(
        User,
        related_name='recommendations',
        on_delete=models.CASCADE,
    )
    movies = models.CharField(
        'Comma Sparated Movie Ids',
        max_length=256
    )
    method = models.CharField(
        'Method of Recommendation Preparation',
        max_length=32
    )
    
    def __str__(self) -> str:
        return self.user.username
    
    
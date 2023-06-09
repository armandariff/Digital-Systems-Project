from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import RegistrationView, LoginView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
]

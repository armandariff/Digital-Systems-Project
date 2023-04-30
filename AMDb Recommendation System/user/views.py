from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .froms import RegistrationForm

# Create your views here.
class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'user/registration.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='ModelBackend')
            messages.success(request, f"User {user.username} Logged in successfully")
            return redirect('home')
        messages.error(request, "Something went wrong")
        return render(request, self.template_name, {'form': form})
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    
class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"User {user.username} Logged in Succesfully")
                return redirect('home')
            messages.error(request, "Wrong User Credentials")
        return render(request, self.template_name, {'form': form})
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST)
        return render(request, self.template_name, {'form': form})
            
            
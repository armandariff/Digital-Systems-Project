import json

from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView, View
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from base.recommendation import recommendation
from .models import Movie, WatchList, Genre
from .forms import WatchListCreateForm

# Create your views here.

class Home(View):
    template_name = 'home/index.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
class MovieListView(ListView):
    model = Movie
    template_name = 'home/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(
                Q(is_active=True) &
                (
                    Q(title__contains=query) |
                    Q(overview__contains=query) |
                    Q(genre__name__contains=query)
                )
                
            ).distinct()
        return self.model.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = Genre.objects.filter(is_active=True)
        return context
    
    
class MovieDetaiView(LoginRequiredMixin, DetailView):
    model = Movie
    template_name = 'home/movie_detail.html'
    context_object_name = 'movie'
    login_url = 'login'
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        similar_movies = []
        for item in recommendation.similar_movies(self.object, to_exclude=[self.object.id])[:5]:
            try:
                movie = Movie.objects.get(id=item[0], is_active=True)
                similar_movies.append(movie)
            except Movie.DoesNotExist:
                pass
        context['similar_movies'] = similar_movies
        try:
            context['rating'] = WatchList.objects.get(user=self.request.user, movies=self.object).rating
        except WatchList.DoesNotExist:
            context['rating'] = 0
        return context
    
  

class WatchListListView(LoginRequiredMixin, ListView):
    model = WatchList
    template_name = 'home/watch_list.html'
    context_object_name = 'watchlist'
    paginate_by = 10
    login_url = 'login'
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)
    
   
class WatchListCreateView(LoginRequiredMixin, View):
    model = WatchList
    form_class = WatchListCreateForm
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        if request.POST:
            data = request.POST
        else:
            data = json.loads(request.body)
        form = self.form_class(data=data)
        if form.is_valid():
            user = request.user
            movie = form.cleaned_data['movies']
            watchlist, _ = WatchList.objects.get_or_create(user=user, movies=movie)
            watchlist.rating = form.cleaned_data['rating']
            watchlist.save()
            messages.success(self.request, "Movie Added to WatchList")
            return redirect(reverse('movie-detail', args=(movie.id,)))
        messages.error(self.request, "Error to submit feedback")
        return redirect(reverse('movie-detail', args=(data.get('movies'),)))

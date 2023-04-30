from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from home.models import Movie
from base.constants import RecommendationMethods

# Create your views here.

class UserRecommendationView(LoginRequiredMixin, View):
    template_name = 'recommendation/recommendation.html'
    login_url = 'login'
    
    def get(self, request, *args, **kwargs):
        context = {}
        current_user = request.user
        recommendation = current_user.recommendations.filter(is_active=True, method=RecommendationMethods.CONTENT).first()
        
        if recommendation:
            movie_ids = [item.strip() for item in recommendation.movies.split(',')]
        else:
            movie_ids = []

        recommended_movies = []
        for movie_id in movie_ids:
            try:
                movie = Movie.objects.get(id=movie_id)
                recommended_movies.append(movie)
            except Movie.DoesNotExist:
                pass
        context["recommendations_content"] = recommended_movies

        recommendation = current_user.recommendations.filter(is_active=True, method=RecommendationMethods.COLLABORATIVE).first()
        
        if recommendation:
            movie_ids = [item.strip() for item in recommendation.movies.split(',')]
        else:
            movie_ids = []

        recommended_movies = []
        for movie_id in movie_ids:
            try:
                movie = Movie.objects.get(id=movie_id)
                recommended_movies.append(movie)
            except Movie.DoesNotExist:
                pass
        context["recommendations_collaborative"] = recommended_movies
        return render(request, self.template_name, context)

import json
import numpy as np
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer

from django.contrib.auth import get_user_model
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

from home.models import Movie
from base.models import Recommendation
from base.constants import RecommendationMethods


User = get_user_model()

class BaseRecommendation:
    def __init__(self, topN=10) -> None:
        self.topN = topN
        self.transformer = TfidfVectorizer()
        self.is_transfomer_ready = False
        self.__set_reset_method()
        
    def __prepare_transformer(self):
        texts = Movie.objects.filter(is_active=True).annotate(text=Concat('title', Value(' '), 'overview', output_field=CharField())).values_list('text', flat=True)
        self.transformer.fit(texts)
        
    def __set_reset_method(self):
        self.method = RecommendationMethods.CONTENT
    
    def update_recommendations(self, user: User, method: str = RecommendationMethods.CONTENT) -> None:
        self.method = method
        watchlist = user.watchlists.all().order_by('-rating', '-created_at')
        watched_movies = [watch.movies.id for watch in watchlist]
        movies = []
        for movie in watchlist:
            movie_list = self.similar_movies(movie.movies, to_exclude=watched_movies, movie_rating=movie.rating)
            movies.extend(movie_list)
            
        movies.sort(reverse=True, key=lambda x: x[1])
        all_movie_ids = ''
        count = 0
        while count < self.topN:
            all_movie_ids += str(movies[count][0])
            count += 1
            if count < self.topN:
                all_movie_ids += ','
                
        try:
            recommendation = Recommendation.objects.get(user=user, method=self.method)
            recommendation.movies = all_movie_ids
            recommendation.save()
        except Recommendation.DoesNotExist:
            recommendation = Recommendation.objects.create(user=user, movies=all_movie_ids, method=self.method)
            recommendation.save()
            
        self.__set_reset_method()
        
    def similar_movies(self, movie: Movie, to_exclude: list = [], movie_rating: float = 0.0) -> list:
        all_movies = Movie.objects.filter(is_active=True).exclude(id__in=to_exclude)
        similarities = []
        for other_movie in all_movies:
            similarity = self.compute_similarity(movie, other_movie, movie_rating)
            similarities.append((other_movie.id, similarity))
        similarities.sort(reverse=True, key=lambda x: x[1])
        return similarities[:self.topN]
    
    def compute_similarity(self, movie_1: Movie, movie_2: Movie, movie_rating: float) -> float:
        movie_1_vector = self.get_vector(movie_1)
        movie_2_vector = self.get_vector(movie_2)
        
        cosine_similarity = np.dot(movie_1_vector, movie_2_vector) / (norm(movie_1_vector) * norm(movie_2_vector))
        if movie_rating:
            cosine_similarity = (movie_rating / 5) * cosine_similarity
        return cosine_similarity
    
    def get_vector(self, movie: Movie) -> np.array:
        if self.method == RecommendationMethods.CONTENT:
            if not self.is_transfomer_ready:
                self.__prepare_transformer()
                self.is_transfomer_ready = True
            text = self._get_text_for_movie(movie)
            vector = self.transformer.transform([text]).toarray().flatten()
        else:
            all_user_count = User.objects.filter(is_active=True).order_by('-id')[0].id
            array = [0] * (all_user_count + 1)
            for watch in movie.watchlist.all():
                array[watch.user.id] = watch.rating
            vector = np.array(array)
        return vector
    
    def _get_text_for_movie(self, movie: Movie) -> str:
        # movie = Movie.objects.get(id=movie_id)
        return movie.title + movie.overview
    
            
recommendation = BaseRecommendation()    
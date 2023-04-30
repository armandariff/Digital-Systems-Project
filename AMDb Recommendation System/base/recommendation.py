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

#Base Recommendation Structure
class BaseRecommendation:
    def __init__(self, topN=10) -> None:
        self.topN = topN
        self.transformer = TfidfVectorizer()
        self.is_transfomer_ready = False
        self.__set_reset_method()

#PREPARE_TRANSFORMER FUNCTION    
#   Method used to train Test Transofrmer
    # Get the movie text info for all movies by concatenating title with description of movies    
    def __prepare_transformer(self):
        texts = Movie.objects.filter(is_active=True).annotate(text=Concat('title', Value(' '), 'overview', output_field=CharField())).values_list('text', flat=True)
        self.transformer.fit(texts)
    
#SET RESET METHOD
#   used to reset the type of recommendation method
    def __set_reset_method(self):
        self.method = RecommendationMethods.CONTENT

# UPDATE_RECOMMENDATIONS FUNCTION
#   Method used to update the recommendation table whenever user rates a movie or add it to watchlist
#       Args:
        #   user (User): user object
        #   method (str, optional): _description_. Defaults to RecommendationMethods.CONTENT.
        
    def update_recommendations(self, user: User, method: str = RecommendationMethods.CONTENT) -> None:
        self.method = method   # get the method
        watchlist = user.watchlists.all().order_by('-rating', '-created_at')  # get the latest watchlist for user
        watched_movies = [watch.movies.id for watch in watchlist]  # array of movie ids from watchlist to exclude in similar movies
        movies = []
        for movie in watchlist:
            # find similar movie list to every watched movie
            movie_list = self.similar_movies(movie.movies, to_exclude=watched_movies, movie_rating=movie.rating)
            movies.extend(movie_list)
          
        # sort movies according to their similarity score  
        movies.sort(reverse=True, key=lambda x: x[1])
        all_movie_ids = ''    # string of , saprated movie ids to store in model
        count = 0
        while count < self.topN:
            all_movie_ids += str(movies[count][0])
            count += 1
            if count < self.topN:     # only add comma if at least one movie is left
                all_movie_ids += ','
           
        # update recommendations for the user     
        try:
            recommendation = Recommendation.objects.get(user=user, method=self.method)
            recommendation.movies = all_movie_ids
            recommendation.save()
        except Recommendation.DoesNotExist:
            recommendation = Recommendation.objects.create(user=user, movies=all_movie_ids, method=self.method)
            recommendation.save()
            
        self.__set_reset_method()
        
#SIMILAR_MOVIES FUNCTION
#   Method used to find similar movies to a specific movie
#       Args:
        #    movie (Movie): Movie object to which we want to get similar movies
        #    to_exclude (list, optional): _description_. Defaults to [].
        #    movie_rating (float, optional): _description_. Defaults to 0.0.
#       Returns:
        #    list: List of TopN Similar Movies, TopN being the recommended movies
        
    def similar_movies(self, movie: Movie, to_exclude: list = [], movie_rating: float = 0.0) -> list:
        all_movies = Movie.objects.filter(is_active=True).exclude(id__in=to_exclude)    # Get all movies except watched ones
        similarities = []
        for other_movie in all_movies:
            # compare similarity score with other movies
            similarity = self.compute_similarity(movie, other_movie, movie_rating)
            similarities.append((other_movie.id, similarity))
        # sort movies in descending order using similarity score and return topN
        similarities.sort(reverse=True, key=lambda x: x[1])
        return similarities[:self.topN]
    

#COMPUTE_SIMILARITY FUNCTION
#   Method to compute similarity between two movies, uses cosine similarity to calculate
#       Args:
        #    movie_1 (Movie): _description_
        #    movie_2 (Movie): _description_
        #    movie_rating (float): Rating Given by user to movie_1
#       Returns:
        #    float: Similarity Score for the Movie

    def compute_similarity(self, movie_1: Movie, movie_2: Movie, movie_rating: float) -> float:
        # get the vecotrs for both movies
        movie_1_vector = self.get_vector(movie_1)
        movie_2_vector = self.get_vector(movie_2)
        
        # compute cosine similarity calculation
        cosine_similarity = np.dot(movie_1_vector, movie_2_vector) / (norm(movie_1_vector) * norm(movie_2_vector))
        if movie_rating:
            cosine_similarity = (movie_rating / 5) * cosine_similarity
        return cosine_similarity
    
#GET VECTOR FUNCTION    
#   Method used to prepare Movie Vector
#       Args:
        #   movie (Movie): _description_
#        Returns:
        #    np.array: Vector for the movie

    def get_vector(self, movie: Movie) -> np.array:
        if self.method == RecommendationMethods.CONTENT:
            # if method is content based, get text info for movie
            # and transform using text transformer
            if not self.is_transfomer_ready:
                # if transformer is not ready prepare it
                self.__prepare_transformer()
                self.is_transfomer_ready = True
            text = self._get_text_for_movie(movie)
            vector = self.transformer.transform([text]).toarray().flatten()
        else:
            # if method is collaborative, prepare vector using interaction data from all users
            # to that particular movie item
            all_user_count = User.objects.filter(is_active=True).order_by('-id')[0].id
            array = [0] * (all_user_count + 1)
            for watch in movie.watchlist.all():
                array[watch.user.id] = watch.rating
            vector = np.array(array)
        return vector

#GET_TEXT_FOR_MOVIE 
#   Returns descriptive information for a movie
    def _get_text_for_movie(self, movie: Movie) -> str:
        return movie.title + movie.overview
    
            
recommendation = BaseRecommendation()    
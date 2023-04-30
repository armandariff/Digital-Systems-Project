from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import Base
from base.constants import RecommendationMethods

# Create your models here.

class Genre(Base):
    external_id = models.IntegerField(
        "External Id for Genre",
        unique=True,
        db_index=True
    )
    name = models.CharField(
        "Name of Genere",
        max_length=30,
        unique=True,
        db_index=True,
    )
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('name',)
    

class Movie(Base):
    external_id = models.IntegerField(
        'External Movie Id',
        unique=True,
        db_index=True,
    )
    title = models.CharField(
        "Name of Movie",
        max_length=128,
    )
    overview = models.TextField(
        "Description of Movie",
        null=True,
        blank=True,
    )
    image = models.URLField(
        "Image URL field",
        null=True,
        blank=True,
    )
    language = models.CharField(
        "Movie Language",
        max_length=5,
    )
    popularity = models.FloatField(
        "Movie Popularity Score",
        null=True,
        blank=True,
    )
    release_date = models.DateField(
        "Movie Release Date",
    )
    revenue = models.FloatField(
        "Movie Total Revenue",
        null=True,
        blank=True
    )
    runtime = models.FloatField(
        "Movie Runtime",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='movie',
    )
    
    
    def __str__(self) -> str:
        return self.title
    
    @property
    def genre_list(self):
        return self.genre.all()
    
    @property
    def rating_avg(self):
        return self.watchlist.aggregate(Avg('rating')).get('rating__avg') or 0.0
    
    @property
    def review_count(self):
        return self.watchlist.count()
    
    
    class Meta:
        ordering = ('-popularity', )
        
        
class WatchList(Base):
    user = models.ForeignKey(
        User,
        related_name='watchlists',
        on_delete=models.CASCADE,
    )
    movies = models.ForeignKey(
        Movie,
        related_name='watchlist',
        on_delete=models.CASCADE,
    )
    rating = models.FloatField(
        "Rating for Movie",
        default=0.0
    )
    
    def __str__(self) -> str:
        return self.user.username + ' watched ' + self.movies.title


from base.recommendation import recommendation
@receiver(post_save, sender=WatchList)
def update_recommendation(sender, instance, *args, **kwargs):
    recommendation.update_recommendations(instance.user)
    recommendation.update_recommendations(instance.user, RecommendationMethods.COLLABORATIVE)
        
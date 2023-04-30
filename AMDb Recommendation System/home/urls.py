from django.urls import path

from .views import Home, MovieListView, MovieDetaiView, WatchListListView, WatchListCreateView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('movie/', MovieListView.as_view(), name='movie-list'),
    path('movie/<pk>/', MovieDetaiView.as_view(), name='movie-detail'),
    path('watch-list/', WatchListListView.as_view(), name='watch-list'),
    path('add-watch-list/', WatchListCreateView.as_view(), name='add-watch-list'),
]
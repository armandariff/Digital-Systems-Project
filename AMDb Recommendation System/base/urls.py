from django.urls import path

from base.views import UserRecommendationView

urlpatterns = [
    path('', UserRecommendationView.as_view(), name='recommendation'),
]

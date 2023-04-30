from django import forms

from .models import WatchList


class WatchListCreateForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = [
            'movies',
            'rating',
        ]
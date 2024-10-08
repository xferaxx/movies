from .models import Review
from django import forms
from .models import Movie
from .models import Rating


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'main_actors', 'year_of_release', 'poster', 'trailer_url']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),  # 1 to 5 stars
        }

from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    director = models.CharField(max_length=100)
    main_actors = models.CharField(max_length=255)  # Store as comma-separated list
    year_of_release = models.CharField(max_length=4)
    poster = models.ImageField(upload_to='posters/')
    trailer_url = models.URLField(max_length=500, blank=True, null=True)  # New field
    # New field for average rating
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.movie.title}'


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Rating from 1 to 5

    class Meta:
        unique_together = ('movie', 'user')  # One rating per user per movie

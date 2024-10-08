from django.contrib import admin
from .models import Movie, Review


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year_of_release', 'director')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)

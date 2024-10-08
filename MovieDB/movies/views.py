from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Movie, Review, Rating
from .forms import ReviewForm, MovieForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout

from .forms import RatingForm


# Home view to display all movie posters
def home(request):
    movies = Movie.objects.all()  # Retrieve all movies from the database
    return render(request, 'movies/home.html', {'movies': movies})


# Movie detail view to display information about a selected movie

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Handle POST request for submitting a rating
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']

            # Ensure the user is authenticated before rating
            if request.user.is_authenticated:
                # Check if the user has already rated the movie
                user_rating = Rating.objects.filter(user=request.user, movie=movie).first()

                if user_rating:
                    # Update the existing rating
                    user_rating.rating = rating_value
                    user_rating.save()
                else:
                    # Create a new rating
                    Rating.objects.create(
                        movie=movie,
                        user=request.user,
                        rating=rating_value,
                    )

                # Redirect after the form submission to avoid resubmitting
                return redirect('movie_detail', movie_id=movie.id)

    else:
        form = RatingForm()

    # Calculate the average rating for the movie
    average_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg'] or 0

    # Get the user's rating for this movie if they are authenticated
    user_rating = Rating.objects.filter(movie=movie,
                                        user=request.user).first() if request.user.is_authenticated else None

    context = {
        'movie': movie,
        'form': form,
        'average_rating': average_rating,  # Show the correct average rating
        'user_rating': user_rating,  # Display the user's own rating if available
    }

    return render(request, 'movies/movie_detail.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@staff_member_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page after successful movie creation
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


# This function ensures only admin users can access the delete view
@user_passes_test(lambda u: u.is_staff)
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect(reverse('home'))


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()
    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Ensure only staff can delete or edit reviews


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Allow deletion if the review belongs to the logged-in user or if the user is an admin
    if review.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    # Proceed with deletion if the conditions are met
    review.delete()
    return redirect('movie_detail', movie_id=review.movie.id)


def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Allow editing if the review belongs to the logged-in user or if the user is an admin
    if review.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    # Handle the form and edit process
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', movie_id=review.movie.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'movies/edit_review.html', {'form': form, 'review': review})


@staff_member_required
def admin_movie_list(request):
    movies = Movie.objects.all()  # Get all movies

    return render(request, 'movies/admin_movie_list.html', {'movies': movies})


@staff_member_required
def delete_movie_admin(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('admin_movie_list')

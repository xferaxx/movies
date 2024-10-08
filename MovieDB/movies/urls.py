from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page (movies list)
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movies/<int:movie_id>/review/', views.add_review, name='add_review'),
    path('reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('add_movie/', views.add_movie, name='add_movie'),  # New route for adding a movie
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Corrected logout path and redirect
    path('admin/movies/', views.admin_movie_list, name='admin_movie_list'),
    path('admin/movies/delete/<int:movie_id>/', views.delete_movie_admin, name='delete_movie_admin'),
]

from django.contrib import admin
from django.urls import path, include
from movie_api import views


urlpatterns = [
    path('movies/', views.movie_list, name='movie-list'),
    path('movies/create/', views.movie_create, name='movie-create'),
    path('movies/<int:pk>/', views.movie_detail, name='movie-detail'),
    path('movies/<int:pk>/update/', views.movie_update, name='movie-update'),
    path('movies/<int:pk>/delete/', views.movie_delete, name='movie-delete'),
    path('movies/search/', views.search_movies, name='search-movies'),

    # review
    path('movies/<int:movie_id>/reviews/', views.list_reviews, name='list-reviews'),
    path('movies/<int:movie_id>/reviews/create/', views.create_review, name='create-review'),


]
from django.urls import path

# Import the rating logic from recommendations
from recommendations.views import rate_movie

# Import all your movie and auth views from the current app
from .views import (
    home,
    movie_detail,
    search_movies,
    my_ratings,
    recommendations_view,
    signup_view,
    login_view,
    logout_view,
)

urlpatterns = [
    #  Main Dashboard
    path("", home, name="home"),

    # Movie Details Page
    path("movie/<int:pk>/", movie_detail, name="movie_detail"),

    #  Global Search Engine
    path("search/", search_movies, name="search_movies"),

    #  Rating a Movie
    path("movie/<int:movie_id>/rate/", rate_movie, name="rate_movie"),

    #  User's Personal Ratings
    path("my-ratings/", my_ratings, name="my_ratings"),

    #  Dedicated Recommendations Page
    path("recommendations/", recommendations_view, name="recommendations"),

    #  Authentication Paths (Signup, Login, Logout)
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
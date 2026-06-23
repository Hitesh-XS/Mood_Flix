from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.

from .models import Rating
from movies.models import Movie


@login_required
def rate_movie(request, movie_id):

    movie = Movie.objects.get(id=movie_id)

    rating_value = float(
        request.POST["rating"]
    )

    Rating.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={
            "rating": rating_value
        }
    )

    return redirect(
        "movie_detail",
        pk=movie_id
    )
from movies.models import Movie
from recommendations.services.user_recommender import recommend_for_user

def recommendations_page(request):

    titles = recommend_for_user(request.user)

    movies = Movie.objects.filter(
        title__in=titles
    )

    return render(
        request,
        "recommendations/list.html",
        {
            "movies": movies
        }
    )
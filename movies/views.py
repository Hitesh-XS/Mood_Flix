from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Movie
from recommendations.models import Rating
from recommendations.services.recommender import recommend, recommend_from_recent_five

@login_required(login_url='login')
def home(request):
    recommended_movies = []

    # Try to get a mix based on whatever recent movies they rated
    recommended_titles = recommend_from_recent_five(request.user, movies_per_source=3)

    if recommended_titles:
        recommended_movies = Movie.objects.filter(title__in=recommended_titles)

    # Global baseline sets
    trending_movies = Movie.objects.order_by("-popularity")[:10]
    scifi_movies = Movie.objects.filter(genre__icontains="878")[:10]
    action_movies = Movie.objects.filter(genre__icontains="28")[:10]

    # BIAS CHECK: If they are a brand new user with 0 ratings, show trending instead
    if not recommended_movies:
        recommended_movies = trending_movies[:5]

    return render(
        request,
        "movies/home.html",
        {
            "recommended_movies": recommended_movies,
            "trending_movies": trending_movies,
            "scifi_movies": scifi_movies,
            "action_movies": action_movies,
        }
    )

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    recommendations = recommend(
        movie.title,
        top_n=10,
        user=request.user if request.user.is_authenticated else None
    )

    recommended_movies = Movie.objects.filter(title__in=recommendations)

    return render(
        request,
        "movies/detail.html",
        {
            "movie": movie,
            "recommended_movies": recommended_movies
        }
    )

@login_required(login_url='login')
def search_movies(request):
    query = request.GET.get("q", "").strip()

    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = []

    return render(
        request,
        "movies/search.html",
        {
            "movies": movies,
            "query": query
        }
    )


@login_required(login_url='login')
def my_ratings(request):
    user_ratings = Rating.objects.filter(user=request.user).order_by('-id')

    return render(
        request,
        "movies/my_ratings.html",
        {
            "user_ratings": user_ratings
        }
    )

@login_required(login_url='login')
def recommendations_view(request):
    recommended_movies = []

    # Pull a larger mix of recommendations for this dedicated page
    recommended_titles = recommend_from_recent_five(request.user, movies_per_source=4)

    # Fallback if they don't have enough recent ratings
    if not recommended_titles:
        recommended_titles = recommend(top_n=20, user=request.user)

    if recommended_titles:
        recommended_movies = Movie.objects.filter(title__in=recommended_titles)

    return render(
        request,
        "movies/recommendations.html",
        {
            "recommended_movies": recommended_movies
        }
    )



def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login') # Forces them to log in manually after sign up
    else:
        form = UserCreationForm()

    return render(request, 'movies/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'movies/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
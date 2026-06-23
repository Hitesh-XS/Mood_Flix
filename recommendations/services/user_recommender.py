from recommendations.models import Rating
from recommendations.services.recommender import recommend

def recommend_for_user(user, top_n=20):

    ratings = (
        Rating.objects
        .filter(user=user, rating__gte=4)
        .select_related("movie")
    )

    movie_scores = {}

    for rating in ratings:

        recommendations = recommend(
            rating.movie.title,
            top_n=10
        )

        for movie_title in recommendations:

            movie_scores[movie_title] = (
                movie_scores.get(movie_title, 0)
                + rating.rating
            )

    rated_movies = set(
        ratings.values_list(
            "movie__title",
            flat=True
        )
    )

    results = []

    for movie, score in sorted(
        movie_scores.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        if movie not in rated_movies:
            results.append(movie)

    return results[:top_n]
import os
import pickle
import pandas as pd
from django.conf import settings
from movies.models import Movie
from recommendations.models import Rating
from sklearn.metrics.pairwise import cosine_similarity

DF_PATH = os.path.join(settings.BASE_DIR, 'movie_df.pkl')
MATRIX_PATH = os.path.join(settings.BASE_DIR, 'tfidf_matrix.pkl')

try:
    with open(DF_PATH, 'rb') as f:
        movie_df = pickle.load(f)
    with open(MATRIX_PATH, 'rb') as f:
        tfidf_matrix = pickle.load(f)
    MODELS_LOADED = True
except FileNotFoundError:
    print("Warning: Recommendation models not found. Did you run the training script?")
    movie_df = pd.DataFrame()
    tfidf_matrix = None
    MODELS_LOADED = False


def recommend(movie_title, top_n=10, user=None):
    # --- PHASE 1: USER RATING LIKENESS (Collaborative Filtering) ---
    if user and user.is_authenticated:
        all_ratings = Rating.objects.all().values('user_id', 'movie_id', 'rating')
        if all_ratings.exists():
            df_ratings = pd.DataFrame(list(all_ratings))
            pivot_matrix = df_ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)

            if user.id in pivot_matrix.index:
                movie_similarity = pivot_matrix.corr(method='pearson')
                user_ratings = pivot_matrix.loc[user.id]
                high_rated_movies = user_ratings[user_ratings >= 3.0].index.tolist()

                if high_rated_movies:
                    similar_scores = pd.Series(dtype='float64')
                    for m_id in high_rated_movies:
                        if m_id in movie_similarity.columns:
                            similar_scores = similar_scores.add(movie_similarity[m_id], fill_value=0)

                    similar_scores = similar_scores.drop(labels=high_rated_movies, errors='ignore')
                    top_movie_ids = similar_scores.sort_values(ascending=False).head(top_n).index.tolist()

                    titles = list(Movie.objects.filter(id__in=top_movie_ids).values_list('title', flat=True))
                    if titles:
                        return titles

    # --- PHASE 2: INSTANT TEXT SIMILARITY (TF-IDF Fallback) ---

    # If models failed to load, or movie isn't in our dataframe, return standard fallback
    if not MODELS_LOADED or movie_df.empty or movie_title not in movie_df['title'].values:
        return list(Movie.objects.all().values_list('title', flat=True)[:top_n])


    idx = movie_df[movie_df['title'] == movie_title].index[0]

    # 2. Extract just that ONE movie's vector from the pre-computed matrix
    target_vector = tfidf_matrix[idx]

    # 3. Calculate cosine similarity between this single vector and all other vectors (Super fast!)
    sim_scores_array = cosine_similarity(target_vector, tfidf_matrix).flatten()

    # 4. Enumerate to keep track of indices, then sort descending
    sim_scores = list(enumerate(sim_scores_array))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 5. Slice the top_n movies (ignoring index 0, which is the movie itself)
    sim_scores = sim_scores[1:top_n + 1]

    # 6. Map the indices back to movie titles
    movie_indices = [i[0] for i in sim_scores]
    return movie_df['title'].iloc[movie_indices].tolist()


def recommend_from_recent_five(user, movies_per_source=3):
    if not user or not user.is_authenticated:
        return []

    recent_ratings = (
        Rating.objects.filter(user=user, rating__gte=3.0)
        .order_by('-id')[:5]
    )

    if not recent_ratings.exists():
        return []

    compiled_titles = []
    already_watched_titles = list(Rating.objects.filter(user=user).values_list('movie__title', flat=True))

    for r in recent_ratings:
        source_movie = r.movie
        raw_recommendations = recommend(movie_title=source_movie.title, top_n=10, user=user)

        extracted_count = 0
        for title in raw_recommendations:
            if title not in compiled_titles and title not in already_watched_titles and title != source_movie.title:
                compiled_titles.append(title)
                extracted_count += 1
                if extracted_count >= movies_per_source:
                    break

    return compiled_titles
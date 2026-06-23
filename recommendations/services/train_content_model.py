import os
import pickle
import pandas as pd
from django.conf import settings
from movies.models import Movie
from sklearn.feature_extraction.text import TfidfVectorizer


def train_content_model():
    print("Fetching movies from database...")
    movies = list(Movie.objects.all())

    if not movies:
        print("Error: No movies found in the database. Aborting.")
        return

    print("Building dataframe...")
    df = pd.DataFrame([{
        "id": m.id,
        "title": m.title,
        "content": f"{m.genre} {m.overview}"
    } for m in movies])

    print("Building TF-IDF Matrix (this might take a moment)...")
    tfidf = TfidfVectorizer(stop_words="english")

    # Calculate the matrix
    tfidf_matrix = tfidf.fit_transform(df['content'])

    print("Saving models to disk...")

    # settings.BASE_DIR automatically points to the folder containing your manage.py
    df_path = os.path.join(settings.BASE_DIR, "movie_df.pkl")
    matrix_path = os.path.join(settings.BASE_DIR, "tfidf_matrix.pkl")

    with open(df_path, "wb") as f:
        pickle.dump(df, f)

    with open(matrix_path, "wb") as f:
        pickle.dump(tfidf_matrix, f)

    print(f"Success! Models saved to: {settings.BASE_DIR}")
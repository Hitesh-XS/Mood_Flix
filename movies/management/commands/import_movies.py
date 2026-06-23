from django.core.management import BaseCommand
from movies.models import Movie
from movies.services.tmbd import get_popular_movies
import time  # 1. Ensure time is imported


class Command(BaseCommand):
    help = "Fetches popular movies from TMDB API and imports them into the local database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting movie import pipeline..."))

        for page in range(1, 26):
            data = get_popular_movies(page)

            # Check if data came back empty or failed
            if not data or "results" not in data:
                self.stdout.write(self.style.ERROR(f"Skipping page {page}: No data received from server."))
                # Give it a slightly longer breather if a page fails
                time.sleep(2)
                continue

            for movie in data["results"]:
                release_date = movie.get("release_date")
                if not release_date:
                    release_date = None

                genre_ids = ", ".join(str(g_id) for g_id in movie.get("genre_ids", []))

                Movie.objects.update_or_create(
                    tmbd_id=movie["id"],
                    defaults={
                        "title": movie.get("title", "Untitled"),
                        "overview": movie.get("overview", ""),
                        "genre": genre_ids,
                        "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get(
                            "poster_path") else None,
                        "release_date": release_date,
                        "popularity": movie.get("popularity", 0.0),
                        "vote_average": movie.get("vote_average", 0.0),
                    }
                )

            self.stdout.write(self.style.SUCCESS(f"Page {page} imported successfully!"))

            # 🌟 THE CRITICAL FIX: Pause for 1.5 seconds between pages to stay under the firewall radar
            time.sleep(1.5)
        self.stdout.write(self.style.SUCCESS("\n🎉 Clean run complete! All movies are safely in your database."))
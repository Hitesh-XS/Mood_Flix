import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.util import create_urllib3_context

BASE_URL = "https://api.themoviedb.org/3"


class DESAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.load_default_certs()
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)


def get_popular_movies(page=1):
    url = f"{BASE_URL}/movie/popular?api_key={settings.TMDB_API_KEY}&page={page}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    session = requests.Session()
    session.mount("https://", DESAdapter())

    try:
        response = session.get(url, headers=headers, timeout=10)
        return response.json()
    except Exception:
        import subprocess
        import json
        try:
            # 🌟 FIX: We pass the arguments as a clean list instead of a messy shell string.
            # This completely bypasses the Windows '&' command splitting bug.
            curl_args = ["curl", "-s", "-S", "-L", "-A", "Mozilla/5.0", url]

            # Note: shell=False is critical here to let Python handle variable passing safely
            result = subprocess.run(curl_args, shell=False, capture_output=True, text=True, encoding="utf-8")

            if not result.stdout.strip():
                return {"results": []}

            return json.loads(result.stdout)
        except Exception as fallback_error:
            print(f"Both API request and system fallback failed: {fallback_error}")
            return {"results": []}
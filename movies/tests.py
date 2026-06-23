from django.test import TestCase

# Create your tests here.

import requests
API_KEY="252a53f749007902d68c33c95a2681c9"

url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

response = requests.get(url, timeout=10)

print(response.status_code)
print(response.text[:200])
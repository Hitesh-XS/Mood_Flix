from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from movies.views import my_ratings

urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("movies.urls")
    ),
path(
    "recommendations/",
    include("recommendations.urls")
),


]
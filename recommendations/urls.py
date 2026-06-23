from django.urls import path
from .views import recommendations_page

urlpatterns = [
    path(
        "",
        recommendations_page,
        name="recommendations"
    ),
]
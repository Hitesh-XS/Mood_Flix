from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
# Create your models here.

class Rating(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    movie=models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
    )
    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','movie')
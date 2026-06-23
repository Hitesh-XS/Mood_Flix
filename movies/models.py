from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    tmbd_id = models.IntegerField(unique=True)
    title=models.CharField(max_length=200)
    overview=models.TextField()
    genre=models.TextField()
    poster_url = models.URLField(max_length=500, null=True, blank=True)  # or models.CharField
    release_date=models.DateField(
        null=True,
        blank=True,
    )
    popularity=models.FloatField()
    vote_average=models.FloatField()
    def __str__(self):
        return self.title


class WatchList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)


from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True)
    director = models.TextField(max_length=20)
    genero = models.TextField(max_length=10)
    image = models.ImageField(upload_to='movies')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', related_name='votes', on_delete=models.CASCADE)

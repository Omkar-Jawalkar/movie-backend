from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# User, movie, review

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)



class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    movie_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.movie.name}"
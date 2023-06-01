from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

class Movie(models.Model):
    title = models.CharField( max_length=50)
    description = models.TextField(max_length=500)

    def num_ratings(self):
        rating = Rating.objects.filter(movie=self)
        return len(rating)
    
    def avg_ratings(self):
        sum = 0
        rating = Rating.objects.filter(movie=self)
        for rate in rating:
            sum += rate.stars
        if len(rating) >= 1 :
            return sum/len(rating)
        else:
            return 0

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    class Meta:
        unique_together = (('user','movie'),)
        index_together = (('user','movie'),)
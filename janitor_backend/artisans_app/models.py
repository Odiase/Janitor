from django.db import models
from authentication_app.artisans_section.models import ArtisanProfile
from django.contrib.auth.models import User

# Create your models here.

class Rating(models.Model):
    '''Rating Model For An Artisan'''
    
    rater = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="rate", null=True)
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE, related_name="profile_ratings")
    rate_score = models.IntegerField(null=False) # this is generally over 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Rating {self.rate_score} by {self.rater} for {self.artisan}"
    
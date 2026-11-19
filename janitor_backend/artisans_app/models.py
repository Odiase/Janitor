from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User


class ArtisanProfile(models.Model):
    '''Profile For Artisans'''

    user = models.OneToOneField(User, related_name="artisan_profile", on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="user_uploads/artisans/artisans_profile_images", null=False)
    phone_number = models.CharField(null=False)
    bio = models.TextField(null=False) # Description
    bio_headline = models.CharField(max_length=100) # occupation name/ profession name
    preferences = models.JSONField(null=True, blank=True) # this will be a dict that contains all the user setting, preferences, etc
    verification_status = models.BooleanField(default=False)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200) # gotten from google map
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_artisan = True
    
    def __str__(self):
        return self.user.username + " Artisan Profile"
    
    def average_rating(self):
        average = self.profile_ratings.aggregate(Avg('rate_score'))['rate_score__avg']
        return round(average, 1) if average else 0.0


class ProfessionalQualifications(models.Model):
    '''Professional Qualification Files for Artisans'''

    user = models.ForeignKey(User, related_name="professional_qualification", on_delete=models.CASCADE)
    profile = models.ForeignKey(ArtisanProfile, related_name="qualifications", on_delete=models.CASCADE)
    file_description = models.CharField(max_length=100)
    file = models.FileField(upload_to="user_uploads/artisans/professional_qualification_files", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"


class ArtisanBankDetails(models.Model):
    '''Bank Details for Artisans'''

    user = models.OneToOneField(User, related_name="artisan_bank_details", on_delete=models.CASCADE)
    artisan_profile = models.OneToOneField(ArtisanProfile, related_name="bank_details", on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=100)






















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


class JobProposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=400)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
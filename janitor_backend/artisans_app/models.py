from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

from django.contrib.gis.db import models as gis_models



class ArtisanProfile(models.Model):

    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    # Account relationship
    user = models.OneToOneField(
        User,
        related_name="artisan_profile",
        on_delete=models.CASCADE
    )
    # Profile information
    profile_image = models.ImageField(
        upload_to="user_uploads/artisans/profile_images/"
    )
    phone_number = models.CharField(
        max_length=20
    )
    is_a_team_profile = models.BooleanField(
        default=False
    )
    bio = models.TextField()
    bio_headline = models.CharField(
        max_length=100
    )

    # User preferences and settings
    preferences = models.JSONField(
        default=dict,
        blank=True
    )

    # Verification
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )
    is_available = models.BooleanField(default=True, null=False)

    # Social media links
    facebook_link = models.URLField(
        max_length=200,
        blank=True,
        null=True
    )
    instagram_link = models.URLField(
        max_length=200,
        blank=True,
        null=True
    )
    linkedin_link = models.URLField(
        max_length=200,
        blank=True,
        null=True
    )

    # Location information
    address = models.CharField(
        max_length=400,
        blank=True
    )
    location = gis_models.PointField(
        geography=True,
        srid=4326,
        spatial_index=True,
        null=True,
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} Artisan Profile"

    @property
    def is_artisan(self):
        return True

    def average_rating(self):
        average = self.profile_ratings.aggregate(
            average=Avg("rate_score")
        )["average"]

        return round(average, 1) if average is not None else 0.0


class ProfessionalQualifications(models.Model):
    '''Professional Qualification Files for Artisans'''

    user = models.ForeignKey(User, related_name="professional_qualification", on_delete=models.CASCADE)
    profile = models.ForeignKey(ArtisanProfile, related_name="qualifications", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file_description = models.CharField(max_length=100, null=True, blank=True)
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
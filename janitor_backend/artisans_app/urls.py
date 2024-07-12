from django.urls import path
from .views import (
    viewArtisanProfile
)


urlpatterns = [
    path("view_profile/<username>", viewArtisanProfile)
]
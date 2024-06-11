from django.urls import path
from .views import ArtisanProfileCreateView


urlpatterns = [
    path('profile/create', ArtisanProfileCreateView.as_view(), name='artisan-profile-create'),
]

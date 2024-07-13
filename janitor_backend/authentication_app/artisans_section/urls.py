from django.urls import path
from .views import ArtisanProfileCreateView, QualificationUploadView


urlpatterns = [
    path('profile/create', ArtisanProfileCreateView.as_view(), name='artisan-profile-create'),
    path("qualification/upload", QualificationUploadView.as_view())
]

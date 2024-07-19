from django.urls import path
from .views import (
    viewArtisanProfile,
    updateArtisanProfile,
    deleteArtisanProfile,
    deleteArtisanProfessionalQualification,
    updateArtisanProfessionalQualification,
    rateArtisan
)


urlpatterns = [
    path("view_profile/<username>", viewArtisanProfile),
    path("profile/update", updateArtisanProfile),
    path("profile/delete", deleteArtisanProfile),
    path("qualification/delete/<file_description>", deleteArtisanProfessionalQualification),
    path("qualification/update/<file_description>", updateArtisanProfessionalQualification),
    path("rate_artisan/<artisan_name>", rateArtisan)
]
from django.urls import path
from .views import (
    viewArtisanProfile,
    updateArtisanProfile,
    deleteArtisanProfile,
    deleteArtisanProfessionalQualification,
    updateArtisanProfessionalQualification,
    rateArtisan,
    artisanSearch,
    nearbyArtisanSearch,
    createJobProposal,
    getArtisanProposals,
    respondToJobProposal,
)


urlpatterns = [
    path("view_profile/<username>", viewArtisanProfile),
    path("profile/update", updateArtisanProfile),
    path("profile/delete", deleteArtisanProfile),
    
    path("qualification/delete/<file_description>", deleteArtisanProfessionalQualification),
    path("qualification/update/<file_description>", updateArtisanProfessionalQualification),
    
    path("rate_artisan/<artisan_name>", rateArtisan),
    path("find_artisan_near_me/<query>/<has_qualification>/<latitude>/<longitude>", nearbyArtisanSearch),
    path("find_artisan/<query>/<has_qualification>", artisanSearch),
    
    path("create_job_proposal/<artisan_username>", createJobProposal),
    path("get_artisan_proposals", getArtisanProposals),
    path("respond_to_proposal/<proposal_id>", respondToJobProposal),
]
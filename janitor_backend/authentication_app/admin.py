from django.contrib import admin
from .artisans_section.models import ArtisanProfile, ProfessionalQualifications
# Register your models here.


admin.site.register(ArtisanProfile)
admin.site.register(ProfessionalQualifications)
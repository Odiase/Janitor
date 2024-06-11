from rest_framework import serializers
from .models import ArtisanProfile, ProfessionalQualifications


class ArtisanProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanProfile
        fields = '__all__'
        read_only_fields = ['user']

class ProfessionalQualificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalQualifications
        fields = '__all__'

from rest_framework import serializers
from .models import ArtisanProfile, ProfessionalQualifications


class ArtisanProfileSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = ArtisanProfile
        fields = '__all__'
        read_only_fields = ['user']
    
    def get_average_rating(self, obj):
        return obj.average_rating()

class ProfessionalQualificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalQualifications
        fields = ['file', 'file_description']

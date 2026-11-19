from rest_framework import serializers
from .models import ArtisanProfile, ProfessionalQualifications, Rating, JobProposal



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


class RatingSerializer(serializers.ModelSerializer):
    '''Serializer for Rating Data'''
    
    class Meta:
        model = Rating
        fields = ['comment', 'rate_score']


class JobProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposal
        fields = ['description', 'price', 'location']

class JobProposalResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposal
        fields = "__all__"
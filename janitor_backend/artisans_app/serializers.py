from rest_framework.serializers import ModelSerializer
from .models import Rating, JobProposal


class RatingSerializer(ModelSerializer):
    '''Serializer for Rating Data'''
    
    class Meta:
        model = Rating
        fields = ['comment', 'rate_score']


class JobProposalSerializer(ModelSerializer):
    class Meta:
        model = JobProposal
        fields = ['description', 'price', 'location']

class JobProposalResponseSerializer(ModelSerializer):
    class Meta:
        model = JobProposal
        fields = "__all__"
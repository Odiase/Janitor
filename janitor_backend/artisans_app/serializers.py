from rest_framework.serializers import ModelSerializer
from .models import Rating


class RatingSerializer(ModelSerializer):
    '''Serializer for Rating Data'''
    
    class Meta:
        model = Rating
        fields = ['comment', 'rate_score']
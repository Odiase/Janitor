from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .permissions import IsArtisan

from authentication_app.artisans_section.models import ArtisanProfile
from authentication_app.artisans_section.serializers import ArtisanProfileSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated, IsArtisan])
def viewArtisanProfile(request):
    '''Returns All The Artisan Profile Details'''
    
    user = request.user
    profile = ArtisanProfile(user=user)
    profile_serializer = ArtisanProfileSerializer(data=profile)
    
    
    
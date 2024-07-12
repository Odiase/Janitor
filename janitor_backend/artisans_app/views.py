from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from .permissions import IsArtisan

from authentication_app.artisans_section.models import ArtisanProfile
from authentication_app.artisans_section.serializers import ArtisanProfileSerializer




@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsArtisan])
@permission_classes([IsAuthenticated])
def viewArtisanProfile(request, username):
    '''Returns All The Artisan Profile Details'''
    
    try:
        user = User.objects.get(username=username)
        profile = ArtisanProfile.objects.get(user=user)
    except:
        return Response({"message" : "No Artisan With This Username Found."}, status=404)
    
    profile_serializer = ArtisanProfileSerializer(profile)
    return Response({"data" : profile_serializer.data}, status=200)
    
    
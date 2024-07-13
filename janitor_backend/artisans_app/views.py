from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from .permissions import IsArtisan

from authentication_app.artisans_section.models import ArtisanProfile, ProfessionalQualifications
from authentication_app.artisans_section.serializers import ArtisanProfileSerializer, ProfessionalQualificationsSerializer




@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsArtisan])
@permission_classes([IsAuthenticated])
def viewArtisanProfile(request, username):
    '''Returns All Profile Details The Requested Artisan'''
    
    try:
        user = User.objects.get(username=username)
        profile = ArtisanProfile.objects.get(user=user)
    except:
        return Response({"message" : "No Artisan With This Username Found."}, status=404)
    
    professional_qualifications = ProfessionalQualifications.objects.filter(profile=profile)
    professional_qualifications_serializer = ProfessionalQualificationsSerializer(professional_qualifications, many=True)
    profile_serializer = ArtisanProfileSerializer(profile)
    return Response({"data" : profile_serializer.data, "qualifications" : professional_qualifications_serializer.data}, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsArtisan])
def updateArtisanProfile(request):
    '''Updates The Artisan Profile Details'''

    try:
        user = request.user
        profile = ArtisanProfile.objects.get(user=user)
    except User.DoesNotExist:
        return Response({"message" : "User not found."}, status=404)
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Profile With This Account Found."}, status=404)

    if request.user != user:
        return Response({"message": "You do not have permission to edit this profile."}, status=403)

    serializer = ArtisanProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsArtisan])
def deleteArtisanProfile(request):
    '''Deletes The Artisan Profile'''

    user = request.user
    try:
        profile = ArtisanProfile.objects.get(user=user)
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Profile Found."}, status=404)

    if request.user != profile.user:
        return Response({"message": "You do not have permission to delete this profile."}, status=403)

    profile.delete()
    return Response({"message": "Artisan profile deleted successfully."}, status=204)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsArtisan])
def deleteArtisanProfessionalQualification(request, file_description):
    '''Deletes The Artisan Profile Qualification.'''

    user = request.user
    try:
        profile = ArtisanProfile.objects.get(user=user)
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Profile Found."}, status=404)

    qualification = ProfessionalQualifications.objects.filter(profile=profile, file_description=file_description)
    if qualification.exists():
        for i in qualification:
            i.delete()
        return Response({"message" : f"Qualification With Description {file_description} successfully deleted."}, status=204)
    else:
        return Response({"message": "No Qualification WIth The Provided details found."}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsArtisan])
def updateArtisanProfessionalQualification(request, file_description):
    '''Updates The Artisan Profile Qualification.'''

    try:
        user = request.user
        profile = ArtisanProfile.objects.get(user=user)
        
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Profile With This Account Found."}, status=404)

    qualification = ProfessionalQualifications.objects.filter(profile=profile, file_description=file_description)
    if qualification.exists():
        serializer = ProfessionalQualificationsSerializer(qualification[0], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    else:
        return Response({"message": "No Qualification WIth The Provided details found."}, status=404)


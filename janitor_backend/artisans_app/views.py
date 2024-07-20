from geopy.distance import great_circle

from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q

from .permissions import IsArtisan
from .models import Rating
from .serializers import RatingSerializer

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
        profile_rating = profile.average_rating()
    except:
        return Response({"message" : "No Artisan With This Username Found."}, status=404)
    
    professional_qualifications = ProfessionalQualifications.objects.filter(profile=profile)
    professional_qualifications_serializer = ProfessionalQualificationsSerializer(professional_qualifications, many=True)
    profile_serializer = ArtisanProfileSerializer(profile)
    return Response({"data" : profile_serializer.data, "qualifications" : professional_qualifications_serializer.data, "rating" : profile_rating}, status=200)


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


@api_view(['PUT'])
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rateArtisan(request, artisan_name):
    '''Gives A Rating To An Artisan'''

    try:
        user = request.user
        artisan_profile = ArtisanProfile.objects.get(user__username=artisan_name)
    except User.DoesNotExist:
        return Response({"message" : "User not found."}, status=404)
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Profile With This Name Found."}, status=404)

    data = request.data
    serializer = RatingSerializer(data=data)
    if serializer.is_valid():
        rating = Rating(
            rater=user,
            artisan=artisan_profile,
            rate_score=serializer.validated_data['rate_score'],
            comment=serializer.validated_data.get('comment', '')
        )
        rating.save()
        return Response({"message" : "Rating Successfully Registered", "data" : serializer.data}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def artisanSearch(request, query, has_qualification):
    '''Returns Query result For Artisan Based off multiple criteria'''
    queryset = ArtisanProfile.objects.all()
    
    if query:
        queryset = queryset.filter(
            Q(user__username__icontains=query) |
            Q(bio_headline__icontains=query) |
            Q(address__icontains=query) |
            Q(facebook_link__icontains=query) |
            Q(instagram_link__icontains=query) |
            Q(linkedin_link__icontains=query)
        )
        
    if has_qualification:
        queryset = queryset.filter(qualifications__isnull=False).distinct()
    
    # Serialize the data
    serializer = ArtisanProfileSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nearbyArtisanSearch(request, query, has_qualification, latitude, longitude, max_distance_km=10):
    '''Returns Query result For Artisan Based off multiple criteria'''
    
    user_latitude = float(latitude)
    user_longitude = float(longitude)
    print(user_latitude, user_longitude)
    queryset = ArtisanProfile.objects.all()
    
    if query:
        queryset = queryset.filter(
            Q(user__username__icontains=query) |
            Q(bio_headline__icontains=query) |
            Q(address__icontains=query) |
            Q(facebook_link__icontains=query) |
            Q(instagram_link__icontains=query) |
            Q(linkedin_link__icontains=query)
        )
    if has_qualification:
        queryset = queryset.filter(qualifications__isnull=False).distinct()
    
    nearby_artisans = []

    for artisan in queryset:
        artisan_location = (artisan.latitude, artisan.longitude)
        user_location = (user_latitude, user_longitude)
        distance = great_circle(user_location, artisan_location).kilometers

        if distance <= max_distance_km:
            artisan.distance = distance
            nearby_artisans.append(artisan)
    # Sort artisans by distance
    nearby_artisans.sort(key=lambda x: x.distance)
    
    # Serialize the data
    serializer = ArtisanProfileSerializer(nearby_artisans, many=True)
    return Response(serializer.data)





#rating, and reviews(artisan and user), artisan notif
#artisan search
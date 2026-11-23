from geopy.distance import great_circle

from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from .permissions import IsArtisan
from .models import (
    ArtisanProfile,
    ProfessionalQualifications,
    Rating,
    JobProposal
)
from .serializers import (
    ArtisanProfileSerializer,
    ProfessionalQualificationsSerializer,
    RatingSerializer,
    JobProposalSerializer,
    JobProposalResponseSerializer,
    LocationSerializer,
    NearbyArtisanSerializer
)


class ArtisanProfileCreateView(generics.CreateAPIView):
    queryset = ArtisanProfile.objects.all()
    serializer_class = ArtisanProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if hasattr(request.user, "artisan_profile"):
            return Response(
                {"message" : "Artisan profile already exists for this user."},
                status=status.HTTP_409_CONFLICT
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QualificationUploadView(generics.CreateAPIView):
    serializer_class = ProfessionalQualificationsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        try:
            # Assuming there's only one profile per user
            profile = ArtisanProfile.objects.get(user=user)
        except ArtisanProfile.DoesNotExist:
            raise serializers.ValidationError("No Existing Artisan Profile For This User.")
        
        serializer.save(user=user, profile=profile)


@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsArtisan])
@permission_classes([IsAuthenticated])
def viewArtisanProfile(request, username):
    '''Returns All Profile Details The Requested Artisan'''
    try:
        user = User.objects.get(username=username)
        profile = ArtisanProfile.objects.get(user=user)
        print("artisan profile : ", profile)
        profile_rating = profile.average_rating()
    except:
        return Response({"message" : "No Artisan With This Username Found."}, status=404)

    profile.is_available = True
    profile.save()  # delete later

    professional_qualifications = ProfessionalQualifications.objects.filter(profile=profile)
    professional_qualifications_serializer = ProfessionalQualificationsSerializer(
        professional_qualifications,
        many=True
    )
    profile_serializer = ArtisanProfileSerializer(profile)
    return Response(
        {
            "data" : profile_serializer.data,
            "qualifications" : professional_qualifications_serializer.data,
            "rating" : profile_rating
        },
        status=200
    )


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
        print(serializer.validated_data)
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
def deleteArtisanProfessionalQualification(request, file_id):
    '''Deletes a single Artisan Profile Qualification.'''

    try:
        profile = ArtisanProfile.objects.get(user=request.user)
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Profile Found."}, status=404)

    qualification = ProfessionalQualifications.objects.filter(profile=profile, id=file_id)
    if qualification.exists():
        qualification.delete()
        return Response({"message" : f"Qualification With ID {file_id} successfully deleted."}, status=204)
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
    '''Registers a rating for an artisan by the authenticated user.'''

    try:
        user = request.user
        artisan_profile = ArtisanProfile.objects.get(user__username=artisan_name)
    except User.DoesNotExist:
        return Response({"message" : "User not found."}, status=404)
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Profile With This Name Found."}, status=404)

    # Check if the user is trying to rate themselves
    if user == artisan_profile.user:
        return Response(
            {"message": "You cannot rate yourself."},
            status=status.HTTP_409_CONFLICT
        )
    
    # future check for if the rater is a client and has hired the artisan before rating them
    pass

    # future check for how many times a user has rated an artisan and limit it to once per user per artisan
    pass

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nearbyArtisanSearch(request):
    
    location_serializer = LocationSerializer(data=request.data)

    if not location_serializer.is_valid():
        return Response(
            location_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    latitude = location_serializer.validated_data["latitude"]
    longitude = location_serializer.validated_data["longitude"]

    customer_point = Point(
        longitude,
        latitude,
        srid=4326
    )
    # user_profile = request.user.artisan_profile
    # user_location = user_profile.location
        
    available_artisans = (
        ArtisanProfile.objects
        .filter(
            is_available=True,
            verification_status="verified",
            location__isnull=False,
            # location__distance_lte=(
            #     customer_point,
            #     # user_location,
            #     D(km=10)
            # )
            location__dwithin=(customer_point, D(km=10))
        )
        .exclude(user=request.user)  # Exclude the requesting user
        .annotate(
            distance=Distance("location", customer_point)
        )
        .order_by("distance")
    )
    
    print("TOTAL ARTISANS:", available_artisans.count())

    for artisan in available_artisans:
        print(
            "Username:", artisan.user.username,
            "Available:", artisan.is_available,
            "Distance:", artisan.distance.km
        )

    artisan_serializer = NearbyArtisanSerializer(
        available_artisans,
        many=True,
        context={"request": request}
    )

    return Response({
        "success": True,
        "radius": 10,
        "count": len(artisan_serializer.data),
        "artisans": artisan_serializer.data
    }, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsArtisan])
def getArtisanProposals(request):
    artisan = ArtisanProfile.objects.get(user=request.user)
    job_proposals = JobProposal.objects.filter(artisan=artisan)
    
    if job_proposals.exists():
        print("It Exists")
        pending_proposals = job_proposals.filter(Q(status__icontains="pending"))
        accepted_proposals = job_proposals.filter(Q(status__icontains="accepted"))
        
        return Response({"all_proposals" : JobProposalResponseSerializer(job_proposals, many=True).data, "pending_proposals" : JobProposalResponseSerializer(pending_proposals, many=True).data, "accepted_proposals" : JobProposalResponseSerializer(accepted_proposals, many=True).data}, status=200)
    return Response({"message" : "No Proposals Found"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createJobProposal(request, artisan_username):
    user = request.user
    data = request.data
    try:
        user_with_artisan_username = User.objects.get(username=artisan_username)
        artisan = ArtisanProfile.objects.get(user=user_with_artisan_username)
    except ArtisanProfile.DoesNotExist:
        return Response({"message" : "No Artisan Found With That Username"}, status=404)
    except User.DoesNotExist:
        return Response({"message" : "No User Found With That Username"}, status=404)
    
    serializer = JobProposalSerializer(data=data)
    if serializer.is_valid():
        proposal = JobProposal.objects.create(
            user=user,
            artisan=artisan,
            description=serializer.validated_data['description'],
            price=serializer.validated_data['price'],
            location = serializer.validated_data['location']
        )
        proposal.save()
        serializer.id = proposal.id
        response_serializer = JobProposalResponseSerializer(proposal)
        return Response({"message" : f"Job Proposal Created and Sent To {artisan.user.username}", "data" : response_serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsArtisan])
def respondToJobProposal(request, proposal_id):
    try:
        proposal = JobProposal.objects.get(id=proposal_id)
    except JobProposal.DoesNotExist:
        return Response({"message": "Job proposal not found."}, status=404)

    if request.user.artisan_profile != proposal.artisan:
        return Response({"message": "You do not have permission to respond to this proposal."}, status=403)

    response = request.data['response']
    if response not in ['accepted', 'declined']:
        return Response({"message": "Invalid response."}, status=400)

    proposal.status = response
    proposal.save()

    return Response(JobProposalResponseSerializer(proposal).data, status=200)



#rating, and reviews(artisan and user), artisan notif
#artisan search
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from social_django.models import UserSocialAuth
from rest_framework.views import APIView
from .models import ArtisanProfile, ProfessionalQualifications
from .serializers import ArtisanProfileSerializer, ProfessionalQualificationsSerializer


class ArtisanProfileCreateView(generics.CreateAPIView):
    queryset = ArtisanProfile.objects.all()
    serializer_class = ArtisanProfileSerializer
    permission_classes = [IsAuthenticated]

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

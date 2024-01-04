from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from social_django.models import UserSocialAuth

from .serializers import UserRegistrationSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    data = request.data
    username = data['username']
    password = data['password']
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## SOCIAL MEDIA AUTHENTICATION
@api_view(['GET'])
@permission_classes([AllowAny])
def initiate_google_auth(request):
    return redirect('social:begin', 'google-oauth2')

from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from social_django.models import UserSocialAuth
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.models import User


from .serializers import UserRegistrationSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer

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
    serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        # If the serializer's response contains 'message', return it
        if 'message' in user:
            return user
        # Otherwise, return the success message
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## SOCIAL MEDIA AUTHENTICATION
@api_view(['GET'])
@permission_classes([AllowAny])
def initiate_google_auth(request):
    return redirect('social:begin', 'google-oauth2')


#### FORGOT PASSWORD
class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            mail_subject = 'Reset your password'
            print("Before Message")
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            print("After Message")
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email])
        return Response({"detail": "Password reset link sent"}, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()

            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
                mail_subject = 'Reset your password'
                message = f"""
                Hi {user.get_username()},
                
                You're receiving this email because you requested a password reset for your account.
                Please go to the following page and choose a new password:

                {reset_link}

                If you didn't request this, please ignore this email.

                Thanks,
                The Team
                """
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email])
        
            return Response({"detail": "Password reset link sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "There Is No Account registered with this email."}, status=status.HTTP_404_NOT_FOUND)



class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            print(user.email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            print(user.username)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been reset"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
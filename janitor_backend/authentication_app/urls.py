from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    user_login, 
    user_logout, 
    user_registration,
    initiate_google_auth
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path("login", user_login),
    path("user_logout", user_logout),
    path('register/', user_registration),
    
    path('google_auth/', initiate_google_auth)
]

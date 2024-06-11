from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .artisans_section.urls import *

from .views import (
    user_login, 
    user_logout, 
    user_registration,
    initiate_google_auth,

    #password reset views
    PasswordResetConfirmView,
    PasswordResetView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path("login", user_login),
    path("user_logout", user_logout),
    path('register/', user_registration),
    
    path('google_auth/', initiate_google_auth),

    # Password Reset
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Artisan Urls
    path("artisan/", include('authentication_app.artisans_section.urls'))
]

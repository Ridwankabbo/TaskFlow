from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    OtpVerificationView,
    ProfileView,
    PassResetView,
    ResendOTPView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('registration/', UserLoginView.as_view(), name='user-login'),
    path('otp-veriti/', OtpVerificationView.as_view(), name='otp-verifi'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('password-reset/', PassResetView.as_view(), name='password-reset'),
    
    
    path('token/access/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

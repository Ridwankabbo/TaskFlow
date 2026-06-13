from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    OtpVerificationView
)
urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/registration/', UserLoginView.as_view(), name='user-login'),
    path('user/otp-veriti/', OtpVerificationView.as_view(), name='otp-verifi')
]

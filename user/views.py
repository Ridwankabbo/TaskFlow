
from rest_framework import status
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    OptVerificationSerializer,
    ResetPasswordSerializer,
)
from .models import ( 
    User,
    UserProfile,
    ThirdPartyPlatforms,
    ThirdPartyPlatformCredentials
) 
from .utils import (
    BaseAPIView,
    OTPManager,
)
# Create your views here.


class UserRegistrationView(BaseAPIView):
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return self.success_response(
                message="Account created successfully, otp send to your email please check to verify your account",
                status_code=status.HTTP_201_CREATED
            )
        return self.failed_response(
            message="Failed to create your account, please try back later",
            data=serializer.errors
        )
            

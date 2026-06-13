
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
    generate_tokens
)
# Create your views here.

# ----------------------------
#   User regestration view
# ----------------------------
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
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
        
# ---------------------------
#   User login view
# ---------------------------
class UserLoginView(BaseAPIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            
            tokens = generate_tokens(request.user)
            return self.success_response(
                message="Login successfull",
                data={
                    "id":request.user.id,
                    "tokens":tokens
                },
                status_code=status.HTTP_200_OK
            )
            
            
# ---------------------------
#   Otp verification view
# ---------------------------        
class OtpVerificationView(BaseAPIView):
    
    def post(self, request):
        serializer = OptVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            return self.success_response(
                message="Otp verified successfull",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        return self.failed_response(
            message='Otp verification failed',
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
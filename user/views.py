
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    OptVerificationSerializer,
    ResendOTPSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer
)
from django.shortcuts import get_object_or_404
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
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# Create your views here.

# ----------------------------
#   User regestration view
# ----------------------------
class UserRegistrationView(BaseAPIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = UserRegistrationSerializer
    @extend_schema(
        request= UserRegistrationSerializer,
        parameters=[
            OpenApiParameter(
                name='sample_params',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Optional query param"
            )
        ]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return self.success_response(
                message="Account created successfully, otp send to your email please check to verify your account",
                data=serializer.data,
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
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = UserLoginSerializer
    @extend_schema(
        request= UserLoginSerializer,
        parameters=[
            OpenApiParameter(
                name='sample_params',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Optional query param"
            )
        ]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
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
        return self.failed_response(
            message='Failed to login',
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
            
# ---------------------------
#   Otp verification view
# ---------------------------        
class OtpVerificationView(BaseAPIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = OptVerificationSerializer
    @extend_schema(
        request=OptVerificationSerializer
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
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
        
# ----------------------
#   RESEND OTP
# ----------------------
class ResendOTPView(BaseAPIView):
    serializer_class = ResendOTPSerializer
    @extend_schema(
        request= ResendOTPSerializer
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(
                message="OTP resend successfull",
                status_code=status.HTTP_200_OK
            )
        return self.failed_response(
            message='Failed to resend OTP',
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )    

# -------------------
#   LOGOUT VIEW
#--------------------
class LogoutView(BaseAPIView):
    def post(self, request):
        try:
            refresh_token = request.data('refresh')
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            return self.success_response(
                message='You are successfully loged out',
                status_code=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return self.failed_response(
                message='Sorry failed to logout, Please try again',
                status_code=status.HTTP_400_BAD_REQUEST
            )

# --------------------------
#   PASSWORD RESET VIEW
# --------------------------
class PassResetView(BaseAPIView):
    serializer_class = ResetPasswordSerializer
    @extend_schema(
        request=ResetPasswordSerializer
    )
    def post(self, request):
        
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')
            user = get_object_or_404(User, id=request.user.id)
            user.password = new_password
            user.save()
            
            return self.success_response(
                message='Password reset successfull',
                status_code=status.HTTP_200_OK
            )
            

            
# ----------------------------
#   USER PROFILE VIEW
#-----------------------------   
class ProfileView(BaseAPIView):
    serializer_class = UserProfileSerializer
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = self.serializer_class(profile)
        
        return self.success_response(
            message='User profile view',
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
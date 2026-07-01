from .models import User, UserProfile
from rest_framework import serializers
from .utils import OTPManager
from django.contrib.auth import authenticate
from rest_framework import status

otp_management = OTPManager()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
        
    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        username = validated_data.get('username')
        user = User.objects.create_user(
            email=email,
            password = password,
            username = username
        )
        generated_otp = otp_management.generate_otp()
        otp_management.store_otp(email, generated_otp, 'singup')
        print("generated otp", generated_otp)
        # otp_management.send_verification_otp(email, generated_otp, 'singup')
        return validated_data
        
    
        
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        
        
    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        
        if not email :
            raise serializers.ValidationError(
                {
                    "message":"Email is required",
                    "status":status.HTTP_400_BAD_REQUEST
                }
            )
        if not password:
            raise serializers.ValidationError(
                {
                    "message":"Password is required",
                    "status":status.HTTP_400_BAD_REQUEST
                }
            )
            
        if not email and password:
            raise serializers.ValidationError(
                {
                    "message":"Email and Password is required",
                    "status":status.HTTP_400_BAD_REQUEST
                }
            )
        
        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError(
                {
                    "message":"Please register before login",
                    "status":status.HTTP_404_BAD_REQUEST
                }
            )
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "message":"Account is not activated",
                    "status":status.HTTP_400_BAD_REQUEST
                }
            )
            
        return attrs 
        
        
class OptVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    purpase = serializers.CharField()
    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        purpase = attrs['purpase']
        verify_otp = otp_management.verify_otp(email=email, otp=otp, purpase=purpase)
        if not verify_otp :
            raise serializers.ValidationError({
                "message":"Invalid otp"
            })
        if purpase == 'singup':
            try:
                user = User.objects.get(email=email)
                user.is_active=True
                user.save()
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "message":"User with this email is not found"
                })
        return attrs

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpase = serializers.CharField()
    
    
    def create(self, validated_data):
        email = validated_data.get('email')
        purpase = validated_data.get('purpase')
        otp_management = OTPManager()
        try:
            user = User.objects.get(email=email)
            regenerate_otp = otp_management.generate_otp()
            otp_management.store_otp(email, regenerate_otp, purpase)
            print("regenerated_otp: ", regenerate_otp)
        except User.DoesNotExist:
            raise ValueError("User with the email doesn't exists")
        return validated_data

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "message":"new password and confirm password doesn't match"
            })
        return attrs
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
    




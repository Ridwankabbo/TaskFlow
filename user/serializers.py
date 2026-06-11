from .models import User, UserProfile
from rest_framework import serializers
from .utils import OTPManager

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
        otp_management.send_verification_otp(email, generated_otp, 'singup')
        return 
        
    
        
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        
        
class OptVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] == attrs['confirm_password']:
            raise serializers.ValidationError({
                "message":"new password and confirm password doesn't match"
            })
        return attrs
    




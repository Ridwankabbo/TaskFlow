from .models import User, UserProfile
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
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
    




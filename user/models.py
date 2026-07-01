from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
# Create your models here.


class CustomUserModel(BaseUserManager):
    
    def create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password, username, **extra_fields):
        user = self.create_user(email, password, username, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        
        user.save(using=self._db)
        
        return user
    
    
class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserModel()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"name:{self.username} email:{self.email}"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_avatar', null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    assignment_count = models.IntegerField(default=0)
    # stripe_customer_id=models.CharField(max_length=255, null=True, blank=True)

    
class ThirdPartyPlatforms(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='third_party_platforms')
    platform_name = models.CharField(max_length=255)
    connection_status = models.BooleanField(default=False)
    
class ThirdPartyPlatformCredentials(models.Model):
    platform = models.ForeignKey(ThirdPartyPlatforms, on_delete=models.CASCADE, related_name='platform_credentials')
    accout_link = models.URLField()
    access_token = models.CharField(max_length=255, null=True, blank=True)
    acces_expire_in = models.IntegerField()
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_expire_in = models.IntegerField()
    
class Assingments(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assingments')
    name = models.CharField()
    description = models.TextField()
    implimentation = models.JSONField(default=list)
    score = models.IntegerField(default=1)
    dedline = models.DateTimeField()
    

from django.core.cache import cache
import random
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def generate_verification_template(otp):
    
    template = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email Address</title>
    <style>
        /* Target specific email client quirks */
        body, table, td, a {{ text-size-adjust: 100%; -webkit-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        table {{ border-collapse: collapse !important; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
    </style>
</head>
<body style="background-color: #f4f6f8; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 0;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td align="center" style="padding: 40px 10px 40px 10px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); overflow: hidden;">
                    <!-- Header/Logo Area -->
                    <tr>
                        <td align="center" style="padding: 40px 40px 20px 40px; border-bottom: 1px solid #f0f0f0;">
                            <!-- Replace with your logo URL -->
                            <img src="https://placeholder.com" alt="Company Logo" width="120" style="display: block; font-family: sans-serif; font-size: 18px; font-weight: bold; color: #1a1a1a;">
                        </td>
                    </tr>
                    <!-- Main Body Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <h2 style="margin: 0 0 20px 0; font-size: 22px; font-weight: 700; color: #1a1a1a; line-height: 1.3;">Verify your email address</h2>
                            <p style="margin: 0 0 30px 0; font-size: 15px; color: #555555; line-height: 1.6;">Thank you for signing up! Please use the verification code below to complete your registration. This code will expire in 15 minutes.</p>
                            
                            <!-- Verification Code Container -->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" style="background-color: #f1f5f9; padding: 20px; border-radius: 6px; letter-spacing: 5px;">
                                        <span style="font-family: 'Courier New', Courier, monospace; font-size: 32px; font-weight: bold; color: #2563eb;">{otp}</span>
                                    </td>
                                </tr>
                            </table>

                            <p style="margin: 30px 0 0 0; font-size: 13px; color: #888888; line-height: 1.5;">If you did not request this email, you can safely ignore it. Your account security has not been compromised.</p>
                        </td>
                    </tr>
                    <!-- Footer Area -->
                    <tr>
                        <td style="padding: 0 40px 40px 40px; text-align: center;">
                            <p style="margin: 0; font-size: 12px; color: #aaaaaa; line-height: 1.5;">&copy; 2026 Your Company Name. All rights reserved.<br>123 Innovation Way, Tech City, TC 94016</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""



class OTPManager:
    
    OTP_EXPIRATION_TIME = 300 # OTP expiration time in seconds
    
    @classmethod
    def generate_otp(self):
        return str(random.randint(100000, 999999))
    
    @classmethod
    def store_otp(self, email, otp, purpose):
        key = f"{email}_{purpose}"
        cache.set(key, otp, timeout=self.OTP_EXPIRATION_TIME)
    
    @classmethod
    def verify_otp(self, email, otp, purpase):
        key = f"{email}_{purpase}"
        stored_opt = cache.get(key)
        if stored_opt==otp:
            cache.delete(key)
                        
            if purpase == "password_reset":
                key = f"{email}_password_reset_verified"
                cache.set(key, True, timeout=self.OTP_EXPIRATION_TIME)
                
            return True
        return False
    @classmethod   
    def is_password_reset_verefied(slef, otp, email):
        return cache.get(f"{email}_password_reset_verified")
    
    @classmethod
    def send_verification_otp(self, email, otp, purpase):
        
        if purpase == "singup":
            subject = "Verify opt for singup"
            from_email = settings.EMAIL_HOST_USER
            to = [email]
            context = {
                'otp': otp
            }
            html_content = render_to_string('email_template/otp_verification.html', context=context)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, from_email, to)
            email.attach_alternative(html_content, 'text/html')
            email.send()
        elif purpase == "password_reset":
            subject = "Password reset opt for verification"
            from_email = settings.EMAIL_HOST_USER
            to = [email]
            context = {
                'otp': otp
            }
            message = generate_verification_template(otp)
            
        else:
            raise ValueError("Invalid otp")
        
           
""" 
    =====================
        BASE API View
    =====================
"""           
from rest_framework.decorators import APIView
from rest_framework.response import Response 
from rest_framework import status

class BaseAPIView(APIView):
    
    def _get_user(self, request):
        return request.user
    
    def _get_user_id(slef, request):
        return request.user.id
    
    def _get_user_profile_object(self, request, profile):
        profile = profile.objects.get(id=request.user)
        return profile
    
    def success_response(self, message, data=None, status_code=None):
        
        return Response({
            "stauts":True,
            "message":message,
            "data":data,
            "status":status_code
        }, status=status.HTTP_200_OK) 
        
    def failed_response(self, message, data, status_code):
        
        return Response({
            "stauts":True,
            "message":message,
            "data":data,
            "status":status_code
        }, status=status.HTTP_400_BAD_REQUEST) 

""" 
    =========================
        TOKEN GENERATOR
    =========================
"""                   
from rest_framework_simplejwt.tokens import RefreshToken               
def generate_tokens(user):
    refresh_token = RefreshToken.for_user(user)
    return {
        "access_token":str(refresh_token.access_token),
        "refresh_token": str(refresh_token)
    }
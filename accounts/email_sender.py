from django.core.mail import send_mail
from django.conf import settings

def OTPEmailSender(email, verify_otp):
	message = f"{email},\n Your OTP is {verify_otp}\nThanks"
	send_mail(
		"Email Verify OTP Is Ready - BUKINOW",
		message,
    	settings.EMAIL_HOST_USER,
    	[email],
    	fail_silently=False)
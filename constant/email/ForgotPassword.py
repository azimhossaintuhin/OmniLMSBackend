# utils.py (or a similar utility file)
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime  # Correct import for datetime
from decouple import config
import logging

# Set up logging
logger = logging.getLogger(__name__)

def send_forgot_password_email(user, reset_link):
    try:
        subject = "Reset Your Password"
        
        # Create a plain text message
        plain_message = f"""
        Hi {user.username},  # You can adjust this based on how you want to address the user.
        
        We received a request to reset your password. Please click the link below to reset it:
        
        {reset_link}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Your Team
        {datetime.now().year}
        """
        
        from_email = config("EMAIL_HOST_USER")  # Get the default from email
        to = user.email  # User's email address
        logger.debug(f'Sending email to {to}')  # Debug log

        # Send the email
        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            fail_silently=False,  # Set to True to ignore errors during sending
        )
        return True
    except Exception as e:
        logger.exception("Exception occurred while sending forgot password email")  # Log the exception
        return False

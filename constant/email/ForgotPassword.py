from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime
from decouple import config
import logging

# Set up logging
logger = logging.getLogger(__name__)

def send_forgot_password_email(user, reset_link):
    try:
        subject = "Reset Your Password"
        
        # Context for the HTML template
        context = {
            'username': user.username,
            'reset_link': reset_link,
            'year': datetime.now().year
        }
        
        try:
            # Move template rendering inside the function
            html_message = render_to_string('forgotpass.html', context)
        except Exception as template_error:
            logger.error(f"Template error: {template_error}")
            # Fallback to plain text email if template fails
            html_message = None
        
        # Create a plain text version for fallback
        plain_message = f"""
        Hi {user.username},  
        
        We received a request to reset your password. Please click the link below to reset it:
        
        {reset_link}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Your Team
        {datetime.now().year}
        """
        
        from_email = config("EMAIL_HOST_USER")
        to = user.email
        
        logger.info(f'Attempting to send password reset email to {to}')

        # Send the email
        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f'Successfully sent password reset email to {to}')
        return True
        
    except Exception as e:
        logger.exception("Exception occurred while sending forgot password email")
        return False
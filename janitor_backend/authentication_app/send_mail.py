# from datetime import datetime
# from smtplib import SMTPAuthenticationError

# # Core Django Packages Import
# from django.template.loader import render_to_string
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.core.mail import EmailMessage
# from django.conf import settings

# # custom library imports
# from .tokens import account_activation_token


# DOMAIN = 'tverza-c9ye.onrender.com'
# def activateEmail(request, user, user_email):
#     """ 
#     Sends an email to the user with an activation link.
#     Args:
#         request: The HTTP request object.
#         user: The user instance for whom the activation email is being sent.
#         user_email: The email address of the user.
#     Returns:
#         A message indicating the result of the email sending operation.
#     """
    
#     email_subject = "Activate Your User Account."
#     message = render_to_string(
#         "authentication_app/account_activation.html",
#         {
#             "user" : user.username,
#             "domain" : DOMAIN,
#             "id" : urlsafe_base64_encode(force_bytes(user.id)),
#             "token" : account_activation_token.make_token(user),
#             "protocol" : "https" if request.is_secure() else "http",
#             "year" : datetime.now().year
#         }
#     )
#     email = EmailMessage(
#         email_subject,
#         message,
#         from_email=settings.EMAIL_HOST_USER,
#         to=[user_email]
#     )
#     email.content_type = "text/html"
#     email.content_subtype = "html"
    
#     try:
#         if email.send():
#             return f"Please Check your Email at '{user_email}', and Click the Activation Link to Complete Your Registration"
#         else:
#             return f"Error Sending Mail to '{user_email}'. Please Check to Make Sure You Entered a Valid Email Address"
#     except SMTPAuthenticationError as e:
#         return f"an Error Occured, {e}"



from datetime import datetime
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from smtplib import SMTPAuthenticationError

from .tokens import account_activation_token


def activateEmail(request, user, user_email):
    email_subject = "Activate Your User Account."

    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = account_activation_token.make_token(user)

    activation_link = (
        f"{settings.FRONTEND_URL}/pages/verify-email.html"
        f"?uid={uid}&token={token}"
    )

    message = render_to_string(
        "authentication_app/account_activation.html",
        {
            "user": user.username,
            "activation_link": activation_link,
            "year": timezone.now().year
        }
    )

    email = EmailMessage(
        email_subject,
        message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email]
    )

    email.content_subtype = "html"

    try:
        if email.send():
            return (
                f"Please check your email at '{user_email}' "
                "and click the activation link to complete registration."
            )

        return f"Error sending mail to '{user_email}'."

    except SMTPAuthenticationError as e:
        return f"An error occurred: {e}"
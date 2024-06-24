from smtplib import SMTPAuthenticationError

# Core Django Packages Import
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings

# custom library imports
from .tokens import account_activation_token


DOMAIN = 'tverza-c9ye.onrender.com'
def activateEmail(request, user, user_email):
    email_subject = "Activate Your User Account."
    message = render_to_string(
        "authentication_app/account_activation.html",
        {
            "user" : user.username,
            # "domain" : request.get_host(),
            "domain" : DOMAIN,
            "id" : urlsafe_base64_encode(force_bytes(user.id)),
            "token" : account_activation_token.make_token(user),
            "protocol" : "https" if request.is_secure() else "http"
        }
    )
    #message = """
    #    <html>
    #    <head></head>
    #    <body>
    #        <h2>Activate Your Account</h2>
    #        <p>Hello {username},</p>
    #        <p>Thank you for registering on our website. Please click the link below to activate your account:</p>
    #        <p><a href="{activation_link}" target="_blank">Activate Now</a></p>
    #        <p>If you did not sign up for an account, please ignore this email.</p>
    #        <p>Regards,<br> Tverza</p>
    #    </body>
    #    </html>
    #""".format(username=user.username, activation_link="https://example.com/activation_link")



    email = EmailMessage(email_subject, message, from_email=settings.EMAIL_HOST_USER, to=[user_email])
    email.content_type = "text/html"
    email.content_subtype = "html"
    print("Sending Mail........")

    try:
        if email.send():
            return f"Please Check your Email at '{user_email}', and Click the Activation Link to Complete Your Registration"
        else:
            return f"Error Sending Mail to '{user_email}'. Please Check to Make Sure You Entered a Valid Email Address"
    except SMTPAuthenticationError as e:
        return f"an Error Occured, {e}"

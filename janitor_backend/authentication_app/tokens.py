from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
        This Generates A Token For User Account Verification (Through Email)
    """
    def __hash__(self, user, timestamp):
        return (
            six.text_type(user.id) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()
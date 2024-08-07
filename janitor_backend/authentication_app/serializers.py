from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .utilities import check_user_activation_status
from .send_mail import activateEmail

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    
    def create(self, validated_data):
        activation_status = check_user_activation_status(validated_data['username'], validated_data['email'])

        if activation_status == "is_not_activated":
            user = User.objects.get(username=validated_data['username'])
            email_message = activateEmail(self.context['request'], user, user.email)
            response = {"message": email_message}
            return response
        elif activation_status == "This Username Already Exists With A Different Email.":
            raise serializers.ValidationError({"username": "This Username Already Exists With A Different Email."})
        else:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            user.is_active = False
            email_message = activateEmail(self.context['request'], user, user.email)
            response = {"message": email_message}
            return response


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, max_length=128)


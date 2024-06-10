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

    # def registerUserAndSendActivationMail(self, request, serializer):
    #     validated_data = serializer.validated_data
    #     response = {}
        
    #     activation_status = check_user_activation_status(validated_data['username'], validated_data['email'])
        
    #     if activation_status == "is_not_activated":
    #         user = User.objects.get(username=validated_data['username'])
    #         email_message = activateEmail(request, user, user.email)
    #     elif activation_status == "This Username Already Exists With A Different Email.":
    #         return Response({"username": "This Username Already Exists With A Different Email."}, status=status.HTTP_401_UNAUTHORIZED)
    #     else:
    #         if serializer.is_valid():   
    #             user = serializer.save()
    #             email_message = activateEmail(request, user, user.email)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    #     response["message"] = email_message
    #     return Response(response, status=status.HTTP_201_CREATED)

    
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
            email_message = activateEmail(self.context['request'], user, user.email)
            response = {"message": email_message}
            return response


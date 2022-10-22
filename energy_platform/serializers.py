from abc import ABC

from rest_framework import serializers
from energy_platform.models import User, Device
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'role')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'description', 'address', 'max_hourly_consumption')


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['name', 'email', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None or not email:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None or not password:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise serializers.ValidationError('An user with this email and password was not found.')

        return {
            'email': user.email,
            'name': user.name,
            'token': user.token
        }

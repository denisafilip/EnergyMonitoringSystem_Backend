from rest_framework import serializers
from energy_platform.models import User, Device, UserToDevice, Consumption, ChatMessage
from django.contrib.auth import authenticate
# from django_grpc_framework import proto_serializers
# from .grpc_gen import chat_pb2


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'role')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'description', 'address', 'max_hourly_consumption')


class UserToDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToDevice
        fields = ('id', 'user', 'device')


class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumption
        fields = ('id', 'mapping', 'consumption', 'timestamp')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=10, read_only=True)

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
            'role': user.role,
            'token': user.token,
        }

"""class ChatMessageProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = ChatMessage
        proto_class = chat_pb2.ChatMessage
        fields = ['id', 'sender', 'receiver', 'content']"""

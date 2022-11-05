from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Device, UserToDevice, Consumption
from .renderers import UserJSONRenderer
from . import serializers


class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('email')
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('email')
        email = self.request.query_params.get('email')
        if email is not None or email:
            queryset = queryset.filter(email=email)
        return queryset


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('name')
    serializer_class = serializers.DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.all().order_by('name')
        name = self.request.query_params.get('name')
        if name is not None or name:
            queryset = queryset.filter(name=name)
        return queryset


class UserToDeviceViewSet(viewsets.ModelViewSet):
    queryset = UserToDevice.objects.values()
    serializer_class = serializers.UserToDeviceSerializer

    def get_queryset(self):
        queryset = UserToDevice.objects.all()
        user = self.request.query_params.get('user')
        if user is not None or user:
            queryset = queryset.filter(user=user)
        device = self.request.query_params.get('device')
        if device is not None or device:
            queryset = queryset.filter(device=device)
        return queryset


class ConsumptionViewSet(viewsets.ModelViewSet):
    queryset = Consumption.objects.all()
    serializer_class = serializers.ConsumptionSerializer

    def get_queryset(self):
        queryset = Consumption.objects.all()
        mapping = self.request.query_params.get('mapping')
        if mapping is not None or mapping:
            queryset = queryset.filter(mapping=mapping)
        timestamp = self.request.query_params.get('timestamp')
        if timestamp is not None or timestamp:
            queryset = queryset.filter(timestamp=timestamp)
        date = self.request.query_params.get('date')
        if date is not None or date:
            queryset = queryset.filter(timestamp__date=date)
        return queryset


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data

        if not user["name"]:
            return Response({
                'error': ['Name field cannot be blank!'],
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user["email"]:
            return Response({
                'error': ['Email field cannot be blank!'],
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user["password"]:
            return Response({
                'error': ['Password field cannot be blank!'],
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        user = request.data

        if not user["email"]:
            return Response({
                'error': ['Email field cannot be blank!'],
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user["password"]:
            return Response({
                'error': ['Password field cannot be blank!'],
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=user, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
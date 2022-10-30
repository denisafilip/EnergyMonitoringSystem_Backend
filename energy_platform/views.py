from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Device
from .renderers import UserJSONRenderer
from . import serializers


class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="CLIENT").values().order_by('email')
    serializer_class = serializers.UserSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = User.objects.filter(role="CLIENT").values().order_by('email')
        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(email=email)
        return queryset


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('description')
    serializer_class = serializers.DeviceSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


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
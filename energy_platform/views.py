from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .renderers import UserJSONRenderer
from .serializers import UserSerializer, LoginSerializer, RegistrationSerializer

import traceback


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('email')
    serializer_class = UserSerializer


"""class LoginViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def create(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
"""


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

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

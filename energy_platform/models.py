from django.db import models
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role="CLIENT"):
        """Create and return a `User` with an email, name, role and password."""
        if name is None:
            raise TypeError('Users must have a name.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(name=name, email=self.normalize_email(email), role=role)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password, role="ADMIN"):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, name, password, role=role)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Role(models.TextChoices):
        ADMIN = "ADMIN"
        CLIENT = "CLIENT"
    role = models.CharField(choices=Role.choices, max_length=10, default=Role.CLIENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'role': self.role,
            'exp': dt
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def is_staff(self):
        return self.role == self.Role.ADMIN


class Device(models.Model):
    name = models.CharField(max_length=100, default="Name")
    description = models.CharField(max_length=500)
    address = models.CharField(max_length=200)
    max_hourly_consumption = models.IntegerField()

    def __str__(self):
        return f"Device {self.name} from {self.address}, consumes max {self.max_hourly_consumption}."


class UserToDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return f"Mapping between client {self.user} and device {self.device}."


class Consumption(models.Model):
    mapping = models.ForeignKey(UserToDevice, on_delete=models.CASCADE)
    consumption = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consumption for {self.mapping} is {self.consumption} at {self.timestamp}."

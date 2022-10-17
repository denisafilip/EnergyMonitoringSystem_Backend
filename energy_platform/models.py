from django.db import models


class User(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Role(models.TextChoices):
        ADMIN = "ADMIN"
        CLIENT = "CLIENT"
    role = models.CharField(choices=Role.choices, max_length=10, default=Role.CLIENT)

    def __str__(self):
        return f"{self.email}"


class Device(models.Model):
    description = models.CharField(max_length=500)
    address = models.CharField(max_length=200)
    max_hourly_consumption = models.IntegerField()

    def __str__(self):
        return f"Description: {self.description}, from {self.address}, consumes {self.max_hourly_consumption} per hour."


class UserToDevice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)


class Consumption(models.Model):
    mapping_id = models.ForeignKey(UserToDevice, on_delete=models.CASCADE)
    consumption = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


from django.contrib import admin
from .models import User, Device, UserToDevice, Consumption

admin.site.register(User)
admin.site.register(Device)
admin.site.register(UserToDevice)
admin.site.register(Consumption)

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'mappings', views.UserToDeviceViewSet)
router.register(r'consumptions', views.ConsumptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(r'login/', views.LoginAPIView.as_view()),
    path(r'register/', views.RegistrationAPIView.as_view())
]

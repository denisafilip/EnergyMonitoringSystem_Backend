from django.urls import include, path
from rest_framework import routers
from . import views
# from .grpc_gen import chat_pb2_grpc

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

"""def grpc_handlers(server):
    chat_pb2_grpc.add_ChatMessageControllerServicer_to_server(views.ChatMessageService.as_servicer(), server)"""


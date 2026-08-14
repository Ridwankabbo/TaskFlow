from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssigmentViewSet

router = DefaultRouter()
router.register(r'', AssigmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
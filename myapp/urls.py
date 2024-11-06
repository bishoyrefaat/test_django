# myapp/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import StapModelViewSet

router = routers.DefaultRouter()
router.register(r"stapmodels", StapModelViewSet, basename="stapmodel")

urlpatterns = [
    path("api/", include(router.urls)),
]

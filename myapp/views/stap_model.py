# myapp/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import StapModel
from ..serializers import StapModelSerializer
import logging

logger = logging.getLogger(__name__)


class StapModelViewSet(viewsets.ModelViewSet):
    queryset = StapModel.objects.all()
    serializer_class = StapModelSerializer

    def list(self, request, *args, **kwargs):
        """List all StapModel instances."""
        response = super().list(request, *args, **kwargs)
        return Response({"data": response.data})

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific StapModel instance."""
        response = super().retrieve(request, *args, **kwargs)
        return Response({"data": response.data})

    def create(self, request, *args, **kwargs):
        """Create a new StapModel instance."""
        response = super().create(request, *args, **kwargs)
        return Response({"data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update an existing StapModel instance."""
        response = super().update(request, *args, **kwargs)
        return Response({"data": response.data})

    def destroy(self, request, *args, **kwargs):
        """Delete a StapModel instance."""
        super().destroy(request, *args, **kwargs)
        return Response(
            {"data": "StapModel deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

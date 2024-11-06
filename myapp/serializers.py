from rest_framework import serializers
from .models import StapModel


class StapModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StapModel
        fields = ["id", "name", "odoo_id", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

from django.contrib import admin
from .models import StapModel
from .services.odoo_service import OdooService
import logging

logger = logging.getLogger(__name__)


@admin.register(StapModel)
class StapModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "odoo_id", "created_at", "updated_at")
    search_fields = ("name",)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to sync with Odoo when saving via admin.
        """
        super().save_model(request, obj, form, change)
        odoo = OdooService()
        try:
            if change:
                # Update existing record in Odoo
                odoo.write_record(
                    "stap.model",
                    obj.odoo_id,
                    {
                        "name": obj.name,
                    },
                )
                logger.info(f"StapModel (ID: {obj.id}) synced to Odoo.")
            else:
                # Create new record in Odoo
                odoo_id = odoo.create_record(
                    "stap.model",
                    {
                        "name": obj.name,
                    },
                )
                obj.odoo_id = odoo_id["data"][0]["id"]
                obj.save(update_fields=["odoo_id"])
                logger.info(
                    f"StapModel (ID: {obj.id}) created in Odoo with Odoo ID: {odoo_id}."
                )
        except Exception as e:
            logger.error(f"Error syncing StapModel to Odoo: {e}")

    def delete_model(self, request, obj):
        """
        Override delete_model to sync deletion with Odoo when deleting via admin.
        """
        odoo = OdooService()
        try:
            if obj.odoo_id:
                odoo.unlink_record("stap.model", obj.odoo_id)
                logger.info(f"StapModel (ID: {obj.id}) deleted from Odoo.")
        except Exception as e:
            logger.error(f"Error deleting StapModel from Odoo: {e}")
        super().delete_model(request, obj)

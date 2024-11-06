# app/services/odoo_service.py
import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class OdooService:
    def __init__(self, config=None):
        """
        Initialize the OdooService with configuration.

        :param config: Optional dictionary to override default settings.
        """
        # Load configuration from Django settings or use defaults
        odoo_config = config or getattr(settings, "ODOO_CONFIG", {})
        self.api_url = odoo_config.get("API_URL", "http://localhost:8069")
        self.db = odoo_config.get("DB", "integration_test4")
        self.username = odoo_config.get("USERNAME", "admin")
        self.password = odoo_config.get("PASSWORD", "admin")
        self.session = requests.Session()
        self.uid = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticate with Odoo and store the user ID (uid).
        """
        url = f"{self.api_url}/web/session/authenticate"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "db": self.db,
                "login": self.username,
                "password": self.password,
            },
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = self.session.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            result = response.json()
            if result.get("result") and result["result"].get("uid"):
                self.uid = result["result"]["uid"]
                logger.info(f"Authenticated with Odoo. UID: {self.uid}")
            else:
                logger.error(f"Authentication failed: {result}")
                raise Exception("Authentication failed.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Odoo: {e}")
            raise

    def call_method(self, model, method, args=None, record_id=None):
        """
        General method to call any Odoo model method.

        :param model: Odoo model name as string (e.g., 'stap.model').
        :param method: Method name to call on the model (e.g., 'create').
        :param args: List of positional arguments for the method.
        :param kwargs: Dictionary of keyword arguments for the method.
        :return: Result from Odoo API.
        """

        url = f"{self.api_url}/api/stap_models{'/'+str(record_id) if record_id else ''}"  # Adjust if using a different endpoint

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "data": args or [],
            },
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = self.session.request(
                method, url, data=json.dumps(payload), headers=headers
            )
            response.raise_for_status()
            result = response.json()
            if "error" in result:
                logger.error(f"Odoo API error: {result['error']}")
                raise Exception(f"Odoo API error: {result['error']}")
            return result.get("result")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to call method '{method}' on model '{model}': {e}")
            raise

    def create_record(self, model, data):
        """
        Create a new record in the specified Odoo model.

        :param model: Odoo model name as string.
        :param data: Dictionary of fields and values to create the record.
        :return: ID of the created record.
        """
        result = self.call_method(model, "post", args=[data])
        logger.info(f"Record created in Odoo {model} with ID: {result}")
        return result

    def write_record(self, model, record_id, data):
        """
        Update an existing record in the specified Odoo model.

        :param model: Odoo model name as string.
        :param record_id: ID of the record to update.
        :param data: Dictionary of fields and values to update.
        :return: True if successful, False otherwise.
        """
        result = self.call_method(model, "put", args=data, record_id=record_id)
        if result:
            logger.info(
                f"Record with ID {record_id} in Odoo {model} updated successfully."
            )
        else:
            logger.error(
                f"Failed to update record with ID {record_id} in Odoo {model}."
            )
        return result

    def unlink_record(self, model, record_id):
        """
        Delete a record from the specified Odoo model.

        :param model: Odoo model name as string.
        :param record_id: ID of the record to delete.
        :return: True if successful, False otherwise.
        """
        result = self.call_method(model, "delete", record_id=record_id)
        if result:
            logger.info(
                f"Record with ID {record_id} in Odoo {model} deleted successfully."
            )
        else:
            logger.error(
                f"Failed to delete record with ID {record_id} in Odoo {model}."
            )
        return result

    def read_record(self, model, record_id, fields=None):
        """
        Read a record's details from the specified Odoo model.

        :param model: Odoo model name as string.
        :param record_id: ID of the record to read.
        :param fields: List of fields to retrieve. If None, retrieves all fields.
        :return: Dictionary of field values.
        """
        result = self.call_method(model, "read", args=[[record_id], fields])
        if result:
            logger.info(
                f"Record with ID {record_id} in Odoo {model} read successfully."
            )
            return result[0]  # Assuming single record
        else:
            logger.error(f"Failed to read record with ID {record_id} in Odoo {model}.")
            return None

    def search_records(
        self, model, domain=None, fields=None, limit=80, offset=0, order=None
    ):
        """
        Search for records in the specified Odoo model.

        :param model: Odoo model name as string.
        :param domain: List defining the search domain.
        :param fields: List of fields to retrieve.
        :param limit: Maximum number of records to return.
        :param offset: Number of records to skip.
        :param order: Sorting order.
        :return: List of records matching the search criteria.
        """
        args = []
        if domain:
            args.append(domain)
        else:
            args.append([])  # Empty domain to fetch all records

        kwargs = {
            "fields": fields or [],
            "limit": limit,
            "offset": offset,
            "order": order or "",
        }

        result = self.call_method(model, "search_read", args=args, kwargs=kwargs)
        logger.info(
            f"Search completed on Odoo {model}. Number of records found: {len(result)}"
        )
        return result

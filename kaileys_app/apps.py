from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError


class KaileysAppConfig(AppConfig):
    """
    Configuration class for the 'kaileys_app' Django application.

    This class defines metadata and settings for the application,
    such as the default field type for auto-incrementing primary keys
    and a human-readable name for the app in the Django admin.
    """

    # Define the type of auto-incrementing primary key for models
    default_auto_field = 'django.db.models.BigAutoField'

    # The name of the app, matching the app directory name
    name = 'kaileys_app'

    # Human-readable name for the app, displayed in the Django admin
    verbose_name = 'Kaileys Consortium'

    def ready(self):
        """
        Automatically creates a superuser if it does not exist.
        This runs after the app registry and database are ready.
        """
    
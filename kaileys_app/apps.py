from django.apps import AppConfig

class KaileysAppConfig(AppConfig):
    """
    Configuration class for the 'kaileys_app' Django application.
    
    This class defines metadata and settings for the application,
    such as the default field type for auto-incrementing primary keys
    and a human-readable name for the app in the Django admin.
    """
    
    # Define the type of auto-incrementing primary key for models
    # BigAutoField is a 64-bit integer, suitable for large datasets
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name of the app, matching the app directory name
    name = 'kaileys_app'
    
    # Human-readable name for the app, displayed in the Django admin
    verbose_name = 'Kaileys Consortium'
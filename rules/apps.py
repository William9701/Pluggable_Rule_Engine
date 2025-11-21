from django.apps import AppConfig


class RulesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rules"

    def ready(self):
        """
        Import rules when the app is ready to ensure they are registered.
        """
        # Import rules to trigger auto-registration
        from . import order_rules  # noqa: F401

from django.apps import AppConfig


class MyauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myAuth"

    def ready(self) -> None:
        from . import notifications  # noqa: F401

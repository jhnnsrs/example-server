from django.apps import AppConfig


class DemoConfig(AppConfig):
    """The demo app.

    A deliberately tiny Django app whose only purpose is to show how to expose
    a model over GraphQL with the arkitekt stack (authentikate + koherent +
    kante + strawberry-django).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "demo"

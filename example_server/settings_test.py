from .settings import *  # noqa
from .settings import DATABASES, AUTHENTIKATE
import logging

# In-memory SQLite keeps the test suite fast and dependency-free, which is all
# the schema/config smoke tests need. Note: executing async GraphQL operations
# that *write* to the DB will deadlock on SQLite (its single writer collides
# with pytest-django's open transaction) — for those, run against a real
# Postgres, as the alpaka service's test harness does.
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
    "OPTIONS": {
        "timeout": 30,
    },
    "TEST": {
        "NAME": ":memory:",
    },
}
# Django forces DEBUG=False under the test runner, and authentikate 3.0 refuses static
# tokens when DEBUG is False. These are deliberate test fixtures, so opt in explicitly.
AUTHENTIKATE = {**AUTHENTIKATE, "allow_static_tokens_in_production": True, "static_tokens": {"test": {"sub": "1"}}}

# Disable migrations for faster tests
class DisableMigrations:
    """Disable migrations during testing for faster test execution."""
    
    def __contains__(self, item: str) -> bool:
        """Check if item is in migration modules."""
        return True
    
    def __getitem__(self, item: str) -> None:
        """Get migration module for item."""
        return None

# For faster test execution, you can uncomment this:
# MIGRATION_MODULES = DisableMigrations()

# Disable logging during tests to reduce noise
logging.disable(logging.CRITICAL)

# Enable database access from async code in tests
DATABASE_ROUTERS = []

# Use in-memory channel layer for tests instead of Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

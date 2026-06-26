"""Filtering and ordering for the demo types.

``strawberry_django`` turns these into GraphQL input types that the auto-paginated
list fields accept (e.g. ``items(filters: {search: "foo"}, order: {name: ASC})``).
"""

import strawberry
import strawberry_django
from django.db.models import Q
from strawberry import auto

from demo import models


@strawberry_django.order_type(models.Item)
class ItemOrder:
    """Ordering options for items."""

    created_at: auto
    name: auto


@strawberry_django.filter_type(models.Item)
class ItemFilter:
    """Filtering options for items."""

    @strawberry_django.filter_field
    def ids(self, value: list[strawberry.ID], prefix: str) -> Q:
        """Keep only items whose id is in ``value``."""
        return Q(**{f"{prefix}id__in": value})

    @strawberry_django.filter_field
    def search(self, value: str, prefix: str) -> Q:
        """Case-insensitive match on the item name."""
        return Q(**{f"{prefix}name__icontains": value})

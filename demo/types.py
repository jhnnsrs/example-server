"""GraphQL types for the demo app.

``kante.django_type`` maps the Django model onto a strawberry type, wiring up
pagination, filtering and ordering. Related ``User`` / ``Organization`` fields
reuse the strawberry types shipped by authentikate, so they resolve out of the
box.
"""

import datetime

import kante
import strawberry
from authentikate.strawberry.types import Organization, User

from demo import filters, models


@kante.django_type(models.Item, pagination=True, filters=filters.ItemFilter, ordering=filters.ItemOrder)
class Item:
    """A simple demo item exposed over GraphQL."""

    id: strawberry.ID
    name: str
    description: str | None
    creator: User | None
    organization: Organization
    created_at: datetime.datetime

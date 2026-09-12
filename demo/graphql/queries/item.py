"""Query resolvers for items.

These are plain functions; the schema turns them into fields. ``Info`` carries
the authenticated request (user, organization, client) populated by
authentikate's extension.
"""

import strawberry
from kante.types import Info

from demo import models, types


def item(info: Info, id: strawberry.ID) -> types.Item:
    """Return a single item by id."""
    return models.Item.objects.get(id=id)

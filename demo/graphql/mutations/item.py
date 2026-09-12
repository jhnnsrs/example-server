"""Mutation resolvers for items.

Each mutation takes a single ``@strawberry.input`` argument and uses the
authenticated identity on ``info.context.request`` (populated by authentikate)
to set ownership. The ``ProvenanceField`` on the model records each write.
"""

import strawberry
from kante.types import Info

from demo import models, types


@strawberry.input
class CreateItemInput:
    """Fields needed to create an item."""

    name: str
    description: str | None = None


def create_item(info: Info, input: CreateItemInput) -> types.Item:
    """Create a new item owned by the requesting user and organization."""
    return models.Item.objects.create(
        name=input.name,
        description=input.description,
        creator=info.context.request.user,
        organization=info.context.request.organization,
    )


@strawberry.input
class UpdateItemInput:
    """Fields needed to update an item; unset fields are left unchanged."""

    id: strawberry.ID
    name: str | None = None
    description: str | None = None


def update_item(info: Info, input: UpdateItemInput) -> types.Item:
    """Update an existing item's name and/or description."""
    item = models.Item.objects.get(id=input.id)
    if input.name is not None:
        item.name = input.name
    if input.description is not None:
        item.description = input.description
    item.save()
    return item


@strawberry.input
class DeleteItemInput:
    """Identifies the item to delete."""

    id: strawberry.ID


def delete_item(info: Info, input: DeleteItemInput) -> strawberry.ID:
    """Delete an item and return its id."""
    item = models.Item.objects.get(id=input.id)
    item.delete()
    return input.id

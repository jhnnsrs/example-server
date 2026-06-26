"""Realtime channel used to drive the ``items`` GraphQL subscription.

``build_channel`` (from kante) gives us a typed pub/sub channel backed by the
configured channel layer (Redis in prod, in-memory in tests). Django signals
broadcast onto it (see ``signals.py``) and the subscription resolver listens.
"""

from kante.channel import build_channel
from pydantic import BaseModel, Field


class ItemSignal(BaseModel):
    """A change to an :class:`~demo.models.Item`.

    Exactly one of the fields is set, carrying the id of the affected item.
    """

    create: int | None = Field(default=None, description="The id of the item that was created.")
    update: int | None = Field(default=None, description="The id of the item that was updated.")
    delete: int | None = Field(default=None, description="The id of the item that was deleted.")


item_channel = build_channel(ItemSignal)

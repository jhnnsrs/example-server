"""Subscription resolver streaming item changes.

The resolver is an async generator: it listens on the ``item_channel`` (fed by
the model signals) and yields an :class:`ItemEvent` for every create/update/
delete. kante's router wires this up over WebSockets.
"""

from typing import AsyncGenerator

import strawberry
from kante.types import Info

from demo import models, types
from demo.channels import item_channel


@strawberry.type
class ItemEvent:
    """A single item change. Exactly one field is populated."""

    create: types.Item | None = None
    update: types.Item | None = None
    delete: strawberry.ID | None = None


async def items(self, info: Info) -> AsyncGenerator[ItemEvent, None]:
    """Subscribe to create/update/delete events for all items."""
    async for signal in item_channel.listen(info.context, ["items"]):
        if signal.create is not None:
            yield ItemEvent(create=await models.Item.objects.aget(id=signal.create))
        elif signal.update is not None:
            yield ItemEvent(update=await models.Item.objects.aget(id=signal.update))
        elif signal.delete is not None:
            yield ItemEvent(delete=strawberry.ID(str(signal.delete)))

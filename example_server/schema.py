"""The GraphQL schema for the example service.

A minimal schema over the ``demo`` app showing the three operation kinds —
query, mutation and subscription — plus the arkitekt extensions:

* ``AuthentikateExtension`` — authenticates the request from its bearer token
  and exposes the user/organization/client on ``info.context.request``.
* ``KoherentExtension`` — attributes every model write in a request to that
  identity (provenance).
* ``DjangoOptimizerExtension`` — batches/prefetches ORM access to avoid N+1s.
"""

import strawberry
import strawberry_django
from authentikate.strawberry.extension import AuthentikateExtension
from koherent.strawberry.extension import KoherentExtension
from strawberry_django.optimizer import DjangoOptimizerExtension

from demo import types
from demo.graphql import mutations, queries, subscriptions


@strawberry.type
class Query:
    """The root query type."""

    items: list[types.Item] = strawberry_django.field(description="List all items (paginated, filterable, orderable).")
    item: types.Item = strawberry_django.field(resolver=queries.item, description="Get a single item by id.")


@strawberry.type
class Mutation:
    """The root mutation type."""

    create_item = strawberry_django.mutation(resolver=mutations.create_item, description="Create a new item.")
    update_item = strawberry_django.mutation(resolver=mutations.update_item, description="Update an existing item.")
    delete_item = strawberry_django.mutation(resolver=mutations.delete_item, description="Delete an item by id.")


@strawberry.type
class Subscription:
    """The root subscription type."""

    items = strawberry.subscription(resolver=subscriptions.items, description="Stream create/update/delete events for items.")


# A federation schema is required because the authentikate types (User,
# Organization, …) are federated entities carrying ``@key`` directives.
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[
        DjangoOptimizerExtension,
        AuthentikateExtension,
        KoherentExtension,
    ],
)

"""Schema-surface tests for the demo GraphQL API.

These assert the rendered SDL exposes the demo operations and the ``Item`` type,
proving the query/mutation/subscription wiring is correct. They need no
database. To test actual *execution* against the DB, point the suite at a real
Postgres (SQLite deadlocks on writes from async resolvers — see settings_test).
"""

from example_server.schema import schema


def test_demo_operations_are_exposed():
    """The root Query/Mutation/Subscription expose the demo fields."""
    sdl = str(schema)

    # Queries
    assert "items(" in sdl or "items:" in sdl
    assert "item(" in sdl

    # Mutations
    assert "createItem(" in sdl
    assert "updateItem(" in sdl
    assert "deleteItem(" in sdl

    # Subscription
    assert "type Subscription" in sdl
    assert "items:" in sdl

    # The Item type and its fields
    assert "type Item" in sdl
    assert "createdAt" in sdl


def test_input_types_present():
    """The mutation input types are part of the schema."""
    sdl = str(schema)
    assert "input CreateItemInput" in sdl
    assert "input UpdateItemInput" in sdl
    assert "input DeleteItemInput" in sdl

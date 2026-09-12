"""Dummy models for the example service.

These exist only to demonstrate how a regular Django model is exposed over
GraphQL using the arkitekt stack. ``Item`` is owned by a :class:`User` within
an :class:`Organization` (both provided by ``authentikate``) and carries a
``ProvenanceField`` (provided by ``koherent``) so every change is recorded and
attributed to the client/user that made it.
"""

from django.db import models
from authentikate.models import Organization, User
from koherent.fields import ProvenanceField


class Item(models.Model):
    """A simple, owned item — the one and only demo model.

    Replace this with your real domain models; the surrounding wiring (types,
    queries, mutations, subscriptions) shows the pattern to follow.
    """

    name = models.CharField(max_length=1000, help_text="The human-readable name of the item.")
    description = models.TextField(null=True, blank=True, help_text="An optional longer description.")
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
        help_text="The user that created this item.",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="The organization this item belongs to.",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this item was created.")

    # Records every change to this model as a provenance-tracked history row,
    # attributed to the client/user (and Rekuest task, when present) it happened
    # under. Powered by koherent + simple_history.
    provenance = ProvenanceField()

    def __str__(self) -> str:
        """Return the item's name."""
        return self.name


from .signals import *  # noqa: E402, F401, F403

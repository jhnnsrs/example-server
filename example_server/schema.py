from kante.types import Info
from typing import AsyncGenerator, List
import strawberry

from core.datalayer import DatalayerExtension
from strawberry import ID as StrawberryID
from typing import Any, Type
from core import types, models
from core import mutations
from core import queries
from core import subscriptions
import strawberry_django
from koherent.strawberry.extension import KoherentExtension
from core.render.objects import types as render_types
from core.duck import DuckExtension
from typing import Annotated
from core.base_models.type.graphql.model import SynapticConnection, Exp2Synapse
from core.base_models.type.graphql.model import ModelConfigModel
from core.base_models.type.graphql.topology import Section
from authentikate.strawberry.extension import AuthentikateExtension
from strawberry_django.optimizer import DjangoOptimizerExtension
import kante

ID = Annotated[StrawberryID, strawberry.argument(description="The unique identifier of an object")]


@strawberry.type
class Query:
    """The root query type"""
    
    test: str = kante.field(resolver=queries.test, description="A simple test query that returns a string")
    
    
@strawberry.type
class Mutation:
    """ The root mutation type"""
    
    create_test_model: types.TestModelType = kante.field(
        resolver=mutations.create_test_model,
        description="Create a test model instance",
    )
    
    
@strawberry.type
class Subscription:
    """The root subscription type"""

    rois = strawberry.subscription(resolver=subscriptions.rois, description="Subscribe to real-time ROI updates")
    traces = strawberry.subscription(resolver=subscriptions.traces, description="Subscribe to real-time image updates")
    files = strawberry.subscription(resolver=subscriptions.files, description="Subscribe to real-time file updates")


schema = strawberry.Schema(
    query=Query,
    subscription=Subscription,
    mutation=Mutation,
    extensions=[
        KoherentExtension,
        AuthentikateExtension,
        DjangoOptimizerExtension,
        DatalayerExtension,
        DuckExtension,
    ],
    types=[SynapticConnection, Exp2Synapse],
)

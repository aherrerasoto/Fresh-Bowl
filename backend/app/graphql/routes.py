
from sqlalchemy.orm import Session
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.graphql.schema import schema


async def get_graphql_context(
    db: Session = Depends(get_db)
):
    return {
        "db": db
    }


router = GraphQLRouter(
    schema,
    path="/graphql",
    context_getter=get_graphql_context,
    dependencies=[
        Depends(require_roles("administrador", "tecnico"))
    ]
)

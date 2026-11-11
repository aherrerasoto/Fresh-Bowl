
import strawberry

from strawberry.types import Info
from sqlalchemy.orm import Session

from app.graphql import resolvers


@strawberry.type
class IngredientType:
    id: int
    name: str
    category: str
    price: int
    stock: int


@strawberry.type
class OrderType:
    id: int
    customer_name: str
    status: str
    delivery_method: str
    total: int


@strawberry.type
class DashboardType:
    available_ingredients: int
    total_orders: int
    total_sales: int


@strawberry.type
class Query:

    @strawberry.field
    def ingredients(self, info: Info) -> list[IngredientType]:
        db: Session = info.context["db"]

        data = resolvers.get_ingredients_data(db)

        return [
            IngredientType(**ingredient)
            for ingredient in data
        ]

    @strawberry.field
    def orders(self, info: Info) -> list[OrderType]:
        db: Session = info.context["db"]

        data = resolvers.get_orders_data(db)

        return [
            OrderType(**order)
            for order in data
        ]

    @strawberry.field
    def dashboard(self, info: Info) -> DashboardType:
        db: Session = info.context["db"]

        data = resolvers.get_dashboard_data(db)

        return DashboardType(**data)


schema = strawberry.Schema(query=Query)

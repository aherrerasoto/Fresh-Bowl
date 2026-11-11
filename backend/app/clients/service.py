from sqlalchemy.orm import Session

from app.clients.models import Client
from app.clients.schemas import ClientCreate, ClientUpdate


def get_clients(db: Session):
    return (
        db.query(Client)
        .filter(Client.active == True)
        .order_by(Client.id)
        .all()
    )


def get_client(db: Session, client_id: int):
    return (
        db.query(Client)
        .filter(Client.id == client_id, Client.active == True)
        .first()
    )


def create_client(db: Session, data: ClientCreate):
    existing = (
        db.query(Client)
        .filter(Client.email == data.email)
        .first()
    )

    if existing:
        if existing.active:
            return "duplicate"

        # Si el cliente estaba desactivado, se reactiva.
        existing.full_name = data.full_name
        existing.email = data.email
        existing.phone = data.phone
        existing.active = True
        db.commit()
        db.refresh(existing)
        return existing

    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)

    return client


def update_client(db: Session, client_id: int, data: ClientUpdate):
    client = get_client(db, client_id)

    if not client:
        return None

    changes = data.model_dump(exclude_unset=True)

    if "email" in changes and changes["email"]:
        duplicate = (
            db.query(Client)
            .filter(
                Client.email == changes["email"],
                Client.id != client_id
            )
            .first()
        )

        if duplicate:
            return "duplicate"

    for field, value in changes.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)

    return client


def deactivate_client(db: Session, client_id: int):
    client = get_client(db, client_id)

    if not client:
        return False

    client.active = False
    db.commit()

    return True
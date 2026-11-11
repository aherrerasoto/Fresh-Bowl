import getpass

from app.core.database import Base, engine, SessionLocal
from app.auth.models import User
from app.core.security import hash_password


def create_admin():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        name = input("Nombre del administrador: ").strip()
        email = input("Correo del administrador: ").strip().lower()
        password = getpass.getpass("Contraseña: ")

        if len(name) < 2:
            print("El nombre debe tener al menos 2 caracteres.")
            return

        if len(password) < 8:
            print("La contraseña debe tener al menos 8 caracteres.")
            return

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print("Ya existe un usuario con ese correo.")
            return

        admin = User(
            full_name=name,
            email=email,
            password_hash=hash_password(password),
            role="administrador",
            active=True
        )

        db.add(admin)
        db.commit()

        print("Administrador creado correctamente.")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
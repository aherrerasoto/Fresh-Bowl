from app.core.vault import get_vault_secret


class Settings:
    APP_NAME = "Fresh Bowl API"
    APP_VERSION = "1.0.0"

    DATABASE_URL = get_vault_secret(
        "DATABASE_URL",
        "sqlite:///./freshbowl.db"
    )

    SECRET_KEY = get_vault_secret(
        "JWT_SECRET_KEY",
        "clave-temporal-solo-para-desarrollo"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    COOKIE_SECURE = (
        get_vault_secret("COOKIE_SECURE", "false").lower() == "true"
    )


settings = Settings()
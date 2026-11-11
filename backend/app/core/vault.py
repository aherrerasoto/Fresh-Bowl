import os
import hvac


def get_vault_secret(secret_name: str, default=None):
    """
    Obtiene un secreto desde HashiCorp Vault.
    Si Vault no está disponible, utiliza la variable de entorno
    correspondiente para permitir el desarrollo local.
    """

    vault_address = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")

    if vault_address and vault_token:
        try:
            client = hvac.Client(
                url=vault_address,
                token=vault_token
            )

            if client.is_authenticated():
                response = client.secrets.kv.v2.read_secret_version(
                    path="freshbowl",
                    mount_point="secret"
                )

                secrets = response["data"]["data"]

                if secret_name in secrets:
                    return secrets[secret_name]

        except Exception:
            pass

    return os.getenv(secret_name, default)
# Módulo 10 – Pruebas, reproducibilidad y despliegue
## Proyecto Fresh Bowl

## 1. Objetivo

Documentar cómo ejecutar, probar y mantener el backend de Fresh Bowl, incluyendo sus dependencias, persistencia, configuración y mecanismos de despliegue.

El objetivo es que otra persona pueda preparar el entorno, iniciar la aplicación y comprobar su funcionamiento siguiendo los pasos descritos en este documento.

## 2. Requisitos del entorno

Para ejecutar el backend se consideran los siguientes componentes:

| Componente | Uso |
|---|---|
| Python 3.13 | Ejecución de la aplicación |
| FastAPI | Desarrollo de la API REST |
| SQLAlchemy | Acceso y persistencia de datos |
| SQLite | Base de datos del entorno de desarrollo |
| Pytest | Ejecución de pruebas automatizadas |
| HTTPX | Pruebas de endpoints |
| Strawberry GraphQL | Consultas agregadas |
| PyJWT | Gestión de tokens JWT |
| pwdlib y Argon2 | Protección de contraseñas |
| HashiCorp Vault | Gestión de secretos, con integración pendiente de validación |
| Docker | Preparación del entorno de despliegue |

## 3. Estructura del proyecto

El backend se organiza en módulos independientes según las responsabilidades del sistema:

```text
backend/
├── app/
│   ├── core/
│   ├── gateway/
│   ├── auth/
│   ├── graphql/
│   ├── inventory/
│   ├── orders/
│   ├── clients/
│   ├── payments/
│   └── main.py
├── tests/
├── docs/
├── scripts/
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

La carpeta `app` contiene la aplicación y sus módulos funcionales. La carpeta `tests` contiene las pruebas automatizadas y `docs` reúne la documentación técnica.

## 4. Instalación y ejecución local

### 4.1 Crear el entorno virtual

Desde la carpeta `backend`, ejecutar:

```powershell
python -m venv ..\.venv
```

### 4.2 Activar el entorno virtual

```powershell
..\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, se puede ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego volver a activar el entorno virtual.

### 4.3 Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4.4 Iniciar la aplicación

Desde la carpeta `backend` y con el entorno virtual activado:

```powershell
python -m uvicorn app.main:app --reload
```

La API queda disponible localmente en:

`http://127.0.0.1:8000`

La documentación interactiva de FastAPI se encuentra en:

`http://127.0.0.1:8000/docs`

El endpoint GraphQL se encuentra en:

`http://127.0.0.1:8000/api/v1/graphql`

## 5. Persistencia de datos

El proyecto utiliza SQLAlchemy para interactuar con la base de datos.

En el entorno de desarrollo se utiliza SQLite, cuya dirección se configura mediante `DATABASE_URL`.

La aplicación mantiene modelos para:

- Usuarios.
- Ingredientes.
- Clientes.
- Pedidos.
- Pagos.

La base de datos permite conservar los registros entre ejecuciones de la aplicación.

La configuración de Docker contempla un volumen denominado `freshbowl-data`, destinado a conservar los datos fuera del ciclo de vida del contenedor.

**Estado:** la persistencia local está implementada. La persistencia mediante el volumen de Docker queda pendiente de una ejecución y verificación satisfactoria del despliegue.

## 6. Configuración de secretos

El archivo `.env.example` contiene las variables de entorno necesarias como referencia:

```text
DATABASE_URL=sqlite:///./freshbowl.db
JWT_SECRET_KEY=CAMBIAR_POR_UNA_CLAVE_SEGURA
COOKIE_SECURE=false
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=
```

El archivo `.env.example` no contiene credenciales reales. Cada entorno debe utilizar su propia configuración.

La aplicación dispone de un módulo de integración con HashiCorp Vault que intenta obtener secretos desde el almacenamiento KV v2.

Si Vault no está disponible o no se configura, el módulo utiliza las variables de entorno o los valores predeterminados definidos para desarrollo.

La integración está preparada en el código, pero su funcionamiento mediante Docker y Vault todavía debe verificarse.

El token de desarrollo `root` configurado en el entorno de Vault no debe utilizarse en producción.

## 7. Pruebas automatizadas

El proyecto utiliza Pytest para verificar el comportamiento del backend.

Las pruebas se encuentran organizadas por módulo:

| Archivo | Funcionalidad evaluada |
|---|---|
| `test_auth.py` | Registro, inicio de sesión y autenticación |
| `test_inventory.py` | Operaciones de inventario |
| `test_clients.py` | Operaciones de clientes |
| `test_orders.py` | Creación y gestión de pedidos |
| `test_payments.py` | Procesamiento simulado de pagos |
| `test_payment_security.py` | Restricciones de acceso a pagos |
| `test_gateway.py` | Políticas de acceso del Gateway |
| `test_graphql.py` | Consultas y autorización GraphQL |

### 7.1 Ejecución de las pruebas

Desde la carpeta `backend`, ejecutar:

```powershell
python -m pytest -v
```

### 7.2 Resultado registrado

En la última ejecución global informada se obtuvo:

| Resultado | Cantidad |
|---|---:|
| Pruebas aprobadas | 56 |
| Pruebas fallidas | 0 |

Este resultado corresponde a la ejecución registrada y no garantiza que futuras modificaciones mantengan el mismo resultado. Por eso se debe repetir la ejecución antes de entregar la versión final.

## 8. Creación del administrador

El proyecto incluye un script para crear un usuario con rol de administrador:

`backend/scripts/create_admin.py`

Para ejecutarlo desde la carpeta `backend`:

```powershell
python scripts/create_admin.py
```

Este procedimiento debe realizarse cuando se prepara una base de datos nueva y todavía no existe un administrador.

Las credenciales utilizadas deben mantenerse privadas y no deben incluirse en el repositorio ni en capturas públicas.

## 9. Preparación del despliegue mediante Docker

El proyecto incorpora:

- `Dockerfile`: define la imagen del backend.
- `docker-compose.yml`: describe los servicios Vault, inicialización de secretos y backend.
- `.dockerignore`: excluye archivos innecesarios del contexto de construcción.

La configuración de Docker Compose fue validada mediante:

```powershell
docker compose config
```

La validación de configuración fue satisfactoria.

### 9.1 Estado de construcción de la imagen

Durante la construcción de la imagen del backend se presentó un problema con BuildKit al leer el archivo Dockerfile desde la ubicación original del proyecto.

Aunque el archivo puede leerse desde PowerShell, la construcción no se completó correctamente.

Por lo tanto, no se considera verificado el despliegue completo mediante Docker.

Se propone repetir la construcción desde una copia de trabajo ubicada fuera de OneDrive y comprobar posteriormente el inicio del backend y Vault.

### 9.2 Estado de Vault

El archivo `docker-compose.yml` contempla el inicio de Vault y la carga de secretos de desarrollo.

Sin embargo, mientras la construcción y ejecución completa del entorno no se hayan verificado, no se puede afirmar que la integración Docker-Vault esté funcionando correctamente.

## 10. Limitaciones conocidas

Se identifican las siguientes limitaciones:

1. El despliegue completo mediante Docker todavía no está verificado.
2. La integración con HashiCorp Vault necesita una prueba de ejecución satisfactoria.
3. La base de datos de desarrollo utiliza SQLite.
4. No existe una integración real con un proveedor de pagos; el procesamiento es simulado.
5. El cliente no dispone actualmente de una consulta para acceder a sus propios pedidos.
6. Deben fortalecerse los controles de propiedad de pedidos y pagos.
7. Se deben incorporar límites de profundidad y complejidad para GraphQL.
8. Las pruebas de carga todavía no cuentan con mediciones registradas.
9. Deben completarse medidas adicionales de seguridad para producción, como HTTPS, protección CSRF y configuración restrictiva de CORS.

## 11. Reproducibilidad de la entrega

Para facilitar la revisión del proyecto, se deben conservar:

- Código fuente del backend.
- Archivo `requirements.txt`.
- Archivo `.env.example`.
- Archivos Docker.
- Pruebas automatizadas.
- Documentación técnica.
- Resultados de ejecución de pruebas.
- Evidencias de ejecución de los endpoints.

La entrega debe permitir identificar qué funcionalidades están implementadas, cuáles fueron verificadas y cuáles permanecen pendientes.

## 12. Conclusión

El backend de Fresh Bowl cuenta con una estructura modular, persistencia mediante SQLAlchemy, autenticación, autorización por roles, operaciones de inventario, clientes, pedidos y pagos simulados.

También dispone de un API Gateway implementado como middleware, un endpoint GraphQL de agregación y pruebas automatizadas.

La última ejecución global registrada obtuvo 56 pruebas aprobadas y ninguna fallida.

La configuración de Docker y Vault se encuentra preparada, pero todavía requiere una ejecución satisfactoria para considerarse verificada. Se mantienen documentadas las limitaciones y mejoras necesarias antes de un despliegue de producción.
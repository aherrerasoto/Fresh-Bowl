# Fresh Bowl – Backend

## 1. Descripción del proyecto

Fresh Bowl es una aplicación para un local de ensaladas personalizadas. El backend proporciona los servicios necesarios para gestionar ingredientes, clientes, pedidos, pagos y autenticación.

La API fue desarrollada con **Python y FastAPI**, utilizando SQLAlchemy para la persistencia de datos y SQLite como base de datos de desarrollo.

## 2. Tecnologías utilizadas

- Python 3.13
- FastAPI: desarrollo de servicios REST.
- SQLAlchemy: gestión de la base de datos.
- SQLite: persistencia de datos durante el desarrollo.
- JWT: autenticación mediante tokens.
- Cookies HttpOnly: almacenamiento del token de acceso.
- pwdlib y Argon2: protección de contraseñas.
- Strawberry GraphQL: consultas y agregación de información.
- HashiCorp Vault: integración preparada para la gestión de secretos.
- Docker Compose: configuración de despliegue preparada.
- Pytest: ejecución de pruebas automatizadas.

## 3. Estructura del proyecto

```text
backend/
│
├── app/
│   ├── auth/
│   ├── clients/
│   ├── core/
│   ├── gateway/
│   ├── graphql/
│   ├── inventory/
│   ├── orders/
│   ├── payments/
│   └── main.py
│
├── docs/
│   ├── ADR-001-decisiones-arquitectura.md
│   ├── API_CONTRACTS.md
│   └── CLASIFICACION_DATOS.md
│
├── scripts/
│   └── create_admin.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 4. Instalación y configuración

### Requisitos previos

- Python 3.13 o superior.
- Visual Studio Code (recomendado).

### Crear el entorno virtual

Desde la carpeta `backend`, ejecutar:

```powershell
python -m venv .venv
```

Activar el entorno virtual:

```powershell
..\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### Instalar dependencias

```powershell
pip install -r requirements.txt
```

### Configuración de variables de entorno

El archivo `.env.example` contiene las variables de configuración de referencia.

Se debe crear un archivo `.env` a partir de este ejemplo y configurar los valores correspondientes para el entorno de ejecución.

## 5. Ejecución del backend

Desde la carpeta `backend`, con el entorno virtual activado:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible en:

`http://127.0.0.1:8000`

### Documentación interactiva

FastAPI genera automáticamente la documentación de los endpoints.

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

## 6. Servicios implementados

| Módulo | Funcionalidad |
|---|---|
| Auth | Registro, inicio y cierre de sesión, consulta del usuario autenticado. |
| Inventory | Consulta y administración de ingredientes y existencias. |
| Clients | Administración de clientes. |
| Orders | Creación y gestión de pedidos. |
| Payments | Registro y consulta de pagos simulados. |
| Gateway | Aplicación de políticas de acceso a los servicios. |
| GraphQL | Consulta de ingredientes, pedidos y datos consolidados para el panel. |

## 7. Roles y permisos

El sistema contempla tres roles:

- **Cliente:** puede registrarse, iniciar sesión y realizar pedidos.
- **Técnico:** puede consultar y gestionar operaciones autorizadas, como pedidos y pagos.
- **Administrador:** tiene permisos de administración de los módulos protegidos.

Las rutas protegidas verifican la autenticación y los permisos correspondientes.

## 8. GraphQL

El backend incorpora un endpoint GraphQL:

`POST /api/v1/graphql`

Permite consultar información de ingredientes, pedidos y un panel consolidado que reúne indicadores de inventario y pedidos.

El acceso está restringido a los roles administrador y técnico.

## 9. Ejecución de pruebas

Para ejecutar todas las pruebas automatizadas:

```powershell
python -m pytest -v
```

### Resultado de las pruebas

En la última ejecución se obtuvieron los siguientes resultados:

- Total de pruebas: 56.
- Pruebas aprobadas: 56.
- Pruebas fallidas: 0.
- Tiempo de ejecución: 5,66 segundos.

Las pruebas cubren autenticación, permisos, inventario, clientes, pedidos, pagos, API Gateway y GraphQL.

## 10. Persistencia y seguridad

La persistencia de datos se realiza mediante SQLAlchemy y SQLite en el entorno de desarrollo.

Las contraseñas se almacenan mediante hash y no como texto plano. La autenticación utiliza JWT mediante cookies HttpOnly y existen controles de acceso según los roles definidos.

Los datos sensibles y las credenciales se consideran información protegida. Se preparó una integración con HashiCorp Vault para gestionar secretos.

## 11. Consideraciones y pendientes

- El proveedor de pagos es simulado y no procesa transacciones bancarias reales.
- SQLite se utiliza como base de datos de desarrollo.
- La configuración de Docker y Docker Compose está preparada, pero su construcción y ejecución deben verificarse.
- La integración con HashiCorp Vault está preparada, pero queda pendiente validar su funcionamiento en el despliegue.
- La integración del frontend con el backend corresponde a la etapa posterior del proyecto.

## 12. Estado del desarrollo

El backend cuenta con los módulos principales implementados y una suite de 56 pruebas automatizadas aprobadas.

La documentación de arquitectura, contratos de API y clasificación de datos se encuentra en la carpeta `docs`.
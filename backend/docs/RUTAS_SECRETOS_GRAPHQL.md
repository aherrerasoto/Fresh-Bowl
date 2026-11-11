# Módulo 6 – Rutas, secretos e integración
## Proyecto Fresh Bowl

## 1. Objetivo

Documentar las rutas HTTP disponibles, sus permisos, los sistemas responsables, las identidades utilizadas y las referencias simbólicas de los secretos de configuración.

También se describen las operaciones GraphQL implementadas y la decisión sobre el uso de gRPC.

## 2. Matriz de rutas HTTP

La aplicación utiliza el prefijo `/api/v1` para sus servicios.

| ID | Gateway | Método | Ruta externa | Acceso | Sistema destino | Control aplicado |
|---|---|---|---|---|---|---|
| R01 | FastAPI Middleware | GET | /api/v1/ingredients/ | Público | Inventory | Consulta de ingredientes |
| R02 | FastAPI Middleware | GET | /api/v1/ingredients/{id} | Público | Inventory | Consulta individual |
| R03 | FastAPI Middleware | POST | /api/v1/ingredients/ | Administrador | Inventory | Autorización por rol |
| R04 | FastAPI Middleware | PATCH | /api/v1/ingredients/{id} | Administrador | Inventory | Autorización por rol |
| R05 | FastAPI Middleware | DELETE | /api/v1/ingredients/{id} | Administrador | Inventory | Autorización por rol |
| R06 | FastAPI Middleware | GET | /api/v1/clients/ | Administrador | Clients | Autorización por rol |
| R07 | FastAPI Middleware | POST | /api/v1/clients/ | Administrador | Clients | Autorización por rol |
| R08 | FastAPI Middleware | PATCH | /api/v1/clients/{id} | Administrador | Clients | Autorización por rol |
| R09 | FastAPI Middleware | DELETE | /api/v1/clients/{id} | Administrador | Clients | Autorización por rol |
| R10 | FastAPI Middleware | POST | /api/v1/orders/ | Público | Orders | Validación de datos y reglas de negocio |
| R11 | FastAPI Middleware | GET | /api/v1/orders/ | Administrador y técnico | Orders | Autenticación y autorización |
| R12 | FastAPI Middleware | GET | /api/v1/orders/{id} | Administrador y técnico | Orders | Autenticación y autorización |
| R13 | FastAPI Middleware | PATCH | /api/v1/orders/{id}/status | Administrador y técnico | Orders | Autenticación y autorización |
| R14 | FastAPI Middleware | POST | /api/v1/payments/ | Público | Payments | Validación del pedido y pago simulado |
| R15 | FastAPI Middleware | GET | /api/v1/payments/ | Administrador y técnico | Payments | Autenticación y autorización |
| R16 | FastAPI Middleware | GET | /api/v1/payments/{id} | Administrador y técnico | Payments | Autenticación y autorización |
| R17 | FastAPI Middleware | POST | /api/v1/auth/register | Público | Auth | Registro con rol cliente |
| R18 | FastAPI Middleware | POST | /api/v1/auth/login | Público | Auth | Verificación de credenciales |
| R19 | FastAPI Middleware | POST | /api/v1/auth/logout | Público | Auth | Eliminación de cookie |
| R20 | FastAPI Middleware | GET | /api/v1/auth/me | Usuario autenticado | Auth | Validación de identidad |
| R21 | Router GraphQL | POST | /api/v1/graphql | Administrador y técnico | GraphQL | Autorización mediante dependencia del router |
| R22 | FastAPI | GET | /gateway/status | Público | Gateway | Estado del componente |
| R23 | FastAPI | GET | /gateway/policies | Público | Gateway | Consulta de políticas configuradas |

### 2.1 Ruta externa y destino interno

Actualmente las rutas externas llegan directamente a los endpoints correspondientes dentro de la misma aplicación FastAPI.

No existe una transformación hacia URLs de microservicios independientes. El Gateway aplica las políticas mediante middleware y los routers reciben las solicitudes dentro del mismo proceso.

Por lo tanto, la ruta externa y el destino lógico coinciden con el endpoint definido en cada módulo.

## 3. Identidades y credenciales

Se distinguen dos categorías:

### 3.1 Credenciales del usuario

La autenticación del usuario se realiza mediante:

- Correo electrónico.
- Contraseña almacenada mediante hash.
- Token JWT generado después de una autenticación válida.
- Cookie HttpOnly denominada `access_token`.

El token permite identificar al usuario y recuperar su rol para aplicar las políticas de autorización.

### 3.2 Credenciales entre sistemas

Las credenciales de infraestructura permiten que los componentes del backend accedan a recursos necesarios para su funcionamiento.

Estas credenciales no deben entregarse al navegador ni compartirse con los usuarios finales.

## 4. Inventario simbólico de secretos

| Referencia | Tipo | Emisor o responsable | Consumidor | Finalidad | Ubicación prevista | Alcance |
|---|---|---|---|---|---|---|
| JWT_SECRET_KEY | Clave criptográfica | Administrador del sistema | Auth y seguridad | Firmar y validar tokens JWT | Vault o variable de entorno protegida | Autenticación del backend |
| DATABASE_URL | Cadena de conexión | Administrador del sistema | SQLAlchemy | Conexión a la base de datos | Vault o variable de entorno protegida | Acceso a la base de datos |
| VAULT_TOKEN | Token de autenticación | Administrador de Vault | Aplicación backend | Autenticarse ante Vault | Variable protegida del entorno | Lectura de secretos autorizados |
| VAULT_ADDR | Configuración de servicio | Administrador de infraestructura | Aplicación backend | Identificar la dirección de Vault | Configuración del entorno | Conexión con Vault |
| COOKIE_SECURE | Configuración de seguridad | Administrador del sistema | Auth | Determinar el atributo Secure de la cookie | Configuración del entorno | Cookies de autenticación |

**Importante:** `VAULT_ADDR` y `COOKIE_SECURE` son parámetros de configuración, no secretos criptográficos. Se incluyen para documentar la configuración de integración.

## 5. Gestión de secretos

La aplicación incorpora un componente de acceso a HashiCorp Vault mediante la biblioteca `hvac`.

La integración está preparada para consultar secretos almacenados en la ruta lógica:

`secret/freshbowl`

Se utiliza el motor KV versión 2 de Vault.

### Responsabilidades

- **Administrador:** responsable de crear, actualizar y revocar las credenciales.
- **Aplicación backend:** consumidora de los secretos necesarios para operar.
- **Vault:** gestor previsto para centralizar el almacenamiento de secretos.

### Almacenamiento y permisos

Los secretos deben mantenerse fuera del código fuente y del navegador.

La aplicación debe disponer únicamente de permisos de lectura sobre los secretos que necesita consumir.

El token administrativo de Vault no debe utilizarse como credencial permanente de producción.

### Rotación y revocación

Se contempla el siguiente procedimiento:

1. Generar una nueva credencial.
2. Actualizar el secreto en el gestor correspondiente.
3. Verificar que la aplicación puede utilizar la nueva credencial.
4. Revocar la credencial anterior.
5. Comprobar que el sistema continúa funcionando.

La rotación y revocación automática no se encuentran implementadas ni verificadas actualmente.

## 6. Operaciones GraphQL

El endpoint GraphQL está disponible en:

`POST /api/v1/graphql`

El schema implementa tres operaciones de consulta.

| Operación | Tipo | Campos principales | Resolver | Subsistemas consultados |
|---|---|---|---|---|
| ingredients | Query | id, name, category, price, stock | get_ingredients_data | Inventory |
| orders | Query | id, customer_name, status, delivery_method, total | get_orders_data | Orders |
| dashboard | Query | available_ingredients, total_orders, total_sales | get_dashboard_data | Inventory y Orders |

### 6.1 Query ingredients

Permite consultar ingredientes activos y disponibles.

Campos devueltos:

- id
- name
- category
- price
- stock

El resolver consulta el módulo Inventory.

### 6.2 Query orders

Permite consultar pedidos registrados.

Campos devueltos:

- id
- customer_name
- status
- delivery_method
- total

El resolver consulta el módulo Orders.

### 6.3 Query dashboard

Permite obtener información consolidada para un panel administrativo.

Indicadores:

- `available_ingredients`: cantidad de ingredientes activos y disponibles.
- `total_orders`: cantidad total de pedidos registrados.
- `total_sales`: suma de los pedidos que no se encuentran cancelados.

Esta operación combina consultas de Inventory y Orders.

### 6.4 Autorización GraphQL

El router GraphQL utiliza una dependencia de autorización que permite el acceso a los roles administrador y técnico.

Actualmente las tres consultas comparten esta política de acceso.

No se han implementado permisos diferenciados por campo ni operaciones Mutation.

## 7. Decisión sobre gRPC

En la versión actual de Fresh Bowl no se implementa gRPC.

La decisión se fundamenta en las características del caso:

- El sistema administra un catálogo de ingredientes.
- Registra pedidos y pagos simulados.
- No necesita comunicación interna de alta frecuencia.
- No contempla procesamiento intensivo en tiempo real.
- Los módulos se ejecutan dentro de una misma aplicación FastAPI.
- La comunicación interna mediante llamadas Python y SQLAlchemy resulta suficiente para el alcance actual.

Por estas razones, agregar gRPC implicaría incorporar contratos `.proto`, clientes, servidores, autenticación entre servicios y mecanismos adicionales de comunicación sin una necesidad funcional demostrada.

La ausencia de gRPC corresponde a una decisión de aplicabilidad y no a una funcionalidad implementada.

## 8. Limitaciones y medidas pendientes

- El Gateway no realiza enrutamiento entre servicios desplegados independientemente.
- La integración con Vault debe verificarse en ejecución.
- No se ha implementado rotación automática de credenciales.
- No existen identidades de servicio independientes para cada módulo.
- Las consultas GraphQL utilizan una política común de autorización por rol.
- Deben reforzarse las validaciones de propiedad de recursos antes de producción.
- No se ha realizado una medición de carga que permita establecer límites de rendimiento.

## 9. Evidencia

La implementación dispone de pruebas automatizadas para autenticación, permisos, servicios y consultas GraphQL.

La ejecución global más reciente registró:

- 56 pruebas aprobadas.
- 0 pruebas fallidas.

La evidencia de ejecución debe conservarse mediante capturas de la terminal y relacionarse con los archivos de prueba correspondientes.

## 10. Conclusión

Fresh Bowl dispone de rutas HTTP organizadas por módulos, autenticación mediante JWT y políticas de autorización según los roles definidos.

Los secretos de infraestructura cuentan con referencias simbólicas y una integración preparada con HashiCorp Vault. GraphQL permite consultar información de inventario y pedidos, incluyendo una agregación funcional de ambos subsistemas.

La utilización de gRPC no se considera necesaria para la arquitectura modular actual, decisión que deberá mantenerse respaldada por las características y necesidades del caso.
# Catálogo de servicios y contratos HTTP – Fresh Bowl

**Proyecto:** Fresh Bowl  
**Versión:** 1.0  
**Arquitectura:** Backend modular con FastAPI  
**Protocolo:** HTTP  
**Formato de intercambio:** JSON

## 1. Objetivo

Documentar los servicios HTTP disponibles en Fresh Bowl, identificando sus rutas, métodos, responsabilidades y políticas de acceso.

La API utiliza el prefijo `/api/v1` para organizar sus endpoints y mantener una versión identificable de los servicios.

## 2. Catálogo de servicios

### 2.1 Servicio de Inventario

**Responsabilidad:** administrar los ingredientes disponibles para personalizar las ensaladas.

| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/v1/ingredients/` | Público |
| GET | `/api/v1/ingredients/{ingredient_id}` | Público |
| POST | `/api/v1/ingredients/` | Administrador |
| PATCH | `/api/v1/ingredients/{ingredient_id}` | Administrador |
| DELETE | `/api/v1/ingredients/{ingredient_id}` | Administrador |

### 2.2 Servicio de Clientes

**Responsabilidad:** administrar la información de los clientes registrados.

| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/v1/clients/` | Administrador |
| GET | `/api/v1/clients/{client_id}` | Administrador |
| POST | `/api/v1/clients/` | Administrador |
| PATCH | `/api/v1/clients/{client_id}` | Administrador |
| DELETE | `/api/v1/clients/{client_id}` | Administrador |

### 2.3 Servicio de Pedidos

**Responsabilidad:** registrar pedidos, consultar su información y administrar sus estados.

| Método | Ruta | Acceso |
|---|---|---|
| POST | `/api/v1/orders/` | Público |
| GET | `/api/v1/orders/` | Administrador y técnico |
| GET | `/api/v1/orders/{order_id}` | Administrador y técnico |
| PATCH | `/api/v1/orders/{order_id}/status` | Administrador y técnico |

### 2.4 Servicio de Pagos

**Responsabilidad:** procesar pagos mediante un proveedor simulado y registrar sus resultados.

| Método | Ruta | Acceso |
|---|---|---|
| POST | `/api/v1/payments/` | Público |
| GET | `/api/v1/payments/` | Administrador y técnico |
| GET | `/api/v1/payments/{payment_id}` | Administrador y técnico |

### 2.5 Servicio de Autenticación

**Responsabilidad:** gestionar el registro de usuarios, inicio y cierre de sesión y consulta del perfil.

| Método | Ruta | Acceso |
|---|---|---|
| POST | `/api/v1/auth/register` | Público |
| POST | `/api/v1/auth/login` | Público |
| POST | `/api/v1/auth/logout` | Público |
| GET | `/api/v1/auth/me` | Usuario autenticado |

### 2.6 API Gateway

**Responsabilidad:** centralizar las políticas de acceso y proporcionar información sobre el estado del Gateway.

| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/v1/gateway/status` | Informativo |
| GET | `/api/v1/gateway/policies` | Informativo |

### 2.7 Servicio GraphQL

**Responsabilidad:** permitir consultas agregadas sobre diferentes módulos del sistema.

| Operación | Endpoint | Acceso |
|---|---|---|
| POST | `/api/v1/graphql` | Administrador y técnico |

Consultas implementadas:

- `ingredients`: obtiene ingredientes disponibles.
- `orders`: obtiene pedidos registrados.
- `dashboard`: combina información de Inventario y Pedidos.

## 3. Formato de intercambio

Los servicios HTTP reciben y entregan información utilizando JSON.

Las solicitudes que contienen información de entrada son validadas mediante esquemas Pydantic.

Las respuestas utilizan códigos HTTP para representar el resultado de las operaciones.

## 4. Códigos de respuesta

| Código | Significado | Situación |
|---|---|---|
| 200 | OK | Consulta o modificación correcta |
| 201 | Created | Registro creado correctamente |
| 401 | Unauthorized | Sesión inexistente o inválida |
| 403 | Forbidden | Usuario sin permisos suficientes |
| 404 | Not Found | Recurso inexistente |
| 409 | Conflict | Conflicto con un registro existente |
| 422 | Unprocessable Content | Datos de entrada inválidos |

## 5. Políticas de seguridad

Los servicios aplican las siguientes medidas:

- Autenticación mediante tokens.
- Cookies HttpOnly para las sesiones.
- Autorización mediante roles.
- Validación de datos de entrada.
- Protección de operaciones administrativas.
- Separación entre operaciones públicas y privadas.

## 6. Integración entre servicios

Los módulos comparten la capa de persistencia y se encuentran organizados dentro de una aplicación FastAPI.

GraphQL permite consultar información de Inventario y Pedidos mediante una sola operación.

El procesamiento de pagos utiliza un adaptador simulado.

## 7. Consideraciones

El catálogo representa las rutas implementadas durante el desarrollo. Los contratos detallados de entrada y salida se encuentran definidos en los esquemas Pydantic de cada módulo.

La integración con el frontend y la validación completa del despliegue Docker se mantienen como actividades separadas o pendientes según el alcance de las evaluaciones.

## 8. Conclusión

El catálogo permite identificar los servicios disponibles en Fresh Bowl, sus responsabilidades y sus mecanismos de acceso. También facilita el mantenimiento del backend y la futura integración con otros componentes.
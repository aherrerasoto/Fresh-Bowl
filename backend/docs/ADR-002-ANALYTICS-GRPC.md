# Módulo 9 – Analytics, gRPC y caracterización de carga
## Proyecto Fresh Bowl

## 1. Objetivo

Evaluar la necesidad de incorporar mecanismos de Analytics y comunicación mediante gRPC en el backend de Fresh Bowl.

Además, se define una estrategia para caracterizar el rendimiento de la aplicación y comprobar su comportamiento frente a diferentes niveles de solicitudes.

## 2. Aplicabilidad de Analytics

**Decisión: Analytics sí aplica al proyecto.**

Fresh Bowl necesita consultar información que permita conocer el estado general del negocio, especialmente la disponibilidad de ingredientes, la cantidad de pedidos y las ventas registradas.

Actualmente existe una consulta GraphQL denominada `dashboard`, que obtiene indicadores de los subsistemas Inventory y Orders.

### 2.1 Indicadores disponibles

| Indicador | Descripción | Fuente |
|---|---|---|
| Ingredientes disponibles | Cantidad de ingredientes activos y disponibles | Inventory |
| Total de pedidos | Cantidad total de pedidos registrados | Orders |
| Total de ventas | Suma de los pedidos que no están cancelados | Orders |

Estos indicadores permiten obtener una visión general de la actividad del negocio.

### 2.2 Implementación

La consulta se encuentra implementada en:

`app/graphql/resolvers.py`

La función `get_dashboard_data` realiza consultas a la base de datos y construye un resultado que reúne información de Inventory y Orders.

La información se entrega mediante el endpoint:

`POST /api/v1/graphql`

Actualmente se trata de una agregación de indicadores básicos. No existe todavía un módulo independiente de analítica avanzada, generación de reportes históricos ni visualización de tendencias.

## 3. Decisión sobre gRPC

**Decisión: No se considera necesario implementar gRPC en esta versión del proyecto.**

### 3.1 Justificación

gRPC es una alternativa para la comunicación entre servicios, especialmente cuando se requiere comunicación eficiente y contratos definidos entre componentes distribuidos.

Sin embargo, Fresh Bowl actualmente utiliza una aplicación FastAPI que contiene los módulos de autenticación, inventario, pedidos, clientes, pagos y GraphQL.

Estos módulos comparten la misma aplicación y acceden a la persistencia mediante SQLAlchemy.

Por lo tanto:

1. No existen microservicios independientes que necesiten comunicarse mediante RPC.
2. Los módulos comparten el entorno de ejecución.
3. Las operaciones actuales pueden resolverse mediante las funciones y servicios internos de la aplicación.
4. Incorporar gRPC aumentaría la complejidad de la arquitectura sin aportar una necesidad funcional comprobada.

### 3.2 Alternativa utilizada

Se mantiene la comunicación interna mediante servicios Python y SQLAlchemy.

Para la consulta agregada de información se utiliza GraphQL, mientras que las operaciones de administración y negocio se exponen mediante endpoints REST.

### 3.3 Condiciones para reconsiderar gRPC

La decisión podría revisarse si Fresh Bowl evoluciona hacia una arquitectura distribuida con servicios independientes, por ejemplo, si Inventory y Orders pasan a ejecutarse en servidores distintos y requieren comunicación interna frecuente.

## 4. Registro de decisión arquitectónica (ADR)

**ADR-002: No incorporar gRPC en la versión actual de Fresh Bowl.**

| Elemento | Descripción |
|---|---|
| Estado | Aceptado |
| Contexto | Backend modular implementado en una aplicación FastAPI |
| Problema | Determinar si se necesita comunicación RPC entre subsistemas |
| Decisión | Mantener comunicación interna mediante servicios Python y utilizar REST y GraphQL para exponer operaciones |
| Alternativas evaluadas | Incorporar gRPC o mantener la arquitectura actual |
| Justificación | No existen servicios distribuidos que requieran comunicación RPC |
| Consecuencia positiva | Menor complejidad de implementación y mantenimiento |
| Consecuencia negativa | Si se distribuyen los módulos en el futuro, podría ser necesario incorporar un mecanismo de comunicación entre servicios |

## 5. Caracterización de carga

La caracterización de carga permite evaluar cómo responde el backend cuando recibe distintas cantidades de solicitudes.

Para Fresh Bowl interesa observar especialmente las operaciones de consulta de ingredientes, creación de pedidos y consulta del dashboard.

### 5.1 Operaciones que se deben evaluar

| Operación | Endpoint | Objetivo |
|---|---|---|
| Consulta de ingredientes | `GET /api/v1/ingredients` | Medir el tiempo de respuesta del catálogo |
| Creación de pedidos | `POST /api/v1/orders` | Evaluar el procesamiento de pedidos |
| Consulta GraphQL | `POST /api/v1/graphql` | Evaluar la agregación de información |
| Inicio de sesión | `POST /api/v1/auth/login` | Evaluar el proceso de autenticación |

### 5.2 Métricas

Se consideran las siguientes métricas:

- Latencia promedio: tiempo promedio de respuesta.
- Latencia p95: tiempo dentro del cual se completa el 95 % de las solicitudes.
- Throughput: cantidad de solicitudes procesadas por segundo.
- Tasa de errores: porcentaje de solicitudes que terminan con error.
- Uso de CPU: recursos de procesamiento utilizados.
- Uso de memoria: memoria utilizada durante la prueba.

### 5.3 Escenarios de prueba propuestos

Se propone evaluar el backend con diferentes niveles de concurrencia:

| Escenario | Usuarios concurrentes | Propósito |
|---|---:|---|
| Bajo | 1 | Comprobar el funcionamiento inicial |
| Medio | 5 | Evaluar solicitudes simultáneas moderadas |
| Alto | 10 | Observar el comportamiento con mayor concurrencia |

Cada escenario debe ejecutarse con una duración definida y utilizando datos de prueba controlados.

### 5.4 Estado de las mediciones

Actualmente no se dispone de resultados de una prueba de carga ejecutada y registrada.

Por lo tanto, no se presentan valores de latencia, throughput, CPU o memoria como si hubieran sido medidos.

Las mediciones deben completarse y registrarse antes de considerar finalizada esta parte de la evaluación.

## 6. Evidencia de pruebas funcionales

El proyecto cuenta con pruebas automatizadas para verificar las operaciones principales del backend.

En la última ejecución registrada se obtuvieron:

- 56 pruebas aprobadas.
- 0 pruebas fallidas.

Estas pruebas permiten comprobar el comportamiento funcional y los controles de acceso, pero no reemplazan una prueba de carga.

## 7. Limitaciones y mejoras pendientes

- Ejecutar pruebas de carga con concurrencia controlada.
- Registrar latencia promedio y p95.
- Medir throughput y tasa de errores.
- Registrar consumo de CPU y memoria.
- Evaluar el comportamiento de GraphQL frente a consultas complejas.
- Reconsiderar gRPC si en el futuro se implementan servicios distribuidos.

## 8. Conclusión

Analytics resulta aplicable a Fresh Bowl porque permite obtener indicadores generales mediante la consulta agregada `dashboard` de GraphQL.

En cambio, gRPC no se considera necesario en la arquitectura actual, ya que los subsistemas forman parte de una misma aplicación FastAPI y no requieren comunicación RPC entre servicios independientes.

Finalmente, el backend dispone de pruebas funcionales automatizadas, pero aún debe completarse la caracterización de carga para contar con mediciones objetivas de rendimiento.
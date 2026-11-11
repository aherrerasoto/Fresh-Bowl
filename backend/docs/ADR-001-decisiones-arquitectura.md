
# ADR-001: Decisiones de arquitectura de Fresh Bowl

- **Estado:** Aceptado
- **Proyecto:** Fresh Bowl
- **Fecha:** Noviembre de 2026

## 1. Contexto

Fresh Bowl es una plataforma de venta de ensaladas personalizadas. El backend debe permitir gestionar ingredientes, clientes, pedidos, pagos y autenticación, manteniendo la protección de los datos y la comunicación entre sus componentes.

Para desarrollar el sistema se consideraron tecnologías que permitieran construir una API, gestionar información persistente, controlar los accesos y facilitar las consultas entre distintos módulos.

## 2. Decisiones tecnológicas

### 2.1 Python y FastAPI

Se seleccionó Python con FastAPI para desarrollar el backend debido a que permite construir servicios HTTP, validar datos y organizar las funcionalidades mediante rutas y módulos independientes.

### 2.2 SQLAlchemy y SQLite

Se utiliza SQLAlchemy como herramienta de acceso a datos y SQLite como base de datos para el entorno de desarrollo.

Esta combinación permite administrar las entidades del sistema y realizar operaciones de persistencia sin incorporar inicialmente un servidor de base de datos adicional.

### 2.3 HTTP y API Gateway

Se utiliza HTTP para la comunicación con los servicios del backend.

Se implementó una capa API Gateway que centraliza políticas de acceso según las rutas, los métodos HTTP y los roles de los usuarios.

### 2.4 GraphQL

Se incorporó GraphQL mediante Strawberry para facilitar consultas que combinan información de distintos módulos.

Actualmente permite consultar ingredientes, pedidos y un resumen general que reúne información de Inventario y Pedidos.

### 2.5 Autenticación y protección de información

Se utiliza autenticación mediante tokens almacenados en cookies HttpOnly y contraseñas protegidas mediante hash.

Los permisos se organizan según los roles de administrador, técnico y cliente.

### 2.6 HashiCorp Vault

Se seleccionó HashiCorp Vault para centralizar la gestión de secretos y evitar almacenar credenciales sensibles directamente en el código fuente.

La integración está preparada, pero su ejecución y validación mediante Docker quedan pendientes.

### 2.7 Docker

Se seleccionó Docker Compose para facilitar la ejecución coordinada del backend y Vault.

La configuración está creada, pero la construcción de la imagen presenta un inconveniente técnico pendiente de resolución.

## 3. Decisión sobre gRPC

Se determinó que gRPC no resulta necesario en la implementación actual.

Los módulos de Inventario, Clientes, Pedidos y Pagos funcionan dentro de una misma aplicación FastAPI y comparten la capa de persistencia.

Por este motivo, la comunicación HTTP y las llamadas internas entre componentes son suficientes para las necesidades actuales.

La incorporación de gRPC podría evaluarse posteriormente si los módulos se separan en servicios independientes y requieren comunicación interna de alto rendimiento.

## 4. Decisión sobre analítica

Se decidió incorporar inicialmente una consulta de resumen mediante GraphQL.

Esta consulta permite obtener:

- Cantidad de ingredientes disponibles.
- Cantidad de pedidos registrados.
- Total de ventas de pedidos no cancelados.

Esta funcionalidad cubre necesidades básicas de consulta operativa. No constituye todavía un sistema avanzado de análisis histórico ni de generación de informes.

## 5. Consecuencias

Las decisiones adoptadas permiten mantener una arquitectura modular y relativamente sencilla de desarrollar y mantener.

Entre sus ventajas se encuentran:

- Separación funcional de los módulos.
- Validación centralizada de solicitudes.
- Consultas agregadas mediante GraphQL.
- Control de acceso basado en roles.
- Posibilidad de incorporar servicios independientes en el futuro.

Como limitaciones actuales se identifican la utilización de SQLite para el entorno de desarrollo, la ausencia de un servicio de analítica avanzado y la validación pendiente del despliegue mediante Docker y Vault.

## 6. Conclusión

La arquitectura seleccionada responde a las necesidades actuales de Fresh Bowl y permite desarrollar sus funcionalidades sin incorporar tecnologías que no aporten un beneficio inmediato.

Las decisiones podrán revisarse si el sistema aumenta su complejidad, volumen de usuarios o necesidad de integración con servicios externos.

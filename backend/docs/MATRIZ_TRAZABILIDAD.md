# Matriz de trazabilidad – Fresh Bowl

## 1. Objetivo

Relacionar las funcionalidades del frontend de Fresh Bowl con los servicios del backend, las pruebas automatizadas y sus resultados. Esta matriz permite comprobar que las operaciones implementadas responden a las necesidades del sistema.

## 2. Matriz de trazabilidad

| ID | Requisito o funcionalidad | Pantalla frontend | Servicio backend | Operación | Prueba relacionada | Resultado |
|---|---|---|---|---|---|---|
| RF-01 | Visualizar los ingredientes disponibles | Catálogo | Inventory | GET /api/v1/ingredients/ | test_inventory.py | Aprobada |
| RF-02 | Consultar información de un ingrediente | Catálogo | Inventory | GET /api/v1/ingredients/{id} | test_inventory.py | Aprobada |
| RF-03 | Personalizar una ensalada seleccionando ingredientes | Personalización | Inventory | GET /api/v1/ingredients/ | test_inventory.py | Aprobada |
| RF-04 | Agregar productos personalizados al carrito | Carrito | Frontend | Gestión local del carrito | No aplica a una ruta backend independiente | Implementación frontend |
| RF-05 | Registrar un pedido con los datos del cliente | Confirmación | Orders | POST /api/v1/orders/ | test_orders.py | Aprobada |
| RF-06 | Validar disponibilidad de ingredientes al realizar un pedido | Confirmación | Orders e Inventory | POST /api/v1/orders/ | test_orders.py | Aprobada |
| RF-07 | Calcular el total del pedido utilizando los precios almacenados en el backend | Confirmación | Orders | POST /api/v1/orders/ | test_orders.py | Aprobada |
| RF-08 | Registrar el pago de un pedido | Confirmación | Payments | POST /api/v1/payments/ | test_payments.py | Aprobada |
| RF-09 | Evitar pagos duplicados | Confirmación | Payments | POST /api/v1/payments/ | test_payments.py | Aprobada |
| RF-10 | Impedir pagos de pedidos cancelados | Confirmación | Payments | POST /api/v1/payments/ | test_payments.py | Aprobada |
| RF-11 | Permitir el registro opcional de clientes | Sin pantalla específica en la versión frontend actual | Auth | POST /api/v1/auth/register | test_auth.py | Aprobada |
| RF-12 | Permitir el inicio de sesión | Sin pantalla específica en la versión frontend actual | Auth | POST /api/v1/auth/login | test_auth.py | Aprobada |
| RF-13 | Consultar información consolidada del sistema | No existe una pantalla de administración en el frontend actual | GraphQL | POST /api/v1/graphql | test_graphql.py | Aprobada |

## 3. Servicios complementarios

| Servicio | Responsabilidad | Acceso |
|---|---|---|
| Auth | Registro, inicio y cierre de sesión y consulta del usuario autenticado | Público para registro e inicio de sesión; autenticado para perfil |
| Clients | Administración de clientes | Administrador |
| Inventory | Consulta y administración de ingredientes y existencias | Consulta pública; administración restringida |
| Orders | Creación y administración de pedidos | Creación pública; consultas y cambios restringidos |
| Payments | Registro y consulta de pagos | Registro público; consultas restringidas |
| Gateway | Aplicación de políticas de acceso | Según las políticas configuradas |
| GraphQL | Consulta y agregación de información de inventario y pedidos | Administrador y técnico |

## 4. Consideraciones

- El carrito administra temporalmente la selección del usuario en el frontend. El pedido se registra en el backend al confirmar la compra.
- Los precios y las reglas de negocio se validan en el backend, evitando depender exclusivamente de los valores enviados por el navegador.
- El pago utiliza un proveedor simulado y no representa una transacción bancaria real.
- Las operaciones administrativas de clientes, inventario, pedidos y pagos están protegidas según los roles definidos.
- La integración directa entre las pantallas del frontend y los servicios del backend se documentará y demostrará según el alcance indicado por el profesor para cada evaluación.

## 5. Evidencias

La ejecución global de las pruebas automatizadas registró 56 pruebas aprobadas y ninguna fallida.

Comando utilizado:

```powershell
python -m pytest -v
```

La captura del resultado de ejecución debe incorporarse como evidencia de las pruebas del backend.


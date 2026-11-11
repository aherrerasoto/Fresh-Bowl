# Módulo 4 – Stakeholders, autenticación y permisos
## Proyecto Fresh Bowl

## 1. Objetivo

Identificar los actores que interactúan con Fresh Bowl y establecer sus permisos sobre los recursos del backend.

El control de acceso se implementa mediante autenticación con JWT, cookies HttpOnly y autorización basada en roles (RBAC).

## 2. Stakeholders

| Stakeholder | Descripción | Necesidades y responsabilidades |
|---|---|---|
| Cliente | Persona que utiliza Fresh Bowl para comprar ensaladas personalizadas | Consultar ingredientes, personalizar su pedido, registrar sus datos y realizar compras |
| Administrador | Responsable de administrar la plataforma | Gestionar ingredientes, clientes, pedidos, pagos y operaciones administrativas |
| Técnico | Responsable de revisar y gestionar operaciones autorizadas del sistema | Consultar pedidos, revisar pagos y acceder a información operativa mediante GraphQL |
| Proveedor de pagos | Componente externo simulado que representa el procesamiento de pagos | Recibir la solicitud de pago y devolver un resultado de aprobación o rechazo |
| Equipo de desarrollo | Responsables de implementar y mantener el sistema | Mantener los servicios, corregir errores, ejecutar pruebas y proteger la información |

## 3. Roles del sistema

### 3.1 Cliente

El cliente puede:
- Registrarse en la plataforma.
- Iniciar y cerrar sesión.
- Consultar su información de autenticación.
- Consultar los ingredientes disponibles.
- Crear pedidos sin necesidad de una cuenta registrada.
- Iniciar el proceso de pago mediante el proveedor simulado.

El cliente no puede consultar la lista general de pedidos, administrar ingredientes ni consultar los pagos registrados.

### 3.2 Técnico

El técnico puede:
- Consultar pedidos registrados.
- Consultar pedidos individuales.
- Modificar el estado de los pedidos mediante las operaciones autorizadas.
- Consultar pagos.
- Acceder a consultas GraphQL de información operativa.

No puede administrar ingredientes ni clientes.

### 3.3 Administrador

El administrador cuenta con permisos de gestión sobre los módulos protegidos.

Puede:
- Crear, consultar, modificar y desactivar ingredientes.
- Consultar y administrar clientes.
- Consultar y gestionar pedidos.
- Consultar pagos.
- Acceder a consultas GraphQL.
- Administrar las operaciones correspondientes a su rol.

## 4. Matriz de permisos por ruta y método HTTP

| Recurso | Método | Ruta | Cliente | Técnico | Administrador |
|---|---|---|---|---|---|
| Auth | POST | /api/v1/auth/register | Permitido | Permitido | Permitido |
| Auth | POST | /api/v1/auth/login | Permitido | Permitido | Permitido |
| Auth | POST | /api/v1/auth/logout | Permitido | Permitido | Permitido |
| Auth | GET | /api/v1/auth/me | Propio usuario autenticado | Propio usuario autenticado | Propio usuario autenticado |
| Inventory | GET | /api/v1/ingredients/ | Permitido | Permitido | Permitido |
| Inventory | GET | /api/v1/ingredients/{id} | Permitido | Permitido | Permitido |
| Inventory | POST | /api/v1/ingredients/ | Denegado | Denegado | Permitido |
| Inventory | PATCH | /api/v1/ingredients/{id} | Denegado | Denegado | Permitido |
| Inventory | DELETE | /api/v1/ingredients/{id} | Denegado | Denegado | Permitido |
| Clients | GET | /api/v1/clients/ | Denegado | Denegado | Permitido |
| Clients | POST | /api/v1/clients/ | Denegado | Denegado | Permitido |
| Clients | PATCH | /api/v1/clients/{id} | Denegado | Denegado | Permitido |
| Clients | DELETE | /api/v1/clients/{id} | Denegado | Denegado | Permitido |
| Orders | POST | /api/v1/orders/ | Permitido | Permitido | Permitido |
| Orders | GET | /api/v1/orders/ | Denegado | Permitido | Permitido |
| Orders | GET | /api/v1/orders/{id} | Denegado | Permitido | Permitido |
| Orders | PATCH | /api/v1/orders/{id}/status | Denegado | Permitido | Permitido |
| Payments | POST | /api/v1/payments/ | Permitido | Permitido | Permitido |
| Payments | GET | /api/v1/payments/ | Denegado | Permitido | Permitido |
| Payments | GET | /api/v1/payments/{id} | Denegado | Permitido | Permitido |
| GraphQL | POST | /api/v1/graphql | Denegado | Permitido | Permitido |

**Consideraciones:**

- Las operaciones públicas no requieren iniciar sesión.
- Las rutas protegidas requieren una cookie de autenticación válida.
- Las operaciones administrativas requieren el rol administrador.
- Las consultas operativas de pedidos, pagos y GraphQL permiten los roles técnico y administrador.
- El registro público siempre crea usuarios con rol cliente; no permite que una persona se asigne privilegios administrativos.

## 5. Mecanismo de autenticación

El sistema utiliza JSON Web Tokens (JWT) para identificar a los usuarios autenticados.

El proceso es el siguiente:

1. El usuario envía sus credenciales al endpoint de inicio de sesión.
2. El backend busca la cuenta correspondiente.
3. Se verifica la contraseña mediante el hash almacenado.
4. Si las credenciales son válidas, se genera un token JWT.
5. El token se almacena en una cookie HttpOnly.
6. En las siguientes solicitudes protegidas, el backend valida el token y obtiene la identidad y el rol del usuario.

La cookie HttpOnly evita que el token sea leído directamente mediante JavaScript desde el navegador.

## 6. Autorización basada en roles

El sistema aplica control de acceso basado en roles (RBAC).

La autorización se realiza mediante las políticas del API Gateway y las dependencias de seguridad de los endpoints protegidos.

Las principales condiciones son:

- Si no existe un token válido, se rechaza la solicitud con HTTP 401.
- Si existe un usuario autenticado, pero no tiene el rol requerido, se responde HTTP 403.
- Si el usuario cumple las condiciones de acceso, puede continuar la operación.
- Los usuarios inactivos no deben poder acceder a los recursos protegidos.

## 7. Protección de recursos

Los permisos se aplican en el backend y no dependen únicamente de la visibilidad de botones o elementos de la interfaz.

Esto evita que un usuario obtenga acceso a una operación simplemente enviando una solicitud HTTP directamente.

Las consultas de información de clientes, pedidos y pagos se restringen según los roles definidos.

## 8. Evidencia de pruebas

Las pruebas automatizadas comprueban distintos escenarios de autenticación y autorización.

Entre los casos ejecutados se encuentran:

| Escenario | Resultado esperado | Evidencia |
|---|---|---|
| Consultar pagos sin autenticación | HTTP 401 | test_payment_security.py |
| Consultar pagos como cliente | HTTP 403 | test_payment_security.py |
| Consultar pedidos sin iniciar sesión | HTTP 401 | test_orders.py |
| Consultar pedidos como cliente | HTTP 403 | test_orders.py |
| Acceder a operaciones administrativas con el rol correcto | Acceso permitido | Pruebas de los módulos |
| Acceder a recursos protegidos con credenciales inválidas | Acceso rechazado | Pruebas de autenticación |

La ejecución global más reciente registró 56 pruebas aprobadas y ninguna fallida.

## 9. Consideraciones de seguridad pendientes

Aunque el backend cuenta con autenticación y autorización por roles, se identifican aspectos que deben considerarse antes de un despliegue de producción:

- Configurar una clave JWT segura y exclusiva para producción.
- Habilitar cookies Secure bajo HTTPS.
- Definir controles de CORS y protección CSRF según el esquema de integración.
- Validar la propiedad de los recursos para evitar que un cliente pueda operar sobre pedidos ajenos.
- Verificar la integración de Vault para la gestión de secretos.
- Evitar almacenar información bancaria real en el sistema.

## 10. Conclusión

Fresh Bowl utiliza autenticación basada en JWT y autorización por roles para controlar el acceso a los recursos del backend.

La separación entre cliente, técnico y administrador permite restringir las operaciones según las responsabilidades de cada actor. Las pruebas automatizadas proporcionan evidencia de que las restricciones principales se aplican correctamente.
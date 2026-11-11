# Módulo 7 – Clasificación y protección de datos
## Proyecto Fresh Bowl

## 1. Objetivo

Identificar y clasificar la información utilizada por Fresh Bowl, establecer las medidas de protección correspondientes y determinar si el sistema necesita almacenar secretos asociados a los clientes.

La clasificación permite definir qué información puede consultarse públicamente y cuál requiere controles de acceso y protección adicionales.

## 2. Clasificación de la información

Se establecen cuatro niveles de clasificación:

- Público: información que puede consultarse sin identificar ni perjudicar a una persona.
- Interno: información utilizada para la operación del negocio y que no necesita divulgarse públicamente.
- Confidencial: información personal o comercial cuyo acceso debe estar restringido.
- Crítico: credenciales y elementos cuya exposición podría comprometer la seguridad del sistema.

### 2.1 Matriz de clasificación

| Información | Ejemplo | Clasificación | Justificación |
|---|---|---|---|
| Nombre del ingrediente | Mix de hojas | Público | Forma parte del catálogo comercial |
| Categoría del ingrediente | Proteína, vegetales | Público | Permite organizar el catálogo |
| Descripción del ingrediente | Descripción del producto | Público | Información necesaria para el cliente |
| Precio del ingrediente | Precio en pesos chilenos | Público | Necesario para mostrar el catálogo |
| Cantidad disponible | Stock de ingredientes | Interno | Información operativa del negocio |
| Estado de disponibilidad | Disponible o no disponible | Público | Permite informar al cliente sobre el catálogo |
| Nombre del cliente | Nombre completo | Confidencial | Permite identificar a una persona |
| Correo electrónico | Correo de contacto | Confidencial | Dato personal utilizado para comunicación |
| Teléfono | Número de contacto | Confidencial | Dato personal |
| Dirección de entrega | Dirección del pedido | Confidencial | Información personal que requiere protección |
| Detalles del pedido | Ingredientes y cantidades | Confidencial | Información asociada a una compra |
| Historial de pedidos | Pedidos anteriores | Confidencial | Permite conocer la actividad de compra |
| Contraseña | Contraseña de acceso | Crítico | Debe protegerse mediante hash |
| Hash de contraseña | Hash Argon2 | Crítico | Permite verificar credenciales |
| Token JWT | Token de autenticación | Crítico | Permite acceder a recursos protegidos |
| Clave JWT | JWT_SECRET_KEY | Crítico | Permite firmar y validar tokens |
| Credenciales de base de datos | DATABASE_URL | Crítico | Permiten acceder a la persistencia |
| Token de Vault | VAULT_TOKEN | Crítico | Permite autenticarse ante el gestor de secretos |

## 3. Justificación de la clasificación

Los datos públicos corresponden principalmente a la información comercial del catálogo, como nombres, descripciones, categorías y precios.

Los datos internos se relacionan con el funcionamiento del negocio, especialmente las existencias y la administración del inventario.

Los datos confidenciales corresponden a información personal de los clientes y a los detalles de sus compras. Su exposición podría afectar la privacidad de las personas.

Los datos críticos corresponden principalmente a credenciales y mecanismos de autenticación. Su divulgación podría permitir accesos no autorizados al sistema.

## 4. Protección de los datos

### 4.1 Contraseñas

Las contraseñas no se almacenan como texto plano.

El sistema utiliza `pwdlib` con Argon2 para generar hashes y verificar las credenciales durante el inicio de sesión.

### 4.2 Autenticación

La autenticación utiliza tokens JWT.

El token se almacena en una cookie HttpOnly denominada `access_token`, evitando que JavaScript pueda leerlo directamente desde el navegador.

### 4.3 Autorización

El backend aplica permisos según los roles definidos:

- Cliente.
- Técnico.
- Administrador.

Las rutas protegidas verifican la autenticación y los permisos correspondientes.

### 4.4 Protección de la persistencia

Los datos se almacenan mediante SQLAlchemy y SQLite en el entorno de desarrollo.

El acceso a la base de datos se realiza desde el backend y no directamente desde el navegador.

Las credenciales de conexión deben mantenerse fuera del código fuente y del frontend.

### 4.5 Protección de pagos

El sistema utiliza un proveedor de pagos simulado.

No almacena números de tarjetas, códigos CVV ni contraseñas bancarias. El registro de pagos conserva información necesaria para identificar el pedido, el monto, el método, el estado y la referencia del proveedor.

## 5. Decisión sobre secretos asociados al cliente

**Decisión: Fresh Bowl no necesita custodiar secretos bancarios ni credenciales de pago de los clientes.**

La decisión se fundamenta en las características del caso:

1. El sistema utiliza un proveedor de pagos simulado.
2. No se realiza conexión directa con cuentas bancarias.
3. No es necesario almacenar números de tarjetas ni códigos de seguridad.
4. Los datos de contacto del cliente no constituyen secretos de autenticación.
5. La autenticación de los usuarios se administra mediante el mecanismo propio de Auth.

Por lo tanto, el sistema protege los datos personales y las credenciales de acceso, pero no mantiene secretos financieros de los clientes.

## 6. Acceso a los datos

| Información | Cliente | Técnico | Administrador |
|---|---|---|---|
| Catálogo de ingredientes | Consulta | Consulta | Consulta y administración |
| Existencias | No administra | No administra | Administración |
| Datos generales de clientes | Sin acceso administrativo | Sin acceso administrativo | Administración |
| Pedidos | Puede crear | Consulta y gestión autorizada | Consulta y gestión autorizada |
| Pagos | Puede iniciar el pago | Consulta | Consulta |
| Información de autenticación propia | Acceso mediante su sesión | Acceso mediante su sesión | Acceso mediante su sesión |
| Credenciales de infraestructura | Sin acceso | Sin acceso | Acceso operativo restringido |

La matriz representa los permisos generales implementados. No implica que exista actualmente una función para que el cliente consulte su historial de pedidos.

## 7. Retención y eliminación de información

Se propone mantener los datos únicamente durante el período necesario para cumplir sus finalidades operativas y administrativas.

Las siguientes medidas se consideran criterios de gestión:

- Los datos de contacto deben conservarse mientras sean necesarios para gestionar las operaciones del cliente.
- Los pedidos deben conservarse durante el período definido por las necesidades administrativas del negocio.
- Las contraseñas deben almacenarse únicamente como hashes.
- Los tokens de autenticación deben tener una duración limitada.
- Las credenciales reemplazadas o comprometidas deben revocarse.
- Los registros técnicos no deben incluir contraseñas, tokens ni datos personales innecesarios.

La política formal de retención, eliminación y respaldo todavía debe definirse e implementarse. No se considera una funcionalidad ya verificada.

## 8. Medidas de seguridad pendientes

Antes de utilizar el sistema en producción se deben considerar las siguientes mejoras:

- Habilitar HTTPS y cookies con atributo Secure.
- Configurar protección CSRF para las operaciones autenticadas mediante cookies.
- Restringir los orígenes permitidos mediante CORS.
- Implementar controles de propiedad de los pedidos para limitar el acceso a los registros de cada cliente.
- Verificar la integración con HashiCorp Vault.
- Definir procedimientos de respaldo y recuperación de la base de datos.
- Establecer una política formal de retención y eliminación de datos.

## 9. Evidencia de implementación

Las medidas de protección cuentan con pruebas automatizadas relacionadas con:

- Registro e inicio de sesión.
- Verificación de contraseñas.
- Acceso a rutas protegidas.
- Restricción de permisos según el rol.
- Rechazo de consultas de pagos sin autenticación.
- Rechazo de consultas de pagos realizadas por clientes.

La última ejecución global registró 56 pruebas aprobadas y ninguna fallida.

## 10. Conclusión

Fresh Bowl clasifica la información según su nivel de exposición y el impacto que tendría su divulgación.

El sistema protege las credenciales mediante hash, utiliza JWT para autenticación y aplica autorización basada en roles.

Se determinó que no es necesario almacenar secretos bancarios de los clientes, ya que el procesamiento de pagos se realiza mediante un proveedor simulado.

Se identifican medidas adicionales de seguridad y gestión de información que deben completarse antes de un despliegue de producción.
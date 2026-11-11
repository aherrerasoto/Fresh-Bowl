# Fresh Bowl – Ensaladas personalizadas

## 1. Descripción del proyecto

Fresh Bowl es un prototipo de una página web para un local de ensaladas personalizadas. Permite que los usuarios revisen un catálogo de ingredientes, seleccionen los que desean incluir en su ensalada, elijan el tamaño, revisen el precio y simulen la confirmación de un pedido.

El proyecto fue desarrollado como parte de la Evaluación 1, enfocándose en el diseño de interfaces, la adaptación a distintos dispositivos y la interacción mediante JavaScript.

## 2. Objetivo

Desarrollar una interfaz web responsive y dinámica que permita simular el proceso de compra de una ensalada personalizada, desde la selección de ingredientes hasta la confirmación del pedido.

## 3. Tecnologías utilizadas

- **HTML5:** estructura y organización del contenido.
- **CSS3:** estilos, colores, distribución y adaptación responsive.
- **Bootstrap 5:** sistema de grillas y componentes para facilitar la adaptación a diferentes tamaños de pantalla.
- **JavaScript:** interacción con los elementos de la página, selección de ingredientes, cálculo de precios y navegación entre secciones.
- **JSON:** almacenamiento local de los datos de los ingredientes.

## 4. Estructura del proyecto

```text
fresh bowl/
│
├── css/
│   └── styles.css
│
├── data/
│   └── ingredientes.json
│
├── diseño/
│   ├── Inicio - Escritorio.png
│   ├── Inicio - Móvil.png
│   ├── Catálogo - Escritorio.png
│   ├── Catálogo - Móvil.png
│   ├── Personalización - Escritorio.png
│   ├── Personalización - Móvil.png
│   ├── Carrito - Escritorio.png
│   ├── Carrito - Móvil.png
│   ├── Confirmación - Escritorio.png
│   └── Confirmación - Móvil.png
│
├── js/
│   └── app.js
│
├── index.html
└── README.md
```

## 5. Funcionalidades principales

- Visualización de la página de inicio.
- Consulta del catálogo de ingredientes.
- Búsqueda y filtrado de ingredientes por categoría.
- Selección y eliminación de ingredientes.
- Personalización del tamaño de la ensalada.
- Cálculo automático del precio.
- Visualización del resumen de la ensalada.
- Incorporación de la ensalada al carrito.
- Confirmación simulada del pedido mediante un servicio Dummy.

## 6. Diseño responsive

La interfaz fue diseñada para adaptarse a distintos tamaños de pantalla, considerando las versiones de escritorio y móvil.

Se realizaron pruebas utilizando los siguientes anchos de pantalla:

- 375 px.
- 576 px.
- 768 px.
- 1200 px.

Se utilizaron grillas, Flexbox y propiedades del modelo de caja (Box Model) para organizar los elementos y mantener una presentación adecuada en los distintos dispositivos.

## 7. Servicios Dummy

El proyecto utiliza servicios simulados para representar operaciones que normalmente serían realizadas por un servidor.

- **Consulta de ingredientes:** obtiene los datos desde el archivo `ingredientes.json`.
- **Creación de pedidos:** simula el envío de un pedido y devuelve una respuesta con un número de confirmación generado automáticamente.

Estas operaciones no utilizan una base de datos ni un servidor real.

## 8. Instrucciones de ejecución

Para ejecutar el proyecto localmente:

1. Descargar o abrir la carpeta del proyecto en Visual Studio Code.
2. Verificar que se encuentren todas las carpetas y archivos.
3. Instalar la extensión Live Server en Visual Studio Code, si todavía no está instalada.
4. Abrir el archivo `index.html`.
5. Hacer clic derecho y seleccionar **Open with Live Server**.
6. La página se abrirá en el navegador predeterminado.

Se recomienda utilizar Live Server para permitir la consulta del archivo JSON local.

## 9. Alcance y limitaciones

Fresh Bowl corresponde a un prototipo de Front-End. Por lo tanto, las operaciones de consulta y creación de pedidos son simuladas.

El proyecto no contempla una base de datos real, procesamiento de pagos, autenticación de usuarios ni conexión con servicios externos de producción.

## 10. Evidencias de diseño

La carpeta `diseño` contiene las propuestas visuales de las cinco pantallas principales, tanto para escritorio como para dispositivos móviles.

Estas imágenes permiten comparar el diseño inicial con la interfaz desarrollada.
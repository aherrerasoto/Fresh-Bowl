
// =====================================
// 1. ELEMENTOS DEL HTML
// =====================================

const botonCrear = document.querySelector("#btnCrear");
const seccionInicio = document.querySelector("#inicio");
const seccionCatalogo = document.querySelector("#catalogo");

const listaIngredientes = document.querySelector("#listaIngredientes");
const cantidadIngredientes = document.querySelector("#cantidadIngredientes");

const buscador = document.querySelector("#buscador");
const botonesCategorias = document.querySelectorAll(".categoria");

const listaSeleccionados = document.querySelector("#listaSeleccionados");
const mensajeSeleccion = document.querySelector("#mensajeSeleccion");
const totalSeleccion = document.querySelector("#totalSeleccion");


// =====================================
// 2. VARIABLES
// =====================================

let ingredientes = [];
let categoriaActual = "Todos";

// Aquí guardaremos los ingredientes elegidos
let seleccionados = [];


// =====================================
// 3. FORMATEAR PRECIOS
// =====================================

function formatearPrecio(precio) {

    return "$" + precio.toLocaleString("es-CL");

}


// =====================================
// 4. CONSULTAR EL ARCHIVO JSON
// =====================================


// =====================================
// 4. CONSULTAR INGREDIENTES (DUMMY)
// =====================================

async function cargarIngredientes() {

    // Estado de carga
    cantidadIngredientes.textContent = "Cargando ingredientes...";

    listaIngredientes.innerHTML =
        "<p>Estamos buscando ingredientes disponibles.</p>";

    try {

        const respuesta = await fetch("data/ingredientes.json");

        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar los ingredientes.");
        }

        ingredientes = await respuesta.json();

        // Comprobamos que los datos sean una lista
        if (!Array.isArray(ingredientes)) {
            throw new Error("El formato de los ingredientes no es válido.");
        }

        // Mostramos los ingredientes
        mostrarIngredientes(ingredientes);

    } catch (error) {

        console.error("Error al cargar ingredientes:", error);

        cantidadIngredientes.textContent = "No se pudieron cargar los ingredientes.";

        // Mensaje de error
        listaIngredientes.innerHTML = "";

        const mensaje = document.createElement("p");
        mensaje.textContent =
            "Ocurrió un problema al consultar los ingredientes.";

        // Botón para volver a intentar
        const botonReintentar = document.createElement("button");

        botonReintentar.textContent = "Reintentar";
        botonReintentar.className = "btn-principal";

        botonReintentar.addEventListener("click", cargarIngredientes);

        listaIngredientes.appendChild(mensaje);
        listaIngredientes.appendChild(botonReintentar);

    }

}



// =====================================
// 5. MOSTRAR TARJETAS
// =====================================

function mostrarIngredientes(datos) {

    listaIngredientes.innerHTML = "";

    cantidadIngredientes.textContent =
        `${datos.length} ingredientes · Hechos para combinar`;

    if (datos.length === 0) {

        listaIngredientes.innerHTML =
            "<p>No encontramos ingredientes disponibles.</p>";

        return;
    }

    datos.forEach(ingrediente => {

        const columna = document.createElement("div");

        columna.className = "col-6 col-lg-4";

        const tarjeta = document.createElement("article");

        tarjeta.className = "tarjeta-ingrediente";

        const precio = ingrediente.precio === 0
            ? "Incluido"
            : formatearPrecio(ingrediente.precio);

        const yaSeleccionado = seleccionados.some(
            item => item.id === ingrediente.id
        );

        tarjeta.innerHTML = `
            <img
                src="${ingrediente.imagen}"
                alt="${ingrediente.nombre}"
            >

            <div class="tarjeta-contenido">

                <small>${ingrediente.categoria}</small>

                <h3>${ingrediente.nombre}</h3>

                <p>${ingrediente.descripcion}</p>

                <div class="tarjeta-pie">

                    <span>${precio}</span>

                    <button
                        class="btn-agregar"
                        data-id="${ingrediente.id}"
                        aria-label="Agregar ${ingrediente.nombre}"
                        ${yaSeleccionado ? "disabled" : ""}
                    >
                        ${yaSeleccionado ? "✓" : "+"}
                    </button>

                </div>

            </div>
        `;

        columna.appendChild(tarjeta);

        listaIngredientes.appendChild(columna);

    });

}


// =====================================
// 6. FILTRAR POR CATEGORÍA
// =====================================

botonesCategorias.forEach(boton => {

    boton.addEventListener("click", () => {

        categoriaActual = boton.dataset.categoria;

        botonesCategorias.forEach(btn => {
            btn.classList.remove("activa");
        });

        boton.classList.add("activa");

        filtrarIngredientes();

    });

});


// =====================================
// 7. BUSCADOR
// =====================================

buscador.addEventListener("input", filtrarIngredientes);


function filtrarIngredientes() {

    const texto = buscador.value.toLowerCase();

    const resultados = ingredientes.filter(ingrediente => {

        const coincideCategoria =
            categoriaActual === "Todos" ||
            ingrediente.categoria === categoriaActual;

        const coincideBusqueda =
            ingrediente.nombre.toLowerCase().includes(texto);

        return coincideCategoria && coincideBusqueda;

    });

    mostrarIngredientes(resultados);

}


// =====================================
// 8. AGREGAR INGREDIENTES
// =====================================

listaIngredientes.addEventListener("click", function(evento) {

    const boton = evento.target.closest(".btn-agregar");

    if (!boton || boton.disabled) {
        return;
    }

    const id = Number(boton.dataset.id);

    const ingrediente = ingredientes.find(
        item => item.id === id
    );

    if (!ingrediente) {
        return;
    }

    seleccionados.push(ingrediente);

    mostrarIngredientes(
        ingredientes.filter(item =>
            categoriaActual === "Todos" ||
            item.categoria === categoriaActual
        ).filter(item =>
            item.nombre.toLowerCase().includes(
                buscador.value.toLowerCase()
            )
        )
    );

    actualizarSeleccion();

});


// =====================================
// 9. ACTUALIZAR RESUMEN
// =====================================

function actualizarSeleccion() {

    listaSeleccionados.innerHTML = "";

    if (seleccionados.length === 0) {

        mensajeSeleccion.textContent =
            "Todavía no has seleccionado ingredientes.";

    } else {

        mensajeSeleccion.textContent =
            `${seleccionados.length} ingredientes seleccionados.`;

    }

    let total = 0;

    seleccionados.forEach(ingrediente => {

        total += ingrediente.precio;

        const elemento = document.createElement("li");

        elemento.textContent =
            `${ingrediente.nombre} - ${
                ingrediente.precio === 0
                    ? "Incluido"
                    : formatearPrecio(ingrediente.precio)
            }`;

        listaSeleccionados.appendChild(elemento);

    });

    totalSeleccion.textContent = formatearPrecio(total);

}


// =====================================
// 10. MOSTRAR CATÁLOGO
// =====================================

botonCrear.addEventListener("click", () => {

    seccionInicio.style.display = "none";

    seccionCatalogo.classList.add("visible");

    seccionCatalogo.scrollIntoView({
        behavior: "smooth"
    });

});


// =====================================
// 11. INICIAR PROGRAMA
// =====================================

cargarIngredientes();

actualizarSeleccion();


// =====================================
// 12. PERSONALIZACIÓN DE LA ENSALADA
// =====================================

const botonContinuar = document.querySelector("#btnContinuar");

const seccionPersonalizacion =
    document.querySelector("#personalizacion");

const botonVolverCatalogo =
    document.querySelector("#btnVolverCatalogo");

const resumenPersonalizacion =
    document.querySelector("#resumenPersonalizacion");

const precioPersonalizacion =
    document.querySelector("#precioPersonalizacion");

const tamanoResumen =
    document.querySelector("#tamanoResumen");

const opcionesTamano =
    document.querySelectorAll('input[name="tamano"]');


// Precio inicial de la ensalada
let precioBase = 5500;


// Mostrar la pantalla de personalización
botonContinuar.addEventListener("click", () => {

    seccionCatalogo.classList.remove("visible");

    seccionPersonalizacion.classList.add("visible");

    actualizarPersonalizacion();

    seccionPersonalizacion.scrollIntoView({
        behavior: "smooth"
    });

});


// Volver al catálogo
botonVolverCatalogo.addEventListener("click", () => {

    seccionPersonalizacion.classList.remove("visible");

    seccionCatalogo.classList.add("visible");

    seccionCatalogo.scrollIntoView({
        behavior: "smooth"
    });

});


// Actualizar cuando se cambia el tamaño
opcionesTamano.forEach(opcion => {

    opcion.addEventListener("change", () => {

        if (opcion.checked) {

            precioBase = opcion.value === "grande"
                ? 7500
                : 5500;

            actualizarPersonalizacion();

        }

    });

});


// Actualizar el resumen y el precio
function actualizarPersonalizacion() {

    resumenPersonalizacion.innerHTML = "";

    seleccionados.forEach(ingrediente => {

        const elemento = document.createElement("li");

        elemento.textContent = ingrediente.nombre;

        resumenPersonalizacion.appendChild(elemento);

    });

    const totalAdicional = seleccionados.reduce(
        (suma, ingrediente) => suma + ingrediente.precio,
        0
    );

    const total = precioBase + totalAdicional;

    const opcionElegida = document.querySelector(
        'input[name="tamano"]:checked'
    );

    const nombreTamano = opcionElegida.value === "grande"
        ? "Grande"
        : "Normal";

    tamanoResumen.textContent =
        `Tamaño: ${nombreTamano}`;

    precioPersonalizacion.textContent =
        formatearPrecio(total);

}


// =====================================
// 13. CARRITO DE COMPRAS
// =====================================

const botonAgregarCarrito =
    document.querySelector("#btnAgregarCarrito");

const seccionCarrito =
    document.querySelector("#carrito");

const carritoTamano =
    document.querySelector("#carritoTamano");

const carritoIngredientes =
    document.querySelector("#carritoIngredientes");

const carritoPrecio =
    document.querySelector("#carritoPrecio");

const carritoSubtotal =
    document.querySelector("#carritoSubtotal");

const carritoTotal =
    document.querySelector("#carritoTotal");


// Agregar la ensalada al carrito
botonAgregarCarrito.addEventListener("click", () => {

    // Obtenemos el precio adicional de los ingredientes
    const totalAdicional = seleccionados.reduce(
        (suma, ingrediente) => suma + ingrediente.precio,
        0
    );

    // Calculamos el precio completo
    const precioFinal = precioBase + totalAdicional;

    // Obtenemos el tamaño seleccionado
    const opcionTamano = document.querySelector(
        'input[name="tamano"]:checked'
    );

    const nombreTamano = opcionTamano.value === "grande"
        ? "Grande"
        : "Normal";

    // Mostramos el tamaño
    carritoTamano.textContent =
        `Tamaño: ${nombreTamano}`;

    // Mostramos los ingredientes
    carritoIngredientes.innerHTML = "";

    seleccionados.forEach(ingrediente => {

        const elemento = document.createElement("li");

        elemento.textContent = ingrediente.nombre;

        carritoIngredientes.appendChild(elemento);

    });

    // Actualizamos los precios
    carritoPrecio.textContent = formatearPrecio(precioFinal);
    carritoSubtotal.textContent = formatearPrecio(precioFinal);
    carritoTotal.textContent = formatearPrecio(precioFinal);

    // Cambiamos de pantalla
    seccionPersonalizacion.classList.remove("visible");
    seccionCarrito.classList.add("visible");

    seccionCarrito.scrollIntoView({
        behavior: "smooth"
    });

});

// =====================================
// 14. CONFIRMACIÓN DEL PEDIDO
// =====================================

// =====================================
// SERVICIO DUMMY: CREAR PEDIDO
// =====================================

async function crearPedidoDummy(pedido) {

    // Simulamos el tiempo de respuesta de un servidor
    await new Promise(resolve => setTimeout(resolve, 1200));

    // Validamos los datos del pedido
    if (!pedido.ingredientes || pedido.ingredientes.length === 0) {
        throw new Error("El pedido no contiene ingredientes.");
    }

    if (pedido.total <= 0) {
        throw new Error("El precio del pedido no es válido.");
    }

    // Simulamos una respuesta exitosa
    return {
        correcto: true,
        numero: Math.floor(1000 + Math.random() * 9000),
        mensaje: "Pedido registrado correctamente."
    };

}

const botonConfirmarPedido =
    document.querySelector("#btnConfirmarPedido");

const seccionConfirmacion =
    document.querySelector("#confirmacion");

const numeroPedido =
    document.querySelector("#numeroPedido");

const confirmacionTamano =
    document.querySelector("#confirmacionTamano");

const confirmacionIngredientes =
    document.querySelector("#confirmacionIngredientes");

const confirmacionTotal =
    document.querySelector("#confirmacionTotal");

const botonVolverInicio =
    document.querySelector("#btnVolverInicio");


// Confirmar pedido

// Confirmar pedido
botonConfirmarPedido.addEventListener("click", async () => {

    // Evitamos enviar el pedido más de una vez
    botonConfirmarPedido.disabled = true;

    botonConfirmarPedido.textContent = "Procesando pedido...";

    // Creamos el objeto con los datos del pedido
    const pedido = {

        tamano: carritoTamano.textContent,

        ingredientes: seleccionados,

        total: seleccionados.reduce(
            (suma, ingrediente) => suma + ingrediente.precio,
            precioBase
        )

    };

    try {

        // Llamamos al servicio Dummy
        const respuesta = await crearPedidoDummy(pedido);

        // Mostramos el número generado por el servicio
        numeroPedido.textContent =
            `PEDIDO #FB-${respuesta.numero}`;

        // Copiamos los datos del carrito
        confirmacionTamano.textContent =
            carritoTamano.textContent;

        confirmacionTotal.textContent =
            formatearPrecio(pedido.total);

        // Mostramos los ingredientes
        confirmacionIngredientes.innerHTML = "";

        seleccionados.forEach(ingrediente => {

            const elemento = document.createElement("li");

            elemento.textContent = ingrediente.nombre;

            confirmacionIngredientes.appendChild(elemento);

        });

        // Mostramos la confirmación
        seccionCarrito.classList.remove("visible");

        seccionConfirmacion.classList.add("visible");

        seccionConfirmacion.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        console.error("Error al crear el pedido:", error);

        alert(
            "No se pudo registrar el pedido. Puedes intentarlo nuevamente."
        );

    } finally {

        // Restauramos el botón
        botonConfirmarPedido.disabled = false;

        botonConfirmarPedido.textContent =
            "Confirmar pedido →";

    }

});


    // Generamos un número de pedido ficticio
    const numero = Math.floor(1000 + Math.random() * 9000);

    numeroPedido.textContent = `PEDIDO #FB-${numero}`;

    // Copiamos el tamaño y precio del carrito
    confirmacionTamano.textContent =
        carritoTamano.textContent;

    confirmacionTotal.textContent =
        carritoTotal.textContent;

    // Mostramos los ingredientes
    confirmacionIngredientes.innerHTML = "";

    seleccionados.forEach(ingrediente => {

        const elemento = document.createElement("li");

        elemento.textContent = ingrediente.nombre;

        confirmacionIngredientes.appendChild(elemento);

    });

    // Cambiamos a la pantalla de confirmación
    seccionCarrito.classList.remove("visible");

    seccionConfirmacion.classList.add("visible");

    seccionConfirmacion.scrollIntoView({
        behavior: "smooth"
    });



// Volver al inicio
botonVolverInicio.addEventListener("click", () => {

    // Reiniciamos la selección
    seleccionados = [];
    precioBase = 5500;
    categoriaActual = "Todos";

    // Restauramos el tamaño normal
    document.querySelector(
        'input[name="tamano"][value="normal"]'
    ).checked = true;

    // Limpiamos la búsqueda
    buscador.value = "";

    // Restauramos la categoría activa
    botonesCategorias.forEach(boton => {
        boton.classList.toggle(
            "activa",
            boton.dataset.categoria === "Todos"
        );
    });

    actualizarSeleccion();
    mostrarIngredientes(ingredientes);

    // Ocultamos la confirmación
    seccionConfirmacion.classList.remove("visible");

    // Mostramos el inicio
    seccionInicio.style.display = "grid";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});

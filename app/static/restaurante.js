let carrito = {};

try {
    const carritoData = localStorage.getItem('carrito');
    if (carritoData) {
        carrito = JSON.parse(carritoData);
    }
} catch (error) {
    console.error("Error al cargar el carrito desde localStorage:", error);
}

const API_AGREGAR_AL_CARRITO = '/agregar_al_carrito';
const API_ELIMINAR_DEL_CARRITO = '/eliminar_del_carrito';
const API_OBTENER_PRODUCTOS_CARRITO = '/obtener_productos_carrito';

let listaProductos = null;
let totalPedido = null;

function agregarAlCarrito(claveProducto) {
    const cantidadInput = document.getElementById(`cantidad-${claveProducto}`);
    const cantidad = parseInt(cantidadInput.value, 10) || 1;

    if (cantidad <= 0) {
        alert("Por favor, ingrese una cantidad válida mayor a cero.");
        return;
    }

    fetch(API_AGREGAR_AL_CARRITO, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            clave_producto: claveProducto,
            cantidad: cantidad
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del servidor:", data);
        if (data.success) {
            alert("Producto agregado al carrito.");
            carrito = { ...carrito, ...data.productos };
            localStorage.setItem('carrito', JSON.stringify(carrito));
            actualizarCarrito();
        } else {
            alert("Error al agregar producto al carrito: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud AJAX:", error);
        alert("Error al agregar producto al carrito. Por favor, intente nuevamente.");
    });
}

function eliminarDelCarrito(claveProducto) {
    fetch(API_ELIMINAR_DEL_CARRITO, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            clave_producto: claveProducto
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Producto eliminado del carrito.");
            const li = document.getElementById(`producto-${claveProducto}`);
            if (li) {
                li.remove();
            }
            localStorage.setItem('carrito', JSON.stringify(data.productos));
            actualizarCarrito();
        } else {
            alert("Error al eliminar producto del carrito: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud AJAX:", error);
        alert("Error al eliminar producto del carrito. Por favor, intente nuevamente.");
    });
}

function actualizarCarrito() {
    const listaProductos = document.getElementById('lista-productos');
    const totalPedido = document.getElementById('total-pedido');

    if (!listaProductos || !totalPedido) {
        console.error("Error: No se encontraron los elementos del carrito.");
        return; 
    }

    listaProductos.innerHTML = '';

    fetch(API_OBTENER_PRODUCTOS_CARRITO)
        .then(response => response.json())
        .then(data => {
            console.log("Datos del carrito recibidos:", data);
            
            let total = 0;
            for (const producto of data.productos) {
                const subtotal = producto.precio * producto.cantidad;
                total += subtotal;

                const li = document.createElement('li');
                li.innerHTML = `
                    ${producto.nombre} x ${producto.cantidad} - $${subtotal.toFixed(2)}
                    <button onclick="eliminarDelCarrito('${producto.clave}', this)">Eliminar</button>
                `;
                listaProductos.appendChild(li);
            }

            totalPedido.textContent = total.toFixed(2);
        })
        .catch(error => {
            console.error('Error al obtener productos del carrito:', error);
            totalPedido.textContent = 'Error al cargar el carrito.';
        });
}

function confirmarPedido() {
    const nombre = document.getElementById('nombre').value;
    const direccion = document.getElementById('direccion').value;
    const telefono = document.getElementById('telefono').value;

    fetch('/confirmar_pedido', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cliente: {
                nombre: nombre,
                direccion: direccion,
                telefono: telefono
            },
            carrito: carrito
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Pedido confirmado correctamente.");
        } else {
            alert("Error al confirmar pedido: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud AJAX:", error);
        alert("Error al confirmar pedido. Por favor, intente nuevamente.");
    });
}




document.addEventListener('DOMContentLoaded', () => {
    listaProductos = document.getElementById('lista-productos');
    totalPedido = document.getElementById('total-pedido');

    if (window.location.pathname === '/finalizar_pedido') {
        actualizarCarrito();
    }
});

///////////////////////////////////////////////////////////////////

function agregarCliente() {
    const clave = document.getElementById('clave').value;
    const nombre = document.getElementById('nombre').value;
    const direccion = document.getElementById('direccion').value;
    const correo = document.getElementById('correo').value;
    const telefono = document.getElementById('telefono').value;


    fetch('/agregar_cliente', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            clave: clave,
            nombre: nombre,
            direccion: direccion,
            correo: correo,
            telefono: telefono
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cliente agregado correctamente.");
        } else {
            alert("Error al agregar cliente: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud AJAX:", error);
        alert("Error al agregar cliente. Por favor, intente nuevamente.");
    });
}

function actualizarCliente() {
    const clave = document.getElementById('clave').value;
    const nombre = document.getElementById('nombre').value;
    const direccion = document.getElementById('direccion').value;
    const correo = document.getElementById('correo').value;
    const telefono = document.getElementById('telefono').value;

    fetch('/actualizar_cliente', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            clave: clave,
            nombre: nombre,
            direccion: direccion,
            correo: correo,
            telefono: telefono
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cliente actualizado correctamente.");
        } else {
            alert("Error al actualizar cliente: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud AJAX:", error);
        alert("Error al actualizar cliente. Por favor, intente nuevamente.");
    });
}

function eliminarCliente() {
    const clave = document.getElementById('clave').value;

    fetch('/eliminar_cliente', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            clave: clave
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cliente eliminado correctamente.");
        } else {
            alert("Error al eliminar cliente: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud AJAX:", error);
        alert("Error al eliminar cliente. Por favor, intente nuevamente.");
    });
}

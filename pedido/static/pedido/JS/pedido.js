let productos = [];
let totalGeneral = 0;

// Mostrar formulario cuando se selecciona cliente
document.getElementById("clienteSelect").addEventListener("change", () => {
    const card = document.getElementById("productosCard");
    card.style.display = document.getElementById("clienteSelect").value ? "block" : "none";
});

function agregarProducto() {
    let nombre = document.getElementById("nombreProducto").value.trim();
    let cantidad = parseInt(document.getElementById("cantidadProducto").value);
    let precio = parseFloat(document.getElementById("precioProducto").value);

    if (!nombre || isNaN(cantidad) || cantidad <= 0 || isNaN(precio) || precio <= 0) {
        alert("Complete todos los campos correctamente.");
        return;
    }

    let subtotal = cantidad * precio;

    productos.push({ nombre, cantidad, precio, subtotal });

    actualizarTabla();
    limpiarInputs();
}

function limpiarInputs() {
    document.getElementById("nombreProducto").value = "";
    document.getElementById("cantidadProducto").value = "";
    document.getElementById("precioProducto").value = "";
}

function actualizarTabla() {
    let tabla = document.getElementById("listaProductos");
    tabla.innerHTML = "";

    totalGeneral = 0;

    productos.forEach((p, index) => {
        totalGeneral += p.subtotal;

        tabla.innerHTML += `
            <tr>
                <td>${p.nombre}</td>
                <td>${p.cantidad}</td>
                <td>$${p.precio.toFixed(2)}</td>
                <td>$${p.subtotal.toFixed(2)}</td>
                <td><span class='delete-btn' onclick="eliminarProducto(${index})">X</span></td>
            </tr>
        `;
    });

    document.getElementById("totalGeneral").innerText = totalGeneral.toFixed(2);
}

function eliminarProducto(index) {
    productos.splice(index, 1);
    actualizarTabla();
}

function guardarPedido() {
    let cliente_id = document.getElementById("clienteSelect").value;

    if (!cliente_id) {
        alert("Seleccione un cliente.");
        return;
    }

    if (productos.length === 0) {
        alert("Agregue al menos un producto.");
        return;
    }

    fetch(URL_GUARDAR, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            cliente_id,
            productos
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert("Pedido guardado correctamente.");

            // Reiniciar formulario
            productos = [];
            actualizarTabla();
            document.getElementById("clienteSelect").value = "";
            document.getElementById("productosCard").style.display = "none";

        } else {
            alert("Error: " + data.error);
        }
    });
}

function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(";");
    for (let c of cookies) {
        const cookie = c.trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length);
            break;
        }
    }
    return cookieValue;
}

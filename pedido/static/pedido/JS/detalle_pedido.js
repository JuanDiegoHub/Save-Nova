let contadorNuevo = 0
let temporizadores = {}

function agregarProducto(){

contadorNuevo++

let tabla = document.querySelector("#tablaProductos")

let fila = document.createElement("tr")

fila.classList.add("producto-nuevo")

fila.innerHTML = `
<td>
<input type="text" class="input-nombre">
</td>

<td>
<input type="number" class="input-cantidad" value="1" oninput="recalcularNuevo(${contadorNuevo})">
</td>

<td>
<input type="number" class="input-precio" value="0" oninput="recalcularNuevo(${contadorNuevo})">
</td>

<td class="subtotal" id="subtotal-nuevo-${contadorNuevo}">
$0
</td>

<td>
<button class="btn-eliminar" onclick="eliminarNuevoProducto(this)">
<i class="fa fa-trash"></i>
</button>
</td>
`

tabla.appendChild(fila)

}

function recalcular(id){

let fila = document.querySelector("#fila-"+id)

let cantidad = parseFloat(fila.querySelector(".input-cantidad").value) || 0
let precio = parseFloat(fila.querySelector(".input-precio").value) || 0

let subtotal = cantidad * precio

document.querySelector("#subtotal-"+id).innerText="$"+subtotal.toFixed(2)

recalcularTotal()

guardarAutomatico(id)

}

function recalcularNuevo(id){

let fila = document.querySelector("#subtotal-nuevo-"+id).closest("tr")

let cantidad = parseFloat(fila.querySelector(".input-cantidad").value) || 0
let precio = parseFloat(fila.querySelector(".input-precio").value) || 0

let subtotal = cantidad * precio

document.querySelector("#subtotal-nuevo-"+id).innerText="$"+subtotal.toFixed(2)

recalcularTotal()

}

function recalcularTotal(){

let subtotales = document.querySelectorAll(".subtotal")

let total = 0

subtotales.forEach(function(td){

let valor = td.innerText.replace("$","")

total += parseFloat(valor) || 0

})

document.querySelector("#totalPedido").innerText="$"+total.toFixed(2)

}

function guardarAutomatico(id){

clearTimeout(temporizadores[id])

temporizadores[id] = setTimeout(function(){

let fila = document.querySelector("#fila-"+id)

let nombre = fila.querySelector(".input-nombre").value
let cantidad = fila.querySelector(".input-cantidad").value
let precio = fila.querySelector(".input-precio").value

fetch(`/pedidos/editar-producto/${id}/`,{

method:"POST",

headers:{
"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
"Content-Type":"application/x-www-form-urlencoded"
},

body:`nombre=${nombre}&cantidad=${cantidad}&precio=${precio}`

})

.then(res=>res.json())

},1000)

}

function eliminarProducto(id){

let filas = document.querySelectorAll("#tablaProductos tr")

if(filas.length <= 1){
alert("El pedido debe tener al menos un producto.")
return
}

if(!confirm("¿Eliminar producto?")) return

fetch(`/pedidos/eliminar-producto/${id}/`,{

method:"POST",

headers:{
"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
}

})

.then(res=>res.json())
.then(data=>{

document.querySelector("#fila-"+id).remove()

recalcularTotal()

})

}

function eliminarNuevoProducto(btn){

let filas = document.querySelectorAll("#tablaProductos tr")

if(filas.length <= 1){
alert("El pedido debe tener al menos un producto.")
return
}

btn.closest("tr").remove()

recalcularTotal()

}

function guardarPedido(){

let nuevos = document.querySelectorAll(".producto-nuevo")

let productos = []

nuevos.forEach(function(fila){

let nombre = fila.querySelector(".input-nombre").value.trim()
let cantidad = fila.querySelector(".input-cantidad").value
let precio = fila.querySelector(".input-precio").value

if(nombre !== "" && precio > 0){

productos.push({
nombre:nombre,
cantidad:cantidad,
precio:precio
})

}

})

fetch(`/pedidos/agregar-productos/${pedidoId}/`,{

method:"POST",

headers:{
"X-CSRFToken": csrfToken,
"Content-Type":"application/json"
},

body: JSON.stringify({
productos:productos
})

})

.then(res=>res.json())
.then(data=>{

window.location.href="/menu/"

})

}

function cancelarPedido(id){

if(!confirm("¿Seguro que deseas cancelar este pedido?")) return

fetch(`/pedidos/cancelar-pedido/${id}/`,{

method:"POST",

headers:{
"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
}

})

.then(res=>res.json())
.then(data=>{

window.location.href="/menu/"

})

}
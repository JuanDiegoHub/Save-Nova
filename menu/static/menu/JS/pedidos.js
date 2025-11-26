function mostrarAbono(id) {
    const form = document.getElementById(`abonoForm-${id}`);
    form.style.display = form.style.display === "none" ? "block" : "none";
}

function pagarPedido(id) {
    if (confirm("¿Deseas pagar toda la deuda?")) {
        window.location.href = `/pedidos/pagar/${id}/`;
    }
}

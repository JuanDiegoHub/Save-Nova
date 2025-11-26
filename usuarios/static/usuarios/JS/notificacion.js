function mostrarToast(texto, tipo = "success") {
    const contenedor = document.getElementById("toast-container");
    if (!contenedor) return;

    const div = document.createElement("div");
    div.classList.add("toast", tipo);
    div.innerText = texto;

    contenedor.appendChild(div);

    setTimeout(() => {
        div.remove();
    }, 1500);
}

function mostrarMensajesDjango(listaMensajes) {
    listaMensajes.forEach(msg => {
        mostrarToast(msg.texto, msg.tipo);
    });
}

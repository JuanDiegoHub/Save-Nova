// busqueda.js
document.addEventListener("DOMContentLoaded", function() {
  const input = document.getElementById("busqueda");
  if (!input) return;

  input.addEventListener("input", function() {
    const filtro = input.value.toLowerCase();
    const pedidos = document.querySelectorAll(".pedido-card");

    pedidos.forEach(pedido => {
      const nombre = pedido.querySelector(".pedido-cliente").textContent.toLowerCase();
      if (nombre.includes(filtro)) {
        pedido.style.display = "block";
      } else {
        pedido.style.display = "none";
      }
    });
  });
});

// ----------------------
// Toggle del menú lateral
// ----------------------

document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.querySelector(".menu-toggle");
    const sidebar = document.querySelector(".dashboard-nav");

    if (menuToggle) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("active");
        });
    }

    // ----------------------
    // Dropdowns del menú
    // ----------------------

    const dropdowns = document.querySelectorAll(".dashboard-nav-dropdown-toggle");

    dropdowns.forEach(drop => {
        drop.addEventListener("click", () => {
            const parent = drop.parentElement;
            parent.classList.toggle("show");

            const menu = parent.querySelector(".dashboard-nav-dropdown-menu");
            if (menu) {
                menu.style.display = menu.style.display === "block" ? "none" : "block";
            }
        });
    });

    // ----------------------
    // Cerrar menú si se hace clic fuera (solo en móvil)
    // ----------------------

    document.addEventListener("click", (e) => {
        if (window.innerWidth <= 900) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove("active");
            }
        }
    });
});

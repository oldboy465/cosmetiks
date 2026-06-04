document.addEventListener("DOMContentLoaded", function () {
    const toasts = document.querySelectorAll(".alert-toast");
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.animation = "slideIn 0.3s ease reverse forwards";
            setTimeout(() => { toast.remove(); }, 300);
        }, 4000);

        const closeBtn = toast.querySelector(".close-toast");
        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                toast.remove();
            });
        }
    });

    const activeUrl = window.location.pathname;
    const menuItems = document.querySelectorAll(".sidebar .menu-item");
    menuItems.forEach(item => {
        if (activeUrl.includes(item.getAttribute("href"))) {
            item.classList.add("active");
        }
    });
});

function toggleSidebar() {
    const sidebar = document.querySelector(".sidebar");
    if (sidebar) {
        sidebar.classList.toggle("open");
    }
}
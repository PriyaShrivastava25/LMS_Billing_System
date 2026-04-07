document.addEventListener("DOMContentLoaded", function() {
    console.log("Student Dashboard Loaded");

    const rows = document.querySelectorAll("table tr");

    rows.forEach(row => {
        row.addEventListener("mouseenter", () => {
            row.style.transform = "scale(1.01)";
            row.style.transition = "0.2s";
        });

        row.addEventListener("mouseleave", () => {
            row.style.transform = "scale(1)";
        });
    });
});

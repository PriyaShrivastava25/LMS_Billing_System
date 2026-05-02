document.addEventListener("DOMContentLoaded", function () {

    setTimeout(() => {
        document.querySelectorAll(".popup-message").forEach(msg => {
            msg.style.display = "none";
        });
    }, 3000);

    document.querySelectorAll(".pay-btn").forEach(btn => {
        btn.addEventListener("click", function () {


            btn.classList.add("disabled");
            btn.innerText = "Processing...";

        });
    });

});

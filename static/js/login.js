
function togglePassword() {
    const passwordField = document.getElementById("password");

    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}


document.getElementById("loginForm").addEventListener("submit", function(e) {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (email === "" || password === "") {
        e.preventDefault();
        alert("All fields are required!");
    }
});

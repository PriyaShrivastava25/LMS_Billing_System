const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const passwordStrength = document.getElementById("passwordStrength");
const passwordMatch = document.getElementById("passwordMatch");
const form = document.getElementById("signupForm");

// Password Strength Checker
password.addEventListener("keyup", function () {
    const value = password.value;

    if (value.length < 6) {
        passwordStrength.textContent = "Weak password";
        passwordStrength.style.color = "red";
    } 
    else if (value.match(/[A-Z]/) && value.match(/[0-9]/)) {
        passwordStrength.textContent = "Strong password";
        passwordStrength.style.color = "green";
    } 
    else {
        passwordStrength.textContent = "Medium strength";
        passwordStrength.style.color = "orange";
    }
});

// Password Match Checker
confirmPassword.addEventListener("keyup", function () {
    if (password.value === confirmPassword.value) {
        passwordMatch.textContent = "Passwords match";
        passwordMatch.style.color = "green";
    } else {
        passwordMatch.textContent = "Passwords do not match";
        passwordMatch.style.color = "red";
    }
});


form.addEventListener("submit", function (e) {
    if (password.value !== confirmPassword.value) {
        e.preventDefault();
        alert("Passwords do not match!");
    }
});


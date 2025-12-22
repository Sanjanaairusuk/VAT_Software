// Get form elements
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const formTitle = document.getElementById("formTitle");

// Get navbar/tab links
const navSignIn = document.getElementById("navSignIn");
const navRegister = document.getElementById("navRegister");
const goRegister = document.getElementById("goRegister");
const goLogin = document.getElementById("goLogin");

// Functions to switch tabs
function showLogin() {
  loginForm.classList.remove("hidden");
  registerForm.classList.add("hidden");
  formTitle.innerText = "Sign in";
}

function showRegister() {
  registerForm.classList.remove("hidden");
  loginForm.classList.add("hidden");
  formTitle.innerText = "Create an account";
}

// Add click event listeners
navSignIn.onclick = showLogin;
navRegister.onclick = showRegister;
goRegister.onclick = showRegister;
goLogin.onclick = showLogin;

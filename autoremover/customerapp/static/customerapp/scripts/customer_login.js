var loginContainer = document.getElementById("login-form-container");
var signupContainer = document.getElementById("signup-form-container");

function openSignup(event) {
  event.preventDefault();
  loginContainer.style.display = "none";
  signupContainer.style.display = "block";
}

function openLogin(event) {
  event.preventDefault();
  loginContainer.style.display = "block";
  signupContainer.style.display = "none";
}

document
  .getElementById("open-signup-form-button")
  .addEventListener("click", openSignup);

document
  .getElementById("open-login-form-button")
  .addEventListener("click", openLogin);

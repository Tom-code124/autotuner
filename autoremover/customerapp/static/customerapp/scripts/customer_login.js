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

var passInput = document.getElementById("password-input");
var confirmPassInput = document.getElementById("password-confirm-input");
var submitSignupButton = document.getElementById("submit-signup-button");
var passMismatchSpan = document.getElementById("pass-mismatch-span");

function checkPasswordMatch() {
  if (passInput.value == confirmPassInput.value) {
    submitSignupButton.disabled = false;
    passMismatchSpan.style.display = "none";
    return true;
  }

  submitSignupButton.disabled = true;
  passMismatchSpan.style.display = "block";
  return false;
}

passInput.addEventListener("change", checkPasswordMatch);
confirmPassInput.addEventListener("change", checkPasswordMatch);

// Initialization for ES Users
import { Input, Ripple, initTE } from "tw-elements";

initTE({ Input, Ripple });

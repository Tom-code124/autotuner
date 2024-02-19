import { getAndInject } from "./modals.js";
import { afterInjection } from "./pricing_modal.js";

function viewButtonClick(event) {
  getAndInject("pricing_modal/", undefined, undefined, afterInjection);
}

document
  .getElementById("view-pricing-button")
  .addEventListener("click", viewButtonClick);

console.log(window.matchMedia("(prefers-color-scheme: dark)"));
console.log(window.matchMedia("(prefers-color-scheme: dark)").matches);

console.log(document.documentElement.classList.add("dark"));
console.log(document.documentElement.classList);

import { turnOnModal, injectModal } from "./modals.js";

function viewButtonClick(event) {
  injectModal("pricing_modal/");
  turnOnModal();
}

document
  .getElementById("view-pricing-button")
  .addEventListener("click", viewButtonClick);

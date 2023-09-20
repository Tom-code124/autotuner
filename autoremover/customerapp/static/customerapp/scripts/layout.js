import { turnOnModal, injectModal } from "./modals.js";

function winolsClick() {
  injectModal("winols_modal/");
  turnOnModal();
}

document
  .getElementById("winols-sidebar-icon")
  .addEventListener("click", winolsClick);

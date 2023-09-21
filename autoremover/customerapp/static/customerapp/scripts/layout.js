import { turnOnModal, getAndInject } from "./modals.js";

function winolsClick() {
  getAndInject(window.location.origin + "/app/winols_modal/");
  turnOnModal();
}

document
  .getElementById("winols-sidebar-icon")
  .addEventListener("click", winolsClick);

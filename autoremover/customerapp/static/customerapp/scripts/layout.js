import { turnOnModal, getAndInject } from "./modals.js";

function winolsClick() {
  getAndInject(
    window.location.origin + "/app/winols_modal/",
    undefined,
    undefined,
    turnOnModal
  );
  turnOnModal();
}

document
  .getElementById("winols-sidebar-icon")
  .addEventListener("click", winolsClick);

import { turnOnModal, turnOffModal } from "./modals.js";

winols_icon = document.getElementById("winols-sidebar-icon");

winols_icon.addEventListener("click", turnOnModal);

document
  .getElementById("modal-background")
  .addEventListener("click", turnOffModal);

document.getElementById("modal-close").addEventListener("click", turnOffModal);

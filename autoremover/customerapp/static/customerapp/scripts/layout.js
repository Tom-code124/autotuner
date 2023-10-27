import { turnOnModal, turnOffModal, getAndInject } from "./modals.js";

function winolsClick() {
  getAndInject(
    window.location.origin + "/app/winols_modal/",
    undefined,
    undefined,
    turnOnModal
  );
}

document
  .getElementById("winols-sidebar-icon")
  .addEventListener("click", winolsClick);

function profileClick() {
  turnOnModal();
  document.getElementById("profile-card").classList.add("on-screen");

  document
    .getElementById("modal-background")
    .addEventListener("click", turnOffModal);
}

// document
//   .getElementById("profile-anchor")
//   .addEventListener("click", profileClick);

var profileModals = [...document.querySelectorAll(".modal")];

function openProfileModal(event) {
  var modalId = event.currentTarget.id + "-modal";

  profileModals.map((item) => {
    if (item.id != modalId) {
      item.style.display = "none";
    } else {
      item.style.display = "block";
    }
  });
}

var profileOpeners = [...document.querySelectorAll(".opener")];

profileOpeners.map((item) => {
  item.addEventListener("click", openProfileModal);
});

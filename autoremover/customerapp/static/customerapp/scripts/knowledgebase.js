import { turnOnModal, injectModal } from "./modals.js";

function viewButtonClick(event) {
  injectModal("knowledge_modal?id=" + event.target.id);
  turnOnModal();
}

[...document.querySelectorAll(".knowledge-button")].map((item) => {
  item.addEventListener("click", viewButtonClick);
});

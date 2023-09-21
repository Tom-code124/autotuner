import { turnOnModal, getAndInject } from "./modals.js";

function viewButtonClick(event) {
  getAndInject("knowledge_modal?id=" + event.target.id);
  turnOnModal();
}

[...document.querySelectorAll(".knowledge-button")].map((item) => {
  item.addEventListener("click", viewButtonClick);
});

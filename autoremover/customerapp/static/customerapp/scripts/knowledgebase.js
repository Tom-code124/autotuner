import { turnOnModal, getAndInject } from "./modals.js";

function viewButtonClick(event) {
  getAndInject(
    "knowledge_modal?id=" + event.target.id,
    undefined,
    undefined,
    turnOnModal
  );
}

[...document.querySelectorAll(".knowledge-button")].map((item) => {
  item.addEventListener("click", viewButtonClick);
});

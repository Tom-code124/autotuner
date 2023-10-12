import { turnOnModal, getAndInject } from "./modals.js";

function viewButtonClick(event) {
  var id = event.target.id.substring(event.target.id.lastIndexOf("-") + 1);
  getAndInject("knowledge_modal?id=" + id, undefined, undefined, turnOnModal);
}

[...document.querySelectorAll(".knowledge-button")].map((item) => {
  item.addEventListener("click", viewButtonClick);
});

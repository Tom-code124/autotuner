import { getAndInject, turnOnModal } from "./modals.js";

function categoryChange(event) {
  getAndInject(
    "price_options_modal?category=" + event.target.value,
    "options-container"
  );
}

function afterInjection() {
  document
    .getElementById("category-select")
    .addEventListener("change", categoryChange);

  turnOnModal();
}

export { afterInjection };

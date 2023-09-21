import { getAndInject, turnOnModal } from "./modals.js";

function categoryChange(event) {
  getAndInject(
    "price_options_modal?category=" + event.target.value,
    "price-options-form"
  );
}

function afterInjection() {
  document
    .getElementById("category-select")
    .addEventListener("change", categoryChange);

  turnOnModal();
}

export { afterInjection };

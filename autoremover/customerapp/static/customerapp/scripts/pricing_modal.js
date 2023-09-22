import { getAndInject, turnOnModal } from "./modals.js";
import { openCalculator } from "./price_options.js";

function categoryChange(event) {
  getAndInject(
    "price_options_modal?category=" + event.target.value,
    "price-options-form",
    undefined,
    openCalculator
  );
}

function afterInjection() {
  document
    .getElementById("category-select")
    .addEventListener("change", categoryChange);

  document.getElementById("calculator-box").style.display = "none";

  turnOnModal();
}

export { afterInjection };

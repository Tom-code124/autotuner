import { getAndInject } from "./modals.js";
import { afterFunc } from "./expenses_modal.js";

getAndInject("expenses_modal", "card-body", undefined, afterFunc);

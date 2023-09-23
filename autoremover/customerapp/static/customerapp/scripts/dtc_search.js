import { getAndInject } from "./modals.js";
import { afterFunc } from "./dtc_search_modal.js";

getAndInject("dtc_search_modal", "card-body", undefined, afterFunc);

var searchInput = document.getElementById("search-input");
var searchButton = document.getElementById("search-button");

function search(event) {
  event.preventDefault();
  var keyword = searchInput.value;

  if (keyword.trim().length != 0) {
    getAndInject(
      "dtc_search_modal?keyword=" + encodeURIComponent(keyword),
      "card-body",
      undefined,
      afterFunc
    );
  }
}

searchButton.addEventListener("click", search);

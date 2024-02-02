import { getAndInject } from "./modals.js";
import { afterFunc } from "./shop_modal.js";

getAndInject("get_products", "card-body", undefined, afterFunc);

var searchInput = document.getElementById("search-input");
var searchButton = document.getElementById("search-button");

function search(event) {
  event.preventDefault();
  var keyword = searchInput.value;

  var url = "get_products";

  if (keyword.trim().length != 0) {
    url += "?keyword=" + encodeURIComponent(keyword);
  }

  getAndInject(url, "card-body", undefined, afterFunc);
}

searchButton.addEventListener("click", search);

import { getAndInject } from "./modals.js";
import { afterFuncEmpty, afterFuncPagination } from "./bosch_modal.js";

getAndInject("bosch_modal", "card-body", undefined, afterFuncEmpty);

var searchInputHeader = document.getElementById("bosch-search-input");
var searchButton = document.getElementById("bosch-search-button");

function search(event) {
  event.preventDefault();
  var keyword = searchInputHeader.value;

  var url = "bosch_modal";

  var isEmptyKeyword = keyword.trim().length === 0;

  if (!isEmptyKeyword) {
    url += "?keyword=" + encodeURIComponent(keyword);
  }

  if (isEmptyKeyword) {
    getAndInject(url, "card-body", undefined, afterFuncEmpty);
  } else {
    getAndInject(url, "card-body", undefined, afterFuncPagination);
  }
}

searchButton.addEventListener("click", search);

export { search };

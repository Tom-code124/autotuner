import { search } from "./bosch_search.js";
import { getAndInject } from "./modals.js";

var searchInputHeader = document.getElementById("bosch-search-input");

function balance(event) {
  var searchInputBody = document.getElementById("bosch-search-input-2");
  var inputToChange =
    event.currentTarget.id == "bosch-search-input"
      ? searchInputBody
      : searchInputHeader;

  inputToChange.value = event.currentTarget.value;
}

function afterFuncEmpty() {
  var searchInputBody = document.getElementById("bosch-search-input-2");

  searchInputBody.addEventListener("input", balance);
  searchInputHeader.addEventListener("input", balance);

  var searchButtonBody = document.getElementById("bosch-search-button-2");
  searchButtonBody.addEventListener("click", search);
}

function loadPagination(event) {
  var currentPage = Number(
    document.getElementById("current-page-button").innerText
  );
  var page = Number(event.currentTarget.innerText);

  if (event.currentTarget.id == "previous-page-button") {
    page = currentPage - 1;
  } else if (event.currentTarget.id == "following-page-button") {
    page = currentPage + 1;
  }

  if (page != currentPage) {
    var keyword = searchInputHeader.value;
    var url = "bosch_modal?page=" + page;

    var isEmptyKeyword = keyword.trim().length === 0;

    if (!isEmptyKeyword) {
      url += "&keyword=" + encodeURIComponent(keyword);
    }

    if (isEmptyKeyword) {
      getAndInject(url, "card-body", undefined, afterFuncEmpty);
    } else {
      getAndInject(url, "card-body", undefined, afterFuncPagination);
    }
  }
}

function afterFuncPagination() {
  var paginationButtons = [...document.querySelectorAll(".pagination-button")];
  paginationButtons.map((item) => {
    item.addEventListener("click", loadPagination);
  });
  searchInputHeader.removeEventListener("input", balance);
}

export { afterFuncEmpty, afterFuncPagination };

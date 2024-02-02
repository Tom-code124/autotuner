import { getAndInject } from "./modals.js";

var searchInput = document.getElementById("search-input");

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
    var keyword = searchInput.value;
    var url = "dtc_search_modal?page=" + page;

    if (keyword.trim().length != 0) {
      url += "&keyword=" + encodeURIComponent(keyword);
    }

    getAndInject(url, "card-body", undefined, afterFunc);
  }
}

function afterFunc() {
  var paginationButtons = [...document.querySelectorAll(".pagination-button")];
  paginationButtons.map((item) => {
    item.addEventListener("click", loadPagination);
  });
}

export { afterFunc };

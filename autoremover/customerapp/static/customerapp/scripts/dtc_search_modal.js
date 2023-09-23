import { getAndInject } from "./modals.js";

var searchInput = document.getElementById("search-input");

function loadPagination(event) {
  var currentPage = Number(
    document.getElementById("current-page-button").innerText
  );
  var keyword = searchInput.value;
  var page = Number(event.target.innerText);

  if (event.target.id == "previous-page-button") {
    page = currentPage - 1;
  } else if (event.target.id == "following-page-button") {
    page = currentPage + 1;
  }

  if (page != currentPage) {
    getAndInject(
      "dtc_search_modal?keyword=" +
        encodeURIComponent(keyword) +
        "&page=" +
        page,
      "card-body",
      undefined,
      afterFunc
    );
  }
}

function afterFunc() {
  var paginationButtons = [...document.querySelectorAll(".pagination-button")];
  paginationButtons.map((item) => {
    item.addEventListener("click", loadPagination);
  });
}

export { afterFunc };

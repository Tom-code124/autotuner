import { getAndInject } from "./modals.js";

// var searchInput = document.getElementById("req-files-search-input");

function loadPagination(event) {
  var currentPage = Number(
    document.getElementById("current-page-button-2").innerText
  );
  var page = Number(event.currentTarget.innerText);

  if (event.currentTarget.id == "previous-page-button-2") {
    page = currentPage - 1;
  } else if (event.currentTarget.id == "following-page-button-2") {
    page = currentPage + 1;
  }

  if (page != currentPage) {
    // var keyword = searchInput.value;
    var url = "bought_files?page=" + page;

    /* if (keyword.trim().length != 0) {
      url += "&keyword=" + encodeURIComponent(keyword);
    } */

    getAndInject(url, "bought-files-page", undefined, afterFuncBought);
  }
}

function afterFuncBought() {
  var paginationButtons = [...document.querySelectorAll(".pagination-button-2")];
  paginationButtons.map((item) => {
    item.addEventListener("click", loadPagination);
  });
}

export { afterFuncBought };

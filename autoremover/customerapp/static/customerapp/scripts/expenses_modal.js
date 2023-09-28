import { getAndInject } from "./modals.js";

function loadPagination(event) {
  var currentPage = Number(
    document.getElementById("current-page-button").innerText
  );
  var page = Number(event.target.innerText);

  if (event.target.id == "previous-page-button") {
    page = currentPage - 1;
  } else if (event.target.id == "following-page-button") {
    page = currentPage + 1;
  }

  if (page != currentPage) {
    var url = "expenses_modal?page=" + page;

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

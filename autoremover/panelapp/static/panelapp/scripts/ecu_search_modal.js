import { getAndInject } from "./modals.js";

var ecuTypeSearchInput = document.getElementById("ecu-type-search-input");
var ecuPaginationDiv = document.getElementById("ecu-pagination-div");

function loadPaginationEcu(event) {
  var ecuTypeSearchInput = document.getElementById("ecu-type-search-input");
  var ecuPaginationDiv = document.getElementById("ecu-pagination-div");
  var currentPage = Number(
    ecuPaginationDiv.querySelector("#current-page-button").innerText
  );
  var page = Number(event.currentTarget.innerText);

  if (event.currentTarget.id == "previous-page-button") {
    page = currentPage - 1;
  } else if (event.currentTarget.id == "following-page-button") {
    page = currentPage + 1;
  }

  if (page != currentPage) {
    var keyword = ecuTypeSearchInput.value;
    var url = "ecu_type_search?ecu_type_page=" + page;

    keyword = keyword.trim();
    if (keyword.length != 0) {
      url += "&ecu_type_keyword=" + encodeURIComponent(keyword);
    } else {
      url += "&ecu_type_keyword= ";
    }

    getAndInject(url, "ecu-list-table", undefined, afterFuncEcu);
  }
}

function afterFuncEcu() {
  var ecuTypeSearchInput = document.getElementById("ecu-type-search-input");
  var ecuPaginationDiv = document.getElementById("ecu-pagination-div");
  var paginationButtons = [
    ...ecuPaginationDiv.querySelectorAll(".pagination-button"),
  ];
  paginationButtons.map((item) => {
    item.addEventListener("click", loadPaginationEcu);
  });
}

export { afterFuncEcu };

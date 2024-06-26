import { getAndInject } from "./modals.js";

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
    var url = "file_requests_modal?page=" + page;

    getAndInject(url, "card-body", undefined, afterFunc);
  }
}

function afterFunc() {
  var paginationButtons = [...document.querySelectorAll(".pagination-button")];
  paginationButtons.map((item) => {
    item.addEventListener("click", loadPagination);
  });

  document.querySelectorAll(".file-request-row").forEach((item) => {
    item.addEventListener("click", openRequestModal);
  });
}

function openRequestModal(event) {
  var modalH3 = document.getElementById("modal-h3");
  var id = event.currentTarget.id.substring(
    0,
    event.currentTarget.id.lastIndexOf("-") + 1
  );
  console.log("clicked file request");

  modalH3.innerText = "Request " + id;
  $("#crud-modal").modal("show");
}

getAndInject("file_requests_modal", "card-body", undefined, afterFunc);

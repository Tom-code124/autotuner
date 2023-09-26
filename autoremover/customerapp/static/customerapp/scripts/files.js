import { getAndInject } from "./modals.js";
import { afterFunc } from "./requested_files_modal.js";

getAndInject("requested_files", "page-content", undefined, afterFunc);

var searchInput = document.getElementById("req-files-search-input");
var searchButton = document.getElementById("req-files-search-button");

function search(event) {
  event.preventDefault();
  var keyword = searchInput.value;

  var url = "requested_files";

  if (keyword.trim().length != 0) {
    url += "?keyword=" + encodeURIComponent(keyword);
  }

  getAndInject(url, "page-content", undefined, afterFunc);
}

searchButton.addEventListener("click", search);

import { getAndInject } from "./modals.js";
import { afterFuncEcu } from "./ecu_search_modal.js";

var fields = document
  .getElementById("vehicle-select-section")
  .querySelectorAll("select, input");

function loadNext(event) {
  var nextIndex = parseInt(
    event.currentTarget.id.substring(
      event.currentTarget.id.lastIndexOf("-") + 1
    )
  );

  var nextId = fields[nextIndex].id;
  var modelFields = {};

  for (let i = 0; i < nextIndex; i++) {
    modelFields[fields[i].name] = fields[i].value;
  }

  var nextName = fields[nextIndex].name;
  var url = "/app/upload/get_vehicle?requested=" + nextName;
  Object.keys(modelFields).forEach((key) => {
    url += "&" + key + "=" + modelFields[key];
  });

  getAndInject(url, nextId, undefined, undefined);
  document.getElementById(nextId).disabled = false;

  for (let i = nextIndex + 1; i < 5; i++) {
    fields[i].value = null;
    fields[i].disabled = true;
  }
}

for (let i = 0; i < 4; i++) {
  fields[i].addEventListener("change", loadNext);
}

function showSelectedVersion(event) {
  var versionDiv = document.getElementById("selected-vehicle-version-div");
  if (event.currentTarget.value != null) {
    var selectedVersionId = document.getElementById(
      "vehicle-version-select-5"
    ).value;
    var selectedVersion;
    var versionB = document.getElementById("selected-vehicle-version");
    event.currentTarget.querySelectorAll("option").forEach((option) => {
      if (option.value == selectedVersionId) {
        selectedVersion = option.innerHTML;
      }
    });
    versionB.innerHTML = selectedVersion;

    versionDiv.classList.remove("hidden");
  } else {
    versionDiv.classList.add("hidden");
  }
}

fields[4].addEventListener("change", showSelectedVersion);

var ecuTypeSearchInput = document.getElementById("ecu-type-search-input");
var ecuTypeSearchButton = document.getElementById("ecu-type-search-button");

function search(event) {
  var keyword = ecuTypeSearchInput.value;
  var url = "ecu_type_search";

  keyword = keyword.trim();
  if (keyword.length != 0) {
    url += "?ecu_type_keyword=" + encodeURIComponent(keyword);
  } else {
    url += "?ecu_type_keyword= ";
  }

  getAndInject(url, "ecu-list-table", undefined, afterFuncEcu);
}

ecuTypeSearchButton.addEventListener("click", search);
ecuTypeSearchInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    search(e);
  }
});

afterFuncEcu();

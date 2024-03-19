import { getAndInject } from "./modals.js";

var fields = document
  .getElementById("vehicle-select-section")
  .querySelectorAll("select, input");

function loadNext(event) {
  var nextIndex = parseInt(
    event.currentTarget.id.substring(
      event.currentTarget.id.lastIndexOf("-") + 1
    )
  );

  for (let i = nextIndex; i < 5; i++) {
    fields[i].value = null;
    fields[i].disabled = true;
  }

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

var selectedEcu = [];
function listSelectedEcu(event) {
  var ecuTypeId = event.currentTarget.id.substring(
    event.currentTarget.id.lastIndexOf("-") + 1
  );

  var ecuNameId = "ecu-name-td-" + ecuTypeId;
  var ecuName = document.getElementById(ecuNameId).innerText;
  var ecuBrandId = "ecu-brand-td-" + ecuTypeId;
  var ecuBrand = document.getElementById(ecuBrandId).innerText;
  var ecuObject = {
    id: ecuTypeId,
    name: ecuName + " (" + ecuBrand + ")",
  };
  if (event.currentTarget.checked) {
    selectedEcu.push(ecuObject);
  } else {
    var index = 0;
    for (let i = 0; i < selectedEcu.length; i++) {
      if (selectedEcu[i].id == ecuObject.id) {
        index = i;
        break;
      }
    }
    selectedEcu.splice(index, 1);
  }

  var ecuLis = "";
  selectedEcu.forEach((ecu) => {
    ecuLis += "<li><b>" + ecu.name + "</b></li>\n";
  });

  if (ecuLis.length != 0) {
    document.getElementById("selected-ecu-types").innerHTML = ecuLis;
    document.getElementById("selected-ecu-type-div").classList.remove("hidden");
  } else {
    document.getElementById("selected-ecu-type-div").classList.add("hidden");
  }
}

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
  var ecuPaginationDiv = document.getElementById("ecu-pagination-div");
  var paginationButtons = [
    ...ecuPaginationDiv.querySelectorAll(".pagination-button"),
  ];
  paginationButtons.map((item) => {
    item.addEventListener("click", loadPaginationEcu);
  });

  document.querySelectorAll(".ecu-type-checkbox").forEach((checkbox) => {
    if (selectedEcu != undefined) {
      selectedEcu.forEach((ecu) => {
        if (ecu.id == checkbox.value) {
          checkbox.checked = true;
        }
      });
    }
    checkbox.addEventListener("change", listSelectedEcu);
  });
}

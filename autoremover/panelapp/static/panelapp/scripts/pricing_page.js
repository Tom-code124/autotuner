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
  if (nextIndex != 4) {
    document.getElementById("filter-version-button").disabled = true;
    var versionDiv = document.getElementById("selected-vehicle-version-div");
    versionDiv.classList.add("hidden");
  }
}

for (let i = 0; i < 4; i++) {
  fields[i].addEventListener("change", loadNext);
}

function showSelectedVersion(event) {
  var versionDiv = document.getElementById("selected-vehicle-version-div");
  if (event.currentTarget.value != "null") {
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
    document.getElementById("filter-version-button").disabled = false;
  } else {
    versionDiv.classList.add("hidden");
    document.getElementById("filter-version-button").disabled = true;
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

  if (selectedEcu != undefined && selectedEcu.length > 0) {
    document.getElementById("filter-ecu-button").disabled = false;
  } else {
    document.getElementById("filter-ecu-button").disabled = true;
  }
}

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

  checkAppliedEcuCheckbox();
}

var versionFilters = [];
var ecuFilters = [];
function checkFiltersVisibility() {
  var hasAnyVersion = versionFilters != undefined && versionFilters.length > 0;
  var hasAnyEcu = ecuFilters != undefined && ecuFilters.length > 0;

  if (hasAnyVersion) {
    document
      .getElementById("no-version-filters-warning-p")
      .classList.add("hidden");
    document
      .getElementById("selected-versions-list-ul")
      .classList.remove("hidden");
  } else {
    document
      .getElementById("no-version-filters-warning-p")
      .classList.remove("hidden");
    document
      .getElementById("selected-versions-list-ul")
      .classList.add("hidden");
  }

  if (hasAnyEcu) {
    document.getElementById("no-ecu-filters-warning-p").classList.add("hidden");
    document
      .getElementById("selected-ecu-types-list-ul")
      .classList.remove("hidden");
  } else {
    document
      .getElementById("no-ecu-filters-warning-p")
      .classList.remove("hidden");
    document
      .getElementById("selected-ecu-types-list-ul")
      .classList.add("hidden");
  }
}

function applyVersionFilter(event) {
  var version_select = document.getElementById("vehicle-version-select-5");
  var version_id = version_select.value;

  var alreadySelected = false;
  if (versionFilters != undefined) {
    versionFilters.forEach((filter) => {
      if (filter.id == version_id) {
        alreadySelected = true;
      }
    });
  }

  if (!alreadySelected) {
    var version_name = version_select
      .querySelector("option[value='" + version_id + "']")
      .innerText.trim();
    versionFilters.push({
      id: version_id,
      name: version_name,
    });
    document.getElementById("selected-versions-list-ul").insertAdjacentHTML(
      "beforeend",
      `<li id="version-remove-li-${version_id}"  class="flex flex-row items-center mt-1"> <button
        id="version-remove-${version_id}"
        type="button"
        class="version-filter-remove-button w-5 h-5 pt-1 pl-1.5 text-white bg-red-700 hover:bg-red-800 font-medium rounded-lg text-sm text-center inline-flex items-center dark:bg-red-600 dark:hover:bg-red-800">
        <svg
          fill="#ffffff"
          version="1.1"
          id="Capa_1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 800 800"
          xml:space="preserve"
          stroke="#ffffff"
          class="w-3 h-3">
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g
            id="SVGRepo_tracerCarrier"
            stroke-linecap="round"
            stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <g>
              <g>
                <path d="M491.613,75.643l-64.235-64.235c-15.202-15.202-39.854-15.202-55.056,0L251.507,132.222L130.686,11.407 c-15.202-15.202-39.853-15.202-55.055,0L11.401,75.643c-15.202,15.202-15.202,39.854,0,55.056l120.821,120.815L11.401,372.328 c-15.202,15.202-15.202,39.854,0,55.056l64.235,64.229c15.202,15.202,39.854,15.202,55.056,0l120.815-120.814l120.822,120.814 c15.202,15.202,39.854,15.202,55.056,0l64.235-64.229c15.202-15.202,15.202-39.854,0-55.056L370.793,251.514l120.82-120.815 C506.815,115.49,506.815,90.845,491.613,75.643z"></path>
              </g>
            </g>
          </g>
        </svg>
      </button><span class="ml-1 text-sm">${version_name}</span></li>`
    );

    var versionFormDiv = document.getElementById("vehicle-versions-form-div");
    versionFormDiv.insertAdjacentHTML(
      "beforeend",
      '<input type="checkbox" id="version-filter-input-' +
        version_id +
        '" value="' +
        version_id +
        '" class="hidden" name="version_filter" />'
    );
  }

  checkFiltersVisibility();

  addRemoveListener();

  // update vehicle table here
}
document
  .getElementById("filter-version-button")
  .addEventListener("click", applyVersionFilter);

function applyEcuFilter(event) {
  if (selectedEcu != undefined) {
    selectedEcu.forEach((ecu) => {
      var alreadySelected = false;
      if (ecuFilters != undefined) {
        ecuFilters.forEach((filter) => {
          if (filter.id == ecu.id) {
            alreadySelected = true;
          }
        });
      }

      if (!alreadySelected) {
        ecuFilters.push(ecu);
        document
          .getElementById("selected-ecu-types-list-ul")
          .insertAdjacentHTML(
            "beforeend",
            `<li id="ecu-remove-li-${ecu.id}" class="flex flex-row items-center mt-1"> <button
            id="ecu-remove-${ecu.id}"
            type="button"
            class="ecu-filter-remove-button w-5 h-5 pt-1 pl-1.5 text-white bg-red-700 hover:bg-red-800 font-medium rounded-lg text-sm text-center inline-flex items-center dark:bg-red-600 dark:hover:bg-red-800">
            <svg
              fill="#ffffff"
              version="1.1"
              id="Capa_1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              viewBox="0 0 800 800"
              xml:space="preserve"
              stroke="#ffffff"
              class="w-3 h-3">
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"></g>
              <g id="SVGRepo_iconCarrier">
                <g>
                  <g>
                    <path d="M491.613,75.643l-64.235-64.235c-15.202-15.202-39.854-15.202-55.056,0L251.507,132.222L130.686,11.407 c-15.202-15.202-39.853-15.202-55.055,0L11.401,75.643c-15.202,15.202-15.202,39.854,0,55.056l120.821,120.815L11.401,372.328 c-15.202,15.202-15.202,39.854,0,55.056l64.235,64.229c15.202,15.202,39.854,15.202,55.056,0l120.815-120.814l120.822,120.814 c15.202,15.202,39.854,15.202,55.056,0l64.235-64.229c15.202-15.202,15.202-39.854,0-55.056L370.793,251.514l120.82-120.815 C506.815,115.49,506.815,90.845,491.613,75.643z"></path>
                  </g>
                </g>
              </g>
            </svg>
          </button><span class="ml-1 text-sm">${ecu.name}</span></li>`
          );

        var ecuFormDiv = document.getElementById("ecu-types-form-div");
        ecuFormDiv.insertAdjacentHTML(
          "beforeend",
          '<input type="checkbox" id="ecu-filter-input-' +
            ecu.id +
            '" value="' +
            ecu.id +
            '" class="hidden" name="ecu_filter" />'
        );
      }
    });
  }

  selectedEcu = [];
  document.getElementById("selected-ecu-type-div").classList.add("hidden");
  event.currentTarget.disabled = true;
  checkAppliedEcuCheckbox();

  checkFiltersVisibility();

  // update vehicle table here
}

document
  .getElementById("filter-ecu-button")
  .addEventListener("click", applyEcuFilter);

function checkAppliedEcuCheckbox() {
  document.querySelectorAll(".ecu-type-checkbox").forEach((checkbox) => {
    if (ecuFilters != undefined) {
      ecuFilters.forEach((filter) => {
        if (filter.id == checkbox.value) {
          if (!checkbox.classList.contains("hidden")) {
            checkbox.checked = false;
            checkbox.classList.add("hidden");
            checkbox.insertAdjacentHTML(
              "afterend",
              `<button
                id="ecu-remove-${checkbox.value}"
                type="button"
                class="ecu-filter-remove-button w-5 h-5 pt-1 pl-1.5 text-white bg-red-700 hover:bg-red-800 font-medium rounded-lg text-sm text-center inline-flex items-center dark:bg-red-600 dark:hover:bg-red-800">
                <svg
                fill="#ffffff"
                version="1.1"
                id="Capa_1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                viewBox="0 0 800 800"
                xml:space="preserve"
                stroke="#ffffff"
                class="w-3 h-3">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  stroke-linecap="round"
                  stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                  <g>
                    <g>
                      <path d="M491.613,75.643l-64.235-64.235c-15.202-15.202-39.854-15.202-55.056,0L251.507,132.222L130.686,11.407 c-15.202-15.202-39.853-15.202-55.055,0L11.401,75.643c-15.202,15.202-15.202,39.854,0,55.056l120.821,120.815L11.401,372.328 c-15.202,15.202-15.202,39.854,0,55.056l64.235,64.229c15.202,15.202,39.854,15.202,55.056,0l120.815-120.814l120.822,120.814 c15.202,15.202,39.854,15.202,55.056,0l64.235-64.229c15.202-15.202,15.202-39.854,0-55.056L370.793,251.514l120.82-120.815 C506.815,115.49,506.815,90.845,491.613,75.643z"></path>
                    </g>
                  </g>
                </g>
                </svg>
                </button>`
            );
          }
        }
      });
    }
  });

  addRemoveListener();
}

function removeFilter(event) {
  var filterType = event.currentTarget.id.substring(
    0,
    event.currentTarget.id.lastIndexOf("-")
  );
  var filterId = event.currentTarget.id.substring(
    event.currentTarget.id.lastIndexOf("-") + 1
  );

  if (filterType == "version-remove") {
    var index = -1;
    for (let i = 0; i < versionFilters.length; i++) {
      if (versionFilters[i].id == filterId) {
        index = i;
        break;
      }
    }
    versionFilters.splice(index, 1);

    document.getElementById("version-remove-li-" + filterId).remove();
    document.getElementById("version-filter-input-" + filterId).remove();
  } else if (filterType == "ecu-remove") {
    var index = -1;
    for (let i = 0; i < ecuFilters.length; i++) {
      if (ecuFilters[i].id == filterId) {
        index = i;
        break;
      }
    }
    ecuFilters.splice(index, 1);

    document.getElementById("ecu-remove-li-" + filterId).remove();
    document.getElementById("ecu-filter-input-" + filterId).remove();
    document.querySelectorAll(".ecu-filter-remove-button").forEach((button) => {
      if (button.id == "ecu-remove-" + filterId) {
        button.remove();
        document
          .querySelectorAll("#ecu-type-" + filterId)
          .forEach((checkbox) => {
            checkbox.classList.remove("hidden");
          });
      }
    });
  }

  checkFiltersVisibility();

  // update vehicle table here
}

function addRemoveListener() {
  document
    .querySelectorAll(".version-filter-remove-button")
    .forEach((button) => {
      button.addEventListener("click", removeFilter);
    });
  document.querySelectorAll(".ecu-filter-remove-button").forEach((button) => {
    button.addEventListener("click", removeFilter);
  });
}

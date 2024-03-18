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

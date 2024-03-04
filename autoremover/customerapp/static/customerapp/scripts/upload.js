import { getAndInject } from "./modals.js";
import { openCalculator, resetCalculator } from "./price_options.js";

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
  var url = "get_vehicle?requested=" + nextName;
  Object.keys(modelFields).forEach((key) => {
    url += "&" + key + "=" + modelFields[key];
  });

  getAndInject(url, nextId, undefined, undefined);
  document.getElementById(nextId).disabled = false;

  for (let i = nextIndex + 1; i < 6; i++) {
    fields[i].value = null;
    fields[i].disabled = true;
  }
}

for (let i = 0; i < 5; i++) {
  fields[i].addEventListener("change", loadNext);
}

var vehicleTab = document.getElementById("select-vehicle-tab");
var optionsTab = document.getElementById("select-options-tab");

var vehicleCard = document.getElementById("select-vehicle-card");
var optionsCard = document.getElementById("select-options-card");

function openVehicleCard(event) {
  vehicleTab.classList.add("active-tab");
  optionsTab.classList.remove("active-tab");

  vehicleCard.classList.remove("pasive-card");
  optionsCard.classList.add("pasive-card");
}

function openOptionsCard() {
  vehicleTab.classList.remove("active-tab");
  optionsTab.classList.add("active-tab");

  vehicleCard.classList.add("pasive-card");
  optionsCard.classList.remove("pasive-card");

  resetCalculator();
  openCalculator();
}

var firstFormFields = document
  .getElementById("select-vehicle-card")
  .querySelectorAll("input, select");

var oldVehicleYearId = -1;
var oldVehicleVersionId = -1;
var oldEcuModelId = -1;

function proceedToOptions(event) {
  var readyToProceed = true;

  for (let i = 0; i < firstFormFields.length; i++) {
    if (firstFormFields[i].value === "null") {
      readyToProceed = false;
    }
  }

  var fileInput = document.getElementById("dropzone-file");

  if (fileInput.value == "") {
    readyToProceed = false;
  }

  var proceedingError = document.getElementById("proceeding-error");

  if (readyToProceed) {
    proceedingError.style.display = "none";

    var vehicleYearId = document.getElementById("vehicle-year-select-4").value;
    var vehicleVersionId = document.getElementById(
      "vehicle-version-select-5"
    ).value;
    var ecuModelId = document.getElementById("ecu-type-select-6").value;

    if (
      vehicleYearId != oldVehicleYearId ||
      vehicleVersionId != oldVehicleVersionId ||
      ecuModelId != oldEcuModelId
    ) {
      var url =
        "get_process_options?vehicle_year_id=" +
        vehicleYearId +
        "&vehicle_version_id=" +
        vehicleVersionId +
        "&ecu_model_id=" +
        ecuModelId;
      getAndInject(url, "price-options-form", undefined, openOptionsCard);

      oldVehicleYearId = vehicleYearId;
      oldVehicleVersionId = vehicleVersionId;
      oldEcuModelId = ecuModelId;
    } else {
      openOptionsCard();
    }
  } else {
    proceedingError.style.display = "block";
  }
}

vehicleTab.addEventListener("click", openVehicleCard);
optionsTab.addEventListener("click", proceedToOptions);

var proceedButton = document.getElementById("continue-button");
proceedButton.addEventListener("click", proceedToOptions);

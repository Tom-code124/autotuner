import { getAndInject } from "./modals.js";
import { openCalculator } from "./price_options.js";

var fields = document
  .getElementById("vehicle-select-section")
  .querySelectorAll("select, input");

function loadNext(event) {
  var nextIndex = parseInt(
    event.target.id.substring(event.target.id.lastIndexOf("-") + 1)
  );

  var nextId = fields[nextIndex].id;
  var modelFields = {};

  for (let i = 0; i < nextIndex; i++) {
    modelFields[fields[i].id] = fields[i].value;
  }

  if (event.target.value != "not-listed") {
    if (nextIndex == 6) {
      fields[nextIndex].disabled = true;
    } else {
      var url = "get_vehicle?requested=" + nextId;
      Object.keys(modelFields).forEach((key) => {
        url += "&" + key + "=" + modelFields[key];
      });

      getAndInject(url, nextId, undefined, undefined);
      document.getElementById(nextId).disabled = false;

      for (let i = nextIndex + 1; i < 7; i++) {
        fields[i].disabled = true;
      }
    }
  } else {
    fields[nextIndex].disabled = false;
  }
}

for (let i = 0; i < 6; i++) {
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

  openCalculator();
}

var firstFormFields = document
  .getElementById("select-vehicle-card")
  .querySelectorAll("input, select");

var oldVehicleId = -1;

function proceedToOptions(event) {
  var readyToProceed = true;

  for (let i = 0; i < firstFormFields.length; i++) {
    if (firstFormFields[i].value === "null") {
      readyToProceed = false;
    }

    var ecuTypeSelect = document.getElementById("ecu-type-select-6");
    var ecuTypeInput = document.getElementById("manual-ecu-type-input");

    if (
      ecuTypeSelect.value == "not-listed" &&
      ecuTypeInput.value.trim().length == 0
    ) {
      readyToProceed = false;
    }

    var fileInput = document.getElementById("file-input");

    if (fileInput.value == "") {
      readyToProceed = false;
    }

    var proceedingError = document.getElementById("proceeding-error");

    if (readyToProceed) {
      proceedingError.style.display = "none";

      var vehicleId = document.getElementById("vehicle-year-select-4").value;

      if (vehicleId != oldVehicleId) {
        var url = "get_process_options?vehicle_id=" + vehicleId;
        getAndInject(url, "price-options-form", undefined, openOptionsCard);
        oldVehicleId = vehicleId;
      } else {
        openOptionsCard();
      }
    } else {
      proceedingError.style.display = "block";
    }
  }
}

vehicleTab.addEventListener("click", openVehicleCard);
optionsTab.addEventListener("click", proceedToOptions);

var proceedButton = document.getElementById("continue-button");
proceedButton.addEventListener("click", proceedToOptions);

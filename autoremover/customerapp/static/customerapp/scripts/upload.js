import { getAndInject } from "./modals.js";

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

  console.log(modelFields);

  if (event.target.value != "not-listed") {
    var url = "get_vehicle?";
    Object.keys(modelFields).forEach((key) => {
      url += key + "=" + modelFields[key] + "&";
    });

    url = url.slice(0, -1);

    console.log(url);

    getAndInject(url, nextId, undefined, undefined);
    document.getElementById(nextId).disabled = false;

    for (let i = nextIndex + 1; i < 7; i++) {
      fields[i].disabled = true;
    }
  } else {
    fields[nextIndex].disabled = false;
  }
}

fields[0].addEventListener("change", loadNext);

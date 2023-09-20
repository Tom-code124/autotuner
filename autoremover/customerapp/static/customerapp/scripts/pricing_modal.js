function injectModal(modal_url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("options-container").innerHTML =
        this.responseText;
    }
  };
  xhttp.open("GET", modal_url, true);
  xhttp.send();
}

function categoryChange(event) {
  injectModal("price_options_modal?category=" + event.target.value);
}

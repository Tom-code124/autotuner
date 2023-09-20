function turnOnModal(event) {
  [...document.querySelectorAll("*:not(body):not(html):not(head)")].map(
    (item) => {
      if (!item.id.includes("modal")) {
        item.classList.add("disable");
        item.classList.add("disable-scroll");
      }
    }
  );

  document.querySelector("body").classList.add("disable-scroll");
  // document.getElementById("modal-body").style.overflow = "scroll";
  document.getElementById("modal-background").style.display = "flex";
}

function turnOffModal(event) {
  if (
    !(event.target.id == "modal-background" || event.target.id == "modal-close")
  ) {
    return;
  }
  [...document.querySelectorAll(".disable")].map((item) => {
    item.classList.remove("disable");
    item.classList.remove("disable-scroll");
  });

  document.querySelector("body").classList.remove("disable-scroll");
  document.getElementById("modal-background").style.display = "none";
}

function injectModal(modal_url) {
  document
    .getElementById("modal-background")
    .addEventListener("click", turnOffModal);

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("modal-background").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", modal_url, true);
  xhttp.send();
}

export { turnOnModal, turnOffModal, injectModal };

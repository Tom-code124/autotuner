function calculate(event) {
  var choiceContent = document.getElementById("choice-content");
  var noChoiceContent = document.getElementById("no-choice-content");

  var choiceUl = document.getElementById("selected-services");
  var taxLi = document.getElementById("tax-li");

  if (event.currentTarget.checked) {
    choiceContent.classList.remove("hidden");
    noChoiceContent.classList.add("hidden");

    var newName = document.getElementById(
      event.currentTarget.id + "-name-span"
    ).innerText;
    var newAmountText = document
      .getElementById(event.currentTarget.id + "-price-span")
      .innerText.trim();
    var newAmount = Number(
      newAmountText.substring(0, newAmountText.lastIndexOf(" "))
    );
    var li = document.createElement("li");
    li.classList.add("price-li");
    li.id = event.currentTarget.id + "-li";

    li.innerHTML = `<div class="row apart-children"><span>${newName}</span><div><span class="price-span">${newAmount}</span>$</div></div>`;

    choiceUl.insertBefore(li, taxLi);

    let sum = 0;
    [...document.querySelectorAll(".price-span")].map((item) => {
      sum += Number(item.innerText);
    });
    let taxRate =
      Number(document.getElementById("tax-percentage-span").innerText) / 100;
    let newTax = sum * taxRate;
    document.getElementById("tax-amount-span").innerText = newTax.toFixed(2);
    document.getElementById("total-amount-span").innerText = (
      sum + newTax
    ).toFixed(2);
  } else {
    let oldLi = document.getElementById(event.currentTarget.id + "-li");
    choiceUl.removeChild(oldLi);

    let sum = 0;
    [...document.querySelectorAll(".price-span")].map((item) => {
      sum += Number(item.innerText);
    });

    if (sum !== 0) {
      let taxRate =
        Number(document.getElementById("tax-percentage-span").innerText) / 100;
      let newTax = sum * taxRate;
      document.getElementById("tax-amount-span").innerText = newTax.toFixed(2);
      document.getElementById("total-amount-span").innerText = (
        sum + newTax
      ).toFixed(2);
    } else {
      choiceContent.classList.add("hidden");
      noChoiceContent.classList.remove("hidden");
    }
  }
}

function openCalculator() {
  document.getElementById("calculator-box").classList.remove("hidden");
  [...document.querySelectorAll(".price-option-check")].map((item) => {
    item.addEventListener("change", calculate);
  });
}

function resetCalculator() {
  var choiceContent = document.getElementById("choice-content");
  var noChoiceContent = document.getElementById("no-choice-content");

  choiceContent.classList.add("hidden");
  noChoiceContent.classList.remove("hidden");

  var selectedServices = document.getElementById("selected-services");
  var selecteds = selectedServices.querySelectorAll(".price-li");

  for (let i = 0; i < selecteds.length; i++) {
    if (selecteds[i].id != "tax-li") {
      selectedServices.removeChild(selecteds[i]);
    }
  }
}

export { openCalculator, resetCalculator };

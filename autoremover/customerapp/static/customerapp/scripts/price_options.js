function calculator() {
  var sum = 0;
  var selecteds = [];

  [...document.querySelectorAll(".price-option-check")].map((item) => {
    if (item.checked) {
      var name = document.getElementById(item.id + "-name-span").innerText;
      var price = Number(
        document.getElementById(item.id + "-price-span").innerText
      );
      var hash = {
        product: name,
        price: price,
      };

      selecteds.push(hash);
      sum += price;
    }
  });

  if (sum !== 0) {
    var taxRate =
      Number(document.getElementById("tax-percentage-span").innerText) / 100;

    var tax = sum * taxRate;
    var total = sum + tax;

    document.getElementById("total-amount-span").innerText = total;
    document.getElementById("tax-amount-span").innerText = tax;

    var ul = document.getElementById("selected-services");

    for (const child of ul.children) {
      if (child.id !== "tax-li") {
        ul.removeChild(child);
      }
    }

    for (const hash of selecteds) {
      var li = document.createElement("li");
      li.classList.add("price-li");

      var inner = `<div class="row apart-children"><span>${hash.product}</span><span>${hash.price}$</span></div>`;
      li.innerHTML = inner;

      ul.insertBefore(li, ul.firstChild);
      document.getElementById("choice-content").style.display = "block";
      document.getElementById("no-choice-content").style.display = "none";
    }
  } else {
    document.getElementById("choice-content").style.display = "none";
    document.getElementById("no-choice-content").style.display = "block";
  }
}

function openCalculator() {
  document.getElementById("calculator-box").style.display = "flex";
  [...document.querySelectorAll(".price-option-check")].map((item) => {
    item.addEventListener("change", calculator);
  });
}

export { openCalculator };

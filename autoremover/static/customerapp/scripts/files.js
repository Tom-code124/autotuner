import { getAndInject } from "./modals.js";
import { afterFunc } from "./requested_files_modal.js";
import { afterFuncBought } from "./bought_files_modal.js";

getAndInject("requested_files", "requested-files-page", undefined, afterFunc);
getAndInject("bought_files", "bought-files-page", undefined, afterFuncBought);

// var searchInput = document.getElementById("req-files-search-input");
// var searchButton = document.getElementById("req-files-search-button");
// function search(event) {
//   event.preventDefault();
//   var keyword = searchInput.value;

//   var url = "requested_files";

//   if (keyword.trim().length != 0) {
//     url += "?keyword=" + encodeURIComponent(keyword);
//   }

//   getAndInject(url, "requested-files-page", undefined, afterFunc);
// }
// searchButton.addEventListener("click", search);

var tabs = [...document.querySelectorAll(".card-header-tab")];
var pages = [...document.querySelectorAll(".subpage")];

function openTab(event){
  var tabId = event.currentTarget.id;
  var pageId = tabId.substring(0, tabId.lastIndexOf("-") + 1) + "page";
  
  var currentTab = document.getElementById(tabId);
  var currentPage = document.getElementById(pageId);

  currentTab.classList.add("active-tab");
  currentPage.style.display = "flex"

  
  for(let i = 0; i < tabs.length; i++){
    var tab = tabs[i];
    var page = pages[i];

    if(tab.id != tabId){
      tab.classList.remove("active-tab");
      page.style.display = "none";
    }
  }
}


tabs.map((item)=>{
  item.addEventListener("click", openTab)
})

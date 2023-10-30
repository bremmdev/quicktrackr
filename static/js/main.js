/**********GLOBAL ERRORS ***********/
document.addEventListener("htmx:beforeSwap", function (event) {
  //clear any existing errors
  document.getElementById("error").innerHTML = "";

  //manually turn on swapping content on errors
  event.detail.shouldSwap = true;
});

//clear category form after successful submission
function clearCategoryForm(event) {
  if (event.detail.xhr.status === 200) {
    document.getElementById("name").value = "";
  }
}

/**********EXPENSES ***********/
//handle bulk delete expenses, takes a type (expense or budget)
function updateDeleteItems(event, type) {
  cnt = Array.from(
    document.querySelectorAll(`[name="selected-${type}"]:checked`)
  ).length;
  btn = document.getElementById(`delete-${type}s-btn`);
  btnTextElement = btn.querySelectorAll("span")[0];
  if (cnt > 0) {
    btn.disabled = false;
    text = cnt === 1 ? type : type + "s";
    btnTextElement.innerHTML = `Delete ${cnt} ${text}`;
  } else {
    btn.disabled = true;
    btnTextElement.innerHTML = `Delete ${type}s`;
  }
}

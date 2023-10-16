/**********GLOBAL ERRORS ***********/
document.addEventListener("htmx:afterRequest", function (event) {
  const errorEl = document.getElementById("error");
  const status = event.detail.xhr.status;

  if (status === 400 || status === 500) {
    errorEl.innerHTML = event.detail.xhr.response;
  } else {
    errorEl.innerHTML = "";
  }
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

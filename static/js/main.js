function styleActiveLink(pathname) {
  console.log('q')
  const path = pathname || window.location.pathname;
  const links = Array.from(document.querySelectorAll("#primary-nav a"));

  links.forEach((link) => {
    if (link.pathname === path) {
      link.classList.add("active-link");
    } else {
      link.classList.remove("active-link");
    }
  });
}

window.onload = function () {
  styleActiveLink();
  ctx = null
};


/**********GLOBAL ERRORS ***********/
document.addEventListener("htmx:afterRequest", function (event) {
  const errorEl = document.getElementById("error");
  const status = event.detail.xhr.status;
  console.log(event.detail)

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

//handle bulk delete expenses form
function updateDeleteExpenses(event) {
  cnt = Array.from(document.querySelectorAll('[name="selected-expense"]:checked')).length
  btn = document.getElementById("delete-expenses-btn")
  btnTextElement = btn.querySelectorAll("span")[0]
  if (cnt > 0) {
    btn.disabled = false;
    text = cnt === 1 ? "expense" : "expenses"
    btnTextElement.innerHTML = `Delete ${cnt} ${text}`
  } else {
    btn.disabled = true;
    btnTextElement.innerHTML = "Delete expenses"
  }
}
function styleActiveLink(pathname) {
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
};

//handle errors
document.addEventListener("htmx:afterRequest", function (event) {
  console.log(event.detail)
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

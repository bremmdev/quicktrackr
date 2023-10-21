//style the active link in the nav bar based on the current path
function styleActiveLink(path) {
  const links = Array.from(document.querySelectorAll("#primary-nav a"));

  links.forEach((link) => {
    link.classList.remove("active-link");
  });

  const activeLink = links.find((link) => link.pathname === path);

  if (activeLink) {
    activeLink.classList.add("active-link");
  }
}

//set active link on page load
window.onload = function () {
  const navPath = "/" + window.location.pathname.split("/")[1];
  styleActiveLink(navPath);
};

//set active link when we push a new state into the history
document.addEventListener("htmx:pushedIntoHistory", function (event) {
  //get the path from the event (for instance /expenses or /budgets)
  const navPath = "/" + event.detail.path.split("/")[1];
  styleActiveLink(navPath);
});

//set active link when we restore a state from the history (back button, forward button, etc.)
document.addEventListener("htmx:historyRestore", function (event) {
  const navPath = "/" + event.currentTarget.location.pathname.split("/")[1];
  styleActiveLink(navPath);
});
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

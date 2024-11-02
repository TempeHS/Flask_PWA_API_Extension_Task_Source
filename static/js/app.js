if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentUrl = window.location.pathname;

  navLinks.forEach((link) => {
    const linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const searchTerm = input.value.trim().toLowerCase();
    if (searchTerm) {
      highlightText(searchTerm);
    }
  });

  function highlightText(searchTerm) {
    const bodyText = document.body.innerHTML;
    const regex = new RegExp(`(${searchTerm})`, "gi");
    const highlightedText = bodyText.replace(
      regex,
      '<span class="highlight">$1</span>'
    );
    document.body.innerHTML = highlightedText;
  }
});

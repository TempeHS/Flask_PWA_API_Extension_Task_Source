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
    const mainContent = document.querySelector("main");
    removeHighlights(mainContent);
    highlightTextNodes(mainContent, searchTerm);
  }

  function removeHighlights(element) {
    const highlightedElements = element.querySelectorAll("span.highlight");
    highlightedElements.forEach((el) => {
      el.replaceWith(el.textContent);
    });
  }

  function highlightTextNodes(element, searchTerm) {
    const regex = new RegExp(`(${searchTerm})`, "gi");
    const walker = document.createTreeWalker(
      element,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );
    let node;
    while ((node = walker.nextNode())) {
      const parent = node.parentNode;
      if (
        parent &&
        parent.nodeName !== "SCRIPT" &&
        parent.nodeName !== "STYLE"
      ) {
        const text = node.nodeValue;
        const highlightedText = text.replace(
          regex,
          '<span class="highlight">$1</span>'
        );
        if (highlightedText !== text) {
          const tempDiv = document.createElement("div");
          tempDiv.innerHTML = highlightedText;
          while (tempDiv.firstChild) {
            parent.insertBefore(tempDiv.firstChild, node);
          }
          parent.removeChild(node);
        }
      }
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("all");

  allButton.addEventListener("click", function () {
    window.location.href = "/";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("python");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=python";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("all");

  allButton.addEventListener("click", function () {
    window.location.href = "/";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("python");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=python";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("c++");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=cpp";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("bash");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=bash";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("sql");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=sql";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("html");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=html";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("css");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=css";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const allButton = document.getElementById("js");

  allButton.addEventListener("click", function () {
    window.location.href = "?lang=javascript";
  });
});

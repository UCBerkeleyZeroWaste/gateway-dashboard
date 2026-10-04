/* Gateway Sustainability Systems: shared header, navigation, and footer for every page.
   Each page sets <body data-root="..." data-page="..."> so links resolve
   from any folder depth and the current page is marked in the nav. */

(function () {
  "use strict";

  document.documentElement.classList.add("js");
  var body = document.body;
  var root = body.getAttribute("data-root") || "";
  var current = body.getAttribute("data-page") || "";

  var LINKS = {
    manual: "https://docs.google.com/presentation/d/1j3IVyxEG0aGZXlMy2ydaw6Dh-32Yhf_N/present",
    survey: "https://docs.google.com/forms/d/1glC-AHEhuP3i5ERi-KG0GDzeFtqlSm39Vx3mVZaOjQc/viewform"
  };

  var NAV = [
    { id: "home", label: "Home", href: "index.html" },
    { id: "construction", label: "Construction", href: "construction.html" },
    { id: "building", num: "01", label: "Building Systems", href: "building-systems.html" },
    { id: "reuse", num: "02", label: "Reuse Systems", href: "reuse.html" },
    { id: "purchasing", num: "03", label: "Circular Purchasing", href: "circular-purchasing.html" },
    { id: "recovery", num: "04", label: "Recovery Systems", href: "recovery.html" },
    { id: "resources", label: "Resource Library", href: "resources/index.html" }
  ];

  function navItems() {
    return NAV.map(function (item) {
      var active = item.id === current ? ' aria-current="page"' : "";
      var num = item.num ? '<span class="nav-num" aria-hidden="true">' + item.num + "</span>" : "";
      return '<li><a href="' + root + item.href + '"' + active + ">" + num + item.label + "</a></li>";
    }).join("");
  }

  var header = document.createElement("header");
  header.className = "site-header";
  header.innerHTML =
    '<div class="wrap">' +
      '<a class="brand" href="' + root + 'index.html">' +
        'Gateway Sustainability Systems' +
      "</a>" +
      '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">' +
        '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>' +
        "Menu" +
      "</button>" +
      '<nav class="site-nav" id="site-nav" aria-label="Main">' +
        "<ul>" + navItems() + "</ul>" +
      "</nav>" +
    "</div>";

  var skip = document.createElement("a");
  skip.className = "skip-link";
  skip.href = "#main";
  skip.textContent = "Skip to main content";

  body.insertBefore(header, body.firstChild);
  body.insertBefore(skip, header);

  var toggle = header.querySelector(".nav-toggle");
  var nav = header.querySelector(".site-nav");

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });

  var footer = document.createElement("footer");
  footer.className = "site-footer";
  footer.innerHTML =
    '<div class="wrap">' +
      '<div class="involved">' +
        '<section aria-labelledby="get-involved">' +
          '<h2 id="get-involved">Get involved</h2>' +
          "<p>Questions, comments, or concerns about zero waste at Gateway? Tell us in our short survey.</p>" +
          "<p>Curious about being your department's Green Team Representative? Let us know. No commitment.</p>" +
          '<a class="btn" href="' + LINKS.survey + '">Take the survey<span class="sr-only"> (Google Form)</span></a>' +
        "</section>" +
        '<details class="fold" data-open-desktop>' +
          '<summary><h2 id="contacts">Who to contact</h2></summary>' +
          '<ul class="contacts">' +
            "<li><strong>Sam Bunke, Zero Waste Specialist</strong>" +
              '<span><a href="mailto:sbunke@berkeley.edu">sbunke@berkeley.edu</a></span>' +
              "<span>Circularity, purchasing, and waste reduction</span></li>" +
            "<li><strong>Sarah Pecora, Facilities Manager, CDSS</strong>" +
              '<span><a href="mailto:specora@berkeley.edu">specora@berkeley.edu</a></span>' +
              "<span>Building operations and waste stations</span></li>" +
            "<li><strong>Campus Facilities Services</strong>" +
              '<span><a href="mailto:fs-general@berkeley.edu">fs-general@berkeley.edu</a></span>' +
              "<span>Maintenance, repairs, and custodial services</span></li>" +
          "</ul>" +
        "</details>" +
      "</div>" +
      '<div class="footer-base">' +
        "<span>Cal Zero Waste Gateway team · UC Berkeley Facilities Services</span>" +
        '<a href="' + LINKS.manual + '">Zero Waste Operations Manual<span class="sr-only"> (Google Slides)</span></a>' +
      "</div>" +
    "</div>";

  body.appendChild(footer);

  /* Long sections fold on phones; open them (and lock them open) on wider screens. */
  var wide = window.matchMedia("(min-width: 768px)");
  function syncFolds() {
    document.querySelectorAll("details[data-open-desktop]").forEach(function (el) {
      var summary = el.querySelector("summary");
      if (wide.matches) {
        el.open = true;
        summary.setAttribute("tabindex", "-1");
      } else {
        summary.removeAttribute("tabindex");
      }
    });
  }
  syncFolds();
  if (wide.addEventListener) wide.addEventListener("change", syncFolds);

  /* Shared helpers for chart pages. Charts load plotly.js from a CDN only on
     pages that call GW.chart(). */
  window.GW = {
    root: root,
    font: '"Inter Tight", system-ui, -apple-system, "Segoe UI", Arial, sans-serif',
    colors: { green: "#0B6E4F", greenMid: "#3F8F43", ink: "#343743", muted: "#5E6878", line: "#D8DCE5" },
    loadJSON: function (path) {
      return fetch(root + path).then(function (response) {
        if (!response.ok) throw new Error("Could not load " + path);
        return response.json();
      });
    }
  };
})();

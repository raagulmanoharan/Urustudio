/* ============================================================
   URU STUDIO — Base interactions
   ============================================================ */
(function () {
  "use strict";

  /* ---- Mobile nav toggle ---- */
  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("primary-nav");

  if (toggle && nav) {
    const closeNav = () => {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
    };

    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
      toggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
    });

    // Close the menu after tapping a link
    nav.querySelectorAll("a").forEach((link) =>
      link.addEventListener("click", closeNav)
    );

    // Close on Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("is-open")) closeNav();
    });
  }

  /* ---- Header shadow on scroll ---- */
  const header = document.getElementById("site-header");
  if (header) {
    const onScroll = () =>
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Current year in footer ---- */
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();

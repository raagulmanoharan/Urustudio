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

  /* ---- Transparent-over-hero → solid cream once past it ---- */
  const header = document.getElementById("site-header");
  if (header) {
    // Transparent only at rest over the hero; cream as soon as you scroll.
    const onScroll = () =>
      header.classList.toggle("is-scrolled", window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Reveal-on-scroll (restrained fade + rise) ---- */
  const revealEls = document.querySelectorAll(".reveal");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (revealEls.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealEls.forEach((el) => el.classList.add("is-visible"));
    } else {
      const observer = new IntersectionObserver(
        (entries, obs) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              obs.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
      );
      revealEls.forEach((el) => observer.observe(el));
    }
  }

  /* ---- Current year in footer ---- */
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();

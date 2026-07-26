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

  /* ---- Enquiry form → open WhatsApp with details prefilled ---- */
  const WA_NUMBER = "91XXXXXXXXXX"; // TODO: replace with the real WhatsApp number
  const enquire = document.getElementById("enquire-form");
  if (enquire) {
    enquire.addEventListener("submit", (e) => {
      e.preventDefault();
      const val = (id) => (document.getElementById(id)?.value || "").trim();
      const name = val("ef-name");
      const date = val("ef-date");
      const city = val("ef-city");
      const qty = val("ef-qty");
      const budget = val("ef-budget");
      const msg = val("ef-msg");
      const lines = [
        "Hi Uru, I'd like to enquire about return gifts.",
        name && `Name: ${name}`,
        date && `Event date: ${date}`,
        city && `Delivery city: ${city}`,
        qty && `Quantity: ${qty}`,
        budget && `Budget per gift: ${budget}`,
        msg && `Details: ${msg}`,
      ].filter(Boolean);
      const url =
        "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
    });
  }

  /* ---- Newsletter signup: friendly inline confirmation (no backend) ---- */
  const signup = document.getElementById("signup-form");
  if (signup) {
    signup.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = signup.querySelector("input");
      if (!input || !input.value.trim()) return;
      signup.innerHTML = '<p style="padding:.7rem 1rem;color:var(--color-accent);font-size:.9rem;">Thank you, we\'ll be in touch.</p>';
    });
  }
})();

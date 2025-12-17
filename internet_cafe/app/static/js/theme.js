(function () {
  function markRevealElements() {
    const selectors = [
      ".container > *",
      "section",
      ".card", ".panel", ".box",
      "form",
      "table",
      "img",
      ".flash"
    ];
    document.querySelectorAll(selectors.join(",")).forEach(el => {
      if (!el.classList.contains("reveal")) el.classList.add("reveal");
    });
  }

  function observeReveals() {
    const els = document.querySelectorAll(".reveal");
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add("is-visible");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });

    els.forEach(el => io.observe(el));
  }

  function markActiveNav() {
    const path = window.location.pathname.replace(/\/+$/, "");
    document.querySelectorAll(".navlink").forEach(a => {
      try {
        const href = new URL(a.href).pathname.replace(/\/+$/, "");
        if (href === path) a.classList.add("is-active");
      } catch(_) {}
    });
  }

  function setupMobileMenu() {
    const btn = document.querySelector(".nav-toggle");
    const links = document.querySelector("#navlinks");
    if (!btn || !links) return;

    btn.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", (e) => {
      if (!links.classList.contains("open")) return;
      if (links.contains(e.target) || btn.contains(e.target)) return;
      links.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    markRevealElements();
    observeReveals();
    markActiveNav();
    setupMobileMenu();
  });
})();
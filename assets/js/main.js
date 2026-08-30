/* Finbolt — shared behaviour for every page */
(function () {
  "use strict";

  /* ---- Mobile drawer ---------------------------------------------------- */
  var drawer = document.querySelector("[data-drawer]");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.setAttribute("data-open", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  }
  document.querySelectorAll("[data-drawer-open]").forEach(function (b) {
    b.addEventListener("click", function () { setDrawer(true); });
  });
  document.querySelectorAll("[data-drawer-close]").forEach(function (b) {
    b.addEventListener("click", function () { setDrawer(false); });
  });
  if (drawer) {
    drawer.addEventListener("click", function (e) {
      if (e.target === drawer) setDrawer(false);
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setDrawer(false);
  });

  /* ---- Audience tabs ---------------------------------------------------- */
  var tabs = document.querySelectorAll("[data-tab]");
  if (tabs.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        var name = tab.getAttribute("data-tab");
        tabs.forEach(function (t) {
          t.setAttribute("aria-selected", String(t === tab));
        });
        document.querySelectorAll("[data-panel]").forEach(function (card) {
          var live = card.getAttribute("data-panel") === name;
          card.classList.toggle("fcard--live", live);
        });
      });
    });
  }

  /* ---- Accordion -------------------------------------------------------- */
  document.querySelectorAll(".acc__q").forEach(function (q) {
    q.addEventListener("click", function () {
      var item = q.closest(".acc__item");
      var open = item.getAttribute("data-open") === "true";
      item.parentElement.querySelectorAll(".acc__item").forEach(function (i) {
        i.setAttribute("data-open", "false");
        i.querySelector(".acc__q").setAttribute("aria-expanded", "false");
      });
      item.setAttribute("data-open", open ? "false" : "true");
      q.setAttribute("aria-expanded", open ? "false" : "true");
    });
  });

  /* ---- Scroll reveal ---------------------------------------------------- */
  var targets = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && targets.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add("is-in"); });
  }

  /* ---- Forms (front-end only — no server attached) ---------------------- */
  document.querySelectorAll("[data-demo-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = form.querySelector(".form__ok");
      if (ok) {
        ok.setAttribute("data-show", "true");
        ok.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }
      form.reset();
    });
  });

  document.querySelectorAll("[data-capture]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.parentElement.querySelector(".capture__note");
      if (note) note.textContent = "Thanks — check your inbox to finish setting up your account.";
      form.reset();
    });
  });

  /* ---- Footer year ------------------------------------------------------ */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();

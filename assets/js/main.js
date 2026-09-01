/* Finbolt — shared behaviour for every page */
(function () {
  "use strict";

  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

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
          card.classList.remove("is-swap");
          if (live) {
            void card.offsetWidth;          /* restart the animation */
            card.classList.add("is-swap");
          }
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

  /* ---- Motion preference ------------------------------------------------ */
  var reduce = window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
    : false;

  /* ---- Scroll reveal ---------------------------------------------------- */
  /* Repeated items (cards, stats, rows) are promoted to reveal targets here
     rather than in the markup, so build.py can regenerate pages freely. */
  var ITEMS = ".stat, .quote, .post, .row-card, .tl, .acc__item";
  var promoted = [];
  document.querySelectorAll(ITEMS).forEach(function (el) {
    el.classList.add("reveal");
    promoted.push(el);
  });

  /* A wrapper that reveals as one block would hide the stagger of the items
     inside it, so hand the animation down to the children. */
  promoted.forEach(function (el) {
    var host = el.parentElement && el.parentElement.closest(".reveal");
    while (host) {
      if (host.querySelectorAll(ITEMS).length > 1) {
        host.classList.remove("reveal");
        host.classList.add("is-in");
      }
      host = host.parentElement && host.parentElement.closest(".reveal");
    }
  });

  /* Split sections come in from the side they sit on. */
  document.querySelectorAll(".split").forEach(function (split) {
    var cols = split.children;
    if (cols.length < 2) return;
    direct(cols[0], "reveal--left");
    direct(cols[cols.length - 1], "reveal--right");
  });
  function direct(col, cls) {
    if (col.classList.contains("reveal")) col.classList.add(cls);
    col.querySelectorAll(".reveal").forEach(function (r) { r.classList.add(cls); });
  }
  document.querySelectorAll(".fcard, .post, .quote").forEach(function (el) {
    el.classList.add("reveal--scale");
  });

  /* Stagger siblings so a grid deals itself in rather than flashing at once. */
  var seen = [];
  document.querySelectorAll(".reveal").forEach(function (el) {
    var parent = el.parentElement;
    if (!parent || seen.indexOf(parent) > -1) return;
    seen.push(parent);
    var kids = [];
    Array.prototype.forEach.call(parent.children, function (c) {
      if (c.classList.contains("reveal")) kids.push(c);
    });
    if (kids.length < 2) return;
    kids.forEach(function (k, i) {
      k.style.setProperty("--rd", Math.min(i * 70, 420) + "ms");
    });
  });

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

  /* ---- Counting figures -------------------------------------------------- */
  /* Splits "10,400+" into prefix, number and suffix so the count keeps the
     original formatting — separators, decimals and units all survive. */
  var counters = [];
  document.querySelectorAll(".stat b, .fcard__stat b, .trusted h2 em").forEach(function (el) {
    var parts = /^([^\d]*)([\d][\d,.]*)(.*)$/.exec(el.textContent.trim());
    if (!parts) return;
    var raw = parts[2].replace(/,/g, "");
    var value = parseFloat(raw);
    if (!isFinite(value)) return;
    var dot = raw.indexOf(".");
    el.setAttribute("data-count", "");
    counters.push({
      el: el,
      value: value,
      decimals: dot > -1 ? raw.length - dot - 1 : 0,
      group: parts[2].indexOf(",") > -1,
      prefix: parts[1],
      suffix: parts[3],
      done: false
    });
  });

  function render(c, value) {
    var n = c.decimals ? value.toFixed(c.decimals) : String(Math.round(value));
    if (c.group) {
      var bits = n.split(".");
      bits[0] = bits[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      n = bits.join(".");
    }
    c.el.textContent = c.prefix + n + c.suffix;
  }

  function runCount(c) {
    if (c.done) return;
    c.done = true;
    if (reduce) return;
    var start = 0;
    var span = 1150;
    function step(now) {
      if (!start) start = now;
      var t = Math.min((now - start) / span, 1);
      render(c, c.value * (1 - Math.pow(1 - t, 3)));   /* easeOutCubic */
      if (t < 1) requestAnimationFrame(step);
      else render(c, c.value);
    }
    render(c, 0);
    requestAnimationFrame(step);
  }

  if (counters.length && "IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        counters.forEach(function (c) { if (c.el === entry.target) runCount(c); });
        co.unobserve(entry.target);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c.el); });
  }

  /* ---- Scroll-linked chrome and parallax --------------------------------- */
  var progress = document.createElement("div");
  progress.className = "progress";
  document.body.appendChild(progress);

  var totop = document.createElement("button");
  totop.className = "totop";
  totop.type = "button";
  totop.setAttribute("aria-label", "Back to top");
  totop.setAttribute("data-show", "false");
  totop.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"' +
    ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"' +
    ' aria-hidden="true"><path d="M12 19V6"/><path d="m5 12 7-7 7 7"/></svg>';
  totop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
  });
  document.body.appendChild(totop);

  var stage = document.querySelector(".hero__stage");
  var band = document.querySelector(".band");
  var ticking = false;

  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    var max = document.documentElement.scrollHeight - window.innerHeight;

    progress.style.setProperty("--p", max > 0 ? Math.min(y / max, 1) : 0);
    totop.setAttribute("data-show", y > 620 ? "true" : "false");

    if (!reduce && y < window.innerHeight * 1.5) {
      /* The stage drifts up faster than the page; the faint grid lags behind. */
      if (stage) stage.style.setProperty("--par", Math.max(-70, -y * 0.06) + "px");
      if (band) band.style.setProperty("--gridY", Math.min(90, y * 0.12) + "px");
    }
    ticking = false;
  }

  window.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(onScroll);
  }, { passive: true });
  onScroll();

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

  /* The hero and CTA capture fields are the front door to sign-up: carry the
     address straight into the register form rather than dead-ending here. */
  document.querySelectorAll("[data-capture]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = form.querySelector('input[type="email"]');
      var email = input && input.value.trim();
      if (!email || !EMAIL.test(email)) {
        if (input) input.focus();
        return;
      }
      window.location.href = "register.html?email=" + encodeURIComponent(email);
    });
  });

  /* ---- Auth forms -------------------------------------------------------- */
  /* Front-end only: this validates and reports, it does not create accounts. */
  function showPassword(btn) {
    var input = btn.parentElement.querySelector("input");
    if (!input) return;
    var reveal = input.type === "password";
    input.type = reveal ? "text" : "password";
    btn.setAttribute("aria-pressed", reveal ? "true" : "false");
    btn.setAttribute("aria-label", reveal ? "Hide password" : "Show password");
  }
  document.querySelectorAll("[data-pw-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () { showPassword(btn); });
  });

  var STRENGTH = ["Too short", "Weak", "Good", "Strong"];
  function strengthOf(v) {
    if (v.length < 8) return 0;
    var score = 1;
    if (/[a-z]/.test(v) && /[A-Z]/.test(v)) score++;
    if (/\d/.test(v)) score++;
    if (/[^A-Za-z0-9]/.test(v)) score++;
    if (v.length >= 12) score++;
    return Math.min(3, score - 1) || 1;
  }
  document.querySelectorAll("[data-strength]").forEach(function (meter) {
    var input = meter.closest(".field-row").querySelector("input");
    var label = meter.querySelector(".strength__label");
    if (!input) return;
    input.addEventListener("input", function () {
      var v = input.value;
      meter.hidden = v.length === 0;
      var level = strengthOf(v);
      meter.setAttribute("data-level", String(level));
      label.textContent = STRENGTH[level];
    });
  });

  function errorFor(input) { return document.getElementById(input.id + "-err"); }

  function setError(input, message) {
    var slot = errorFor(input);
    if (slot) slot.textContent = message || "";
    if (message) {
      input.setAttribute("aria-invalid", "true");
      if (slot) input.setAttribute("aria-describedby", slot.id);
    } else {
      input.removeAttribute("aria-invalid");
    }
    return !message;
  }

  function checkField(input, mode) {
    var v = (input.value || "").trim();
    if (input.type === "email") {
      if (!v) return setError(input, "Enter your email address.");
      return setError(input, EMAIL.test(v) ? "" : "That does not look like an email address.");
    }
    if (input.type === "password") {
      if (!v) return setError(input, "Enter your password.");
      if (mode === "register") {
        if (v.length < 8) return setError(input, "Use at least 8 characters.");
        if (!/[A-Za-z]/.test(v) || !/\d/.test(v))
          return setError(input, "Mix in at least one letter and one number.");
      }
      return setError(input, "");
    }
    if (input.required) return setError(input, v ? "" : "This field is required.");
    return true;
  }

  document.querySelectorAll("[data-auth]").forEach(function (form) {
    var mode = form.getAttribute("data-auth");
    var fields = [].slice.call(form.querySelectorAll("input[required]"))
      .filter(function (i) { return i.type !== "checkbox"; });
    var terms = form.querySelector('input[name="terms"]');
    var done = form.parentElement.querySelector("[data-auth-done]");

    fields.forEach(function (input) {
      /* Report on the way out of a field, then keep it live once it has failed. */
      input.addEventListener("blur", function () { checkField(input, mode); });
      input.addEventListener("input", function () {
        if (input.getAttribute("aria-invalid") === "true") checkField(input, mode);
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = null;
      fields.forEach(function (input) {
        if (!checkField(input, mode) && !bad) bad = input;
      });
      if (terms) {
        var slot = document.getElementById("r-terms-err");
        var ok = terms.checked;
        if (slot) slot.textContent = ok ? "" : "Please accept the terms to continue.";
        if (!ok && !bad) bad = terms;
      }
      if (bad) { bad.focus(); return; }

      form.hidden = true;
      var swap = form.parentElement.querySelector(".auth__swap");
      if (swap) swap.hidden = true;
      if (done) {
        done.hidden = false;
        done.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
      }
    });
  });

  /* Someone arriving from a capture field already told us their address. */
  var seeded = /[?&]email=([^&]+)/.exec(window.location.search);
  if (seeded) {
    var target = document.querySelector('[data-auth] input[type="email"]');
    if (target) {
      try { target.value = decodeURIComponent(seeded[1].replace(/\+/g, " ")); }
      catch (err) { /* malformed escape in the query string — leave it blank */ }
    }
  }

  /* ---- Footer year ------------------------------------------------------ */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();

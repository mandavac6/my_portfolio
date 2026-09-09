/* ==========================================================================
   Presentation layer only.
   Every value on the page is already in the HTML that Python rendered; this
   file adds motion on top and degrades to a fully readable page without it.
   ========================================================================== */

(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Navigation ---------- */

  function initNav() {
    var nav = document.querySelector("[data-nav]");
    if (!nav) return;

    var onScroll = function () {
      nav.classList.toggle("is-scrolled", window.scrollY > 60);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    var toggle = nav.querySelector("[data-nav-toggle]");
    var menu = document.getElementById("mobile-menu");
    if (!toggle || !menu) return;

    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      menu.hidden = !open;
    };

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    menu.querySelectorAll("[data-nav-close]").forEach(function (link) {
      link.addEventListener("click", function () { setOpen(false); });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setOpen(false);
    });
  }

  /* ---------- Scroll reveal ---------- */

  function initReveal() {
    var targets = document.querySelectorAll(".reveal");
    if (!targets.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );

    targets.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- Count-up numbers ---------- */

  function formatCount(value, decimals, prefix, suffix) {
    return prefix + value.toFixed(decimals) + suffix;
  }

  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count-to"));
    var decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    if (isNaN(target)) return;

    var duration = 1600;
    var start = null;

    var step = function (now) {
      if (start === null) start = now;
      var progress = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = formatCount(eased * target, decimals, prefix, suffix);
      if (progress < 1) requestAnimationFrame(step);
    };

    el.textContent = formatCount(0, decimals, prefix, suffix);
    requestAnimationFrame(step);
  }

  function initCounters() {
    var counters = document.querySelectorAll("[data-count-to]");
    if (!counters.length || reduceMotion || !("IntersectionObserver" in window)) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          animateCount(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.4 }
    );

    counters.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- Cycling dashboard values ---------- */

  function initTickers() {
    if (reduceMotion) return;

    document.querySelectorAll("[data-ticker]").forEach(function (el) {
      var values;
      try {
        values = JSON.parse(el.getAttribute("data-ticker"));
      } catch (err) {
        return;
      }
      if (!Array.isArray(values) || values.length < 2) return;

      var interval = parseInt(el.getAttribute("data-interval") || "2400", 10);
      var index = 0;

      setInterval(function () {
        if (document.hidden) return;
        index = (index + 1) % values.length;
        el.textContent = values[index];
        el.style.animation = "none";
        void el.offsetWidth; // restart the fade
        el.style.animation = "";
      }, interval);
    });
  }

  /* ---------- Project detail toggles ---------- */

  function initProjects() {
    document.querySelectorAll("[data-project-toggle]").forEach(function (button) {
      var panelId = button.getAttribute("aria-controls");
      var panel = document.getElementById(panelId);
      if (!panel) return;

      button.addEventListener("click", function () {
        var open = button.getAttribute("aria-expanded") === "true";
        button.setAttribute("aria-expanded", String(!open));
        panel.hidden = open;
      });
    });
  }

  /* ---------- Hero particle field ---------- */

  function initParticles() {
    var canvas = document.querySelector("[data-particles]");
    if (!canvas || reduceMotion) return;

    var ctx = canvas.getContext("2d");
    if (!ctx) return;

    var COUNT = 75;
    var MAX_DIST = 140;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);

    // Colours come from the stylesheet so the theme stays in one place.
    var css = getComputedStyle(document.documentElement);
    var dotRgb = (css.getPropertyValue("--particle-rgb") || "122, 79, 42").trim();
    var linkRgb = (css.getPropertyValue("--particle-link-rgb") || "160, 101, 53").trim();
    var particles = [];
    var frame = null;
    var width = 0;
    var height = 0;

    function resize() {
      width = canvas.offsetWidth;
      height = canvas.offsetHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function spawn() {
      return {
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: Math.random() * 1.5 + 0.5,
        alpha: Math.random() * 0.5 + 0.2
      };
    }

    function loop() {
      ctx.clearRect(0, 0, width, height);

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(" + dotRgb + ", " + p.alpha * 0.42 + ")";
        ctx.fill();
      }

      for (var a = 0; a < particles.length; a++) {
        for (var b = a + 1; b < particles.length; b++) {
          var dx = particles[a].x - particles[b].x;
          var dy = particles[a].y - particles[b].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist >= MAX_DIST) continue;
          ctx.beginPath();
          ctx.moveTo(particles[a].x, particles[a].y);
          ctx.lineTo(particles[b].x, particles[b].y);
          ctx.strokeStyle = "rgba(" + linkRgb + ", " + (1 - dist / MAX_DIST) * 0.14 + ")";
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }

      frame = requestAnimationFrame(loop);
    }

    resize();
    for (var i = 0; i < COUNT; i++) particles.push(spawn());
    loop();

    var resizeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resize, 150);
    });

    // Stop burning frames while the hero is off screen.
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && frame === null) {
            loop();
          } else if (!entry.isIntersecting && frame !== null) {
            cancelAnimationFrame(frame);
            frame = null;
          }
        });
      }).observe(canvas);
    }
  }

  /* ---------- Boot ---------- */

  function init() {
    initNav();
    initReveal();
    initCounters();
    initTickers();
    initProjects();
    initParticles();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

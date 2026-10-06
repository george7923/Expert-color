(function () {
  "use strict";

  // Mobile menu.
  var header = document.querySelector(".site-header");
  var toggle = header.querySelector(".nav-toggle");
  function setMenu(open) {
    header.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open);
  }
  toggle.addEventListener("click", function () { setMenu(!header.classList.contains("nav-open")); });
  header.querySelectorAll(".nav a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });

  // Color swatch fan behind the products.
  var fan = document.getElementById("fan");
  var palette = [
    "#d6232a", "#ef5a24", "#f7931e", "#fcc520", "#f4e22b", "#a8c93a", "#3fa535",
    "#12877a", "#1b9bc4", "#1f63b0", "#3b3f9a", "#7a3f98", "#8b8f94", "#3e4146"
  ];
  var from = -58, to = 64;
  palette.forEach(function (color, i) {
    var strip = document.createElement("i");
    strip.style.background = color;
    strip.style.transform = "rotate(" + (from + (to - from) * i / (palette.length - 1)) + "deg)";
    fan.appendChild(strip);
  });

  // Typing a color code updates every label on the page.
  var input = document.getElementById("cod");
  var targets = document.querySelectorAll("[data-color-code]");
  function setCode(value) {
    var code = value.trim().toUpperCase() || "—";
    targets.forEach(function (el) {
      el.textContent = code;
      var box = el.parentElement;
      if (!box.classList.contains("code")) return;
      // Shrink long codes so they stay inside their white label.
      el.style.fontSize = "";
      var room = box.clientWidth - 8;
      if (el.offsetWidth > room) {
        el.style.fontSize = parseFloat(getComputedStyle(el).fontSize) * room / el.offsetWidth + "px";
      }
    });
  }
  setCode(input.value);
  input.addEventListener("input", function () { setCode(input.value); });

  // Scale the fixed-size product showcase to the width of its container (up to MAX_SCALE).
  var showcase = document.querySelector(".showcase");
  var wrap = showcase.parentElement;
  var DESIGN_W = 860, DESIGN_H = 640, MAX_SCALE = 1.3;
  function fit() {
    var scale = Math.min(MAX_SCALE, wrap.parentElement.clientWidth / DESIGN_W);
    showcase.style.transform = "scale(" + scale + ")";
    wrap.style.width = DESIGN_W * scale + "px";
    wrap.style.height = DESIGN_H * scale + "px";
    sizeCanvas();
  }

  // Paint mist from the spray nozzle onto the scratch on the car.
  var hero = document.querySelector(".hero");
  var canvas = document.getElementById("mist");
  var ctx = canvas.getContext && canvas.getContext("2d");
  var animate = ctx && !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var particles = [];
  var origin = { x: 0, y: 0 }, target = { x: 0, y: 0 };
  var width = 0, height = 0, active = false;

  // Position of a point on an element, in hero (CSS) pixels.
  function anchor(selector, fx, fy) {
    var box = hero.getBoundingClientRect();
    var r = hero.querySelector(selector).getBoundingClientRect();
    return { x: r.left - box.left + r.width * fx, y: r.top - box.top + r.height * fy };
  }

  function sizeCanvas() {
    var ratio = window.devicePixelRatio || 1;
    width = hero.clientWidth;
    height = hero.clientHeight;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    // The car (the spray target) is hidden on narrow screens.
    active = hero.querySelector(".hero-car").offsetParent !== null;
    if (active) {
      origin = anchor(".spray .nozzle", .5, .3);
      target = anchor("#scratch", 0, 0);
    } else {
      ctx.clearRect(0, 0, width, height);
      particles = [];
    }
  }

  function spawn() {
    var dx = target.x - origin.x, dy = target.y - origin.y;
    var angle = Math.atan2(dy, dx) + (Math.random() - .5) * .22;
    var speed = Math.hypot(dx, dy) / 70 * (.7 + Math.random() * .5);
    particles.push({
      x: origin.x, y: origin.y, vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed,
      life: 0, max: 60 + Math.random() * 30, r: 1 + Math.random() * 2.5
    });
  }

  function frame() {
    requestAnimationFrame(frame);
    if (!active) return;
    ctx.clearRect(0, 0, width, height);
    for (var n = 0; n < 2; n++) spawn();
    particles = particles.filter(function (p) { return p.life < p.max; });
    particles.forEach(function (p) {
      p.life++; p.x += p.vx; p.y += p.vy; p.vy += .01;
      var t = p.life / p.max;
      ctx.globalAlpha = .55 * (1 - t) * Math.min(1, p.life / 6);
      ctx.fillStyle = "#fff";
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r * (1 + t * 1.5), 0, Math.PI * 2);
      ctx.fill();
    });
  }

  fit();
  window.addEventListener("resize", fit);
  if (animate) requestAnimationFrame(frame);
})();

(function () {
  "use strict";

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

  // Scale the fixed-size poster to the width of its container.
  var poster = document.querySelector(".poster");
  var wrap = poster.parentElement;
  var DESIGN_W = 775, DESIGN_H = 900;
  var scale = 1;
  function fit() {
    scale = wrap.clientWidth / DESIGN_W;
    poster.style.transform = "scale(" + scale + ")";
    wrap.style.height = DESIGN_H * scale + "px";
    sizeCanvas();
  }

  // Paint mist from the spray nozzle onto the scratch on the car.
  var canvas = document.getElementById("mist");
  var ctx = canvas.getContext && canvas.getContext("2d");
  var animate = ctx && !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var particles = [];
  var origin = { x: 0, y: 0 }, target = { x: 0, y: 0 };

  // Position of an element's point inside the poster, in design pixels.
  function anchor(selector, fx, fy) {
    var box = poster.getBoundingClientRect();
    var r = poster.querySelector(selector).getBoundingClientRect();
    return { x: (r.left - box.left + r.width * fx) / scale, y: (r.top - box.top + r.height * fy) / scale };
  }

  function sizeCanvas() {
    var ratio = scale * (window.devicePixelRatio || 1);
    canvas.width = Math.round(DESIGN_W * ratio);
    canvas.height = Math.round(DESIGN_H * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    origin = anchor(".spray .nozzle", .5, .3);
    target = anchor(".car", .4, .55);
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
    ctx.clearRect(0, 0, DESIGN_W, DESIGN_H);
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
    requestAnimationFrame(frame);
  }

  fit();
  window.addEventListener("resize", fit);
  if (animate) requestAnimationFrame(frame);
})();

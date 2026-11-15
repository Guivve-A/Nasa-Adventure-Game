// Zingularity: Artemis — landing. Animaciones con GSAP; todo funciona tambien sin el.
(function () {
  "use strict";

  // ---- Enlaces de descarga: se cambian solo aqui ----
  var DESCARGAS = {
    // Archivo del ultimo "release" de GitHub. Debe llamarse exactamente asi al publicarlo.
    windows: "https://github.com/Guivve-A/Nasa-Adventure-Game/releases/latest/download/Zingularity-Artemis-Windows.zip",
    repo: "https://github.com/Guivve-A/Nasa-Adventure-Game"
  };

  var doc = document;
  var gsap = window.gsap;
  var quieto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Con "reducir movimiento" quedan solo fundidos suaves: sin desplazamientos, giros ni cambio automatico.
  var animar = !!gsap;
  var pleno = animar && !quieto;
  function mov(v) { return pleno ? v : 0; }
  doc.documentElement.classList.add("js");
  function uno(sel, raiz) { return (raiz || doc).querySelector(sel); }
  function todos(sel, raiz) { return Array.prototype.slice.call((raiz || doc).querySelectorAll(sel)); }

  todos("[data-descarga]").forEach(function (a) {
    var url = DESCARGAS[a.getAttribute("data-descarga")];
    if (url) { a.href = url; }
  });

  // ---- Insignia: Guayaquil, la Luna y Marte ----
  var insignia = uno("#insignia");
  var fotos = todos("img", insignia);
  var botonesDestino = todos("#destinos button");
  var destino = 0, turno = null;

  function mostrarDestino(n) {
    if (n === destino) { return; }
    var sale = fotos[destino], entra = fotos[n];
    entra.loading = "eager";
    botonesDestino.forEach(function (b, i) { b.setAttribute("aria-pressed", String(i === n)); });
    if (animar) {
      gsap.killTweensOf([sale, entra]);
      gsap.set(entra, { zIndex: 2 });
      gsap.set(sale, { zIndex: 1 });
      gsap.fromTo(entra, { opacity: 0, scale: pleno ? 1.12 : 1 }, { opacity: 1, scale: 1, duration: .8, ease: "power2.out" });
      gsap.to(sale, { opacity: 0, duration: .8, ease: "power2.out" });
      if (pleno) { gsap.fromTo(insignia, { rotate: -4 }, { rotate: 0, duration: .8, ease: "back.out(2)" }); }
    }
    sale.classList.remove("activa");
    entra.classList.add("activa");
    destino = n;
  }
  function pararTurno() { if (turno) { window.clearInterval(turno); turno = null; } }
  botonesDestino.forEach(function (b, i) {
    b.addEventListener("click", function () { pararTurno(); mostrarDestino(i); });
  });
  if (pleno) {
    turno = window.setInterval(function () {
      if (!doc.hidden && !insignia.matches(":hover")) { mostrarDestino((destino + 1) % fotos.length); }
    }, 4800);
  }

  // ---- Pestanas de capturas ----
  var pestanas = todos(".pestanas [role=tab]");
  function elegir(pestana, enfocar, conAnimacion) {
    pestanas.forEach(function (p) {
      var activa = p === pestana;
      p.setAttribute("aria-selected", String(activa));
      p.tabIndex = activa ? 0 : -1;
      doc.getElementById(p.getAttribute("aria-controls")).hidden = !activa;
    });
    if (enfocar) { pestana.focus(); }
    if (animar && conAnimacion) {
      var panel = doc.getElementById(pestana.getAttribute("aria-controls"));
      gsap.fromTo(todos(".grupo-texto, figure", panel),
        { opacity: 0, y: mov(26) },
        { opacity: 1, y: 0, duration: .5, ease: "power2.out", stagger: .07, overwrite: true });
    }
  }
  pestanas.forEach(function (p, i) {
    p.addEventListener("click", function () { elegir(p, false, true); });
    p.addEventListener("keydown", function (e) {
      var paso = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!paso) { return; }
      e.preventDefault();
      elegir(pestanas[(i + paso + pestanas.length) % pestanas.length], true, true);
    });
  });
  if (pestanas.length) { elegir(pestanas[0], false, false); }

  // ---- Visor de capturas, con flechas ----
  var visor = uno("#visor"), imagen = uno("#visor-imagen"), pie = uno("#visor-pie");
  var serie = [], puesto = 0;
  function pintarVisor(sentido) {
    var boton = serie[puesto], img = uno("img", boton);
    imagen.src = img.currentSrc || img.src;
    imagen.alt = img.alt;
    pie.textContent = uno("figcaption", boton.parentNode).textContent;
    if (animar) {
      gsap.fromTo(imagen, { opacity: 0, x: mov(40 * sentido), scale: sentido || !pleno ? 1 : .96 },
        { opacity: 1, x: 0, scale: 1, duration: .35, ease: "power2.out", overwrite: true });
    }
  }
  function pasar(paso) {
    puesto = (puesto + paso + serie.length) % serie.length;
    pintarVisor(paso);
  }
  todos(".ampliar").forEach(function (boton) {
    var titulo = uno("figcaption strong", boton.parentNode);
    boton.setAttribute("aria-label", "Ampliar la captura: " + (titulo ? titulo.textContent : ""));
    boton.addEventListener("click", function () {
      if (!visor.showModal) { window.open(uno("img", boton).src, "_blank"); return; }
      serie = todos(".ampliar", boton.closest(".grupo"));
      puesto = serie.indexOf(boton);
      visor.showModal();
      pintarVisor(0);
    });
  });
  uno("#visor-cerrar").addEventListener("click", function () { visor.close(); });
  uno("#visor-anterior").addEventListener("click", function () { pasar(-1); });
  uno("#visor-siguiente").addEventListener("click", function () { pasar(1); });
  visor.addEventListener("click", function (e) { if (e.target === visor) { visor.close(); } });
  visor.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { pasar(1); } else if (e.key === "ArrowLeft") { pasar(-1); }
  });

  if (!animar) { return; }

  // ---- Entrada de la portada ----
  if (pleno) {
    var titulo = uno(".portada h1");
    var palabras = titulo.textContent.split(" ");
    titulo.setAttribute("aria-label", titulo.textContent);
    titulo.textContent = "";
    palabras.forEach(function (palabra, i) {
      var caja = doc.createElement("span"), dentro = doc.createElement("span");
      caja.className = "palabra";
      caja.setAttribute("aria-hidden", "true");
      dentro.textContent = palabra;
      caja.appendChild(dentro);
      titulo.appendChild(caja);
      if (i < palabras.length - 1) { titulo.appendChild(doc.createTextNode(" ")); }
    });
    gsap.timeline({ defaults: { ease: "power3.out" } })
      .from(".palabra span", { yPercent: 110, duration: .9, stagger: .12 })
      .from(".entrada, .acciones, .etiqueta", { opacity: 0, y: 22, duration: .6, stagger: .1 }, "-=.5")
      .from(".insignia", { scale: .6, opacity: 0, rotate: -12, duration: 1, ease: "back.out(1.6)" }, .15)
      .from(".destinos button", { opacity: 0, y: 10, duration: .4, stagger: .07 }, "-=.45");
  } else {
    gsap.from(".portada h1, .entrada, .acciones, .etiqueta, .destino", { opacity: 0, duration: .6, stagger: .08, ease: "power1.out" });
  }

  // ---- La insignia sigue al puntero ----
  if (pleno && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    var portada = uno(".portada");
    var giroX = gsap.quickTo(insignia, "rotationX", { duration: .6, ease: "power2.out" });
    var giroY = gsap.quickTo(insignia, "rotationY", { duration: .6, ease: "power2.out" });
    portada.addEventListener("pointermove", function (e) {
      var r = portada.getBoundingClientRect();
      giroY((e.clientX - r.left) / r.width * 22 - 11);
      giroX(-((e.clientY - r.top) / r.height * 16 - 8));
    });
    portada.addEventListener("pointerleave", function () { giroX(0); giroY(0); });
  }

  // ---- Al bajar ----
  if (window.ScrollTrigger) {
    gsap.registerPlugin(window.ScrollTrigger);
    gsap.to("#progreso", { scaleX: 1, ease: "none", scrollTrigger: { start: 0, end: "max", scrub: .3 } });

    todos(".capturas h2, .recursos h2, .cierre h2").forEach(function (h) {
      gsap.from(h, { opacity: 0, x: mov(-36), duration: .7, ease: "power3.out", scrollTrigger: { trigger: h, start: "top 86%" } });
    });
    gsap.from(".pestanas button", { opacity: 0, y: mov(16), duration: .45, stagger: .06, ease: "power2.out",
      scrollTrigger: { trigger: ".pestanas", start: "top 88%" } });
    gsap.from("#g-explora figure", { opacity: 0, y: mov(40), duration: .6, stagger: .09, ease: "power2.out",
      scrollTrigger: { trigger: "#g-explora .rejilla", start: "top 84%" } });
    gsap.from(".columnas > div", { opacity: 0, y: mov(34), duration: .6, stagger: .12, ease: "power2.out",
      scrollTrigger: { trigger: ".columnas", start: "top 84%" } });
    gsap.from(".cierre p, .cierre .boton", { opacity: 0, y: mov(20), duration: .5, stagger: .1, ease: "power2.out",
      scrollTrigger: { trigger: ".cierre", start: "top 75%" } });
  }
})();

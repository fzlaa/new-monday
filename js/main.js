(() => {
  'use strict';

  const page = document.querySelector('.page');

  /* ---------- Scroll reveal (class set in <head>) ---------- */

  if (document.documentElement.classList.contains('reveal-on')) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-revealed');
        io.unobserve(e.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
    page.querySelectorAll('[data-reveal]').forEach((n) => io.observe(n));
  }

  /* ---------- Mobile menu ---------- */

  const menuBtn = document.querySelector('.menu-toggle');
  const menu = document.getElementById('menu-mobile');

  const setMenu = (open) => {
    menu.hidden = !open;
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.textContent = open ? 'Fermer' : 'Menu';
  };
  menuBtn.addEventListener('click', () => setMenu(menu.hidden));
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !menu.hidden) { setMenu(false); menuBtn.focus(); }
  });
  // Close the menu when the layout switches back to desktop.
  new ResizeObserver(([e]) => { if (e.contentRect.width >= 760 && !menu.hidden) setMenu(false); }).observe(page);

  /* ---------- Film player ---------- */

  // Native <video>: poster + design play button first, then the browser's own
  // controls (pause, volume, fullscreen). Sound is on because play starts from a click.
  const frame = document.querySelector('[data-player]');
  const video = frame.querySelector('video');
  const playBtn = frame.querySelector('[data-player-play]');

  const start = () => {
    frame.classList.add('is-started');
    video.controls = true;
    const p = video.play();
    if (p && p.catch) p.catch(() => {});
    video.focus({ preventScroll: true });
  };

  playBtn.addEventListener('click', start);
  // Before the first play, a click anywhere on the poster starts the film too.
  video.addEventListener('click', () => { if (!frame.classList.contains('is-started')) start(); });
  // Back to the poster and the big play button once the film is over.
  video.addEventListener('ended', () => {
    if (document.fullscreenElement === video) document.exitFullscreen().catch(() => {});
    if (video.webkitDisplayingFullscreen) video.webkitExitFullscreen();
    video.controls = false;
    frame.classList.remove('is-started');
    video.load();
  });

  /* ---------- Testimonials ---------- */

  const QUOTES = [
    { q: '« Je pensais que l’IA, c’était pour les développeurs. Maintenant, c’est moi que mes collègues viennent voir. »', who: 'Nadia B.', img: 'images/temoignage-nadia.jpg', role: 'Assistante de direction, groupe industriel' },
    { q: '« Mon premier compte-rendu en dix minutes. J’ai cru que j’avais oublié quelque chose. »', who: 'Thomas L.', img: 'images/temoignage-thomas.jpg', role: 'Contrôleur de gestion, groupe de distribution' },
    { q: '« On a travaillé sur nos vrais contrats. Le lundi suivant, je m’en servais déjà. »', who: 'Claire M.', img: 'images/temoignage-claire.jpg', role: 'Juriste, groupe de services' },
  ];

  const quotes = document.querySelector('[data-quotes]');
  const fade = quotes.querySelector('.quotes__fade');
  const qText = quotes.querySelector('[data-quote-text]');
  const qWho = quotes.querySelector('[data-quote-who]');
  const qRole = quotes.querySelector('[data-quote-role]');
  const qImg = quotes.querySelector('[data-quote-img]');
  const dotsWrap = quotes.querySelector('[data-quote-dots]');
  let qi = 0;
  let fadeTimer;

  const dots = QUOTES.map((q, i) => {
    const d = document.createElement('button');
    d.type = 'button';
    d.className = 'quotes__dot';
    d.setAttribute('aria-label', 'Témoignage ' + (i + 1) + ' : ' + q.who);
    d.addEventListener('click', () => goQuote(i));
    dotsWrap.appendChild(d);
    return d;
  });
  // Preload the other portraits so the swap stays smooth.
  QUOTES.forEach((q) => { new Image().src = q.img; });
  const syncDots = () => dots.forEach((d, i) => d.setAttribute('aria-current', String(i === qi)));
  syncDots();

  const goQuote = (i) => {
    const next = (i + QUOTES.length) % QUOTES.length;
    if (next === qi) return;
    clearTimeout(fadeTimer);
    fade.classList.add('is-fading');
    fadeTimer = setTimeout(() => {
      qi = next;
      qText.textContent = QUOTES[qi].q;
      qWho.textContent = QUOTES[qi].who;
      qRole.textContent = QUOTES[qi].role;
      qImg.src = QUOTES[qi].img;
      syncDots();
      fade.classList.remove('is-fading');
    }, 220);
  };

  quotes.querySelector('[data-quote-prev]').addEventListener('click', () => goQuote(qi - 1));
  quotes.querySelector('[data-quote-next]').addEventListener('click', () => goQuote(qi + 1));

  /* ---------- FAQ (one answer open at a time) ---------- */

  const items = [...document.querySelectorAll('.faq__item')];
  items.forEach((item) => {
    const btn = item.querySelector('.faq__q');
    btn.addEventListener('click', () => {
      const open = !item.classList.contains('is-open');
      items.forEach((other) => {
        const isTarget = other === item && open;
        other.classList.toggle('is-open', isTarget);
        other.querySelector('.faq__q').setAttribute('aria-expanded', String(isTarget));
      });
    });
  });
})();

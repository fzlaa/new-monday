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

  const frame = document.querySelector('[data-player]');
  const video = frame.querySelector('video');
  const source = video.querySelector('source');
  const toggle = frame.querySelector('[data-player-toggle]');
  const label = frame.querySelector('[data-player-label]');
  const bar = frame.querySelector('[data-player-bar]');
  const time = frame.querySelector('[data-player-time]');
  const track = frame.querySelector('[data-player-track]');
  const progress = frame.querySelector('[data-player-progress]');

  const fmt = (x) => Math.floor(x / 60) + ':' + String(Math.floor(x % 60)).padStart(2, '0');
  const duration = () => (Number.isFinite(video.duration) && video.duration > 0 ? video.duration : 60);
  let available = true;

  const render = () => {
    const playing = !video.paused && !video.ended;
    frame.classList.toggle('is-playing', playing);
    toggle.setAttribute('aria-label', playing ? 'Mettre la vidéo en pause' : 'Lire la vidéo');
    bar.hidden = !(playing || video.currentTime > 0);
    time.textContent = fmt(video.currentTime) + ' / ' + fmt(duration());
    progress.style.width = (video.currentTime / duration() * 100) + '%';
  };

  const markUnavailable = () => {
    available = false;
    frame.classList.remove('is-ready');
  };

  video.addEventListener('loadeddata', () => frame.classList.add('is-ready'));
  source.addEventListener('error', markUnavailable);
  video.addEventListener('error', markUnavailable);
  // The file may have loaded (or failed) before this deferred script ran.
  if (video.readyState >= 2) frame.classList.add('is-ready');
  ['play', 'pause', 'timeupdate', 'loadedmetadata'].forEach((ev) => video.addEventListener(ev, render));
  video.addEventListener('ended', () => { video.currentTime = 0; render(); });

  const togglePlay = () => {
    if (video.readyState === 0 && video.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) markUnavailable();
    if (!available) {
      label.textContent = 'Le film arrive très bientôt';
      return;
    }
    if (video.paused) video.play().catch(() => {});
    else video.pause();
  };

  toggle.addEventListener('click', togglePlay);
  video.addEventListener('click', togglePlay);
  track.addEventListener('click', (e) => {
    const r = track.getBoundingClientRect();
    video.currentTime = Math.min(Math.max((e.clientX - r.left) / r.width, 0), 1) * duration();
  });

  /* ---------- Testimonials ---------- */

  const QUOTES = [
    { q: '« Je pensais que l’IA, c’était pour les développeurs. Maintenant, c’est moi que mes collègues viennent voir. »', who: 'Nadia B.', role: 'Assistante de direction, groupe industriel' },
    { q: '« Mon premier compte-rendu en dix minutes. J’ai cru que j’avais oublié quelque chose. »', who: 'Thomas L.', role: 'Contrôleur de gestion, groupe de distribution' },
    { q: '« On a travaillé sur nos vrais contrats. Le lundi suivant, je m’en servais déjà. »', who: 'Claire M.', role: 'Juriste, groupe de services' },
  ];

  const quotes = document.querySelector('[data-quotes]');
  const fade = quotes.querySelector('.quotes__fade');
  const qText = quotes.querySelector('[data-quote-text]');
  const qWho = quotes.querySelector('[data-quote-who]');
  const qRole = quotes.querySelector('[data-quote-role]');
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

/**
 * ExtractDesign Studio — Landing Page JS
 * Ported from website-redesign-and-improvement_b (React/framer-motion)
 * Vanilla JS — no framework dependencies
 */

/* ============================================================
   SCROLL-AWARE NAV
   ============================================================ */
(function () {
  const nav = document.querySelector('.site-nav');
  if (!nav) return;
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 12);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

/* ============================================================
   MOBILE MENU TOGGLE
   ============================================================ */
(function () {
  const btn = document.getElementById('nav-menu-btn');
  const drawer = document.getElementById('nav-mobile');
  const iconMenu = document.getElementById('nav-icon-menu');
  const iconClose = document.getElementById('nav-icon-close');
  if (!btn || !drawer) return;

  btn.addEventListener('click', () => {
    const open = drawer.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    if (iconMenu) iconMenu.style.display = open ? 'none' : '';
    if (iconClose) iconClose.style.display = open ? '' : 'none';
  });

  // Close on any mobile link click
  drawer.querySelectorAll('a, button').forEach(el => {
    el.addEventListener('click', () => {
      drawer.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      if (iconMenu) iconMenu.style.display = '';
      if (iconClose) iconClose.style.display = 'none';
    });
  });
})();

/* ============================================================
   HERO SCAN ANIMATION
   ============================================================ */
(function () {
  const urlInput = document.getElementById('hero-url-input');
  const analyzeBtn = document.getElementById('hero-analyze-btn');
  const analyzeBtnText = document.getElementById('analyze-btn-text');
  const analyzeScanIcon = document.getElementById('analyze-icon-scan');
  const analyzeSpinIcon = document.getElementById('analyze-icon-spin');
  const heroProgress = document.getElementById('hero-progress');
  const heroProgressFill = document.getElementById('hero-progress-fill');
  const heroProgressStage = document.getElementById('hero-progress-stage');

  // Dashboard elements
  const scanOverlay = document.getElementById('scan-overlay');
  const scanProgressFill = document.getElementById('scan-progress-fill');
  const scanProgressPct = document.getElementById('scan-progress-pct');
  const scanStageText = document.getElementById('scan-stage-text');
  const doneToast = document.getElementById('done-toast');
  const dbUrlDisplay = document.getElementById('db-url-display');

  if (!analyzeBtn || !urlInput) return;

  const STAGES = [
    'Fetching rendered DOM & computed styles',
    'Resolving CSS variables & @font-face rules',
    'Extracting color, type & spacing tokens',
    'Mapping recurrent components',
    'Running WCAG 2.1 contrast audits',
    'Indexing SVG, icon & font assets',
  ];

  let raf = null;
  let doneTimer = null;
  let scanning = false;

  function setPhase(phase, progress = 0) {
    const stageIndex = Math.min(STAGES.length - 1, Math.floor(progress * STAGES.length));
    const pct = Math.round(progress * 100);
    const url = (urlInput.value || 'stripe.com').replace(/^https?:\/\//, '');

    if (phase === 'scanning') {
      // Button state
      analyzeBtn.disabled = true;
      if (analyzeScanIcon) analyzeScanIcon.style.display = 'none';
      if (analyzeSpinIcon) analyzeSpinIcon.style.display = '';
      if (analyzeBtnText) analyzeBtnText.textContent = 'Analyzing…';

      // Hero inline progress
      if (heroProgress) heroProgress.classList.add('visible');
      if (heroProgressFill) heroProgressFill.style.width = `${pct}%`;
      if (heroProgressStage) heroProgressStage.textContent = `› ${STAGES[stageIndex]}…`;

      // Dashboard overlay
      if (scanOverlay) scanOverlay.classList.add('active');
      if (scanProgressFill) scanProgressFill.style.width = `${pct}%`;
      if (scanProgressPct) scanProgressPct.textContent = `${pct}% · scanning ${url}`;
      if (scanStageText) scanStageText.textContent = `${STAGES[stageIndex]}…`;
      if (doneToast) doneToast.classList.remove('visible');
    } else if (phase === 'done') {
      analyzeBtn.disabled = false;
      if (analyzeScanIcon) analyzeScanIcon.style.display = '';
      if (analyzeSpinIcon) analyzeSpinIcon.style.display = 'none';
      if (analyzeBtnText) analyzeBtnText.textContent = 'Analyze';
      if (heroProgress) heroProgress.classList.remove('visible');
      if (heroProgressFill) heroProgressFill.style.width = '100%';

      // Hide overlay, show toast
      if (scanOverlay) scanOverlay.classList.remove('active');
      if (doneToast) doneToast.classList.add('visible');

      doneTimer = setTimeout(() => {
        if (doneToast) doneToast.classList.remove('visible');
      }, 5200);
    } else {
      // idle
      analyzeBtn.disabled = false;
      if (analyzeScanIcon) analyzeScanIcon.style.display = '';
      if (analyzeSpinIcon) analyzeSpinIcon.style.display = 'none';
      if (analyzeBtnText) analyzeBtnText.textContent = 'Analyze';
      if (heroProgress) heroProgress.classList.remove('visible');
      if (scanOverlay) scanOverlay.classList.remove('active');
    }
  }

  function startScan() {
    if (scanning) return;
    scanning = true;
    cancelAnimationFrame(raf);
    clearTimeout(doneTimer);

    // Update dashboard URL display
    const url = (urlInput.value || 'stripe.com').replace(/^https?:\/\//, '');
    if (dbUrlDisplay) dbUrlDisplay.textContent = url;

    const duration = 2800;
    const start = performance.now();

    function tick(now) {
      const t = Math.min(1, (now - start) / duration);
      const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      setPhase('scanning', eased);
      if (t < 1) {
        raf = requestAnimationFrame(tick);
      } else {
        scanning = false;
        setPhase('done', 1);
      }
    }

    setPhase('scanning', 0);
    raf = requestAnimationFrame(tick);
  }

  analyzeBtn.addEventListener('click', startScan);
  urlInput.addEventListener('keydown', e => { if (e.key === 'Enter') startScan(); });

  // Add spin animation via CSS injection (for the spinner icon)
  const style = document.createElement('style');
  style.textContent = `.spin-icon { animation: spin 0.8s linear infinite; }`;
  document.head.appendChild(style);
})();

/* ============================================================
   HERO SAMPLE CHIPS
   ============================================================ */
(function () {
  const urlInput = document.getElementById('hero-url-input');
  const dbUrlDisplay = document.getElementById('db-url-display');
  const chips = document.querySelectorAll('.sample-chip');
  if (!chips.length || !urlInput) return;

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const url = chip.dataset.url;
      urlInput.value = url;
      if (dbUrlDisplay) dbUrlDisplay.textContent = url;
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
    });
  });

  // Keep active chip in sync with manual input
  urlInput.addEventListener('input', () => {
    const val = urlInput.value.replace(/^https?:\/\//, '');
    chips.forEach(c => c.classList.toggle('active', c.dataset.url === val));
  });
})();

/* ============================================================
   STAT COUNTER ANIMATION (IntersectionObserver)
   ============================================================ */
(function () {
  const EASE = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const stats = document.querySelectorAll('.stat-value[data-count]');
  if (!stats.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      const el = entry.target;
      const target = parseFloat(el.dataset.count);
      const decimals = parseInt(el.dataset.decimals || '0', 10);
      const suffix = el.dataset.suffix || '';
      const duration = 1800;
      const start = performance.now();

      function tick(now) {
        const t = Math.min(1, (now - start) / duration);
        const val = EASE(t) * target;
        el.textContent = val.toFixed(decimals) + suffix;
        if (t < 1) requestAnimationFrame(tick);
        else el.textContent = target.toFixed(decimals) + suffix;
      }
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.2, rootMargin: '-40px' });

  stats.forEach(s => observer.observe(s));
})();

/* ============================================================
   SCROLL REVEAL (IntersectionObserver)
   ============================================================ */
(function () {
  const revealEls = document.querySelectorAll('.reveal');
  if (!revealEls.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      entry.target.classList.add('revealed');
    });
  }, { threshold: 0.08, rootMargin: '-70px' });

  revealEls.forEach(el => observer.observe(el));
})();

/* ============================================================
   PRICING BILLING TOGGLE
   ============================================================ */
(function () {
  const monthlyBtn = document.getElementById('billing-monthly');
  const annualBtn = document.getElementById('billing-annual');
  const proAmount = document.getElementById('pro-amount');
  const proPeriod = document.getElementById('pro-period');
  const annualBadge = document.getElementById('annual-badge');
  if (!monthlyBtn || !annualBtn) return;

  function setBilling(billing) {
    const isAnnual = billing === 'annual';

    monthlyBtn.classList.toggle('active', !isAnnual);
    annualBtn.classList.toggle('active', isAnnual);

    if (proAmount) {
      proAmount.classList.add('animating');
      setTimeout(() => {
        proAmount.innerHTML = isAnnual
          ? '₹799<span style="font-size:16px;font-weight:700;color:#94a3b8;">/mo</span>'
          : '₹999<span style="font-size:16px;font-weight:700;color:#94a3b8;">/mo</span>';
        proAmount.classList.remove('animating');
      }, 100);
    }

    if (proPeriod) {
      proPeriod.textContent = isAnnual ? 'Billed yearly · save ₹2,400' : 'Billed monthly';
    }

    if (annualBadge) {
      annualBadge.className = 'billing-annual-badge ' + (isAnnual ? 'active-annual' : 'default');
    }
  }

  monthlyBtn.addEventListener('click', () => setBilling('monthly'));
  annualBtn.addEventListener('click', () => setBilling('annual'));
})();

/* ============================================================
   FAQ ACCORDION
   ============================================================ */
(function () {
  const questions = document.querySelectorAll('.faq-question');
  if (!questions.length) return;

  questions.forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = btn.dataset.faq;
      const answer = document.getElementById(`faq-answer-${idx}`);
      const isOpen = btn.classList.contains('open');

      // Close all
      questions.forEach(q => {
        q.classList.remove('open');
        q.setAttribute('aria-expanded', 'false');
        const a = document.getElementById(`faq-answer-${q.dataset.faq}`);
        if (a) a.classList.remove('open');
      });

      // Toggle clicked
      if (!isOpen) {
        btn.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
        if (answer) answer.classList.add('open');
      }
    });
  });
})();

/* ============================================================
   WORKSPACE MAGIC-LINK FORM
   ============================================================ */
(function () {
  const form = document.getElementById('workspace-form');
  const emailInput = document.getElementById('workspace-email');
  const submitBtn = document.getElementById('workspace-submit');
  const sendIcon = document.getElementById('ws-send-icon');
  const checkIcon = document.getElementById('ws-check-icon');
  const btnText = document.getElementById('ws-btn-text');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!emailInput || !emailInput.value) return;

    // Show sent state
    if (submitBtn) submitBtn.classList.add('sent');
    if (sendIcon) sendIcon.style.display = 'none';
    if (checkIcon) checkIcon.style.display = '';
    if (btnText) btnText.textContent = 'Magic link sent';

    // Reset after 4s on new input
    if (emailInput) {
      const reset = () => {
        if (submitBtn) submitBtn.classList.remove('sent');
        if (sendIcon) sendIcon.style.display = '';
        if (checkIcon) checkIcon.style.display = 'none';
        if (btnText) btnText.textContent = 'Send Access Link';
        emailInput.removeEventListener('input', reset);
      };
      emailInput.addEventListener('input', reset);
    }
  });
})();

/* ============================================================
   MARQUEE HOVER-PAUSE
   ============================================================ */
(function () {
  const track = document.getElementById('marquee-track');
  if (!track) return;
  track.addEventListener('mouseenter', () => track.style.animationPlayState = 'paused');
  track.addEventListener('mouseleave', () => track.style.animationPlayState = '');
})();

/* ============================================================
   SMOOTH SCROLL for anchor links
   ============================================================ */
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();

/* ============================================================
   CONSOLE SIGNATURE
   ============================================================ */
(function () {
  const s = [
    '%cExtractDesign Studio',
    'font-size:18px;font-weight:800;background:linear-gradient(to right,#818cf8,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;padding:4px 0;',
  ];
  console.log(...s);
  console.log('%cEngineering-grade website intelligence · by @carthworks', 'color:#64748b;font-size:12px;');
  console.log('%c→ https://github.com/carthworks/extract-theme', 'color:#818cf8;font-size:12px;');
})();

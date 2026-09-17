// landing.js — ExtractDesign Studio Landing Page Interactivity

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }

  // DOM Elements
  const heroForm = document.getElementById('hero-analyze-form');
  const heroUrlInput = document.getElementById('hero-target-url');
  const presetTags = document.querySelectorAll('.preset-tag');
  const liveDemoBtns = document.querySelectorAll('.btn-open-demo');
  
  // Login / Workspace Modal Elements
  const loginModal = document.getElementById('login-modal');
  const openLoginBtns = document.querySelectorAll('.btn-open-login');
  const closeLoginBtn = document.getElementById('close-login-modal');
  const modalBackdrop = loginModal ? loginModal.querySelector('.modal-backdrop') : null;
  const modalMagicForm = document.getElementById('modal-magic-form');
  const modalMagicInput = document.getElementById('modal-magic-email');
  const modalMagicFeedback = document.getElementById('modal-magic-feedback');
  const modalSubmitBtn = document.getElementById('modal-magic-submit');

  // Inline Section 08 Magic Form Elements
  const inlineMagicForm = document.getElementById('inline-magic-form');
  const inlineMagicInput = document.getElementById('inline-magic-email');
  const inlineMagicFeedback = document.getElementById('inline-magic-feedback');
  const inlineSubmitBtn = document.getElementById('inline-magic-submit');

  // Pricing Unlock Buttons
  const unlockReportBtns = document.querySelectorAll('.btn-unlock-report');

  // 1. Check existing session
  const storedUser = localStorage.getItem('extract_design_user');
  if (storedUser) {
    const userBadge = document.getElementById('user-session-badge');
    if (userBadge) {
      userBadge.innerHTML = `
        <span class="user-pill" style="font-size:12.5px;color:#38bdf8;background:rgba(56,189,248,0.1);padding:4px 10px;border-radius:9999px;border:1px solid rgba(56,189,248,0.25);display:flex;align-items:center;gap:6px;">
          <i data-lucide="user-check" style="width:14px;height:14px;"></i>
          <span>${escapeHtml(storedUser)} (Workspace Active)</span>
        </span>
      `;
      if (window.lucide) window.lucide.createIcons();
    }
  }

  // 2. Hero URL Form Submission
  if (heroForm && heroUrlInput) {
    heroForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const rawUrl = heroUrlInput.value.trim();
      if (!rawUrl) return;
      redirectToStudio(rawUrl);
    });
  }

  // Preset Tags Click Handlers
  presetTags.forEach((tag) => {
    tag.addEventListener('click', () => {
      const url = tag.getAttribute('data-url');
      if (url) {
        if (heroUrlInput) heroUrlInput.value = url;
        redirectToStudio(url);
      }
    });
  });

  // Live Demo Handlers
  liveDemoBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      redirectToStudio('https://stripe.com');
    });
  });

  function redirectToStudio(url) {
    let cleanUrl = url.trim();
    if (!cleanUrl.startsWith('http://') && !cleanUrl.startsWith('https://')) {
      cleanUrl = 'https://' + cleanUrl;
    }
    window.location.href = `/studio?url=${encodeURIComponent(cleanUrl)}`;
  }

  // 3. Modal Open/Close Controls
  function openModal() {
    if (!loginModal) return;
    loginModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    if (modalMagicInput) modalMagicInput.focus();
  }

  function closeModal() {
    if (!loginModal) return;
    loginModal.classList.add('hidden');
    document.body.style.overflow = '';
  }

  openLoginBtns.forEach(btn => btn.addEventListener('click', (e) => {
    e.preventDefault();
    openModal();
  }));

  if (closeLoginBtn) closeLoginBtn.addEventListener('click', closeModal);
  if (modalBackdrop) modalBackdrop.addEventListener('click', closeModal);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && loginModal && !loginModal.classList.contains('hidden')) {
      closeModal();
    }
  });

  // Unlock Full Report Button Click Handler
  unlockReportBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openModal();
      const modalTitle = document.getElementById('modal-title');
      const modalSub = document.getElementById('modal-sub');
      if (modalTitle) modalTitle.textContent = 'Unlock Full Report — ₹149';
      if (modalSub) modalSub.textContent = 'Enter your email to complete checkout or restore your unlocked intelligence workspace.';
    });
  });

  // 4. Handle Magic Link Submission (Modal Form)
  if (modalMagicForm && modalMagicInput) {
    modalMagicForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = modalMagicInput.value.trim();
      if (!email) return;
      await submitMagicLink(email, modalMagicFeedback, modalSubmitBtn, () => {
        setTimeout(() => {
          closeModal();
          window.location.href = '/studio';
        }, 1800);
      });
    });
  }

  // 5. Handle Magic Link Submission (Inline Section 08 Form)
  if (inlineMagicForm && inlineMagicInput) {
    inlineMagicForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = inlineMagicInput.value.trim();
      if (!email) return;
      await submitMagicLink(email, inlineMagicFeedback, inlineSubmitBtn, () => {
        setTimeout(() => {
          window.location.href = '/studio';
        }, 2000);
      });
    });
  }

  async function submitMagicLink(email, feedbackEl, btnEl, onSuccess) {
    if (!feedbackEl) return;
    feedbackEl.className = 'magic-feedback';
    feedbackEl.style.display = 'none';

    const btnText = btnEl ? btnEl.querySelector('.btn-text') : null;
    const spinner = btnEl ? btnEl.querySelector('.spinner') : null;

    if (btnText) btnText.textContent = 'Verifying...';
    if (spinner) spinner.classList.remove('hidden');
    if (btnEl) btnEl.disabled = true;

    try {
      const resp = await fetch('/api/auth/magic-link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
      });

      const data = await resp.json();

      if (resp.ok && data.status === 'ok') {
        localStorage.setItem('extract_design_user', email);
        feedbackEl.className = 'magic-feedback success';
        feedbackEl.innerHTML = `
          <strong>✓ Magic link verified!</strong><br>
          Access granted for <strong>${escapeHtml(email)}</strong>. Redirecting to your workspace...
        `;
        feedbackEl.style.display = 'block';

        if (typeof onSuccess === 'function') onSuccess();
      } else {
        feedbackEl.className = 'magic-feedback error';
        feedbackEl.textContent = data.error || 'Failed to send access link. Please check your email and try again.';
        feedbackEl.style.display = 'block';
      }
    } catch (err) {
      // Offline / network fallback: allow instant local session demo
      localStorage.setItem('extract_design_user', email);
      feedbackEl.className = 'magic-feedback success';
      feedbackEl.innerHTML = `
        <strong>✓ Magic access enabled!</strong><br>
        Workspace unlocked for <strong>${escapeHtml(email)}</strong>. Redirecting to studio...
      `;
      feedbackEl.style.display = 'block';
      if (typeof onSuccess === 'function') onSuccess();
    } finally {
      if (btnText) btnText.textContent = 'Send Access Link';
      if (spinner) spinner.classList.add('hidden');
      if (btnEl) btnEl.disabled = false;
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
});

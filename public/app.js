// app.js - ExtractTheme Studio Workbench Client Application

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const form = document.getElementById('extract-form');
  const targetUrlInput = document.getElementById('target-url');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = submitBtn.querySelector('.btn-text');
  const spinner = submitBtn.querySelector('.spinner');
  
  const toggleFlagsBtn = document.getElementById('toggle-flags');
  const flagsPanel = document.getElementById('flags-panel');
  const flagsArrow = document.getElementById('flags-arrow');

  const flagCrawl = document.getElementById('flag-crawl');
  const flagMaxColors = document.getElementById('flag-max-colors');
  const maxColorsVal = document.getElementById('max-colors-val');
  const flagMinCount = document.getElementById('flag-min-count');
  const minCountVal = document.getElementById('min-count-val');
  const flagColorTolerance = document.getElementById('flag-color-tolerance');
  const colorToleranceVal = document.getElementById('color-tolerance-val');
  const flagRootFontSize = document.getElementById('flag-root-font-size');
  const flagOutputDir = document.getElementById('flag-output-dir');
  const flagNoVerify = document.getElementById('flag-no-verify');

  const terminalSection = document.getElementById('terminal-section');
  const terminalLog = document.getElementById('terminal-log');
  const clearLogBtn = document.getElementById('clear-log-btn');

  const refreshProjectsBtn = document.getElementById('refresh-projects');
  const searchProjectsInput = document.getElementById('search-projects');
  const projectsGrid = document.getElementById('projects-grid');

  const previewModal = document.getElementById('preview-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalFilePath = document.getElementById('modal-file-path');
  const modalCode = document.getElementById('modal-code');
  const modalCopyBtn = document.getElementById('modal-copy-btn');
  const modalCloseBtn = document.getElementById('modal-close');
  const modalBackdrop = previewModal.querySelector('.modal-backdrop');

  const statusBadge = document.querySelector('.status-badge');
  if (statusBadge) {
    statusBadge.innerHTML = `<span class="pulse"></span> Host Active: ${window.location.origin}`;
  }

  let allProjects = [];

  // --- Initial Load ---
  fetchProjects();

  // --- Event Listeners ---

  // Live Slider Values
  flagMaxColors.addEventListener('input', (e) => {
    maxColorsVal.textContent = e.target.value;
  });

  flagMinCount.addEventListener('input', (e) => {
    minCountVal.textContent = e.target.value;
  });

  flagColorTolerance.addEventListener('input', (e) => {
    colorToleranceVal.textContent = e.target.value;
  });

  // Toggle Flags Panel Accordion
  toggleFlagsBtn.addEventListener('click', () => {
    const isHidden = flagsPanel.classList.toggle('hidden');
    flagsArrow.textContent = isHidden ? '▼' : '▲';
  });

  // Preset Pills Click
  document.querySelectorAll('.preset-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      targetUrlInput.value = pill.dataset.url;
      targetUrlInput.focus();
    });
  });

  // Clear Terminal Log
  clearLogBtn.addEventListener('click', () => {
    terminalLog.textContent = '';
  });

  // Refresh Projects
  refreshProjectsBtn.addEventListener('click', fetchProjects);

  // Search Filter Projects
  searchProjectsInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().strip ? e.target.value.toLowerCase().trim() : '';
    renderProjects(allProjects.filter(p => p.domain.toLowerCase().includes(query)));
  });

  // Form Submit Execution
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = targetUrlInput.value.trim();
    if (!url) return;

    // Show Terminal
    terminalSection.classList.remove('hidden');
    terminalLog.textContent = `🚀 Initializing extraction pipeline for: ${url}\n`;
    terminalLog.textContent += `▸ Connecting to server background task...\n\n`;

    // Disable Submit Button
    submitBtn.disabled = true;
    btnText.textContent = 'Extracting...';
    spinner.classList.remove('hidden');

    const payload = {
      url: url,
      crawl: parseInt(flagCrawl.value, 10),
      max_colors: parseInt(flagMaxColors.value, 10),
      min_count: parseInt(flagMinCount.value, 10),
      color_tolerance: parseFloat(flagColorTolerance.value),
      root_font_size: parseInt(flagRootFontSize.value, 10),
      output_dir: flagOutputDir.value.trim(),
      no_verify: flagNoVerify.checked,
    };

    try {
      const response = await fetch('/api/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.body) {
        throw new Error('ReadableStream not supported by browser response.');
      }

      terminalLog.textContent = '';
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value, { stream: true });
        terminalLog.textContent += text;
        terminalLog.scrollTop = terminalLog.scrollHeight;
      }

      // Refresh projects list after stream finishes
      await fetchProjects();

      // Auto scroll to projects section
      document.querySelector('.projects-section').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
      terminalLog.textContent += `\n❌ NETWORK ERROR: ${err.message}\n`;
    } finally {
      submitBtn.disabled = false;
      btnText.textContent = '⚡ Extract Design System';
      spinner.classList.add('hidden');
    }
  });

  // --- API Functions ---

  async function fetchProjects() {
    try {
      const res = await fetch('/api/projects');
      if (!res.ok) {
        throw new Error(`HTTP ${res.status} ${res.statusText}`);
      }
      const data = await res.json();
      allProjects = data.projects || [];
      renderProjects(allProjects);
    } catch (err) {
      console.error('fetchProjects error:', err);
      projectsGrid.innerHTML = `<div class="skeleton-card" style="color:var(--danger)">Failed to load extracted projects from server (${err.message}).</div>`;
    }
  }

  function renderProjects(projects) {
    if (!projects || projects.length === 0) {
      projectsGrid.innerHTML = `
        <div class="skeleton-card" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
          <p style="font-size: 16px; margin-bottom: 8px;">No design systems extracted yet.</p>
          <p style="color: var(--text-sub); font-size: 13px;">Enter a URL above to extract your first theme!</p>
        </div>
      `;
      return;
    }

    projectsGrid.innerHTML = projects.map(proj => {
      const meta = proj.meta || {};
      const logoFile = meta.logo ? (meta.logo.logo_svg || meta.logo.logo_img || meta.logo.favicon) : null;

      const logoThumb = logoFile 
        ? `<img src="/output/${encodeURIComponent(proj.domain)}/${encodeURIComponent(logoFile)}" class="project-logo-thumb" alt="Logo">`
        : `<div class="project-logo-thumb" style="display:flex;align-items:center;justify-content:center;font-size:16px;">🌐</div>`;

      const formattedDate = meta.generated ? new Date(meta.generated).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : 'Extracted';

      const frameworkPills = (meta.frameworks || []).map(fw => 
        `<span class="stat-pill fw-pill">${escapeHtml(fw)}</span>`
      ).join('');

      const topColors = meta.top_colors || [];
      const colorChipsHtml = topColors.length > 0 
        ? `<div class="theme-color-bar" title="Site extracted color palette">
            ${topColors.map(hex => `<div class="color-swatch-chip" style="background:${escapeHtml(hex)}" title="${escapeHtml(hex)}"></div>`).join('')}
           </div>`
        : '';

      return `
        <div class="project-card">
          <div>
            <div class="project-card-header">
              <div class="project-title-area">
                ${logoThumb}
                <div>
                  <div class="project-domain">${escapeHtml(proj.domain)}</div>
                  <div class="project-date">${formattedDate}</div>
                </div>
              </div>
            </div>

            ${colorChipsHtml}

            <div class="project-stats-pills">
              <span class="stat-pill">🎨 Colors: <strong>${meta.colors_count || 0}</strong></span>
              <span class="stat-pill">🔤 Fonts: <strong>${meta.fonts_count || 0}</strong></span>
              <span class="stat-pill">📦 Font Files: <strong>${meta.font_files_count || 0}</strong></span>
              <span class="stat-pill">✨ Gradients: <strong>${meta.gradients_count || 0}</strong></span>
              ${frameworkPills}
            </div>
          </div>

          <div class="project-actions">
            ${proj.has_style_guide ? `<a href="/output/${encodeURIComponent(proj.domain)}/style-guide.html" target="_blank" class="btn btn-primary">🚀 Style Guide</a>` : ''}
            <button type="button" class="btn btn-secondary view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="DESIGN.md">📝 DESIGN.md</button>
            ${proj.has_tokens ? `<button type="button" class="btn btn-secondary view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="design-tokens.json">Tokens</button>` : ''}
            <button type="button" class="btn btn-secondary view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="theme.css">CSS</button>
          </div>
        </div>
      `;
    }).join('');

    // Attach click listeners to view tokens/css buttons
    document.querySelectorAll('.view-tokens-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        openFilePreview(btn.dataset.domain, btn.dataset.file);
      });
    });
  }

  async function openFilePreview(domain, file) {
    modalTitle.textContent = `${domain} / ${file}`;
    modalFilePath.textContent = `${domain}/${file}`;
    modalCode.textContent = 'Loading content...';
    previewModal.classList.remove('hidden');

    try {
      const res = await fetch(`/output/${encodeURIComponent(domain)}/${encodeURIComponent(file)}`);
      const text = await res.text();
      modalCode.textContent = text;
    } catch (err) {
      modalCode.textContent = `Error loading file: ${err.message}`;
    }
  }

  // Close Modal
  function closeModal() {
    previewModal.classList.add('hidden');
  }

  modalCloseBtn.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', closeModal);

  // Copy Code to Clipboard
  modalCopyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(modalCode.textContent);
    const originalText = modalCopyBtn.textContent;
    modalCopyBtn.textContent = '✅ Copied!';
    setTimeout(() => {
      modalCopyBtn.textContent = originalText;
    }, 1500);
  });

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
});

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
  const projectsTableWrapper = document.getElementById('projects-table-wrapper');
  const projectsTableBody = document.getElementById('projects-table-body');
  const viewCardBtn = document.getElementById('view-card-btn');
  const viewTableBtn = document.getElementById('view-table-btn');
  const projectsCount = document.getElementById('projects-count');

  const previewModal = document.getElementById('preview-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalFilePath = document.getElementById('modal-file-path');
  const modalCode = document.getElementById('modal-code');
  const modalCopyBtn = document.getElementById('modal-copy-btn');
  const modalCloseBtn = document.getElementById('modal-close');
  const modalBackdrop = previewModal.querySelector('.modal-backdrop');

  const statusBadge = document.querySelector('.status-badge');

  const paginationWrapper = document.getElementById('pagination-wrapper');
  const paginationSummary = document.getElementById('pagination-summary');
  const prevPageBtn = document.getElementById('prev-page-btn');
  const nextPageBtn = document.getElementById('next-page-btn');
  const paginationPages = document.getElementById('pagination-pages');
  const pageSizeSelect = document.getElementById('page-size-select');

  // --- Lucide Icon Helper ---
  function refreshIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  function icon(name, extraClass = 'icon-sm', extraStyle = '') {
    return `<i data-lucide="${name}" class="${extraClass}" ${extraStyle ? `style="${extraStyle}"` : ''}></i>`;
  }

  // Initial Icon Rendering
  refreshIcons();

  if (statusBadge) {
    statusBadge.innerHTML = `<span class="pulse"></span> Host Active: ${window.location.origin}`;
  }

  let allProjects = [];
  let filteredProjects = [];
  let currentPage = 1;
  const storedPageSize = localStorage.getItem('extract_theme_pagesize') || '6';
  let pageSize = storedPageSize === 'all' ? 'all' : parseInt(storedPageSize, 10);
  if (pageSizeSelect) {
    pageSizeSelect.value = String(storedPageSize);
  }

  let currentView = localStorage.getItem('extract_theme_view') || 'cards';
  applyViewMode(currentView);

  if (viewCardBtn && viewTableBtn) {
    viewCardBtn.addEventListener('click', () => {
      currentView = 'cards';
      localStorage.setItem('extract_theme_view', 'cards');
      applyViewMode('cards');
    });

    viewTableBtn.addEventListener('click', () => {
      currentView = 'table';
      localStorage.setItem('extract_theme_view', 'table');
      applyViewMode('table');
    });
  }

  function applyViewMode(view) {
    if (!viewCardBtn || !viewTableBtn || !projectsGrid || !projectsTableWrapper) return;
    if (view === 'table') {
      viewTableBtn.classList.add('active');
      viewCardBtn.classList.remove('active');
      projectsTableWrapper.classList.remove('hidden');
      projectsGrid.classList.add('hidden');
    } else {
      viewCardBtn.classList.add('active');
      viewTableBtn.classList.remove('active');
      projectsGrid.classList.remove('hidden');
      projectsTableWrapper.classList.add('hidden');
    }
    refreshIcons();
  }

  // --- Pagination Controls Listeners ---
  if (prevPageBtn) {
    prevPageBtn.addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage--;
        renderPaginatedView();
      }
    });
  }

  if (nextPageBtn) {
    nextPageBtn.addEventListener('click', () => {
      const totalPages = pageSize === 'all' ? 1 : Math.ceil(filteredProjects.length / pageSize);
      if (currentPage < totalPages) {
        currentPage++;
        renderPaginatedView();
      }
    });
  }

  if (pageSizeSelect) {
    pageSizeSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      pageSize = val === 'all' ? 'all' : parseInt(val, 10);
      localStorage.setItem('extract_theme_pagesize', val);
      currentPage = 1;
      renderPaginatedView();
    });
  }

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
    if (flagsArrow) {
      flagsArrow.setAttribute('data-lucide', isHidden ? 'chevron-down' : 'chevron-up');
      refreshIcons();
    }
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
  refreshProjectsBtn.addEventListener('click', async () => {
    refreshProjectsBtn.disabled = true;
    refreshProjectsBtn.innerHTML = `${icon('rotate-cw', 'icon-sm spin')} <span>Refreshing...</span>`;
    refreshIcons();
    try {
      await fetchProjects();
    } finally {
      refreshProjectsBtn.disabled = false;
      refreshProjectsBtn.innerHTML = `${icon('rotate-cw', 'icon-sm')} <span>Refresh</span>`;
      refreshIcons();
    }
  });

  // Search Filter Projects
  searchProjectsInput.addEventListener('input', (e) => {
    const query = e.target.value.trim().toLowerCase();
    filteredProjects = query ? allProjects.filter(p => p.domain.toLowerCase().includes(query)) : allProjects;
    currentPage = 1;
    renderPaginatedView();
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
    refreshIcons();

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
      btnText.textContent = 'Extract';
      spinner.classList.add('hidden');
      refreshIcons();
    }
  });

  // --- API Functions ---

  async function fetchProjects() {
    try {
      const res = await fetch(`/api/projects?_t=${Date.now()}`, {
        cache: 'no-store',
        headers: { 'Cache-Control': 'no-cache' }
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status} ${res.statusText}`);
      }
      const data = await res.json();
      allProjects = data.projects || [];
      if (statusBadge) {
        if (data.storage_configured) {
          statusBadge.innerHTML = `<span class="pulse" style="background:#10b981;box-shadow:0 0 8px rgba(16,185,129,0.5)"></span> Cloud Storage: Connected`;
          statusBadge.title = 'Persistent S3 / R2 storage active';
        } else {
          statusBadge.innerHTML = `<span class="pulse" style="background:#f59e0b;box-shadow:0 0 8px rgba(245,158,11,0.5)"></span> Storage: Local Ephemeral`;
          statusBadge.title = 'S3 / R2 not configured. Files stored on local disk only.';
        }
      }
      const query = searchProjectsInput.value.trim().toLowerCase();
      filteredProjects = query ? allProjects.filter(p => p.domain.toLowerCase().includes(query)) : allProjects;
      renderPaginatedView();
    } catch (err) {
      console.error('fetchProjects error:', err);
      projectsGrid.innerHTML = `<div class="skeleton-card" style="color:var(--danger)">Failed to load extracted projects from server (${err.message}).</div>`;
    }
  }

  function renderPaginatedView() {
    if (projectsCount) {
      projectsCount.textContent = (filteredProjects || []).length;
    }

    if (!filteredProjects || filteredProjects.length === 0) {
      const emptyHtml = `
        <div class="skeleton-card" style="grid-column: 1 / -1; text-align: center; padding: 48px 24px;">
          <div style="margin-bottom: 12px; color: var(--primary);">${icon('folder-open', 'icon-lg')}</div>
          <p style="font-size: 16px; font-weight: 600; margin-bottom: 6px;">No design systems found</p>
          <p style="color: var(--text-sub); font-size: 13px;">Enter a URL in the left sidebar to extract a new theme.</p>
        </div>
      `;
      projectsGrid.innerHTML = emptyHtml;
      if (projectsTableBody) {
        projectsTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-sub);">${icon('inbox', 'icon-md', 'display:block;margin:0 auto 8px auto;')}No extracted design systems found.</td></tr>`;
      }
      if (paginationWrapper) {
        paginationWrapper.classList.add('hidden');
      }
      refreshIcons();
      return;
    }

    const total = filteredProjects.length;
    const effectivePageSize = pageSize === 'all' ? total : pageSize;
    const totalPages = Math.max(1, Math.ceil(total / effectivePageSize));

    currentPage = Math.max(1, Math.min(currentPage, totalPages));

    const startIdx = (currentPage - 1) * effectivePageSize;
    const endIdx = Math.min(startIdx + effectivePageSize, total);
    const visibleProjects = filteredProjects.slice(startIdx, endIdx);

    // Render Cards Format
    projectsGrid.innerHTML = visibleProjects.map(proj => {
      const meta = proj.meta || {};
      const logoFile = meta.logo ? (meta.logo.logo_svg || meta.logo.logo_img || meta.logo.favicon) : null;

      const logoThumb = logoFile 
        ? `<img src="/output/${encodeURIComponent(proj.domain)}/${encodeURIComponent(logoFile)}" class="project-logo-thumb" alt="Logo">`
        : `<div class="project-logo-thumb" style="display:flex;align-items:center;justify-content:center;">${icon('globe', 'icon-sm', 'color:var(--text-sub);')}</div>`;

      const formattedDate = meta.generated ? new Date(meta.generated).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : 'Extracted';

      const frameworkPills = (meta.frameworks || []).map(fw => 
        `<span class="stat-pill fw-pill">${icon('layers', 'icon-xs')} ${escapeHtml(fw)}</span>`
      ).join('');

      const topColors = meta.top_colors || [];
      const colorChipsHtml = topColors.length > 0 
        ? `<div class="theme-color-bar" title="Site extracted color palette">
            ${topColors.map(hex => `<div class="color-swatch-chip" style="background:${escapeHtml(hex)}" title="${escapeHtml(hex)}"></div>`).join('')}
           </div>`
        : '';

      const brandTitle = meta.brand_name || proj.domain;
      const copyrightText = meta.copyright || `© 2026 ${brandTitle}. All rights reserved.`;

      return `
        <div class="project-card">
          <div>
            <div class="project-card-header">
              <div class="project-title-area">
                ${logoThumb}
                <div>
                  <div class="project-brand-title">${escapeHtml(brandTitle)}</div>
                  <div class="project-domain-row">
                    <span class="project-domain">${escapeHtml(proj.domain)}</span>
                    <span class="project-date-inline">&bull; ${formattedDate}</span>
                  </div>
                </div>
              </div>
            </div>

            ${colorChipsHtml}

            <div class="project-stats-pills">
              <span class="stat-pill">${icon('palette', 'icon-xs')} Colors: <strong>${meta.colors_count || 0}</strong></span>
              <span class="stat-pill">${icon('type', 'icon-xs')} Fonts: <strong>${meta.fonts_count || 0}</strong></span>
              <span class="stat-pill">${icon('folder-archive', 'icon-xs')} Files: <strong>${meta.font_files_count || 0}</strong></span>
              <span class="stat-pill">${icon('sparkles', 'icon-xs')} Gradients: <strong>${meta.gradients_count || 0}</strong></span>
              ${frameworkPills}
            </div>

            <div class="card-copyright-row" title="${escapeHtml(meta.legal_notice || copyrightText)}">
              ${icon('shield-check', 'icon-xs', 'color:var(--text-muted);')}
              <span class="copyright-text">${escapeHtml(copyrightText)}</span>
            </div>
          </div>

          <div class="project-actions">
            ${proj.has_style_guide ? `<a href="/output/${encodeURIComponent(proj.domain)}/style-guide.html" target="_blank" class="btn btn-primary btn-icon btn-sm" title="Launch Interactive Style Guide">${icon('external-link', 'icon-xs')} <span>Launch</span></a>` : ''}
            <a href="/api/download?domain=${encodeURIComponent(proj.domain)}" class="btn btn-download btn-icon btn-sm" download title="Download complete design system ZIP">${icon('download', 'icon-xs')} <span>Download</span></a>
            <button type="button" class="btn btn-secondary btn-sm view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="DESIGN.md">${icon('file-text', 'icon-xs')} <span>DESIGN.md</span></button>
            ${proj.has_tokens ? `<button type="button" class="btn btn-secondary btn-sm view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="design-tokens.json">${icon('code-2', 'icon-xs')} <span>Tokens</span></button>` : ''}
            <button type="button" class="btn btn-secondary btn-sm view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="theme.css">${icon('file-code', 'icon-xs')} <span>CSS</span></button>
          </div>
        </div>
      `;
    }).join('');

    // Render Table Format
    if (projectsTableBody) {
      projectsTableBody.innerHTML = visibleProjects.map(proj => {
        const meta = proj.meta || {};
        const logoFile = meta.logo ? (meta.logo.logo_svg || meta.logo.logo_img || meta.logo.favicon) : null;

        const logoThumb = logoFile 
          ? `<img src="/output/${encodeURIComponent(proj.domain)}/${encodeURIComponent(logoFile)}" class="project-logo-thumb" style="width:26px;height:26px;" alt="Logo">`
          : `<div class="project-logo-thumb" style="width:26px;height:26px;display:flex;align-items:center;justify-content:center;">${icon('globe', 'icon-xs', 'color:var(--text-sub);')}</div>`;

        const formattedDate = meta.generated ? new Date(meta.generated).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }) : 'Recent';

        const topColors = (meta.top_colors || []).slice(0, 5);
        const colorChipsHtml = topColors.length > 0 
          ? `<div class="table-color-bar">
              ${topColors.map(hex => `<div class="table-color-chip" style="background:${escapeHtml(hex)}" title="${escapeHtml(hex)}"></div>`).join('')}
             </div>`
          : '';

        const frameworkBadges = (meta.frameworks || []).slice(0, 2).map(fw => 
          `<span class="stat-pill fw-pill" style="font-size:9.5px;padding:1px 4px;">${icon('layers', 'icon-xs')} ${escapeHtml(fw)}</span>`
        ).join('');

        const brandTitle = meta.brand_name || proj.domain;
        const copyrightText = meta.copyright || `© 2026 ${brandTitle}. All rights reserved.`;

        return `
          <tr>
            <td>
              <div class="table-site-cell">
                ${logoThumb}
                <div class="table-site-info">
                  <div class="table-brand-title">${escapeHtml(brandTitle)}</div>
                  <div class="table-domain-meta">
                    <span class="table-domain">${escapeHtml(proj.domain)}</span>
                    <span class="project-date" style="font-size:9.5px;">&bull; ${formattedDate}</span>
                  </div>
                  <div class="table-copyright-pill" title="${escapeHtml(meta.legal_notice || copyrightText)}">
                    ${icon('shield-check', 'icon-xs')} <span>${escapeHtml(copyrightText)}</span>
                  </div>
                </div>
              </div>
            </td>
            <td>
              <div class="table-palette-wrap">
                ${colorChipsHtml}
                <span class="stat-pill" style="font-size:9.5px;padding:1px 4px;">${icon('palette', 'icon-xs')} ${meta.colors_count || 0}</span>
              </div>
            </td>
            <td>
              <div style="display:flex;gap:3px;flex-wrap:wrap;align-items:center;">
                <span class="stat-pill" style="font-size:9.5px;padding:1px 4px;">${icon('type', 'icon-xs')} ${meta.fonts_count || 0}</span>
                <span class="stat-pill" style="font-size:9.5px;padding:1px 4px;">${icon('folder-archive', 'icon-xs')} ${meta.font_files_count || 0}</span>
                ${frameworkBadges}
              </div>
            </td>
            <td>
              <div style="display:flex;gap:3px;">
                <button type="button" class="btn btn-secondary btn-table-inspect view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="DESIGN.md" title="View DESIGN.md">${icon('file-text', 'icon-xs')} <span>Doc</span></button>
                ${proj.has_tokens ? `<button type="button" class="btn btn-secondary btn-table-inspect view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="design-tokens.json" title="View JSON Tokens">${icon('code-2', 'icon-xs')} <span>Tokens</span></button>` : ''}
                <button type="button" class="btn btn-secondary btn-table-inspect view-tokens-btn" data-domain="${escapeHtml(proj.domain)}" data-file="theme.css" title="View Theme CSS">${icon('file-code', 'icon-xs')} <span>CSS</span></button>
              </div>
            </td>
            <td>
              <div class="table-actions-cell">
                <a href="/api/download?domain=${encodeURIComponent(proj.domain)}" class="btn btn-download btn-icon btn-table-action" download title="Download ${escapeHtml(proj.domain)} Design System ZIP">
                  ${icon('download', 'icon-xs')} <span>Download</span>
                </a>
                ${proj.has_style_guide ? `
                  <a href="/output/${encodeURIComponent(proj.domain)}/style-guide.html" target="_blank" class="btn btn-primary btn-icon btn-table-action" title="Launch ${escapeHtml(proj.domain)} Style Guide">
                    ${icon('external-link', 'icon-xs')} <span>Launch</span>
                  </a>
                ` : ''}
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }

    // Attach click listeners to view tokens/css buttons in both card and table views
    document.querySelectorAll('.view-tokens-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        openFilePreview(btn.dataset.domain, btn.dataset.file);
      });
    });

    // Update Pagination UI Elements
    if (paginationWrapper) {
      paginationWrapper.classList.remove('hidden');
    }

    if (paginationSummary) {
      paginationSummary.textContent = `Showing ${startIdx + 1}–${endIdx} of ${total}`;
    }

    if (prevPageBtn) {
      prevPageBtn.disabled = currentPage <= 1;
    }

    if (nextPageBtn) {
      nextPageBtn.disabled = currentPage >= totalPages;
    }

    if (paginationPages) {
      paginationPages.innerHTML = '';
      if (totalPages <= 1) {
        paginationPages.innerHTML = `<button type="button" class="page-num-btn active">1</button>`;
      } else {
        for (let i = 1; i <= totalPages; i++) {
          if (totalPages > 7) {
            if (i !== 1 && i !== totalPages && Math.abs(i - currentPage) > 1) {
              if (i === 2 || i === totalPages - 1) {
                const ellipsis = document.createElement('span');
                ellipsis.className = 'page-ellipsis';
                ellipsis.textContent = '...';
                paginationPages.appendChild(ellipsis);
              }
              continue;
            }
          }
          const pageBtn = document.createElement('button');
          pageBtn.type = 'button';
          pageBtn.className = `page-num-btn ${i === currentPage ? 'active' : ''}`;
          pageBtn.textContent = i;
          pageBtn.addEventListener('click', () => {
            currentPage = i;
            renderPaginatedView();
          });
          paginationPages.appendChild(pageBtn);
        }
      }
    }

    // Refresh all Lucide icons in newly rendered DOM
    refreshIcons();
  }

  async function openFilePreview(domain, file) {
    const proj = allProjects.find(p => p.domain === domain) || {};
    const meta = proj.meta || {};
    const brandTitle = meta.brand_name || domain;
    const copyrightText = meta.copyright || `© 2026 ${brandTitle}. All rights reserved.`;

    modalTitle.innerHTML = `<span style="font-weight:700;color:var(--text-main);">${escapeHtml(brandTitle)}</span> <span style="font-size:12px;color:var(--text-sub);font-weight:400;">(${escapeHtml(domain)})</span> &bull; <span style="color:var(--primary);font-size:13px;font-family:var(--font-mono);">${escapeHtml(file)}</span>`;
    modalFilePath.innerHTML = `<span style="display:inline-flex;align-items:center;gap:6px;"><span class="modal-path-tag">${escapeHtml(domain)}/${escapeHtml(file)}</span> <span class="modal-copy-pill" title="${escapeHtml(meta.legal_notice || copyrightText)}">${icon('shield-check', 'icon-xs')} ${escapeHtml(copyrightText)}</span></span>`;
    modalCode.textContent = 'Loading content...';
    previewModal.classList.remove('hidden');
    refreshIcons();

    try {
      const res = await fetch(`/output/${encodeURIComponent(domain)}/${encodeURIComponent(file)}`);
      const text = await res.text();
      modalCode.textContent = text;
    } catch (err) {
      modalCode.textContent = `Error loading file: ${err.message}`;
    }
    refreshIcons();
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
    const origHtml = modalCopyBtn.innerHTML;
    modalCopyBtn.innerHTML = `${icon('check', 'icon-xs')} <span>Copied!</span>`;
    refreshIcons();
    setTimeout(() => {
      modalCopyBtn.innerHTML = origHtml;
      refreshIcons();
    }, 1500);
  });

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
});


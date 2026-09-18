// app.js - ExtractDesign Studio Workbench Client Application

// =========================================================================
// 🚀 Developer Console Signature & Interactive DevTools Helper
// =========================================================================
(function initConsoleSignature() {
  if (typeof window === 'undefined' || window.__EXTRACT_DESIGN_SIGNATURE__) return;
  window.__EXTRACT_DESIGN_SIGNATURE__ = true;

  const headerStyle = 'font-size: 14px; font-weight: 700; background: linear-gradient(135deg, #6366f1, #06b6d4); color: #ffffff; padding: 6px 14px; border-radius: 6px; text-shadow: 0 1px 2px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.15);';
  const labelStyle = 'font-weight: 600; color: #06b6d4;';
  const textStyle = 'color: #94a3b8;';
  const linkStyle = 'color: #818cf8; font-weight: 500; text-decoration: underline;';
  const quoteStyle = 'font-style: italic; color: #10b981;';
  const tipStyle = 'font-family: monospace; color: #38bdf8; background: rgba(56,189,248,0.1); padding: 2px 6px; border-radius: 4px;';

  console.log('%c🎨 ExtractDesign Studio v2.0.0 — Reverse-Engineering Engine', headerStyle);
  console.log(
    '%c👨‍💻 Developer:%c Karthikeyan T (@carthworks)\n' +
    '%c✉️  Email:     %ctkarthikeyan@gmail.com\n' +
    '%c💼 LinkedIn:  %chttps://www.linkedin.com/in/carthworks\n' +
    '%c🐙 GitHub:    %chttps://github.com/carthworks\n' +
    '%c🌐 Portfolio: %chttps://carthworks.github.io\n' +
    '%c📦 Project:   %chttps://github.com/carthworks/extract-theme\n' +
    '%c📜 License:   %cApache-2.0\n' +
    '%c✨ Mission:   %c"Reverse-engineer design systems, UI components & website intelligence from any live URL."',
    labelStyle, textStyle,
    labelStyle, textStyle,
    labelStyle, linkStyle,
    labelStyle, linkStyle,
    labelStyle, linkStyle,
    labelStyle, linkStyle,
    labelStyle, textStyle,
    labelStyle, quoteStyle
  );

  console.log(
    '%c💡 DevTools Tip:%c Run %cExtractDesign.help()%c to inspect projects and interactive tools!',
    'font-weight:bold; color:#f59e0b;',
    'color:#94a3b8;',
    tipStyle,
    'color:#94a3b8;'
  );

  // Global Interactive DevTools API
  window.ExtractDesign = {
    version: '2.0.0',
    developer: {
      name: 'Karthikeyan T',
      handle: '@carthworks',
      email: 'tkarthikeyan@gmail.com',
      linkedIn: 'https://www.linkedin.com/in/carthworks',
      github: 'https://github.com/carthworks',
      portfolio: 'https://carthworks.github.io'
    },
    project: {
      name: 'ExtractDesign Studio',
      repo: 'https://github.com/carthworks/extract-theme',
      license: 'Apache-2.0'
    },
    security: {
      contact: 'tkarthikeyan@gmail.com',
      policy: 'Report vulnerabilities responsibly via GitHub issues or direct email.'
    },
    help: () => {
      console.table({
        'ExtractDesign.inspect(domain)': 'Open intelligence dashboard for any domain (e.g. ExtractDesign.inspect("stripe.com"))',
        'ExtractDesign.listProjects()': 'List all currently extracted design systems and metadata in console table',
        'ExtractDesign.developer': 'Developer profile and social contact links',
        'ExtractDesign.project': 'Repository, version, and licensing details',
        'ExtractDesign.security': 'Security disclosure and vulnerability contact'
      });
      return '🚀 ExtractDesign DevTools helper ready!';
    },
    inspect: (domain) => {
      if (typeof window.openIntelligenceDashboard === 'function') {
        window.openIntelligenceDashboard(domain);
        return `Opening dashboard for ${domain}...`;
      }
      return 'Dashboard controller initializing...';
    },
    listProjects: () => {
      if (window.__EXTRACT_DESIGN_PROJECTS__) {
        console.table(window.__EXTRACT_DESIGN_PROJECTS__.map(p => ({
          domain: p.domain,
          archetype: p.meta?.style_archetype || 'Modern Web',
          components: p.meta?.components_count || 0,
          colors: p.meta?.colors_count || 0,
          a11yScore: p.meta?.intelligence_scores?.accessibility ?? 'N/A',
          seoScore: p.meta?.intelligence_scores?.seo ?? 'N/A'
        })));
        return `${window.__EXTRACT_DESIGN_PROJECTS__.length} projects loaded.`;
      }
      return 'No projects loaded yet.';
    }
  };
})();

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
  const sortSelect = document.getElementById('sort-projects');

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
  let activeSort = localStorage.getItem('extract_theme_sort') || 'newest';
  let newlyScannedDomain = null;

  if (sortSelect) {
    sortSelect.value = activeSort;
    sortSelect.addEventListener('change', (e) => {
      activeSort = e.target.value;
      localStorage.setItem('extract_theme_sort', activeSort);
      const query = searchProjectsInput ? searchProjectsInput.value.trim().toLowerCase() : '';
      filteredProjects = query ? allProjects.filter(p => p.domain.toLowerCase().includes(query)) : allProjects;
      filteredProjects = sortProjectsList(filteredProjects, activeSort);
      currentPage = 1;
      renderPaginatedView();
    });
  }

  function sortProjectsList(list, sortMode = activeSort) {
    const getTs = (p) => {
      if (!p) return 0;
      const meta = p.meta || {};
      if (typeof meta.timestamp === 'number' && meta.timestamp > 0) return meta.timestamp * 1000;
      if (meta.generated) {
        const parsed = Date.parse(meta.generated);
        if (!isNaN(parsed)) return parsed;
      }
      return 0;
    };

    return [...list].sort((a, b) => {
      if (newlyScannedDomain && sortMode === 'newest') {
        const aMatch = a.domain && a.domain.toLowerCase() === newlyScannedDomain.toLowerCase();
        const bMatch = b.domain && b.domain.toLowerCase() === newlyScannedDomain.toLowerCase();
        if (aMatch && !bMatch) return -1;
        if (!aMatch && bMatch) return 1;
      }
      if (sortMode === 'newest') {
        return getTs(b) - getTs(a); // Newest / latest scan first
      } else if (sortMode === 'oldest') {
        return getTs(a) - getTs(b);
      } else if (sortMode === 'alpha-asc') {
        return (a.domain || '').localeCompare(b.domain || '');
      } else if (sortMode === 'alpha-desc') {
        return (b.domain || '').localeCompare(a.domain || '');
      }
      return getTs(b) - getTs(a);
    });
  }

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
  fetchProjects().then(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const qUrl = searchParams.get('url');
    if (qUrl) {
      targetUrlInput.value = qUrl;
      const cleanHost = qUrl.replace(/^https?:\/\//i, '').replace(/^www\./i, '').split('/')[0].replace(/[^\w.-]/g, '_');
      const existing = (allProjects || []).find(p => p.domain === cleanHost || p.domain.replace(/_/g, '.') === cleanHost);
      if (existing) {
        openIntelligenceDashboard(existing.domain);
      }
    }
  });

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
    filteredProjects = sortProjectsList(filteredProjects, activeSort);
    currentPage = 1;
    renderPaginatedView();
  });

  // Form Submit Execution
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = targetUrlInput.value.trim();
    if (!url) return;

    // Track newly scanned domain name to guarantee top placement
    try {
      const parsed = new URL(url.startsWith('http') ? url : `https://${url}`);
      newlyScannedDomain = parsed.hostname.replace(/^www\./, '').toLowerCase().replace(/[^\w.-]/g, '_');
    } catch (_) {
      newlyScannedDomain = url.replace(/^https?:\/\//i, '').replace(/^www\./i, '').split('/')[0].toLowerCase().replace(/[^\w.-]/g, '_');
    }

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

      // Reset search filter and guarantee Newest First ordering
      if (searchProjectsInput) searchProjectsInput.value = '';
      activeSort = 'newest';
      if (sortSelect) sortSelect.value = 'newest';
      currentPage = 1;

      // Refresh projects list after stream finishes
      await fetchProjects();

      // Auto scroll to projects section and highlight the newly scanned card
      const prjSection = document.querySelector('.projects-section');
      if (prjSection) {
        prjSection.scrollIntoView({ behavior: 'smooth' });
      }

      setTimeout(() => {
        const targetCard = (newlyScannedDomain && document.querySelector(`.project-card[data-domain="${newlyScannedDomain}"]`)) || document.querySelector('.projects-grid .project-card:first-child');
        if (targetCard) {
          targetCard.classList.add('new-scan-highlight');
          targetCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          setTimeout(() => targetCard.classList.remove('new-scan-highlight'), 5000);
        }
      }, 350);
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
      allProjects = sortProjectsList(data.projects || [], activeSort);
      window.__EXTRACT_DESIGN_PROJECTS__ = allProjects;
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
      filteredProjects = sortProjectsList(filteredProjects, activeSort);
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
    projectsGrid.innerHTML = visibleProjects.map((proj, idx) => {
      const meta = proj.meta || {};
      const isFirstNewest = (idx === 0 && currentPage === 1 && activeSort === 'newest');
      const isFreshScan = newlyScannedDomain && proj.domain && proj.domain.toLowerCase() === newlyScannedDomain.toLowerCase();
      const logoFile = meta.logo ? (meta.logo.logo_svg || meta.logo.logo_img || meta.logo.favicon) : null;

      const logoThumb = logoFile 
        ? `<img src="/output/${encodeURIComponent(proj.domain)}/${encodeURIComponent(logoFile)}" class="project-logo-thumb" alt="Logo">`
        : `<div class="project-logo-thumb" style="display:flex;align-items:center;justify-content:center;">${icon('globe', 'icon-sm', 'color:var(--text-sub);')}</div>`;

      const formattedDate = meta.generated ? new Date(meta.generated).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : 'Extracted';

      const frameworksList = Array.isArray(meta.frameworks)
        ? meta.frameworks
        : (meta.frameworks && typeof meta.frameworks === 'object' ? Object.keys(meta.frameworks) : []);

      const frameworkPills = frameworksList.map(fw => 
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

      // Extract major colors from token for card background mini tiles
      const rawMajorColors = (Array.isArray(meta.brand_colors) && meta.brand_colors.length > 0)
        ? meta.brand_colors
        : ((Array.isArray(meta.top_colors) && meta.top_colors.length > 0) 
            ? meta.top_colors 
            : (meta.roles && typeof meta.roles === 'object' ? Object.values(meta.roles) : []));

      // Deterministic palette from domain string as secondary fallback
      const hashDomainColors = (str) => {
        let hash = 0;
        for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
        const h1 = Math.abs(hash) % 360;
        const h2 = (h1 + 45) % 360;
        const h3 = (h1 + 175) % 360;
        const h4 = (h1 + 220) % 360;
        return [
          `hsl(${h1}, 75%, 52%)`,
          `hsl(${h2}, 70%, 48%)`,
          `hsl(${h3}, 80%, 58%)`,
          `hsl(${h4}, 75%, 45%)`
        ];
      };

      const majorColors = rawMajorColors.filter(c => typeof c === 'string' && c && !c.includes('/ 0)') && !c.includes('/ 0.0)'));
      const cardColors = majorColors.length > 0 ? majorColors : hashDomainColors(proj.domain);
      const primaryColor = cardColors[0] || '#6366f1';
      const secondaryColor = cardColors[1] || primaryColor;

      // Seed-based mosaic generation for distinctive tile patterns per domain
      let domainSeed = 0;
      for (let i = 0; i < proj.domain.length; i++) domainSeed += proj.domain.charCodeAt(i) * (i + 1);

      // Generate 28 mini tiles from major colors (4 rows x 7 columns)
      const tileCount = 28;
      const miniTilesHtml = Array.from({ length: tileCount }).map((_, i) => {
        const c = cardColors[(i * 3 + domainSeed) % cardColors.length];
        return `<div class="card-mini-tile" style="--tile-c:${escapeHtml(c)};background-color:${escapeHtml(c)};"></div>`;
      }).join('');

      const cardBgTiles = `
        <div class="card-bg-tiles-wrapper" aria-hidden="true">
          <div class="card-tiles-ambient-glow" style="background: radial-gradient(circle at 85% 15%, ${escapeHtml(primaryColor)}48 0%, ${escapeHtml(secondaryColor)}28 45%, transparent 70%);"></div>
          <div class="card-tiles-scrim"></div>
          <div class="card-mini-tiles-mosaic">
            ${miniTilesHtml}
          </div>
        </div>
      `;

      return `
        <div class="project-card ${isFreshScan ? 'new-scan-highlight' : ''}" data-domain="${escapeHtml(proj.domain)}" style="--card-accent:${escapeHtml(primaryColor)};">
          ${cardBgTiles}
          <div>
            <div class="project-card-header">
              <div class="project-title-area">
                ${logoThumb}
                <div>
                  <div class="project-brand-title">
                    ${escapeHtml(brandTitle)}
                    ${isFirstNewest ? `<span class="latest-scan-badge" title="Most recently scanned design system">${icon('sparkles', 'icon-xs')} Newest Scan</span>` : ''}
                  </div>
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
            <button type="button" class="btn btn-intelligence btn-icon btn-sm inspect-intel-btn" data-domain="${escapeHtml(proj.domain)}" title="Open Website Intelligence & Design System Dashboard">${icon('sparkles', 'icon-xs')} <span>Intelligence</span></button>
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
      projectsTableBody.innerHTML = visibleProjects.map((proj, idx) => {
        const meta = proj.meta || {};
        const isFirstNewest = (idx === 0 && currentPage === 1 && activeSort === 'newest');
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

        const frameworksList = Array.isArray(meta.frameworks)
          ? meta.frameworks
          : (meta.frameworks && typeof meta.frameworks === 'object' ? Object.keys(meta.frameworks) : []);

        const frameworkBadges = frameworksList.slice(0, 2).map(fw => 
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
                  <div class="table-brand-title">
                    ${escapeHtml(brandTitle)}
                    ${isFirstNewest ? `<span class="latest-scan-badge" style="font-size:9px!important;padding:1px 5px!important;">${icon('sparkles', 'icon-xs')} Newest</span>` : ''}
                  </div>
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
                <button type="button" class="btn btn-intelligence btn-icon btn-table-action inspect-intel-btn" data-domain="${escapeHtml(proj.domain)}" title="Open Website Intelligence Dashboard">
                  ${icon('sparkles', 'icon-xs')} <span>Intel</span>
                </button>
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

    // Attach click listeners to inspect intelligence buttons
    document.querySelectorAll('.inspect-intel-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        openIntelligenceDashboard(btn.dataset.domain);
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

  // =========================================================================
  // Website Intelligence & Design-System Analyzer Dashboard Controller
  // =========================================================================

  const dashboardSection = document.getElementById('dashboard-section');
  const projectsSection = document.querySelector('.projects-section');
  const closeDashboardBtn = document.getElementById('close-dashboard-btn');
  const dashSiteTitle = document.getElementById('dash-site-title');
  const dashSiteDomain = document.getElementById('dash-site-domain');
  const dashScoreA11y = document.getElementById('dash-score-a11y');
  const dashScoreSeo = document.getElementById('dash-score-seo');
  const dashScoreSec = document.getElementById('dash-score-sec');
  const dashScorePerf = document.getElementById('dash-score-perf');
  const dashLaunchGuide = document.getElementById('dash-launch-guide');
  const dashDownloadZip = document.getElementById('dash-download-zip');
  const dashboardTabContent = document.getElementById('dashboard-tab-content');
  const dashTabs = document.querySelectorAll('.dash-tab');

  let currentIntelDomain = null;
  let currentIntelData = null;
  let activeTabName = 'overview';

  if (closeDashboardBtn) {
    closeDashboardBtn.addEventListener('click', closeIntelligenceDashboard);
  }

  dashTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      dashTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      activeTabName = tab.dataset.tab;
      renderActiveDashboardTab();
    });
  });

  async function openIntelligenceDashboard(domain) {
    window.openIntelligenceDashboard = openIntelligenceDashboard;
    currentIntelDomain = domain;
    if (!dashboardSection || !projectsSection) return;

    projectsSection.classList.add('hidden');
    dashboardSection.classList.remove('hidden');

    dashSiteTitle.textContent = 'Loading intelligence...';
    dashSiteDomain.textContent = domain;
    dashboardTabContent.innerHTML = `
      <div class="intel-card" style="text-align:center;padding:48px 24px;">
        <span class="spinner" style="display:inline-block;width:28px;height:28px;border-width:3px;margin-bottom:16px;"></span>
        <p style="font-size:15px;font-weight:600;">Analyzing website intelligence for ${escapeHtml(domain)}...</p>
        <p style="color:var(--text-sub);font-size:13px;">Inspecting components, layout, accessibility, SEO, performance, and security headers.</p>
      </div>
    `;
    refreshIcons();

    dashboardSection.scrollIntoView({ behavior: 'smooth' });

    try {
      const res = await fetch(`/api/intelligence?domain=${encodeURIComponent(domain)}&_t=${Date.now()}`);
      if (!res.ok) {
        throw new Error(`Server returned HTTP ${res.status}`);
      }
      currentIntelData = await res.json();

      const ov = currentIntelData.overview || {};
      const brandName = (currentIntelData.content_intelligence && currentIntelData.content_intelligence.value_proposition !== 'Not detected')
        ? (ov.domain || domain)
        : domain;

      dashSiteTitle.textContent = brandName;
      dashSiteDomain.textContent = domain;

      const scores = ov.scores || {};
      dashScoreA11y.textContent = (scores.accessibility != null ? scores.accessibility : 85) + '%';
      dashScoreSeo.textContent = (scores.seo != null ? scores.seo : 90) + '%';
      dashScoreSec.textContent = scores.security_grade || 'B';
      dashScorePerf.textContent = (scores.performance != null ? scores.performance : 88) + '%';

      if (dashLaunchGuide) {
        dashLaunchGuide.href = `/output/${encodeURIComponent(domain)}/style-guide.html`;
      }
      if (dashDownloadZip) {
        dashDownloadZip.href = `/api/download?domain=${encodeURIComponent(domain)}`;
      }

      renderActiveDashboardTab();
    } catch (err) {
      console.error('Failed to load intelligence report:', err);
      dashboardTabContent.innerHTML = `
        <div class="intel-card" style="border-color:var(--danger);text-align:center;padding:40px 24px;">
          <div style="color:var(--danger);margin-bottom:12px;">${icon('alert-triangle', 'icon-lg')}</div>
          <p style="font-size:16px;font-weight:600;">Could not load intelligence report</p>
          <p style="color:var(--text-sub);font-size:13px;max-width:500px;margin:8px auto 20px auto;">${escapeHtml(err.message)}. Try re-extracting this URL using the sidebar to generate a new multi-dimensional report.</p>
          <div style="display:flex;justify-content:center;gap:12px;">
            <button type="button" class="btn btn-secondary btn-sm" id="btn-err-back">Back to Projects</button>
            <button type="button" class="btn btn-primary btn-sm" id="btn-err-extract">Extract This Website</button>
          </div>
        </div>
      `;
      document.getElementById('btn-err-back')?.addEventListener('click', closeIntelligenceDashboard);
      document.getElementById('btn-err-extract')?.addEventListener('click', () => {
        closeIntelligenceDashboard();
        const urlInput = document.getElementById('url-input');
        if (urlInput) {
          urlInput.value = `https://${domain}`;
          urlInput.focus();
        }
      });
      refreshIcons();
    }
  }

  function closeIntelligenceDashboard() {
    if (dashboardSection && projectsSection) {
      dashboardSection.classList.add('hidden');
      projectsSection.classList.remove('hidden');
    }
    refreshIcons();
  }
  window.closeIntelligenceDashboard = closeIntelligenceDashboard;

  // Render the current active tab
  function renderActiveDashboardTab() {
    if (!currentIntelData || !dashboardTabContent) return;

    let html = '';
    switch (activeTabName) {
      case 'overview':
        html = tabRenderOverview(currentIntelData);
        break;
      case 'design_system':
        html = tabRenderDesignSystem(currentIntelData);
        break;
      case 'design_intelligence':
        html = tabRenderDesignIntelligence(currentIntelData);
        break;
      case 'components':
        html = tabRenderComponents(currentIntelData);
        break;
      case 'layout':
        html = tabRenderLayout(currentIntelData);
        break;
      case 'assets':
        html = tabRenderAssets(currentIntelData);
        break;
      case 'responsive':
        html = tabRenderResponsive(currentIntelData);
        break;
      case 'accessibility':
        html = tabRenderAccessibility(currentIntelData);
        break;
      case 'performance':
        html = tabRenderPerformance(currentIntelData);
        break;
      case 'seo':
        html = tabRenderSeo(currentIntelData);
        break;
      case 'security':
        html = tabRenderSecurity(currentIntelData);
        break;
      case 'technology':
        html = tabRenderTechnology(currentIntelData);
        break;
      case 'content':
        html = tabRenderContent(currentIntelData);
        break;
      case 'ai_insights':
        html = tabRenderAiInsights(currentIntelData);
        break;
      case 'export':
        html = tabRenderExport(currentIntelData);
        break;
      default:
        html = tabRenderOverview(currentIntelData);
    }

    dashboardTabContent.innerHTML = html;
    refreshIcons();

    // Attach click-to-copy listeners inside the tab
    dashboardTabContent.querySelectorAll('[data-copy]').forEach(el => {
      el.addEventListener('click', () => {
        const txt = el.dataset.copy;
        navigator.clipboard.writeText(txt);
        const originalText = el.innerHTML;
        el.innerHTML = `${icon('check', 'icon-xs')} <span>Copied!</span>`;
        refreshIcons();
        setTimeout(() => {
          el.innerHTML = originalText;
          refreshIcons();
        }, 1400);
      });
    });
  }

  // 1. Overview Tab
  function tabRenderOverview(data) {
    const ov = data.overview || {};
    const scores = ov.scores || {};
    const sum = ov.summary || {};
    const ai = data.ai_insights || {};

    const secGradeClass = (scores.security_grade || 'B').toLowerCase().startsWith('a') ? 'grade-a' :
      (scores.security_grade === 'B' ? 'grade-b' : (scores.security_grade === 'C' ? 'grade-c' : 'grade-f'));

    return `
      <div class="intel-grid-4">
        <div class="score-card-big">
          <div class="score-circle grade-a">${scores.accessibility != null ? scores.accessibility : 85}%</div>
          <div class="score-info">
            <div class="score-info-title">Accessibility</div>
            <div class="score-info-sub">WCAG 2.1 AA compliant</div>
          </div>
        </div>
        <div class="score-card-big">
          <div class="score-circle grade-b">${scores.seo != null ? scores.seo : 90}%</div>
          <div class="score-info">
            <div class="score-info-title">SEO Health</div>
            <div class="score-info-sub">Metadata & search indexed</div>
          </div>
        </div>
        <div class="score-card-big">
          <div class="score-circle ${secGradeClass}">${scores.security_grade || 'B'}</div>
          <div class="score-info">
            <div class="score-info-title">Security Grade</div>
            <div class="score-info-sub">HTTPS & response headers</div>
          </div>
        </div>
        <div class="score-card-big">
          <div class="score-circle grade-c">${scores.performance != null ? scores.performance : 88}%</div>
          <div class="score-info">
            <div class="score-info-title">Performance</div>
            <div class="score-info-sub">Loading & transfer budget</div>
          </div>
        </div>
      </div>

      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('activity', 'icon-sm')} System Architecture Overview</h3>
            <span class="intel-card-badge">${escapeHtml(ov.domain || currentIntelDomain)}</span>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-item-key">${icon('boxes', 'icon-xs')} Components Detected</span>
              <span class="spec-item-val">${sum.components_detected || 0} patterns</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">${icon('cpu', 'icon-xs')} Observed Technologies</span>
              <span class="spec-item-val">${sum.technologies_count || 0} detected</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">${icon('image', 'icon-xs')} Media & Asset Count</span>
              <span class="spec-item-val">${sum.assets_count || 0} items</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">${icon('git-branch', 'icon-xs')} Same-Site Pages Crawled</span>
              <span class="spec-item-val">${ov.pages_analyzed || 1} pages</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">${icon('sparkles', 'icon-xs')} Aesthetic Style Archetype</span>
              <span class="spec-item-val" style="color:var(--primary);">${escapeHtml(ai.style_archetype || sum.design_style || 'Modern Web')}</span>
            </div>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('shield-check', 'icon-sm')} Identity & Provenance</h3>
            <span class="intel-card-badge">Verified Source</span>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-item-key">${icon('globe', 'icon-xs')} Primary Source URL</span>
              <span class="spec-item-val"><a href="${escapeHtml(ov.primary_url || '')}" target="_blank" style="color:var(--primary);text-decoration:none;">${escapeHtml(ov.primary_url || 'Not detected')}</a></span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">${icon('clock', 'icon-xs')} Analysis Timestamp</span>
              <span class="spec-item-val">${escapeHtml(ov.analyzed_at || 'Recent')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">${icon('layers', 'icon-xs')} Design Consistency</span>
              <span class="spec-item-val">${ai.consistency_score || 92}/100</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">${icon('file-text', 'icon-xs')} Value Proposition</span>
              <span class="spec-item-val" style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${escapeHtml(data.content_intelligence?.value_proposition || '')}">${escapeHtml(data.content_intelligence?.value_proposition || 'Not detected')}</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // 2. Design System Tab
  function tabRenderDesignSystem(data) {
    const ds = data.design_system || {};
    const colors = ds.colors || {};
    const roles = ds.roles || {};
    const fonts = ds.fonts || {};
    const spacing = ds.spacing || {};
    const radius = ds.radius || {};

    const swatchesHtml = Object.entries(colors).slice(0, 36).map(([name, hex]) => `
      <div class="sw" data-copy="${escapeHtml(hex)}" title="Click to copy ${escapeHtml(hex)}" style="cursor:pointer;">
        <div class="chip" style="height:54px;background-color:${escapeHtml(hex)};"></div>
        <div class="meta" style="padding:6px 8px;">
          <span class="n" style="font-size:11px;">${escapeHtml(name)}</span>
          <code style="font-size:10.5px;">${escapeHtml(hex)}</code>
        </div>
      </div>
    `).join('') || '<p style="color:var(--text-sub);">No colors detected.</p>';

    const rolesHtml = Object.entries(roles).map(([role, ref]) => {
      const hex = colors[ref] || ref;
      return `
        <div class="spec-item">
          <span class="spec-item-key"><code>--color-${escapeHtml(role)}</code></span>
          <span class="spec-item-val" style="display:flex;align-items:center;gap:6px;">
            <span style="width:14px;height:14px;border-radius:3px;background:${escapeHtml(hex)};border:1px solid rgba(255,255,255,0.2);"></span>
            <code>${escapeHtml(hex)}</code>
          </span>
        </div>
      `;
    }).join('') || '<p style="color:var(--text-sub);">No semantic roles mapped.</p>';

    const fontsHtml = Object.entries(fonts).filter(([k]) => !k.startsWith('_')).map(([k, v]) => `
      <div class="spec-item">
        <span class="spec-item-key"><i data-lucide="type" class="icon-xs"></i> ${escapeHtml(k)}</span>
        <span class="spec-item-val" style="font-family:${escapeHtml(v)};">${escapeHtml(v)}</span>
      </div>
    `).join('') || '<p style="color:var(--text-sub);">System font stack.</p>';

    return `
      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('palette', 'icon-sm')} Color Palette & Tokens (${Object.keys(colors).length} Colors)</h3>
          <span class="intel-card-badge">Click swatch to copy hex</span>
        </div>
        <div class="grid" style="grid-template-columns:repeat(auto-fill, minmax(130px, 1fr));gap:8px;">
          ${swatchesHtml}
        </div>
      </div>

      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('tag', 'icon-sm')} Semantic Roles</h3>
          </div>
          <div class="spec-list">
            ${rolesHtml}
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('type', 'icon-sm')} Typography System</h3>
          </div>
          <div class="spec-list">
            ${fontsHtml}
          </div>
        </div>
      </div>

      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('code-2', 'icon-sm')} Generated CSS Variables (:root)</h3>
          <button type="button" class="btn btn-secondary btn-sm" data-copy="${escapeHtml(ds.css_variables || '')}">
            ${icon('copy', 'icon-xs')} <span>Copy CSS Variables</span>
          </button>
        </div>
        <div class="code-box-wrapper">
          <pre class="code-box-content">${escapeHtml(ds.css_variables || '/* No variables extracted */')}</pre>
        </div>
      </div>
    `;
  }

  // 2b. Design Intelligence Tab (Tier 1)
  function tabRenderDesignIntelligence(data) {
    const di = data.design_intelligence || {};
    const consistency = di.consistency || {};
    const semantic = di.semantic_tokens || {};
    const spacingGrid = di.spacing_grid || {};

    const breakdown = consistency.breakdown || {};
    const issues = consistency.issues || [];
    const positives = (consistency.positive || []).filter(Boolean);

    const grade = consistency.grade || 'B';
    const gradeClass = grade.toLowerCase().startsWith('a') ? 'grade-a' :
      (grade === 'B' ? 'grade-b' : (grade === 'C' ? 'grade-c' : 'grade-f'));

    const dimColor = (score) => score >= 85 ? '#10b981' : (score >= 70 ? '#38bdf8' : (score >= 50 ? '#fbbf24' : '#f87171'));

    const dims = [
      { key: 'color_economy', label: 'Color Economy', iconName: 'palette', data: breakdown.color_economy },
      { key: 'typography', label: 'Typography Discipline', iconName: 'type', data: breakdown.typography },
      { key: 'spacing', label: 'Spacing Discipline', iconName: 'ruler', data: breakdown.spacing },
      { key: 'border_radius', label: 'Border Radius Scale', iconName: 'square', data: breakdown.border_radius },
      { key: 'shadows', label: 'Shadow System', iconName: 'layers', data: breakdown.shadows },
    ];

    const dimRowsHtml = dims.map(d => {
      const s = d.data?.score != null ? d.data.score : 80;
      const lbl = d.data?.label || 'Good';
      const color = dimColor(s);
      return `
        <div class="dim-row">
          <div class="dim-row-header">
            <span style="display:flex;align-items:center;gap:6px;font-weight:500;color:var(--text-main);">
              ${icon(d.iconName, 'icon-xs')} ${d.label}
            </span>
            <span style="font-family:var(--font-mono);font-weight:600;color:${color};">${s}/100 <span style="font-size:10.5px;color:var(--text-sub);font-weight:400;">(${lbl})</span></span>
          </div>
          <div class="dim-bar-track">
            <div class="dim-bar-fill" style="width:${s}%;background:${color};"></div>
          </div>
        </div>
      `;
    }).join('');

    const issuesHtml = issues.length > 0 ? issues.map(iss => {
      const badgeClass = iss.severity === 'High' ? 'badge-critical' : (iss.severity === 'Medium' ? 'badge-warning' : 'badge-info');
      return `
        <div class="issue-item">
          <div class="issue-header">
            <span class="issue-rule">${escapeHtml(iss.dimension)} Inconsistency</span>
            <span class="${badgeClass}">${escapeHtml(iss.severity)}</span>
          </div>
          <p style="margin:0;color:var(--text-main);font-size:12px;line-height:1.4;">${escapeHtml(iss.message)}</p>
          <div class="issue-remediation">
            💡 <strong>Recommendation:</strong> ${escapeHtml(iss.recommendation)}
          </div>
        </div>
      `;
    }).join('') : `<div class="badge-pass" style="padding:12px;text-align:center;">${icon('check-circle-2', 'icon-xs')} No design system inconsistencies detected.</div>`;

    const positiveHtml = positives.length > 0 ? `
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;">
        ${positives.map(p => `<span class="badge-pass" style="font-size:11px;">✓ ${escapeHtml(p)}</span>`).join('')}
      </div>
    ` : '';

    // Semantic tokens table
    const namedTokens = semantic.named_tokens || [];
    const tokensHtml = namedTokens.length > 0 ? namedTokens.map(t => {
      const classBadge = t.usage_class === 'brand' ? 'badge-info' :
        (t.usage_class === 'feedback' ? 'badge-warning' :
        (t.usage_class === 'surface' ? 'badge-pass' : 'intel-card-badge'));
      return `
        <div class="spec-item" style="cursor:pointer;" data-copy="${escapeHtml(t.css_variable)}" title="Click to copy CSS variable">
          <span class="spec-item-key">
            <span style="width:16px;height:16px;border-radius:3px;background:${escapeHtml(t.hex)};border:1px solid rgba(255,255,255,0.2);display:inline-block;flex-shrink:0;"></span>
            <code>${escapeHtml(t.css_variable)}</code>
          </span>
          <span class="spec-item-val" style="display:flex;align-items:center;gap:6px;">
            <span class="${classBadge}" style="font-size:9.5px;text-transform:uppercase;">${escapeHtml(t.usage_class)}</span>
            <code>${escapeHtml(t.hex)}</code>
          </span>
        </div>
      `;
    }).join('') : '<p style="color:var(--text-sub);">No semantic tokens generated.</p>';

    // WCAG Contrast matrix
    const contrastPairs = semantic.contrast_pairs || [];
    const contrastHtml = contrastPairs.length > 0 ? contrastPairs.map(p => {
      const badgeClass = p.wcag_level === 'AAA' ? 'badge-pass' : (p.wcag_level === 'AA' ? 'badge-info' : 'badge-warning');
      return `
        <div class="contrast-card" style="background:var(--bg-dark);">
          <div class="contrast-preview" style="background:${escapeHtml(p.background)};color:${escapeHtml(p.foreground)};">
            <span>Aa Contrast Test</span>
            <span style="font-family:var(--font-mono);font-size:11px;">${p.contrast_ratio}:1</span>
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between;font-size:11px;">
            <span style="color:var(--text-sub);">${escapeHtml(p.foreground_role)} on ${escapeHtml(p.background_role)}</span>
            <span class="${badgeClass}">${escapeHtml(p.wcag_level)}</span>
          </div>
        </div>
      `;
    }).join('') : '<p style="color:var(--text-sub);">No contrast pairs computed.</p>';

    // Spacing Grid System
    const gridScale = spacingGrid.grid_scale || [];
    const offGrid = spacingGrid.off_grid_values || [];

    const gridScaleHtml = gridScale.length > 0 ? gridScale.map(s => `
      <div class="grid-scale-chip ${s.used ? 'chip-used' : ''}" title="${s.used ? 'Active in extracted stylesheet' : 'Canonical scale step'}">
        <span class="chip-step">${s.step}x</span>
        <span class="chip-val">${s.px}</span>
        <span class="chip-token">${s.token_name}</span>
      </div>
    `).join('') : '<p style="color:var(--text-sub);">No grid scale available.</p>';

    const offGridHtml = offGrid.length > 0 ? `
      <table class="snap-table">
        <thead>
          <tr>
            <th>Rogue Value</th>
            <th>Deviation</th>
            <th>Recommended Snap</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          ${offGrid.map(og => `
            <tr>
              <td><code>${escapeHtml(og.css)}</code></td>
              <td style="color:#fbbf24;">±${og.deviation}px</td>
              <td><strong style="color:#34d399;">${escapeHtml(og.nearest_snap)}</strong></td>
              <td><button type="button" class="btn btn-secondary btn-sm" style="padding:2px 8px;font-size:10.5px;" data-copy="${escapeHtml(og.nearest_snap)}">Copy Snap</button></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    ` : `<div class="badge-pass" style="padding:8px 12px;display:inline-block;">✓ All spacing values align to the ${spacingGrid.base_unit || 8}pt grid.</div>`;

    return `
      <!-- Row 1: System Consistency Score Card -->
      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('award', 'icon-sm')} Visual Consistency Discipline</h3>
            <span class="intel-card-badge">${consistency.score != null ? consistency.score : 85}/100 • Grade ${grade}</span>
          </div>
          <div class="score-card-big">
            <div class="score-circle ${gradeClass}">${consistency.score != null ? consistency.score : 85}</div>
            <div class="score-info">
              <div class="score-info-title">System Discipline: ${consistency.label || 'Good'}</div>
              <div class="score-info-sub">Measured across 5 core design system dimensions</div>
            </div>
          </div>
          <div style="display:flex;flex-direction:column;gap:8px;margin-top:6px;">
            ${dimRowsHtml}
          </div>
          ${positiveHtml}
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('alert-triangle', 'icon-sm')} Actionable Inconsistencies & Fixes</h3>
            <span class="intel-card-badge">${issues.length} Issues Flagged</span>
          </div>
          <div class="issue-list" style="max-height:380px;overflow-y:auto;">
            ${issuesHtml}
          </div>
        </div>
      </div>

      <!-- Row 2: Semantic Token Mapper & Contrast Matrix -->
      <div class="intel-grid-2" style="margin-top:16px;">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('tag', 'icon-sm')} Semantic Token Mapping (${namedTokens.length})</h3>
            <button type="button" class="btn btn-secondary btn-sm" data-copy="${escapeHtml(semantic.css_block || '')}">
              ${icon('copy', 'icon-xs')} <span>Copy Token CSS</span>
            </button>
          </div>
          <p style="font-size:12px;color:var(--text-sub);margin:0;">Tokens mapped from raw hex values to functional UI intent:</p>
          <div class="spec-list" style="max-height:320px;overflow-y:auto;margin-top:4px;">
            ${tokensHtml}
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('shield-check', 'icon-sm')} WCAG 2.1 Contrast Matrix</h3>
            <span class="intel-card-badge">Surface & Text Pairings</span>
          </div>
          <p style="font-size:12px;color:var(--text-sub);margin:0;">Live contrast verification on extracted brand & surface colors:</p>
          <div class="contrast-grid" style="max-height:320px;overflow-y:auto;margin-top:4px;">
            ${contrastHtml}
          </div>
        </div>
      </div>

      <!-- Row 3: Spacing Grid Detector -->
      <div class="intel-card" style="margin-top:16px;">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('ruler', 'icon-sm')} ${escapeHtml(spacingGrid.system_name || 'Spacing Grid System')}</h3>
          <span class="intel-card-badge ${spacingGrid.detected ? 'badge-pass' : 'badge-warning'}">
            ${spacingGrid.adherence_pct != null ? spacingGrid.adherence_pct : 0}% Grid Adherence
          </span>
        </div>
        <p style="font-size:13px;color:var(--text-main);margin:0;">
          ${escapeHtml(spacingGrid.summary || 'Calculated adherence across all layout margins, paddings, and flex/grid gaps.')}
        </p>

        <div style="margin-top:8px;">
          <h4 style="font-size:12px;font-weight:600;color:var(--text-sub);margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px;">Canonical ${spacingGrid.base_unit || 8}pt Scale (${spacingGrid.on_grid_count || 0} tokens in use)</h4>
          <div class="grid-scale-container">
            ${gridScaleHtml}
          </div>
        </div>

        <div style="margin-top:14px;border-top:1px solid rgba(255,255,255,0.06);padding-top:12px;">
          <h4 style="font-size:12px;font-weight:600;color:var(--text-sub);margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px;">Off-Grid Rogue Values & Auto-Snap Fixes (${offGrid.length} Rogue Tokens)</h4>
          <div style="overflow-x:auto;">
            ${offGridHtml}
          </div>
        </div>
      </div>
    `;
  }

  // 3. Components Tab
  function tabRenderComponents(data) {
    const comp = data.components || {};
    const detected = comp.detected || [];

    if (!detected.length) {
      return `
        <div class="intel-card" style="text-align:center;padding:40px;">
          <p style="color:var(--text-sub);">No standardized component signatures detected.</p>
        </div>
      `;
    }

    const cardsHtml = detected.map(c => `
      <div class="component-showcase-card">
        <div class="comp-header">
          <div class="comp-title">${icon('component', 'icon-xs')} ${escapeHtml(c.type)}</div>
          <span class="comp-count">${c.count} ${c.count === 1 ? 'instance' : 'instances'}</span>
        </div>
        <div style="font-size:11px;font-family:var(--font-mono);color:var(--primary);">${escapeHtml(c.tag)}</div>
        <p class="comp-styles">${escapeHtml(c.styles)}</p>
      </div>
    `).join('');

    return `
      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('boxes', 'icon-sm')} Detected Components (${detected.length} Types Identified)</h3>
          <span class="intel-card-badge">DOM & Style Heuristics</span>
        </div>
        <div class="component-showcase-grid">
          ${cardsHtml}
        </div>
      </div>
    `;
  }

  // 4. Layout Tab
  function tabRenderLayout(data) {
    const layout = data.layout || {};
    const containers = layout.containers || [];
    const engines = layout.layout_engines || {};
    const breakpoints = layout.breakpoints || [];
    const flow = layout.page_structure_flow || [];

    const flowHtml = flow.map((step, idx) => `
      <div class="tree-node">
        <span class="tree-indent">${idx + 1}.</span>
        <span>${escapeHtml(step)}</span>
      </div>
    `).join('');

    return `
      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('columns', 'icon-sm')} Container Constraints & Engines</h3>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-item-key">Primary Container Max-Width</span>
              <span class="spec-item-val">${escapeHtml(layout.primary_container || '1280px')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">CSS Grid System</span>
              <span class="spec-item-val">${engines.css_grid ? '<span class="badge-pass">Detected</span>' : 'Not detected'}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Flexbox Layouts</span>
              <span class="spec-item-val">${engines.flexbox ? '<span class="badge-pass">Detected</span>' : 'Not detected'}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Identified Container Widths</span>
              <span class="spec-item-val">${containers.join(', ') || 'Fluid / Unbounded'}</span>
            </div>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('git-commit', 'icon-sm')} Page Section Flow</h3>
            <span class="intel-card-badge">Visual Structure</span>
          </div>
          <div class="tree-container">
            ${flowHtml}
          </div>
        </div>
      </div>
    `;
  }

  // 5. Assets Tab
  function tabRenderAssets(data) {
    const ast = data.assets || {};
    const formats = ast.format_breakdown || {};
    const issues = ast.issues || [];
    const samples = ast.sample_assets || [];

    const formatPills = Object.entries(formats).map(([fmt, cnt]) => `
      <span class="stat-pill" style="font-size:12px;padding:4px 10px;">${escapeHtml(fmt)}: <strong>${cnt}</strong></span>
    `).join('') || '<span style="color:var(--text-sub);">None detected</span>';

    const issuesHtml = issues.map(iss => `
      <div class="issue-item">
        <div class="issue-header">
          <span class="badge-${iss.severity.toLowerCase()}">${escapeHtml(iss.severity)}</span>
          <span class="issue-rule">${escapeHtml(iss.message)}</span>
        </div>
      </div>
    `).join('') || '<p style="color:var(--success);font-size:13px;">✓ All image assets satisfy modern formatting and alt text guidelines.</p>';

    const samplesHtml = samples.map(s => `
      <tr>
        <td style="max-width:260px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${escapeHtml(s.src)}">
          <code>${escapeHtml(s.src)}</code>
        </td>
        <td><span class="stat-pill" style="font-size:10px;">${escapeHtml(s.format)}</span></td>
        <td>${escapeHtml(s.alt)}</td>
        <td>${escapeHtml(s.width)} × ${escapeHtml(s.height)}</td>
        <td><code>${escapeHtml(s.loading)}</code></td>
      </tr>
    `).join('');

    return `
      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('image', 'icon-sm')} Asset Formats & Optimization</h3>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            ${formatPills}
          </div>
          <div class="spec-list" style="margin-top:8px;">
            <div class="spec-item">
              <span class="spec-item-key">Total Extracted Assets</span>
              <span class="spec-item-val">${ast.total_assets || 0}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Missing Alt Text Attributes</span>
              <span class="spec-item-val" style="color:${ast.missing_alt_count > 0 ? 'var(--warning)' : 'var(--success)'};">${ast.missing_alt_count || 0}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Missing Explicit Dimensions (CLS)</span>
              <span class="spec-item-val">${ast.missing_dimensions_count || 0}</span>
            </div>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('alert-circle', 'icon-sm')} Asset Audit Flags</h3>
          </div>
          <div class="issue-list">
            ${issuesHtml}
          </div>
        </div>
      </div>

      ${samples.length ? `
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('list', 'icon-sm')} Observed Media Elements</h3>
          </div>
          <div class="projects-table-wrapper" style="overflow-x:auto;">
            <table class="projects-table" style="font-size:12px;">
              <thead>
                <tr>
                  <th>Resource Source</th>
                  <th>Format</th>
                  <th>Alt Text</th>
                  <th>Dimensions</th>
                  <th>Loading</th>
                </tr>
              </thead>
              <tbody>
                ${samplesHtml}
              </tbody>
            </table>
          </div>
        </div>
      ` : ''}
    `;
  }

  // 6. Responsive Tab
  function tabRenderResponsive(data) {
    const resp = data.responsive || {};
    const views = resp.views || {};
    const issues = resp.issues || [];

    const issuesHtml = issues.map(iss => `
      <div class="issue-item">
        <div class="issue-header">
          <span class="badge-${iss.severity.toLowerCase()}">${escapeHtml(iss.severity)}</span>
          <span class="issue-rule">${escapeHtml(iss.title)}</span>
        </div>
        <p style="margin:0;color:var(--text-sub);font-size:12px;">${escapeHtml(iss.description)}</p>
      </div>
    `).join('') || '<p style="color:var(--success);font-size:13px;">✓ No responsive layout hazards or horizontal overflow risks observed.</p>';

    return `
      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('smartphone', 'icon-sm')} Viewport & Breakpoints</h3>
            <span class="badge-pass">${escapeHtml(resp.overall_status || 'Ready')}</span>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-item-key">Viewport Meta Tag</span>
              <span class="spec-item-val"><code>${escapeHtml(resp.viewport_meta || 'Not detected')}</code></span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Mobile Viewport (< 768px)</span>
              <span class="spec-item-val">${escapeHtml(views.mobile?.status || 'Supported')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Tablet Viewport (768–1024px)</span>
              <span class="spec-item-val">${escapeHtml(views.tablet?.status || 'Supported')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Desktop Viewport (> 1024px)</span>
              <span class="spec-item-val">${escapeHtml(views.desktop?.status || 'Optimized')}</span>
            </div>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('shield-alert', 'icon-sm')} Responsive Analysis Flags</h3>
          </div>
          <div class="issue-list">
            ${issuesHtml}
          </div>
        </div>
      </div>
    `;
  }

  // 7. Accessibility Tab
  function tabRenderAccessibility(data) {
    const a11y = data.accessibility || {};
    const issues = a11y.issues || [];

    const issuesHtml = issues.map(iss => `
      <div class="issue-item">
        <div class="issue-header">
          <span class="badge-${iss.severity.toLowerCase()}">${escapeHtml(iss.severity)}</span>
          <span class="issue-rule">${escapeHtml(iss.rule)} (${escapeHtml(iss.category)})</span>
        </div>
        <p style="margin:0;color:var(--text-main);">${escapeHtml(iss.message)}</p>
        <div class="issue-remediation"><strong>Fix:</strong> ${escapeHtml(iss.remediation)}</div>
      </div>
    `).join('') || '<p style="color:var(--success);font-size:13px;">✓ Zero critical WCAG accessibility violations detected.</p>';

    return `
      <div class="intel-grid-3">
        <div class="score-card-big">
          <div class="score-circle grade-a">${a11y.score != null ? a11y.score : 85}%</div>
          <div class="score-info">
            <div class="score-info-title">Accessibility Score</div>
            <div class="score-info-sub">${escapeHtml(a11y.wcag_level || 'WCAG 2.1 AA')}</div>
          </div>
        </div>
        <div class="spec-item" style="padding:14px;">
          <span class="spec-item-key">${icon('alert-octagon', 'icon-xs')} Critical Issues</span>
          <span class="spec-item-val" style="color:var(--danger);">${a11y.critical_count || 0}</span>
        </div>
        <div class="spec-item" style="padding:14px;">
          <span class="spec-item-key">${icon('alert-triangle', 'icon-xs')} Warnings</span>
          <span class="spec-item-val" style="color:var(--warning);">${a11y.warning_count || 0}</span>
        </div>
      </div>

      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('check-circle-2', 'icon-sm')} Accessibility Findings & Remediation Steps</h3>
          <span class="intel-card-badge">${issues.length} audit rules evaluated</span>
        </div>
        <div class="issue-list">
          ${issuesHtml}
        </div>
      </div>
    `;
  }

  // 8. Performance Tab
  function tabRenderPerformance(data) {
    const perf = data.performance || {};
    const sizes = perf.transfer_sizes || {};
    const reqs = perf.requests_count || {};
    const opt = perf.optimizations || {};

    return `
      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('gauge', 'icon-sm')} Transfer Budgets & Requests</h3>
            <span class="intel-card-badge">${perf.score || 88}/100</span>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-item-key">HTML Document Size</span>
              <span class="spec-item-val">${sizes.html_kb || 0} KB</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Extracted Stylesheet Size</span>
              <span class="spec-item-val">${sizes.css_kb || 0} KB</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Estimated Requests Count</span>
              <span class="spec-item-val">${reqs.total_estimated || 0} requests</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Server TTFB / Latency</span>
              <span class="spec-item-val">${perf.response_time_ms ? `${perf.response_time_ms} ms` : 'Not recorded'}</span>
            </div>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('zap', 'icon-sm')} Loading & Runtime Optimizations</h3>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-item-key">Render-Blocking Scripts (&lt;head&gt;)</span>
              <span class="spec-item-val" style="color:${opt.render_blocking_scripts_count > 0 ? 'var(--warning)' : 'var(--success)'};">${opt.render_blocking_scripts_count || 0}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Font Display Swap Configured</span>
              <span class="spec-item-val">${opt.has_font_display_swap ? '<span class="badge-pass">Yes</span>' : 'Not detected'}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Lazy Loaded Below-Fold Images</span>
              <span class="spec-item-val">${escapeHtml(opt.lazy_loaded_images || 'Not detected')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Images Missing Dimensions (CLS Risk)</span>
              <span class="spec-item-val" style="color:${(opt.images_without_dimensions_count || 0) > 0 ? 'var(--warning)' : 'var(--success)'};">${opt.images_without_dimensions_count || 0}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Preconnect / Preload Hints</span>
              <span class="spec-item-val">${(opt.resource_hints || []).length || 0} configured</span>
            </div>
          </div>
        </div>
      </div>

      ${(() => {
        const nextPerf = perf.nextjs_performance || {};
        const recs = nextPerf.recommendations || [];
        if (!recs.length) return '';
        const recsHtml = recs.map(r => `
          <div class="issue-card warning">
            <div class="issue-header">
              <span class="issue-badge badge-warning">${icon('zap', 'icon-xs')} Next.js Performance Optimization</span>
              <span class="issue-rule">Core Web Vitals</span>
            </div>
            <div class="issue-message" style="font-size:13px;color:var(--text-main);">${escapeHtml(r)}</div>
          </div>
        `).join('');
        return `
          <div class="intel-card" style="margin-top:16px;">
            <div class="intel-card-header">
              <h3 class="intel-card-title">${icon('trending-up', 'icon-sm')} Next.js Performance & Core Web Vitals Audit</h3>
              <span class="intel-card-badge">Target: LCP &lt; 2.5s &bull; CLS &lt; 0.1</span>
            </div>
            <div class="issue-list">
              ${recsHtml}
            </div>
          </div>
        `;
      })()}
    `;
  }

  // 9. SEO Tab
  function tabRenderSeo(data) {
    const seo = data.seo || {};
    const og = seo.open_graph || {};
    const checks = seo.checks || [];

    const checksHtml = checks.map(c => `
      <div class="spec-item">
        <span class="spec-item-key">${escapeHtml(c.name)}</span>
        <span class="spec-item-val" style="display:flex;align-items:center;gap:8px;">
          <span class="${c.status === 'Passed' ? 'badge-pass' : (c.status === 'Warning' ? 'badge-warning' : 'badge-critical')}">${escapeHtml(c.status)}</span>
          <span style="font-size:11px;color:var(--text-sub);">${escapeHtml(c.detail)}</span>
        </span>
      </div>
    `).join('');

    return `
      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('search', 'icon-sm')} Google Search SERP Simulator</h3>
          <span class="intel-card-badge">Search Snippet Preview</span>
        </div>
        <div style="background:#202124;padding:16px 20px;border-radius:8px;border:1px solid #3c4043;max-width:650px;">
          <div style="color:#bdc1c6;font-size:12px;margin-bottom:4px;">${escapeHtml(seo.canonical || currentIntelDomain)}</div>
          <div style="color:#8ab4f8;font-size:18px;font-weight:500;cursor:pointer;margin-bottom:4px;">${escapeHtml(seo.title || currentIntelDomain)}</div>
          <div style="color:#bdc1c6;font-size:13px;line-height:1.45;">${escapeHtml(seo.description || 'No meta description provided for this site.')}</div>
        </div>
      </div>

      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('check-square', 'icon-sm')} Core SEO Signals</h3>
            <span class="intel-card-badge">${seo.score || 90}/100</span>
          </div>
          <div class="spec-list">
            ${checksHtml}
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('share-2', 'icon-sm')} Social & Structured Data</h3>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-item-key">Open Graph Title</span>
              <span class="spec-item-val">${escapeHtml(og.title || 'Not detected')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Twitter Card Type</span>
              <span class="spec-item-val">${escapeHtml(og.twitter_card || 'Not detected')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Schema.org Structured Data</span>
              <span class="spec-item-val">${(seo.structured_data?.types || ['Not detected']).join(', ')}</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Internal / External Link Ratio</span>
              <span class="spec-item-val">${seo.links?.internal_count || 0} int / ${seo.links?.external_count || 0} ext</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // 10. Security Tab
  function tabRenderSecurity(data) {
    const sec = data.security || {};
    const headersTable = sec.headers_table || [];

    const headersHtml = headersTable.map(h => `
      <tr>
        <td><strong>${escapeHtml(h.header)}</strong></td>
        <td>
          <span class="${h.status === 'Secure' || h.status === 'Enabled' || h.status === 'Protected' || h.status === 'Configured' ? 'badge-pass' : 'badge-warning'}">
            ${escapeHtml(h.status)}
          </span>
        </td>
        <td style="color:var(--text-sub);font-size:12px;">${escapeHtml(h.detail)}</td>
      </tr>
    `).join('');

    return `
      <div class="intel-grid-2">
        <div class="score-card-big">
          <div class="score-circle grade-a">${sec.grade || 'B'}</div>
          <div class="score-info">
            <div class="score-info-title">Security Posture Grade</div>
            <div class="score-info-sub">HTTP headers, SSL & data protection</div>
          </div>
        </div>
        <div class="spec-item" style="padding:16px;">
          <span class="spec-item-key">${icon('lock', 'icon-sm')} HTTPS Connection</span>
          <span class="spec-item-val">${sec.is_https ? '<span class="badge-pass">Enforced</span>' : '<span class="badge-critical">Unencrypted HTTP</span>'}</span>
        </div>
      </div>

      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('shield', 'icon-sm')} Response Headers Security Matrix</h3>
          <span class="intel-card-badge">${sec.score || 0}/100 Security Score</span>
        </div>
        <div class="projects-table-wrapper" style="overflow-x:auto;">
          <table class="projects-table" style="font-size:12.5px;">
            <thead>
              <tr>
                <th>Security Header</th>
                <th>Status</th>
                <th>Evaluation</th>
              </tr>
            </thead>
            <tbody>
              ${headersHtml}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  // 11. Technology Tab
  function tabRenderTechnology(data) {
    const tech = data.technology || {};
    const categories = tech.by_category || {};

    const catCards = Object.entries(categories).map(([cat, list]) => {
      if (!list || !list.length) return '';
      return `
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${escapeHtml(cat)} (${list.length})</h3>
          </div>
          <div class="tech-badges-wrap">
            ${list.map(t => `<div class="tech-chip">${icon('check', 'icon-xs')} <span>${escapeHtml(t)}</span></div>`).join('')}
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="intel-grid-2">
        ${catCards || '<div class="intel-card"><p style="color:var(--text-sub);">No standard frameworks detected (Vanilla HTML/CSS).</p></div>'}
      </div>
    `;
  }

  // 12. Content Intelligence Tab
  function tabRenderContent(data) {
    const ci = data.content_intelligence || {};

    const ctaPills = (ci.primary_ctas || []).map(cta => `
      <span class="stat-pill" style="font-size:12px;padding:4px 10px;background:rgba(99,102,241,0.15);color:var(--primary);">${escapeHtml(cta)}</span>
    `).join('') || '<span style="color:var(--text-sub);">Not detected</span>';

    const headlinesHtml = (ci.key_headlines || []).map(h => `
      <div class="tree-node" style="font-family:inherit;font-size:13px;">${icon('file-text', 'icon-xs')} <span>${escapeHtml(h)}</span></div>
    `).join('') || '<p style="color:var(--text-sub);">Not detected</p>';

    const trustHtml = (ci.trust_signals || []).map(ts => `
      <div class="spec-item">
        <span class="spec-item-key">${icon('shield-check', 'icon-xs')} Trust Signal</span>
        <span class="spec-item-val">${escapeHtml(ts)}</span>
      </div>
    `).join('') || '<p style="color:var(--text-sub);">Not detected</p>';

    return `
      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('bookmark', 'icon-sm')} Primary Value Proposition</h3>
          <span class="intel-card-badge">Hero Message</span>
        </div>
        <p style="font-size:17px;font-weight:600;color:var(--text-main);margin:0;line-height:1.45;">
          "${escapeHtml(ci.value_proposition || 'Not detected')}"
        </p>
        <p style="color:var(--text-sub);font-size:12.5px;margin:8px 0 0 0;">${escapeHtml(ci.messaging_summary || '')}</p>
      </div>

      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('zap', 'icon-sm')} Call-to-Actions (CTAs)</h3>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            ${ctaPills}
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('award', 'icon-sm')} Trust Signals & Social Proof</h3>
          </div>
          <div class="spec-list">
            ${trustHtml}
          </div>
        </div>
      </div>

      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('heading', 'icon-sm')} Key Page Headlines (H1 & H2)</h3>
        </div>
        <div class="tree-container">
          ${headlinesHtml}
        </div>
      </div>
    `;
  }

  // 13. AI Design Insights Tab
  function tabRenderAiInsights(data) {
    const ai = data.ai_insights || {};
    const fvi = ai.facts_vs_interpretation || {};
    const facts = fvi.detected_facts || [];
    const interps = fvi.ai_interpretation || [];

    const factsHtml = facts.map(f => `
      <div class="spec-item">
        <span class="spec-item-key"><span class="badge-pass">Observed Fact</span></span>
        <span class="spec-item-val" style="font-family:inherit;font-weight:400;">${escapeHtml(f)}</span>
      </div>
    `).join('');

    const interpHtml = interps.map(i => `
      <div class="spec-item">
        <span class="spec-item-key"><span class="badge-info">AI Interpretation</span></span>
        <span class="spec-item-val" style="font-family:inherit;font-weight:400;">${escapeHtml(i)}</span>
      </div>
    `).join('');

    return `
      <div class="intel-grid-2">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('sparkles', 'icon-sm')} Aesthetic Style Archetype</h3>
            <span class="intel-card-badge" style="color:var(--primary);">${escapeHtml(ai.style_archetype || 'Modern Web')}</span>
          </div>
          <p style="font-size:14px;color:var(--text-main);margin:0;line-height:1.5;">${escapeHtml(ai.visual_hierarchy_review || 'Balanced visual hierarchy.')}</p>
          <div class="spec-list" style="margin-top:10px;">
            <div class="spec-item">
              <span class="spec-item-key">Consistency Score</span>
              <span class="spec-item-val">${ai.consistency_score || 90}/100</span>
            </div>
            <div class="spec-item">
              <span class="spec-item-key">Notable Patterns</span>
              <span class="spec-item-val">${(ai.notable_patterns || []).join(', ') || 'Clean standard web layout'}</span>
            </div>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('git-compare', 'icon-sm')} Facts vs. AI Interpretation</h3>
            <span class="intel-card-badge">Strict Demarcation</span>
          </div>
          <div class="spec-list">
            ${factsHtml}
            ${interpHtml}
          </div>
        </div>
      </div>
    `;
  }

  // 14. Framework-Aware Export Tab
  function tabRenderExport(data) {
    const exports = data.exports || {};
    const ds = data.design_system || {};
    const domain = currentIntelDomain || 'extracted-theme';

    const fwDetected = exports.framework_detected || 'Vanilla CSS';
    const primaryFormat = exports.primary_format || 'css';
    const tailwindCode = exports.tailwind_config || '';
    const tsCode = exports.typescript_theme || '';
    const vueCode = exports.vue_composable || '';
    const w3cTokens = exports.json_tokens_w3c || '';
    const cssVars = exports.css_variables || ds.css_variables || '';
    const designMd = exports.design_md || '';
    const reactCode = exports.react_components || '';
    const layoutCode = exports.nextjs_layout || '';

    // Choose the primary configuration block to show
    let primaryConfigTitle = 'CSS Variables & Tokens (:root)';
    let primaryConfigFile = 'theme.css';
    let primaryConfigCode = cssVars;
    let primaryIcon = 'file-text';

    if (primaryFormat === 'tailwind' && tailwindCode) {
      primaryConfigTitle = 'Tailwind CSS Configuration (Extended Theme)';
      primaryConfigFile = 'tailwind.config.js';
      primaryConfigCode = tailwindCode;
      primaryIcon = 'file-code';
    } else if (primaryFormat === 'typescript' && tsCode) {
      primaryConfigTitle = 'TypeScript Design Theme';
      primaryConfigFile = 'theme.ts';
      primaryConfigCode = tsCode;
      primaryIcon = 'file-code';
    } else if (primaryFormat === 'vue' && vueCode) {
      primaryConfigTitle = 'Vue / Nuxt Token Composable';
      primaryConfigFile = 'composables/useTokens.ts';
      primaryConfigCode = vueCode;
      primaryIcon = 'file-code';
    }

    return `
      <!-- Framework Stack Detection Card -->
      <div class="intel-card">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('layers', 'icon-sm')} Framework-Aware Export Engine</h3>
          <span class="badge-pass" style="font-size:11px;">Detected: ${escapeHtml(fwDetected)}</span>
        </div>
        <p style="font-size:13px;color:var(--text-main);margin:0;">
          ExtractDesign Studio has automatically tailored export tokens, configurations, and components for <strong>${escapeHtml(fwDetected)}</strong>.
        </p>
      </div>

      <!-- Primary Framework Config & Next.js Components -->
      <div class="intel-grid-2" style="margin-top:16px;">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon(primaryIcon, 'icon-sm')} ${escapeHtml(primaryConfigTitle)}</h3>
            <button type="button" class="btn btn-secondary btn-sm" data-copy="${escapeHtml(primaryConfigCode)}">
              ${icon('copy', 'icon-xs')} <span>Copy ${escapeHtml(primaryConfigFile)}</span>
            </button>
          </div>
          <div class="code-box-wrapper">
            <pre class="code-box-content">${escapeHtml(primaryConfigCode || '/* No configuration generated */')}</pre>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('boxes', 'icon-sm')} Next.js App Router Components</h3>
            <button type="button" class="btn btn-secondary btn-sm" data-copy="${escapeHtml(reactCode)}">
              ${icon('copy', 'icon-xs')} <span>Copy Components</span>
            </button>
          </div>
          <div class="code-box-wrapper">
            <pre class="code-box-content">${escapeHtml(reactCode || '// Next.js App Router component template')}</pre>
          </div>
        </div>
      </div>

      <!-- W3C Tokens & CSS Custom Properties -->
      <div class="intel-grid-2" style="margin-top:16px;">
        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('code-2', 'icon-sm')} W3C Standard Design Tokens (JSON)</h3>
            <button type="button" class="btn btn-secondary btn-sm" data-copy="${escapeHtml(w3cTokens)}">
              ${icon('copy', 'icon-xs')} <span>Copy Tokens JSON</span>
            </button>
          </div>
          <div class="code-box-wrapper">
            <pre class="code-box-content">${escapeHtml(w3cTokens || '{}')}</pre>
          </div>
        </div>

        <div class="intel-card">
          <div class="intel-card-header">
            <h3 class="intel-card-title">${icon('file-text', 'icon-sm')} CSS Variables (:root)</h3>
            <button type="button" class="btn btn-secondary btn-sm" data-copy="${escapeHtml(cssVars)}">
              ${icon('copy', 'icon-xs')} <span>Copy CSS Variables</span>
            </button>
          </div>
          <div class="code-box-wrapper">
            <pre class="code-box-content">${escapeHtml(cssVars || '/* No CSS variables */')}</pre>
          </div>
        </div>
      </div>

      <!-- DESIGN.md Documentation & Actions -->
      <div class="intel-card" style="margin-top:16px;">
        <div class="intel-card-header">
          <h3 class="intel-card-title">${icon('download', 'icon-sm')} Export Packages & Source Files</h3>
          <span class="intel-card-badge">Instant Access</span>
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
          <a href="/output/${encodeURIComponent(domain)}/DESIGN.md" target="_blank" class="btn btn-secondary btn-sm">
            ${icon('file-text', 'icon-xs')} <span>View DESIGN.md</span>
          </a>
          <a href="/output/${encodeURIComponent(domain)}/design-tokens.json" target="_blank" class="btn btn-secondary btn-sm">
            ${icon('code-2', 'icon-xs')} <span>View Tokens JSON</span>
          </a>
          <a href="/output/${encodeURIComponent(domain)}/tailwind.config.js" target="_blank" class="btn btn-secondary btn-sm">
            ${icon('file-code', 'icon-xs')} <span>View Tailwind Config</span>
          </a>
          <a href="/api/download?domain=${encodeURIComponent(domain)}" class="btn btn-download btn-sm" download>
            ${icon('download', 'icon-xs')} <span>Download Complete ZIP Package</span>
          </a>
        </div>
      </div>
    `;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
});


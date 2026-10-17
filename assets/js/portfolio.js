/* Progressive enhancement: every research record is readable without JavaScript. */
(() => {
  'use strict';
  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const darkPreference = window.matchMedia('(prefers-color-scheme: dark)');
  const currentTheme = () => root.dataset.theme || (darkPreference.matches ? 'dark' : 'light');
  const updateThemeLabel = () => {
    if (!themeButton) return;
    const next = currentTheme() === 'dark' ? 'light' : 'dark';
    themeButton.textContent = next === 'dark' ? 'Dark' : 'Light';
    themeButton.setAttribute('aria-label', 'Switch to ' + next + ' theme');
  };
  if (themeButton) {
    themeButton.hidden = false;
    updateThemeLabel();
    themeButton.addEventListener('click', () => {
      root.dataset.theme = currentTheme() === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('portfolio-theme', root.dataset.theme); } catch (_) {}
      updateThemeLabel();
    });
    darkPreference.addEventListener('change', updateThemeLabel);
  }

  document.querySelectorAll('[data-filter-list]').forEach(list => {
    const form = list.querySelector('[data-filters]');
    const items = [...list.querySelectorAll('[data-filter-item]')];
    const groups = [...list.querySelectorAll('[data-filter-group]')];
    const count = list.querySelector('.filter-count');
    const empty = list.querySelector('.empty-state');
    if (!form) return;
    const applyFilters = () => {
      const fields = new FormData(form);
      let shown = 0;
      items.forEach(item => {
        const matches = [...fields].every(([key, value]) => !value || (item.dataset[key] || '').split('|').includes(value));
        item.hidden = !matches;
        if (matches) shown++;
      });
      groups.forEach(group => { group.hidden = ![...group.querySelectorAll('[data-filter-item]')].some(item => !item.hidden); });
      count.textContent = shown + ' of ' + items.length + (list.dataset.filterList === 'publications' ? ' papers' : ' articles');
      empty.hidden = shown > 0;
    };
    form.hidden = false;
    const note = list.querySelector('.filter-note');
    if (note) note.hidden = false;
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('change', applyFilters);
    form.addEventListener('reset', () => setTimeout(applyFilters, 0));
    applyFilters();
    window.addEventListener('hashchange', () => {
      const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target && items.includes(target) && target.hidden) {
        form.reset();
        setTimeout(() => { applyFilters(); target.scrollIntoView(); }, 0);
      }
    });
  });

  document.querySelectorAll('[data-copy-reference]').forEach(button => {
    if (!navigator.clipboard || !window.isSecureContext) return;
    button.hidden = false;
    button.addEventListener('click', async () => {
      const details = button.closest('details');
      const status = details.querySelector('.copy-status');
      try {
        await navigator.clipboard.writeText(details.querySelector('.reference').textContent.trim());
        status.textContent = 'Reference copied.';
      } catch (_) {
        status.textContent = 'Copy unavailable. Select the reference text above to copy it.';
      }
    });
  });

  const geometry = document.querySelector('[data-geometry]');
  if (geometry) {
    geometry.querySelector('.geometry-controls').hidden = false;
    const slider = document.getElementById('geometry-radius');
    const render = () => {
      const radius = Number(slider.value);
      document.getElementById('geometry-value').value = radius.toFixed(1);
      document.getElementById('euclid-ring').setAttribute('r', radius * 25);
      document.getElementById('hyperbolic-ring').setAttribute('r', Math.tanh(radius / 2) * 100);
      document.getElementById('euclid-metric').textContent = 'Circumference: ' + (2 * Math.PI * radius).toFixed(2);
      document.getElementById('hyperbolic-metric').textContent = 'Circumference: ' + (2 * Math.PI * Math.sinh(radius)).toFixed(2);
      document.getElementById('euclid-label').textContent = 'Euclidean plane: a circle at distance ' + radius.toFixed(1) + ' from the origin';
      document.getElementById('hyperbolic-label').textContent = 'Poincaré disk: a circle at hyperbolic distance ' + radius.toFixed(1) + ' from the origin';
    };
    slider.addEventListener('input', render);
    render();
  }
})();

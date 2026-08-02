(function () {
  'use strict';

  function setStatus(container, message, isError) {
    const status = container.querySelector('[data-chart-status]');
    if (!status) return;
    status.textContent = message;
    status.hidden = false;
    status.classList.toggle('chart-status-error', Boolean(isError));
  }

  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }

  // Vega renders to canvas, so it cannot read the CSS custom properties that
  // theme the rest of the page. A spec may instead carry
  // usermeta.themes.{light,dark}, each a Vega-Lite `config` object; the matching
  // one is merged in at render time and re-applied when the theme changes.
  function applyTheme(spec) {
    const themes = spec.usermeta && spec.usermeta.themes;
    if (!themes) return spec;

    const themed = Object.assign({}, spec);
    themed.config = Object.assign({}, spec.config, themes[currentTheme()] || {});
    return themed;
  }

  async function renderChart(container) {
    const specUrl = container.dataset.vegaSpec;

    if (!specUrl || typeof window.vegaEmbed !== 'function') {
      setStatus(container, 'The chart library could not be loaded.', true);
      return;
    }

    try {
      const response = await fetch(specUrl, {
        headers: { Accept: 'application/json' }
      });
      if (!response.ok) throw new Error('Chart data request failed');

      const spec = await response.json();

      async function draw() {
        await window.vegaEmbed(container, applyTheme(spec), {
          actions: true,
          renderer: 'canvas',
          tooltip: true
        });
        const status = container.querySelector('[data-chart-status]');
        if (status) status.hidden = true;
      }

      await draw();

      if (spec.usermeta && spec.usermeta.themes) {
        let theme = currentTheme();
        new MutationObserver(function () {
          if (currentTheme() === theme) return;
          theme = currentTheme();
          draw().catch(function (error) {
            console.error('Unable to re-render Vega-Lite chart for theme', error);
          });
        }).observe(document.documentElement, {
          attributes: true,
          attributeFilter: ['data-theme']
        });
      }
    } catch (error) {
      console.error('Unable to render Vega-Lite chart', error);
      setStatus(container, 'This interactive chart is temporarily unavailable. The chart data remains available below.', true);
    }
  }

  function initialize() {
    document.querySelectorAll('[data-vega-spec]').forEach(renderChart);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
})();

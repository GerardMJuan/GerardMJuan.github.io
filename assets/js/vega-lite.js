(function () {
  'use strict';

  function setStatus(container, message, isError) {
    const status = container.querySelector('[data-chart-status]');
    if (!status) return;
    status.textContent = message;
    status.hidden = false;
    status.classList.toggle('chart-status-error', Boolean(isError));
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
      await window.vegaEmbed(container, spec, {
        actions: true,
        renderer: 'canvas',
        tooltip: true
      });
      setStatus(container, '', false);
      const status = container.querySelector('[data-chart-status]');
      if (status) status.hidden = true;
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

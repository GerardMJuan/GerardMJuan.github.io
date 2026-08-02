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
    const specUrl = container.dataset.plotlySpec;

    if (!specUrl || typeof window.Plotly === 'undefined') {
      setStatus(container, 'The chart library could not be loaded.', true);
      return;
    }

    try {
      const response = await fetch(specUrl, {
        headers: { Accept: 'application/json' }
      });
      if (!response.ok) throw new Error('Chart data request failed');

      const figure = await response.json();
      if (!Array.isArray(figure.data)) throw new Error('Plotly data must be an array');

      const config = Object.assign({
        responsive: true,
        displaylogo: false
      }, figure.config || {});

      await window.Plotly.newPlot(
        container,
        figure.data,
        figure.layout || {},
        config
      );
      setStatus(container, '', false);
      const status = container.querySelector('[data-chart-status]');
      if (status) status.hidden = true;
    } catch (error) {
      console.error('Unable to render Plotly chart', error);
      setStatus(container, 'This interactive chart is temporarily unavailable. The chart data remains available below.', true);
    }
  }

  function initialize() {
    document.querySelectorAll('[data-plotly-spec]').forEach(renderChart);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
})();

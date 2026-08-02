---
layout: default
title: Lab
permalink: /lab/
description: A small demonstration of the site's interactive publishing capabilities.
math: true
mermaid: true
vega_lite: true
plotly: true
---

<header class="page-intro">
  <h1>Lab</h1>
  <p>This page is a living smoke test for richer posts: the source remains Markdown and JSON, while the browser adds the interactive layer.</p>
</header>

## LaTeX

Inline math works with \(e^{i\pi} + 1 = 0\). Display equations work too:

\[
\int_0^1 x^2\,dx = \frac{1}{3}
\]

## Mermaid

<div class="mermaid-wrapper" role="img" aria-label="Diagram showing Markdown moving through Jekyll to static HTML and browser interactivity">
  <pre class="mermaid">
flowchart LR
  A[Markdown] --> B[Jekyll]
  B --> C[Static HTML]
  C --> D[Browser interactivity]
  </pre>
</div>

## Vega-Lite

The specification is stored at <code>assets/data/example-vega.json</code> and loaded by a reusable include.

{% include vega-lite.html id="vega-demo" spec="/assets/data/example-vega.json" label="Example Vega-Lite bar chart showing posts by month" %}

## Plotly

Plotly figures use the same pattern: a versioned browser library plus a local JSON figure.

{% include plotly.html id="plotly-demo" spec="/assets/data/example-plotly.json" label="Example Plotly line chart showing posts by month" %}

## Authoring pattern

Enable only what a page needs in its front matter:

<pre><code>math: true
mermaid: true
vega_lite: true
plotly: true</code></pre>

For interactive data, keep the data and specification reviewable in the repository. Heavy computation should happen before publishing, with the generated artifact and its provenance linked from the post.

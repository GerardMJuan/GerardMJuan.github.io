---
layout: default
title: Publications
permalink: /publications/
description: Peer-reviewed publications in medical imaging, neuroimaging and machine learning.
vega_lite: true
---

{%- assign pubs = site.data.publications.entries -%}
{%- assign years = pubs | map: "year" | sort -%}
{%- assign first_year = years | first -%}
{%- assign last_year = years | last -%}
{%- assign journals = pubs | where: "type", "journal" -%}

<header class="page-intro">
  <h1>Publications</h1>
  <p>
    Peer-reviewed work, mostly on brain MRI — Alzheimer's disease during the Ph.D.,
    multiple sclerosis after it, and fetal imaging now. The complete and always-current
    list lives on
    <a href="https://scholar.google.com/citations?user=9Qzpt7kAAAAJ">Google Scholar</a>.
  </p>
</header>

<ul class="pub-stats">
  <li class="pub-stat">
    <span class="pub-stat-value">{{ pubs | size }}</span>
    <span class="pub-stat-label">Listed here</span>
  </li>
  <li class="pub-stat">
    <span class="pub-stat-value">{{ journals | size }}</span>
    <span class="pub-stat-label">Journal articles</span>
  </li>
  <li class="pub-stat">
    <span class="pub-stat-value">{{ first_year }}&ndash;{{ last_year }}</span>
    <span class="pub-stat-label">Span</span>
  </li>
</ul>

<div class="pub-chart">
  {% include vega-lite.html
     id="publications-timeline"
     label="Timeline of publications by year, coloured by research thread"
     spec="/assets/data/publications-vega.json" %}
</div>

{%- comment -%}
  Grouped by year, newest first. This list doubles as the chart's accessible
  fallback — every point above appears here as text.
{%- endcomment -%}
{%- assign by_year = pubs | group_by: "year" | sort: "name" | reverse -%}
{% for group in by_year %}
  <h2 class="pub-year-heading">{{ group.name }}</h2>
  <ul class="pub-list">
    {% for pub in group.items %}
      <li class="pub-item">
        <h3 class="pub-title">{{ pub.title }}</h3>

        {%- comment -%} Emphasise Gerard's own name wherever it appears. {%- endcomment -%}
        {%- assign authors = pub.authors -%}
        {%- for alias in site.data.publications.self_names -%}
          {%- capture marked -%}<span class="pub-self">{{ alias }}</span>{%- endcapture -%}
          {%- assign authors = authors | replace: alias, marked -%}
        {%- endfor -%}
        <p class="pub-authors">{{ authors }}</p>

        <p class="pub-venue">
          {{ pub.venue }}{% if pub.details %}, {{ pub.details }}{% endif %}.
        </p>

        <p class="pub-meta">
          <span class="pub-type">{{ pub.type }}</span>
          {% if pub.doi %}
            <a class="pub-link" href="https://doi.org/{{ pub.doi }}">DOI: {{ pub.doi }}</a>
          {% elsif pub.url %}
            <a class="pub-link" href="{{ pub.url }}">{{ pub.url_label | default: "Read" }}</a>
          {% endif %}
        </p>
      </li>
    {% endfor %}
  </ul>
{% endfor %}

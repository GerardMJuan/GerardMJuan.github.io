---
layout: default
title: Projects
permalink: /projects/
description: Selected projects, experiments, and tools.
---

<header class="page-intro">
  <h1>Projects</h1>
  <p>A small index of projects and experiments. Each entry lives in the <code>_projects/</code> collection, so it can be edited as a Markdown file from any device.</p>
</header>

{% assign projects = site.projects | sort: "date" | reverse %}
{% if projects.size == 0 %}
  <p class="empty-state">Projects will appear here as they are added.</p>
{% else %}
  <div class="projects-grid">
    {% for project in projects %}
      <article class="project-card">
        <p class="project-kicker">Project</p>
        <h2><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h2>
        {% if project.description %}
          <p>{{ project.description }}</p>
        {% endif %}
        <a class="read-more" href="{{ project.url | relative_url }}">View project</a>
      </article>
    {% endfor %}
  </div>
{% endif %}

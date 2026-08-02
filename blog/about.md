---
layout: default
title: About
permalink: /about/
description: Who I am, what I work on, and how this site is built.
---

# About

I'm Gerard Martí Juan. I work on machine learning for medical images, and I have
been pointing it at brains for about a decade now — first in Alzheimer's disease,
then multiple sclerosis, and currently in fetuses, which are the least cooperative
imaging subjects I have ever worked with.

Day to day that means two things: I'm a **Senior AI Researcher** at
[Eden](https://eden.ai), building healthcare AI, and a **Research Scientist** at
[UPF BCN MedTech](https://www.upf.edu/web/bcn-medtech) in Barcelona, working on
fetal brain MRI.

## What I actually find interesting

<!-- TODO(gerard): the two paragraphs below are a point of view I drafted from the
     recurring themes in your own papers — multi-centric studies, quality control,
     progression modelling. They are a plausible version of your opinions, not a
     verified one. Rewrite them in your own words or delete them. -->

Most of the interesting problems in medical imaging are not modelling problems.
A model that reaches a good number on a curated benchmark and a model that survives
contact with a second hospital's scanner are rarely the same model, and the gap
between them is where the actual work is: harmonisation, quality control, missing
modalities, and the awkward fact that clinical data is longitudinal, irregular,
and full of holes.

I also think we under-invest in the boring infrastructure — reproducible pipelines,
sane preprocessing, honest validation — relative to how much of the final result
depends on it. A lot of my published work is, one way or another, about that.

## Background

I did my **Ph.D. in Information and Communication Technologies** at Universitat
Pompeu Fabra, finishing in 2021 *Cum Laude*, on data-driven methods for
characterising heterogeneity in Alzheimer's disease — essentially, on the fact
that "Alzheimer's disease" describes a lot of rather different-looking brains.
Before that, an MSc in Computer Vision at Universitat Autònoma de Barcelona and a
BSc in Informatics Engineering at Universitat Politècnica de Catalunya.

Things I work with regularly: brain MRI (structural, functional, diffusion),
disease progression modelling, multimodal data integration, and the pipeline
plumbing that holds all of it together.

<!-- TODO(gerard): a paragraph of non-work personality goes a long way here, and I
     could not write it for you without inventing things. A few shapes that tend
     to work — pick one:
       - what you do away from a screen (a sport, cooking, music, the mountains)
       - what you are reading or playing right now, and whether you'd recommend it
       - something you have changed your mind about in the last few years
       - why Barcelona, if there is a story there
     Two or three sentences is plenty. -->

## Elsewhere

- [GitHub](https://github.com/GerardMJuan)
- [Google Scholar](https://scholar.google.com/citations?user=9Qzpt7kAAAAJ)
- [ORCiD](https://orcid.org/0000-0003-4729-7182)
- [LinkedIn](https://linkedin.com/in/gerardmjuan)

The best way to reach me is email:
[gerardmartijuan@gmail.com](mailto:gerardmartijuan@gmail.com).

## Colophon {#colophon}

This site is a [Jekyll](https://jekyllrb.com/) build on GitHub Pages. It started
life as [Jekyll Now](https://github.com/barryclark/jekyll-now) years ago; by now
every layout, include and stylesheet has been rewritten, but the original
attribution stays in the page source where it belongs.

A few deliberate choices:

- **No trackers, no analytics, no cookies.** I have no idea who visits, and I like it
  that way. Two scripts do still come from a CDN: the search index loads from unpkg
  the first time you focus the search box, and the pages with charts or equations
  pull those libraries from jsDelivr. Everything else is served from here.
- **No JavaScript frameworks.** Dark mode is a set of CSS custom properties plus a
  handful of lines of vanilla JS.
- **Type is [Newsreader](https://github.com/productiontype/Newsreader)**, an
  open-licence variable serif, self-hosted rather than pulled from Google Fonts.
- **Icons are inline SVG.** The CV page used to load Font Awesome, Google Fonts and a
  284 KB icon webfont to draw five contact links. Now it loads nothing.
- **[Publications]({{ '/publications/' | relative_url }}) come from one YAML file**
  that renders both the list and the timeline chart above it, so the two cannot
  drift apart.
- **CI does the nagging.** Every push runs a small Python validator that checks
  internal links, missing image alt text, duplicate element IDs and malformed
  chart data, so the site fails loudly rather than quietly.

The whole thing is
[on GitHub](https://github.com/GerardMJuan/GerardMJuan.github.io) if you want to
take anything from it.

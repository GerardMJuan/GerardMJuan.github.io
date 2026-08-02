# GerardMJuan.github.io

Personal website, research notes, projects, and blog posts. The site is built with Jekyll and published to GitHub Pages.

## Work from any device

- For quick Markdown edits, open the repository in [github.dev](https://github.dev) by pressing a period on GitHub.
- For a local preview and a terminal, create a GitHub Codespace. The repository includes a Jekyll dev-container configuration.
- In the Codespace, run <code>bundle exec jekyll serve --livereload</code> and open the forwarded port 4000.

## Content workflow

- Add a post under <code>_posts/</code> using <code>YYYY-MM-DD-title.md</code> and Jekyll front matter.
- Keep unfinished posts in <code>_drafts/</code> until they are ready.
- Update the profile and CV in <code>blog/about.md</code> and <code>blog/cv.md</code>.
- Add navigation items in <code>_data/navigation.yml</code>. The nav is deliberately short; <code>/lab/</code> is unlisted.
- Project pages still work from <code>_projects/</code> (permalink <code>/projects/:name/</code>), but there is no index page linking them.

### Publications

<code>_data/publications.yml</code> is the single source: <code>blog/publications.md</code> renders the list from it and <code>assets/data/publications-vega.json</code> builds the timeline chart from the same entries, so the two cannot drift apart.

To refresh from Google Scholar (which has no API and blocks scripted access), export BibTeX from the profile and convert it:

    python3 scripts/import_bibtex.py citations.bib --merge _data/publications.yml > /tmp/pubs.yml
    mv /tmp/pubs.yml _data/publications.yml

<code>--merge</code> carries over the <code>topic:</code> values, which BibTeX does not contain and which colour the chart.

### Design tokens

Colours, fonts and spacing live as CSS custom properties in <code>_sass/_tokens.scss</code>. <code>_sass/_darkmode.scss</code> overrides only those values — if something does not respond to the theme, fix the component to read a <code>var(--…)</code> rather than adding a dark-mode rule.

## Rich posts

Pages can opt into browser-side capabilities with front matter:

    math: true
    mermaid: true
    vega_lite: true
    plotly: true

- MathJax renders LaTeX in the browser.
- Mermaid renders diagrams from Markdown-adjacent code blocks.
- Vega-Lite and Plotly render interactive charts from versioned libraries and local JSON files.
- Put chart specifications and data in <code>assets/data/</code> so changes stay reviewable and reproducible.
- Heavy Python or R computation should happen before publishing; commit the generated artifact, provenance, and a link to the source analysis.

The <code>/lab/</code> page exercises all four capabilities and doubles as a deployment smoke test. Reusable chart includes look like:

    {% include vega-lite.html id="my-chart" spec="/assets/data/example-vega.json" label="Description of the chart" %}

## CI/CD

Pull requests build and validate the site but do not publish it. A push to the default branch builds and deploys it through GitHub Pages Actions. Enable **Settings → Pages → Build and deployment → GitHub Actions** once in the repository settings.

The CI validator checks JSON data, chart-spec references, Mermaid blocks, generated HTML, local links, duplicate IDs, image alt text, and generated search JSON.

## Local commands

    bundle install
    bundle exec jekyll serve --livereload
    bundle exec jekyll build
    python scripts/validate_site.py --site ./_site

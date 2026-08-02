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
- Add public CV files under <code>assets/cv/</code> and link them from the CV page.
- Add project pages under <code>_projects/</code>; the collection is listed at <code>/projects/</code>.
- Keep a short current snapshot in <code>blog/now.md</code>.
- Add navigation items in <code>_data/navigation.yml</code>.

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

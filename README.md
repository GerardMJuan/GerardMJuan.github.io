# GerardMJuan.github.io

Personal website, research notes, projects, and blog posts. The site is built with Jekyll and published to GitHub Pages.

## Work from any device

- For quick Markdown edits, open the repository in [github.dev](https://github.dev) by pressing `.` on GitHub.
- For a local preview and a terminal, create a GitHub Codespace. The repository includes a Jekyll dev-container configuration.
- In the Codespace, run `bundle exec jekyll serve --livereload` and open the forwarded port 4000.

## Content workflow

- Add a post under `_posts/` using `YYYY-MM-DD-title.md` and Jekyll front matter.
- Keep unfinished posts in `_drafts/` until they are ready.
- Update the profile and CV in `blog/about.md` and `blog/cv.md`.
- Add public CV files under `assets/cv/` and link them from the CV page.
- Add navigation items in `_data/navigation.yml`.

Pull requests build the site but do not publish it. A push to the default branch builds and deploys the site through GitHub Pages. Enable **Settings → Pages → Build and deployment → GitHub Actions** once in the repository settings.

## Local commands

```bash
bundle install
bundle exec jekyll serve --livereload
bundle exec jekyll build
```

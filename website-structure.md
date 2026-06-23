# Website structure

This is a custom Jekyll theme (no external theme gem) hosted on GitHub Pages.

## Styling
- `assets/main.scss` — entry point, imports the partials below.
- `_sass/_variables.scss` — colours, fonts, spacing, breakpoints (design tokens).
- `_sass/_base.scss` — reset and typography.
- `_sass/_layout.scss` — wrapper, header/nav, footer, sections.
- `_sass/_components.scss` — hero, buttons, cards, chips, prose, lists.

## Layouts (`_layouts/`)
- `default.html` — HTML shell (head + header + footer).
- `page.html` — generic content page with a header band + prose body.
- `post.html` / `event.html` — single blog post / event.
- `pipeline.html` — single pipeline page.
  Posts, events and pipelines get their layout automatically via `defaults` in `_config.yml`.

## Includes (`_includes/`)
- `head.html` — meta, Open Graph, favicon, fonts, stylesheet.
- `header.html` — sticky nav; the Pipelines dropdown is built from the `_pipelines` collection.
- `footer.html` — footer with links and partner logos.

## Data (`_data/`)
- `nav.yml` — main navigation items.
- `pillars.yml` — the four-pillar mission story (homepage).
- `team.yml` — current and previous team (about page).
- `funders.yml` — funders, hosts, associated orgs (about page).
- `ambassadors.yml` — academic ambassadors (partners page).

## Pages
- `index.html` — homepage (hero + pillars + pipelines + news + CTA).
- `about.html`, `services.html`, `partners.html`, `pipelines.html`, `jobs.html` — built from data + Liquid.
- `blog.html`, `events.html` — list posts/events.
- `citations.md` — uses the `page` layout.
- `404.html` — not-found page.

## Adding a pipeline
Create a file in `_pipelines/`. Front matter: `title`, `nav_order`, `status`
(`Released` / `In development` / `Early development`), and a short `summary`.
It appears automatically in the nav dropdown, the homepage, and `/pipelines/`.

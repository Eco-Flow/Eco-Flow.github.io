# Maintainer's guide

How to run, update and operate the Eco-Flow website. This file is **not published** —
it's excluded from the Jekyll build (see `exclude` in `_config.yml`), so site visitors
never see it. It only appears here in the repository for maintainers.

For the file/folder map, see [website-structure.md](website-structure.md).
For first-time local setup, see [test_locally.md](test_locally.md).

---

## TL;DR — the common tasks

| I want to…                | Do this |
|---------------------------|---------|
| Write a blog post         | Add a file to [`_posts/`](_posts) |
| Announce an event         | Add a file to [`_events/`](_events) |
| Add / edit a pipeline     | Add or edit a file in [`_pipelines/`](_pipelines) |
| Change the team list      | Edit [`_data/team.yml`](_data/team.yml) |
| Change funders / partners | Edit [`_data/funders.yml`](_data/funders.yml) |
| Change ambassadors        | Edit [`_data/ambassadors.yml`](_data/ambassadors.yml) |
| Change the nav menu       | Edit [`_data/nav.yml`](_data/nav.yml) |
| Change colours / fonts    | Edit [`_sass/_variables.scss`](_sass/_variables.scss) |
| Publish changes           | Commit and push to the `publish` branch |

Images go in [`img/`](img) and are referenced as `/img/your-file.png`.

---

## Running the site locally (preview before publishing)

You need Ruby 3.3 (matches GitHub Pages). Installed once via Homebrew as `ruby@3.3`.

```bash
# from the repository root
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8   # avoids "Invalid US-ASCII" build errors

bundle install            # first time only
bundle exec jekyll serve  # then open http://127.0.0.1:4000
```

`jekyll serve` auto-rebuilds as you save files, so you can see changes live. Stop it with
`Ctrl-C`. (If `bundle`/`jekyll` aren't found, see [test_locally.md](test_locally.md).)

---

## Writing a blog post

1. Create a file in `_posts/` named `YYYY-MM-DD-short-title.md` (the date in the filename
   matters — it sets the post date and ordering).
2. Start it with this front matter:

   ```yaml
   ---
   title: 'Your post title'
   date: 2026-06-23
   description: 'One sentence shown on the blog list and as the social-media preview.'
   author: 'Your Name'
   tags: ["nextflow", "nf-core", "hackathon"]
   ---
   ```
3. Write the body in Markdown below the front matter.
4. Add any images to `img/` and reference them as `/img/your-image.png`.

Notes:
- The layout is applied automatically — **do not** add `layout:` yourself.
- Future-dated posts are hidden from the blog until that date arrives.
- Don't repeat the title as a heading at the top of the body; it's shown automatically.

## Announcing an event

Same pattern, in `_events/` named `YYYY-MM-DD-short-name.md`:

```yaml
---
title: 'Workshop / event name'
date: 2026-07-21
description: 'One-sentence summary.'
author: 'Your Name'
tags: ["workshop", "metabarcoding"]
---
```

The Events page automatically lists it under **Upcoming** until its date passes, then moves
it to **Past events**.

## Adding or editing a pipeline

Each pipeline is a file in `_pipelines/`, e.g. `_pipelines/my-pipeline.md`:

```yaml
---
title: "Eco-Flow/my-pipeline"
nav_order: 8                     # controls order in the nav dropdown & lists
status: Released                 # Released | In development | Early development
summary: "One sentence shown on the pipeline cards."
---
```

Then write the full description in Markdown. A new pipeline automatically appears in:
- the **Pipelines** dropdown in the top navigation,
- the **featured pipelines** on the homepage,
- the **/pipelines/** listing, grouped by its `status`.

Use `/img/...` (a leading slash) for images in pipeline pages so they work on every URL.
The `status` value must be spelled exactly as one of the three options above, or the
pipeline won't show up in a group on the listing page.

---

## Editing the data-driven pages (no HTML needed)

These pages are built from YAML data files — edit the data, not the page:

- **Team** (About page): [`_data/team.yml`](_data/team.yml) — `current:` and `previous:`
  lists, each entry with `name`, `role`, `photo`, `bio`, and optional `link` and
  `linkedin` (a LinkedIn URL; adds a "Connect" button to that person's card).
- **Funders / hosts / associated orgs** (About page):
  [`_data/funders.yml`](_data/funders.yml) — `funding:`, `hosts:`, `associated:`.
- **Ambassadors** (Partners page): [`_data/ambassadors.yml`](_data/ambassadors.yml) —
  `name`, `affiliation`, `url`.
- **External projects** (Pipelines page "Projects we support"):
  [`_data/external_projects.yml`](_data/external_projects.yml) — projects we advise on
  but don't own. Each entry: `name`, `org`, `url` (links out to the repo), `summary`.
- **Homepage mission pillars**: [`_data/pillars.yml`](_data/pillars.yml).
- **Top navigation**: [`_data/nav.yml`](_data/nav.yml).

Photos/logos referenced in these files live in `img/` and use the `/img/...` path.

## Changing the look (colours, fonts, spacing)

All design tokens are in [`_sass/_variables.scss`](_sass/_variables.scss) — change a value
there and it updates everywhere. For example `$green` is the primary brand colour and
`$font-head` is the heading font. Larger structural styles live in the other `_sass/_*.scss`
partials. The header, footer and `<head>` (favicon, social-card image, fonts) are in
[`_includes/`](_includes).

---

## Publishing changes (deploying to the live site)

The live site is served from the **`publish`** branch via GitHub Pages.

```bash
git add -A
git commit -m "Describe your change"
git push origin publish
```

GitHub rebuilds and deploys automatically within a minute or two to
<https://eco-flow.github.io/>. For bigger changes, work on a branch and open a Pull
Request into `publish` instead of committing directly.

**Tip:** preview locally with `jekyll serve` first — if it builds cleanly there, it will
build on GitHub (same Ruby/Jekyll versions).

### If a deploy fails
Check the repository's **Actions / Pages** tab on GitHub for the error. The most common
causes are a YAML typo in front matter or a data file (indentation matters), or a
referenced image that doesn't exist in `img/`.

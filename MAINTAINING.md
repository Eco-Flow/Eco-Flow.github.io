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
| Update the stats page numbers | Edit the manual figures in [`numbers.html`](numbers.html) — see ["Eco-Flow in numbers"](#the-eco-flow-in-numbers-page-numbers) |
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
repo: Eco-Flow/my-pipeline        # owner/name on GitHub — see "Live GitHub stats" below
nav_order: 8                     # controls order in the nav dropdown & lists
status: Released                 # Released | In development | Early development
summary: "One sentence shown on the pipeline cards."
---
```

A new pipeline automatically appears in:
- the **Pipelines** dropdown in the top navigation,
- the **featured pipelines** on the homepage,
- the **/pipelines/** listing, grouped by its `status`.

The `status` value must be spelled exactly as one of the three options above, or the pipeline
won't show up in a group on the listing page.

**Don't write a Markdown body for a pipeline with a `repo:` field** — the page content is the
repo's own `README.md`, synced automatically (see below). Anything you type in the body would
just be overridden by the README on the next sync, since the layout prefers the synced README
whenever one exists. The one exception is [`_pipelines/about.md`](_pipelines/about.md), which
has no `repo:` and keeps its own hand-written body, since it's an explainer page, not a single
pipeline.

If a repo's README isn't ready to show publicly yet (e.g. still full of `TODO nf-core:`
boilerplate), set `sync_readme: false` in that pipeline's front matter and write a short
hand-written body instead — see [`_pipelines/gwas.md`](_pipelines/gwas.md) for an example. The
stats badges (stars, release, updated) still come from the repo as normal; only the page body
falls back to your Markdown.

### Live GitHub stats and synced README

Any pipeline with a `repo:` field gets:
- a stats badge (★ stars, latest release tag, last updated date) on its card and its own page,
  from [`_data/pipelines_meta.yml`](_data/pipelines_meta.yml);
- its full page content pulled from the repo's `README.md`, from
  [`_data/pipeline_readmes.yml`](_data/pipeline_readmes.yml) — unless `sync_readme: false`.

Both files are **auto-generated** — don't edit them by hand. They're refreshed automatically
**every day at ~04:17 UTC, and on every push/merge to `publish`**, by the
[`sync-pipeline-meta`](.github/workflows/sync-pipeline-meta.yml) GitHub Action (also runnable
on demand from the **Actions** tab → *Run workflow*), which runs
[`scripts/sync_pipeline_meta.py`](scripts/sync_pipeline_meta.py) against the GitHub API for
every `repo:` value found in `_pipelines/`. The README sync strips the nf-core logo/badges
header and rewrites relative links/images to absolute GitHub URLs, so it's not quite a 1:1 raw
dump — but otherwise whatever's in the repo's README (including unfinished `TODO nf-core:`
boilerplate on early-stage pipelines) is what shows up on the site. **To change a pipeline
page's content, edit the README in that pipeline's own repo** — it appears here on the next
nightly sync. A pipeline with no `repo:` field, or no GitHub release yet, just shows whichever
badges it has data for.

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
- **Training course** (the `/training/` page): [`_data/training.yml`](_data/training.yml) —
  course intro, repo link, and the list of `parts` (each linking to its lesson on GitHub).
- **Homepage mission pillars**: [`_data/pillars.yml`](_data/pillars.yml).
- **Top navigation**: [`_data/nav.yml`](_data/nav.yml).

Photos/logos referenced in these files live in `img/` and use the `/img/...` path.

---

## The "Eco-Flow in numbers" page (`/numbers/`)

The stats page at [`numbers.html`](numbers.html) (linked under the **About ▾** dropdown) mixes
two kinds of figure. A **★ next to a section heading means that section updates itself
automatically** from a live source; everything else is either counted from the site's own
content or typed in by hand. The legend at the top of the page explains this to visitors.

### Manually-maintained figures — edit these by hand

A couple of numbers have no source to count from, so they're written directly into
[`numbers.html`](numbers.html), in the **"Eco-Flow general stats"** section under the comment
`Manually-maintained figures: edit the numbers below`:

- **Trainees taught** — currently `234`
- **Events** — currently `9` (this is the *claimed* total; the Events page itself only lists
  the events that have their own file in [`_events/`](_events))

To change them, just edit the number inside the relevant `<div class="stats__num">…</div>` and
publish. The other tiles in that section (training modules, pipelines, blog posts, ambassadors,
core team, projects we support) are **counted automatically** from your content — add a pipeline
or a post and the count goes up on its own.

### Auto figures (★) — don't edit by hand

- **Web stats** (page views, visits, countries, top pages, world map) come from **Cloudflare
  Web Analytics**, written into [`_data/stats.yml`](_data/stats.yml) by the
  [`sync-cloudflare-stats`](.github/workflows/sync-cloudflare-stats.yml) GitHub Action
  (automatically **every day at ~05:37 UTC, and on every push/merge to `publish`**, or on
  demand from the Actions tab). It runs
  [`scripts/fetch_cloudflare_stats.py`](scripts/fetch_cloudflare_stats.py).
  - It needs one repo secret: **`CLOUDFLARE_API_TOKEN`** (a token with *Account Analytics →
    Read*). Set under **Settings → Secrets and variables → Actions**.
  - The Cloudflare **site tag** (different from the public beacon token!) is set in the script as
    `SITE_TAG`. If analytics ever read zero, the script logs which site tags actually have data.
  - The tracking beacon itself lives in [`_includes/head.html`](_includes/head.html) and loads on
    every page — it's cookieless, so no consent banner is needed.
- **GitHub stats** (total stars, tracked repos, stars-by-pipeline) come from the same
  [`_data/pipelines_meta.yml`](_data/pipelines_meta.yml) used by the pipeline pages — refreshed by
  the `sync-pipeline-meta` Action described above.

### The world map

Shaded by page views per country, using a **vendored** copy of jsVectorMap in
[`assets/vendor/jsvectormap/`](assets/vendor/jsvectormap) (no third-party CDN). Cloudflare only
reports location at country level, so there's no within-country (e.g. UK regional) breakdown.

### Historical snapshots (for trends over time)

The live Cloudflare/GitHub figures are *current* only — to keep a history we append a weekly
row to [`_data/stats_history.csv`](_data/stats_history.csv) (date, weekly/30-day page views,
weekly visits, countries, total GitHub stars, pipeline count). This is done **every Monday at
~06:00 UTC** (or on demand from the Actions tab) by the
[`snapshot-stats`](.github/workflows/snapshot-stats.yml) Action, which runs
[`scripts/snapshot_stats.py`](scripts/snapshot_stats.py) against the already-synced data files.

It's just collecting the history for now — nothing on the site plots it yet. Because the weekly
`pageviews_7d` figures tile the timeline, a running sum gives cumulative traffic; `github_stars`
is already cumulative. The CSV is in `_data/`, so a future chart could read it directly via
`site.data.stats_history`. **Don't edit the CSV by hand** — it's appended automatically.

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

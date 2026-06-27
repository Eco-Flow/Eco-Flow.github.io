#!/usr/bin/env python3
"""Append a weekly snapshot of key stats to _data/stats_history.csv.

Reads the already-synced data files — _data/stats.yml (Cloudflare web stats)
and _data/pipelines_meta.yml (GitHub stars) — and records one row per run so
we can chart traffic and GitHub stars over time later. Run weekly by the
`snapshot-stats` GitHub Action.

Notes:
- `pageviews_7d` / `visits_7d` are that week's figures; taken weekly they tile
  the timeline, so a running sum gives cumulative totals.
- `github_stars` is already a cumulative count.
- Re-running on the same day updates that day's row rather than duplicating it.
"""

import csv
import datetime
import os

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_PATH = os.path.join(REPO_ROOT, "_data", "stats.yml")
META_PATH = os.path.join(REPO_ROOT, "_data", "pipelines_meta.yml")
HISTORY_PATH = os.path.join(REPO_ROOT, "_data", "stats_history.csv")

FIELDS = ["date", "pageviews_7d", "pageviews_30d", "visits_7d",
          "countries_7d", "github_stars", "pipelines"]


def load_yaml(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def main():
    stats = load_yaml(STATS_PATH)
    meta = load_yaml(META_PATH)
    stars = sum(int((v or {}).get("stars") or 0) for v in meta.values())

    row = {
        "date": datetime.date.today().isoformat(),
        "pageviews_7d": int(stats.get("pageviews_7d") or 0),
        "pageviews_30d": int(stats.get("pageviews_30d") or 0),
        "visits_7d": int(stats.get("visits_7d") or 0),
        "countries_7d": int(stats.get("countries_7d") or 0),
        "github_stars": stars,
        "pipelines": len(meta),
    }

    rows = []
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, newline="") as f:
            rows = list(csv.DictReader(f))

    # Replace today's row if it already exists, then keep sorted by date.
    rows = [r for r in rows if r.get("date") != row["date"]]
    rows.append(row)
    rows.sort(key=lambda r: r["date"])

    with open(HISTORY_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in FIELDS})

    print(f"Snapshot {row['date']}: {row['pageviews_7d']} views/7d, "
          f"{row['visits_7d']} visits/7d, {stars} GitHub stars.")


if __name__ == "__main__":
    main()

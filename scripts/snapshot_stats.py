#!/usr/bin/env python3
"""Weekly stats history row.

Appends one flat row per week to _data/stats_history.csv, for charting trends
over time. Reads the already-synced data files (stats.yml, pipelines_meta.yml).

The cumulative all-time totals (_data/stats_totals.yml) are NOT maintained here
any more — they're built daily from accurate per-day Cloudflare figures by
scripts/fetch_cloudflare_stats.py. This script only records the weekly trend
snapshot.

Idempotent: re-running on the same day overwrites that day's row rather than
adding a duplicate.
"""

import csv
import datetime
import os

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_PATH = os.path.join(REPO_ROOT, "_data", "stats.yml")
META_PATH = os.path.join(REPO_ROOT, "_data", "pipelines_meta.yml")
HISTORY_PATH = os.path.join(REPO_ROOT, "_data", "stats_history.csv")

CSV_FIELDS = ["date", "pageviews_7d", "pageviews_30d", "visits_7d",
              "countries_7d", "github_stars", "pipelines"]


def load_yaml(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def write_history_row(stats, stars, meta, today):
    row = {
        "date": today,
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
    rows = [r for r in rows if r.get("date") != today]
    rows.append(row)
    rows.sort(key=lambda r: r["date"])
    with open(HISTORY_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in CSV_FIELDS})


def main():
    today = datetime.date.today().isoformat()
    stats = load_yaml(STATS_PATH)
    meta = load_yaml(META_PATH)
    stars = sum(int((v or {}).get("stars") or 0) for v in meta.values())

    write_history_row(stats, stars, meta, today)

    print(f"History row {today}: {stats.get('pageviews_7d', 0)} views / "
          f"{stats.get('visits_7d', 0)} visits in the last 7 days; {stars} GitHub stars.")


if __name__ == "__main__":
    main()

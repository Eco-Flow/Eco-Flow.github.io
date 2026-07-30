#!/usr/bin/env python3
"""Fetch Cloudflare Web Analytics into Jekyll data files.

Writes two files the /numbers/ page renders:

- _data/stats.yml        : the live snapshot — accurate 7-day figures plus
                           wider (30/90-day) headline totals.
- _data/stats_totals.yml : a persisted, cumulative ledger of all-time totals
                           (page views, visits, per-page and per-country
                           counts), built by summing accurate *per-day*
                           Cloudflare figures.

Why per-day accumulation: Cloudflare only returns unsampled data over short
windows. A single wide query (e.g. 90 days) is sampled — counts come back as
lumpy multiples of the sample rate and rare events (a country with one visit)
get dropped. So for true all-time totals we query **one calendar day at a
time** (always unsampled) and add each day into the ledger exactly once,
tracked in `counted_dates`. Summing non-overlapping days gives a real total
with no double-counting and no sampling — the number that matches the
Cloudflare dashboard.

Idempotent: only whole days up to *yesterday* are ingested (today is still in
progress), and a day already in `counted_dates` is never re-added. So the daily
schedule, the 12h backup run, and per-push runs can all fire without
double-counting, and a gap (Actions down for days) self-heals on the next run.

Runs from GitHub Actions (see .github/workflows/sync-cloudflare-stats.yml) so
the API token stays a repo secret and never reaches the public site.

Required environment variables (set as GitHub Actions secrets):
  CLOUDFLARE_API_TOKEN   - token with "Account Analytics: Read" permission

Optional:
  CLOUDFLARE_ACCOUNT_ID  - account ID; if omitted, it is auto-discovered from
                           the token (the token is scoped to one account)
  CLOUDFLARE_SITE_TAG    - the Web Analytics site tag (defaults to the tag
                           already baked into the public beacon, so usually
                           not needed)
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(REPO_ROOT, "_data", "stats.yml")
LEDGER_PATH = os.path.join(REPO_ROOT, "_data", "stats_totals.yml")

API_URL = "https://api.cloudflare.com/client/v4/graphql"
LAUNCH_DATE = "2026-06-27"  # first day the beacon was live

# Ledger schema marker. Bump this to force a clean rebuild of stats_totals.yml
# (discarding any totals produced by an earlier, less accurate method).
LEDGER_METHOD = "per-day-visits"  # bump to force a clean rebuild of the ledger

API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
# The Web Analytics GraphQL site tag (NOT the public beacon token — they differ).
# Discovered via the SITES_QUERY diagnostic. Override with CLOUDFLARE_SITE_TAG.
SITE_TAG = os.environ.get("CLOUDFLARE_SITE_TAG", "4d8094a5292c4a7db2bc1a1a0f73e78d")


def load_yaml(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def graphql_raw(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if payload.get("errors"):
        raise RuntimeError(f"GraphQL errors: {payload['errors']}")
    return payload["data"]["viewer"]["accounts"]


def graphql(query, variables):
    accounts = graphql_raw(query, variables)
    if not accounts:
        raise RuntimeError("No Cloudflare account accessible with this token.")
    return accounts[0]


ACCOUNTS_QUERY = "query { viewer { accounts { accountTag } } }"


def discover_account_tag():
    """Find the account the token is scoped to, so a (possibly wrong) account
    ID secret isn't needed."""
    acct = graphql(ACCOUNTS_QUERY, {})
    print(f"Using Cloudflare account: {acct['accountTag']}")
    return acct["accountTag"]


TOTALS_QUERY = """
query Totals($account: String!, $site: String!, $start: Date!, $end: Date!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
      totals: rumPageloadEventsAdaptiveGroups(
        filter: { siteTag: $site, date_geq: $start, date_leq: $end }
        limit: 1
      ) {
        count
        sum { visits }
      }
    }
  }
}
"""

BREAKDOWN_QUERY = """
query Breakdown($account: String!, $site: String!, $start: Date!, $end: Date!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
      pages: rumPageloadEventsAdaptiveGroups(
        filter: { siteTag: $site, date_geq: $start, date_leq: $end }
        limit: 50
        orderBy: [count_DESC]
      ) {
        count
        dimensions { requestPath }
      }
      countries: rumPageloadEventsAdaptiveGroups(
        filter: { siteTag: $site, date_geq: $start, date_leq: $end }
        limit: 250
        orderBy: [count_DESC]
      ) {
        count
        sum { visits }
        dimensions { countryName }
      }
    }
  }
}
"""


# Single-day breakdown used to build the cumulative ledger. Cloudflare samples
# by the query's date SPAN (not its grouping), so a wide query returns rounded,
# lumpy counts that drop rare countries. We therefore query ONE day per request
# (the narrowest possible span) to keep each day's figures unsampled, then sum.
DAY_QUERY = """
query Day($account: String!, $site: String!, $day: Date!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
      totals: rumPageloadEventsAdaptiveGroups(
        filter: { siteTag: $site, date_geq: $day, date_leq: $day }
        limit: 1
      ) {
        count
        sum { visits }
      }
      pages: rumPageloadEventsAdaptiveGroups(
        filter: { siteTag: $site, date_geq: $day, date_leq: $day }
        limit: 200
        orderBy: [count_DESC]
      ) {
        count
        dimensions { requestPath }
      }
      countries: rumPageloadEventsAdaptiveGroups(
        filter: { siteTag: $site, date_geq: $day, date_leq: $day }
        limit: 250
        orderBy: [count_DESC]
      ) {
        count
        sum { visits }
        dimensions { countryName }
      }
    }
  }
}
"""


SITES_QUERY = """
query Sites($account: String!, $start: Date!, $end: Date!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
      sites: rumPageloadEventsAdaptiveGroups(
        filter: { date_geq: $start, date_leq: $end }
        limit: 20
        orderBy: [count_DESC]
      ) {
        count
        dimensions { siteTag }
      }
    }
  }
}
"""


def totals(start, end):
    data = graphql(TOTALS_QUERY, {"account": ACCOUNT_ID, "site": SITE_TAG,
                                  "start": start, "end": end})
    groups = data.get("totals") or []
    if not groups:
        return 0, 0
    g = groups[0]
    return int(g["count"]), int((g.get("sum") or {}).get("visits") or 0)


def update_ledger(yesterday):
    """Accumulate accurate per-day figures into the cumulative ledger.

    Reads the previous ledger, queries Cloudflare for every day not yet counted
    (up to `yesterday`), and adds each whole day exactly once. Returns the new
    ledger dict.
    """
    prev = load_yaml(LEDGER_PATH)
    # Discard any ledger built by an older method so the totals rebuild cleanly
    # from accurate per-day data.
    if prev.get("method") != LEDGER_METHOD:
        if prev:
            print("Ledger method changed - rebuilding all-time totals from launch.")
        prev = {}

    counted = set(prev.get("counted_dates") or [])
    pages = {p["path"]: int(p["views"]) for p in (prev.get("top_pages") or [])}
    countries = {c["name"]: int(c["views"]) for c in (prev.get("top_countries") or [])}
    # Per-country visits, tracked alongside page views so the /numbers/ country
    # list can be shown in visits (sessions) rather than clicks.
    country_visits = {c["name"]: int(c.get("visits") or 0)
                      for c in (prev.get("top_countries") or [])}
    pv = int(prev.get("pageviews") or 0)
    vis = int(prev.get("visits") or 0)

    # Walk every day from launch to yesterday, querying each uncounted day with
    # its own single-day request (so it stays unsampled) and adding it once.
    # Already-counted days are skipped without a request, so after the initial
    # backfill this makes just one request per run.
    day = datetime.date.fromisoformat(LAUNCH_DATE)
    last = datetime.date.fromisoformat(yesterday)
    ingested = 0
    while day <= last:
        iso = day.isoformat()
        day += datetime.timedelta(days=1)
        if iso in counted:
            continue

        data = graphql(DAY_QUERY, {"account": ACCOUNT_ID, "site": SITE_TAG,
                                   "day": iso})
        tgroups = data.get("totals") or []
        if tgroups:
            pv += int(tgroups[0]["count"])
            vis += int((tgroups[0].get("sum") or {}).get("visits") or 0)
        for g in (data.get("pages") or []):
            path = g["dimensions"]["requestPath"] or "/"
            pages[path] = pages.get(path, 0) + int(g["count"])
        for g in (data.get("countries") or []):
            name = g["dimensions"]["countryName"] or "Unknown"
            countries[name] = countries.get(name, 0) + int(g["count"])
            country_visits[name] = (country_visits.get(name, 0)
                                    + int((g.get("sum") or {}).get("visits") or 0))

        counted.add(iso)
        ingested += 1

    print(f"Ledger: ingested {ingested} new day(s); "
          f"{pv} page views / {vis} visits all-time across {len(countries)} countries.")

    return {
        "updated": datetime.date.today().isoformat(),
        "method": LEDGER_METHOD,
        "counted_dates": sorted(counted),
        "pageviews": pv,
        "visits": vis,
        "countries_count": len(countries),
        "top_pages": _ranked(pages, "path"),
        # Ranked by visits (sessions), which is what the page displays.
        "top_countries": _ranked(countries, "name", visits=country_visits,
                                 by="visits"),
    }


def _ranked(counts, key, visits=None, by="views"):
    """Turn a {name: views} map into a list sorted by count (desc), then name.

    If `visits` is given, each entry also carries a "visits" figure, and `by`
    chooses which of the two the ranking uses.
    """
    def entry(n, v):
        e = {key: n, "views": v}
        if visits is not None:
            e["visits"] = visits.get(n, 0)
        return e

    rows = [entry(n, v) for n, v in counts.items()]
    return sorted(rows, key=lambda e: (-e[by], e[key]))


def main():
    global ACCOUNT_ID
    if not API_TOKEN:
        sys.exit("CLOUDFLARE_API_TOKEN must be set.")
    # Use the supplied account ID if present (required for tokens scoped to one
    # account). If absent, discover it (works for "All accounts" tokens).
    if ACCOUNT_ID:
        print(f"Using supplied account ID: {ACCOUNT_ID}")
    else:
        ACCOUNT_ID = discover_account_tag()

    today = datetime.date.today()
    d = lambda days: (today - datetime.timedelta(days=days)).isoformat()
    end = today.isoformat()
    yesterday = (today - datetime.timedelta(days=1)).isoformat()

    # Wider headline totals. These span up to 90 days (Cloudflare caps a single
    # query at ~93 days) and are *sampled*, so they're only a rough headline;
    # the accurate all-time figures come from the per-day ledger below.
    pv_all, v_all = totals(d(90), end)
    pv_30, v_30 = totals(d(30), end)
    pv_7, v_7 = totals(d(7), end)

    if pv_all == 0:
        # Diagnostic: which site tags actually have data in this account?
        diag = graphql(SITES_QUERY, {"account": ACCOUNT_ID, "start": d(30), "end": end})
        sites = diag.get("sites") or []
        if sites:
            print("No data for our site tag. Site tags with data (last 30d):")
            for s in sites:
                print(f"  {s['dimensions']['siteTag']}: {s['count']} page views")
            print(f"(We queried siteTag={SITE_TAG})")
        else:
            print(f"No RUM data in this account yet for the last 30 days "
                  f"(queried siteTag={SITE_TAG}). Likely too soon after setup.")

    # Live breakdowns use the 7-day window: at low traffic Cloudflare samples
    # wider queries, so the 7-day window is the accurate "recent" view.
    bd = graphql(BREAKDOWN_QUERY, {"account": ACCOUNT_ID, "site": SITE_TAG,
                                   "start": d(7), "end": end})

    top_pages = [
        {"path": (p["dimensions"]["requestPath"] or "/"), "views": int(p["count"])}
        for p in (bd.get("pages") or [])
    ]
    country_groups = bd.get("countries") or []
    top_countries = [
        {"name": (c["dimensions"]["countryName"] or "Unknown"),
         "views": int(c["count"]),
         "visits": int((c.get("sum") or {}).get("visits") or 0)}
        for c in country_groups[:100]
    ]
    top_countries.sort(key=lambda c: (-c["visits"], c["name"]))

    # Accurate cumulative all-time totals, summed from unsampled per-day figures.
    ledger = update_ledger(yesterday)

    out = {
        "updated": end,
        "since": LAUNCH_DATE,
        "pageviews_all": pv_all,
        "visits_all": v_all,
        "pageviews_30d": pv_30,
        "visits_30d": v_30,
        "pageviews_7d": pv_7,
        "visits_7d": v_7,
        "countries_7d": len(country_groups),
        # All-time country count comes from the accurate ledger.
        "countries_all": ledger["countries_count"],
        "top_pages": top_pages,
        "top_countries": top_countries,
    }

    stats_header = (
        "# Auto-generated by scripts/fetch_cloudflare_stats.py (GitHub Actions).\n"
        "# DO NOT edit by hand - values are overwritten on the next nightly sync.\n"
    )
    with open(OUTPUT_PATH, "w") as f:
        f.write(stats_header)
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)

    ledger_header = (
        "# Auto-generated by scripts/fetch_cloudflare_stats.py (GitHub Actions).\n"
        "# Cumulative all-time totals, summed from accurate per-day Cloudflare\n"
        "# figures. Each day is counted once (see counted_dates). DO NOT edit.\n"
    )
    with open(LEDGER_PATH, "w") as f:
        f.write(ledger_header)
        yaml.safe_dump(ledger, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {OUTPUT_PATH}: {pv_all} page views (90d headline), {pv_7} in 7d.")


if __name__ == "__main__":
    main()

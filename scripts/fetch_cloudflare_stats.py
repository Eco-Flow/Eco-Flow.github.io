#!/usr/bin/env python3
"""Fetch Cloudflare Web Analytics totals into a Jekyll data file.

Writes _data/stats.yml with page views, visits, country count and top pages,
which the /numbers/ page renders. Runs from GitHub Actions (see
.github/workflows/sync-cloudflare-stats.yml) so the API token stays a repo
secret and never reaches the public site.

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

API_URL = "https://api.cloudflare.com/client/v4/graphql"
LAUNCH_DATE = "2026-06-27"  # first day the beacon was live

API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
# The Web Analytics GraphQL site tag (NOT the public beacon token — they differ).
# Discovered via the SITES_QUERY diagnostic. Override with CLOUDFLARE_SITE_TAG.
SITE_TAG = os.environ.get("CLOUDFLARE_SITE_TAG", "4d8094a5292c4a7db2bc1a1a0f73e78d")


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
        limit: 10
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

    # "Total" spans 90 days (Cloudflare caps a single query at ~93 days) so it
    # is always a superset of the 30- and 7-day figures.
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

    bd = graphql(BREAKDOWN_QUERY, {"account": ACCOUNT_ID, "site": SITE_TAG,
                                   "start": d(30), "end": end})

    top_pages = [
        {"path": (p["dimensions"]["requestPath"] or "/"), "views": int(p["count"])}
        for p in (bd.get("pages") or [])
    ]
    country_groups = bd.get("countries") or []
    # Keep up to 100 countries: the page lists the top few and uses the full
    # set to shade the world map. "countryName" is actually an ISO-2 code (GB).
    top_countries = [
        {"name": (c["dimensions"]["countryName"] or "Unknown"), "views": int(c["count"])}
        for c in country_groups[:100]
    ]

    out = {
        "updated": end,
        "since": LAUNCH_DATE,
        "pageviews_all": pv_all,
        "visits_all": v_all,
        "pageviews_30d": pv_30,
        "visits_30d": v_30,
        "pageviews_7d": pv_7,
        "visits_7d": v_7,
        "countries_30d": len(country_groups),
        "top_pages": top_pages,
        "top_countries": top_countries,
    }

    header = (
        "# Auto-generated by scripts/fetch_cloudflare_stats.py (GitHub Actions).\n"
        "# DO NOT edit by hand - values are overwritten on the next nightly sync.\n"
    )
    with open(OUTPUT_PATH, "w") as f:
        f.write(header)
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {OUTPUT_PATH}: {pv_all} page views all-time, {pv_30} in 30d.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Sync per-pipeline GitHub data into Jekyll data files:

- _data/pipelines_meta.yml    star count, latest release, last-updated date
- _data/pipeline_readmes.yml  cleaned-up README content (badges/logo header
                               stripped, relative links/images rewritten to
                               absolute GitHub URLs)

The repo list is derived from the `repo:` front matter field in _pipelines/*.md
(not a separate config), so adding `repo:` to a new pipeline file is enough to
pick it up on the next sync.
"""

import datetime
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINES_DIR = os.path.join(REPO_ROOT, "_pipelines")
META_OUTPUT_PATH = os.path.join(REPO_ROOT, "_data", "pipelines_meta.yml")
README_OUTPUT_PATH = os.path.join(REPO_ROOT, "_data", "pipeline_readmes.yml")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Matches a whole line that's made up entirely of one or more badge images
# wrapped in a link, e.g. [![label](badge.svg)](https://...), which is how
# nf-core-template READMEs render their CI/Slack/social badges.
BADGE_LINE_RE = re.compile(r"^\[!\[.*\]\(.*\)\]\(.*\)$")
PLAIN_IMAGE_LINE_RE = re.compile(r"^!\[.*\]\(.*\)$")

IMG_MD_RE = re.compile(r"(!\[[^\]]*\]\()([^)]+)(\))")
LINK_MD_RE = re.compile(r"(?<!!)(\[[^\]]*\]\()([^)]+)(\))")
IMG_HTML_RE = re.compile(r'(<img[^>]*\ssrc=")([^"]+)(")')
SOURCE_HTML_RE = re.compile(r'(<source[^>]*\ssrcset=")([^"]+)(")')


def collect_pipelines():
    pipelines = []
    for path in sorted(glob.glob(os.path.join(PIPELINES_DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if not text.startswith("---"):
            continue
        front_matter = text.split("---", 2)[1]
        data = yaml.safe_load(front_matter) or {}
        repo = data.get("repo")
        if repo:
            pipelines.append(repo)
    return sorted(set(pipelines))


def api_get(path, raw=False):
    url = f"https://api.github.com{path}"
    accept = "application/vnd.github.raw+json" if raw else "application/vnd.github+json"
    req = urllib.request.Request(url, headers={"Accept": accept})
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    with urllib.request.urlopen(req) as resp:
        body = resp.read()
        return body.decode("utf-8") if raw else json.loads(body)


def format_date(iso_str):
    return datetime.datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %-d, %Y")


def fetch_meta(repo, repo_info):
    meta = {
        "stars": repo_info.get("stargazers_count", 0),
        "updated_at": format_date(repo_info["pushed_at"]),
    }
    try:
        release = api_get(f"/repos/{repo}/releases/latest")
        meta["latest_release"] = release.get("tag_name")
        meta["released_at"] = format_date(release["published_at"])
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    return meta


def is_relative_url(url):
    return not re.match(r"^(https?:|mailto:|#)", url)


def rewrite_relative_url(url, repo, branch, raw):
    if not is_relative_url(url):
        return url
    base = "https://raw.githubusercontent.com" if raw else "https://github.com"
    path = url.lstrip("./")
    return f"{base}/{repo}/{branch}/{path}" if raw else f"{base}/{repo}/blob/{branch}/{path}"


def rewrite_links(text, repo, branch):
    text = IMG_MD_RE.sub(lambda m: m.group(1) + rewrite_relative_url(m.group(2), repo, branch, raw=True) + m.group(3), text)
    text = IMG_HTML_RE.sub(lambda m: m.group(1) + rewrite_relative_url(m.group(2), repo, branch, raw=True) + m.group(3), text)
    text = SOURCE_HTML_RE.sub(lambda m: m.group(1) + rewrite_relative_url(m.group(2), repo, branch, raw=True) + m.group(3), text)
    text = LINK_MD_RE.sub(lambda m: m.group(1) + rewrite_relative_url(m.group(2), repo, branch, raw=False) + m.group(3), text)
    return text


def strip_badge_header(text):
    """Drop the nf-core-style logo <h1> block and any leading badge lines."""
    text = re.sub(r"^\s*<h1>.*?</h1>\s*", "", text, count=1, flags=re.DOTALL)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == "" or BADGE_LINE_RE.match(stripped) or PLAIN_IMAGE_LINE_RE.match(stripped):
            i += 1
            continue
        break
    return "\n".join(lines[i:]).strip()


def fetch_readme(repo, branch):
    try:
        raw_text = api_get(f"/repos/{repo}/readme", raw=True)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    cleaned = strip_badge_header(raw_text)
    return rewrite_links(cleaned, repo, branch)


def main():
    repos = collect_pipelines()
    if not repos:
        print("No pipelines with a `repo:` front matter field found.")
        return

    meta_result = {}
    readme_result = {}
    for repo in repos:
        print(f"Fetching {repo}...")
        try:
            repo_info = api_get(f"/repos/{repo}")
            meta_result[repo] = fetch_meta(repo, repo_info)
            readme = fetch_readme(repo, repo_info.get("default_branch", "main"))
            if readme:
                readme_result[repo] = readme
        except urllib.error.HTTPError as e:
            print(f"  failed: {e}", file=sys.stderr)

    os.makedirs(os.path.dirname(META_OUTPUT_PATH), exist_ok=True)
    with open(META_OUTPUT_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(meta_result, f, sort_keys=True, default_flow_style=False)
    print(f"Wrote {META_OUTPUT_PATH}")

    with open(README_OUTPUT_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(readme_result, f, sort_keys=True, default_flow_style=False, default_style="|")
    print(f"Wrote {README_OUTPUT_PATH}")


if __name__ == "__main__":
    main()

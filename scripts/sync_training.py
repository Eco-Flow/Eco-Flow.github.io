#!/usr/bin/env python3
"""Sync the Eco-Flow Nextflow training lessons into this site.

The lessons are authored in the separate Eco-Flow/training repo
(eco-flow-training/docs/*.md). This pulls the lessons listed in
_data/training.yml into the `training` Jekyll collection so they render
natively at /training/<name>/ instead of linking out to GitHub.

For each lesson it:
  - fetches the raw Markdown,
  - strips the leading H1 (the layout renders the title),
  - rewrites cross-lesson `.md` links to /training/<name>/,
  - rewrites relative `img/` paths to /assets/training/img/,
  - prepends Jekyll front matter (layout / title / num / type / order),
and writes _training/<name>.md. Referenced relative images are downloaded
into assets/training/img/.

Which lessons are synced (and their order/metadata) is driven entirely by
_data/training.yml — add a part there and it gets picked up on the next run.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "_data", "training.yml")
OUT_DIR = os.path.join(REPO_ROOT, "_training")
IMG_DIR = os.path.join(REPO_ROOT, "assets", "training", "img")

# Source of the lessons (raw Markdown + the img/ folder beside them).
RAW_BASE = "https://raw.githubusercontent.com/Eco-Flow/training/main/eco-flow-training/docs/"
# Where images end up in the built site (no baseurl, so a root-absolute path).
IMG_WEB_BASE = "/assets/training/img/"

IMG_MD_RE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)([^)]*\))")
LINK_MD_RE = re.compile(r"(?<!!)(\[[^\]]*\]\()([^)\s]+)([^)]*\))")
IMG_HTML_RE = re.compile(r'(<img[^>]*?\ssrc=")([^"]+)(")', re.IGNORECASE)
H1_RE = re.compile(r"^\s*#\s+\S.*$", re.MULTILINE)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "eco-flow-sync"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def slug(filename):
    """nfcore_rnaseq.md -> nfcore-rnaseq (matches Jekyll's :name permalink,
    which replaces non-alphanumerics — including underscores — with hyphens)."""
    base = re.sub(r"\.md$", "", filename)
    return re.sub(r"[^A-Za-z0-9]+", "-", base).strip("-").lower()


def rewrite_link_target(url, known_slugs):
    """Rewrite a cross-lesson .md link to its on-site path; leave others alone."""
    m = re.match(r"^(?:\.{1,2}/)*(?:docs/)?([\w\-]+)\.md(#.*)?$", url)
    if not m:
        return url
    base, anchor = m.group(1), m.group(2) or ""
    if base.lower() == "readme":
        return "/training/" + anchor
    base_slug = re.sub(r"[^A-Za-z0-9]+", "-", base).strip("-").lower()
    if base_slug in known_slugs:
        return "/training/{}/{}".format(base_slug, anchor)
    return url


def rewrite_image_target(url, referenced):
    """Rewrite a relative img/ path to the on-site asset path; record the file."""
    if re.match(r"^(?:https?:)?//", url) or url.startswith("data:"):
        return url  # external / inline image — leave as-is
    name = url.split("/")[-1]
    referenced.add(name)
    return IMG_WEB_BASE + name


def transform(content, known_slugs, referenced):
    # Drop the first H1 — the layout renders the title from front matter.
    content = H1_RE.sub("", content, count=1).lstrip("\n")

    # Drop the source's hand-maintained breadcrumb lines (a line starting with
    # 🧭 that links to the previous/next lesson + course menu). The layout
    # already renders the authoritative "Part N" eyebrow and prev/next nav from
    # _data/training.yml, so these are redundant — and their hard-coded part
    # numbers can disagree with the site's ordering. Also strip the horizontal
    # rule the source pairs with the breadcrumb at the very top and bottom.
    content = re.sub(r"(?m)^[ \t]*🧭.*$", "", content).strip("\n")
    content = re.sub(r"^-{3,}[ \t]*\n+", "", content)
    content = re.sub(r"\n+[ \t]*-{3,}[ \t]*$", "", content).strip("\n")

    content = IMG_MD_RE.sub(
        lambda m: m.group(1) + rewrite_image_target(m.group(2), referenced) + m.group(3),
        content,
    )
    content = IMG_HTML_RE.sub(
        lambda m: m.group(1) + rewrite_image_target(m.group(2), referenced) + m.group(3),
        content,
    )
    content = LINK_MD_RE.sub(
        lambda m: m.group(1) + rewrite_link_target(m.group(2), known_slugs) + m.group(3),
        content,
    )
    return content


def front_matter(part, order):
    fields = {
        "layout": "training",
        "title": part.get("title", ""),
        "num": str(part.get("num", "")),
        "type": part.get("type", ""),
        "order": order,
    }
    if part.get("bonus"):
        fields["bonus"] = True
    lines = ["---"]
    for key, value in fields.items():
        lines.append("{}: {}".format(key, json.dumps(value)))
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main():
    with open(DATA_PATH) as fh:
        data = yaml.safe_load(fh)

    parts = data.get("parts", [])
    known_slugs = {slug(p["file"]) for p in parts}
    referenced = set()

    os.makedirs(OUT_DIR, exist_ok=True)

    for order, part in enumerate(parts):
        filename = part["file"]
        url = RAW_BASE + filename
        try:
            raw = fetch(url).decode("utf-8")
        except urllib.error.HTTPError as exc:
            print("ERROR fetching {}: {}".format(url, exc), file=sys.stderr)
            return 1

        body = transform(raw, known_slugs, referenced)
        out_path = os.path.join(OUT_DIR, filename)
        with open(out_path, "w") as fh:
            fh.write(front_matter(part, order))
            fh.write(body.rstrip() + "\n")
        print("wrote {}".format(os.path.relpath(out_path, REPO_ROOT)))

    if referenced:
        os.makedirs(IMG_DIR, exist_ok=True)
    for name in sorted(referenced):
        img_url = RAW_BASE + "img/" + urllib.request.quote(name)
        try:
            blob = fetch(img_url)
        except urllib.error.HTTPError as exc:
            print("WARN image {}: {}".format(img_url, exc), file=sys.stderr)
            continue
        with open(os.path.join(IMG_DIR, name), "wb") as fh:
            fh.write(blob)
        print("wrote {}".format(os.path.relpath(os.path.join(IMG_DIR, name), REPO_ROOT)))

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Pull Lichess user-blog posts (Atom feed) into website/blog/posts.json as url entries.

Usage:
  python website/blog/import_lichess.py
  python website/blog/import_lichess.py lucaistschlecht
  python website/blog/import_lichess.py lucaistschlecht --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent
POSTS_JSON = BLOG_DIR / "posts.json"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
DEFAULT_USER = "lucaistschlecht"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text or "post"


def load_posts() -> list[dict]:
    if not POSTS_JSON.exists():
        return []
    data = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError(f"{POSTS_JSON} must contain a JSON array")
    return data


def save_posts(posts: list[dict]) -> None:
    posts = sorted(posts, key=lambda p: p.get("date", ""), reverse=True)
    POSTS_JSON.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch_atom(username: str) -> str:
    url = f"https://lichess.org/@/{username}/blog.atom"
    req = urllib.request.Request(url, headers={"User-Agent": "leo.com-blog-import/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_entries(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    entries: list[dict] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title_el = entry.find("atom:title", ATOM_NS)
        link_el = entry.find("atom:link[@rel='alternate']", ATOM_NS)
        if link_el is None:
            link_el = entry.find("atom:link", ATOM_NS)
        published_el = entry.find("atom:published", ATOM_NS)
        if published_el is None:
            published_el = entry.find("atom:updated", ATOM_NS)

        title = (title_el.text or "").strip() if title_el is not None else ""
        href = (link_el.get("href") or "").strip() if link_el is not None else ""
        published = (published_el.text or "").strip() if published_el is not None else ""
        if not title or not href:
            continue

        tags: list[str] = ["lichess", "chess"]
        for cat in entry.findall("atom:category", ATOM_NS):
            term = (cat.get("term") or cat.get("label") or "").strip()
            if term:
                tag = term.lower()
                if tag not in tags:
                    tags.append(tag)

        # Prefer the human slug from the Lichess URL path
        # .../blog/<slug>/<id>
        m = re.search(r"/blog/([^/]+)/[^/]+/?$", href)
        path_slug = m.group(1) if m else slugify(title)
        slug = f"lichess-{path_slug}"

        try:
            post_date = datetime.fromisoformat(published.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            post_date = published[:10] if len(published) >= 10 else ""

        entries.append(
            {
                "slug": slug,
                "title": title,
                "date": post_date,
                "tags": tags,
                "url": href,
            }
        )
    return entries


def sync_lichess(username: str, dry_run: bool = False) -> tuple[int, int]:
    xml_text = fetch_atom(username)
    fetched = parse_entries(xml_text)
    if not fetched:
        raise RuntimeError(f"No blog entries found for @{username}")

    posts = load_posts()
    by_url = {p.get("url"): i for i, p in enumerate(posts) if p.get("url")}
    by_slug = {p.get("slug"): i for i, p in enumerate(posts)}

    added = 0
    updated = 0
    for entry in fetched:
        idx = by_url.get(entry["url"])
        if idx is None:
            idx = by_slug.get(entry["slug"])
        if idx is not None:
            # Keep local-only fields; refresh remote metadata
            existing = posts[idx]
            if existing.get("file"):
                # Don't overwrite a local markdown post that happens to share a slug
                if existing.get("url") != entry["url"]:
                    entry["slug"] = f"{entry['slug']}-{entry['url'].rstrip('/').split('/')[-1]}"
                    posts.append(entry)
                    added += 1
                    continue
            posts[idx] = {**existing, **entry}
            updated += 1
        else:
            posts.append(entry)
            added += 1

    if dry_run:
        print(f"Would sync {len(fetched)} Lichess posts ({added} new, {updated} updated)")
        for e in sorted(fetched, key=lambda p: p["date"], reverse=True):
            print(f"  {e['date']}  {e['title']}")
            print(f"           {e['url']}")
        return added, updated

    save_posts(posts)
    return added, updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Import Lichess blog posts as external url entries")
    parser.add_argument("username", nargs="?", default=DEFAULT_USER, help=f"Lichess username (default: {DEFAULT_USER})")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and print without writing posts.json")
    args = parser.parse_args()

    try:
        added, updated = sync_lichess(args.username, dry_run=args.dry_run)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run:
        print(f"Synced @{args.username}: {added} added, {updated} updated → {POSTS_JSON}")


if __name__ == "__main__":
    main()

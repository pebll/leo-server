#!/usr/bin/env python3
"""Import a Joplin MD + front matter export into website/blog/.

Usage:
  python website/blog/import_joplin.py /path/to/export-folder
  python website/blog/import_joplin.py /path/to/export-folder --force
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

try:
    import frontmatter
except ImportError:
    print("Missing dependency: python-frontmatter (pip install python-frontmatter)", file=sys.stderr)
    sys.exit(1)

BLOG_DIR = Path(__file__).resolve().parent
POSTS_JSON = BLOG_DIR / "posts.json"
POSTS_DIR = BLOG_DIR / "posts"
ASSETS_DIR = BLOG_DIR / "assets"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text or "post"


def find_markdown(export_dir: Path) -> Path:
    candidates = sorted(export_dir.rglob("*.md"), key=lambda p: (len(p.parts), str(p)))
    if not candidates:
        raise FileNotFoundError(f"No .md file found under {export_dir}")
    # Prefer shallowest; if several at same depth, require a single clear choice
    min_depth = len(candidates[0].parts)
    at_depth = [p for p in candidates if len(p.parts) == min_depth]
    if len(at_depth) > 1:
        names = "\n  ".join(str(p.relative_to(export_dir)) for p in at_depth)
        raise RuntimeError(f"Multiple markdown files at the same depth; export one note only:\n  {names}")
    return at_depth[0]


def find_resource_dirs(export_dir: Path) -> list[Path]:
    return sorted(p for p in export_dir.rglob("_resources") if p.is_dir())


def parse_date(value) -> str:
    if value is None or value == "":
        return date.today().isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(text[:10] if fmt == "%Y-%m-%d" and "T" in text else text, fmt).date().isoformat()
        except ValueError:
            pass
    if "T" in text:
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            pass
    # Joplin sometimes uses "YYYY-MM-DD HH:MM:SS"
    try:
        return datetime.strptime(text[:19], "%Y-%m-%d %H:%M:%S").date().isoformat()
    except ValueError:
        return date.today().isoformat()


def parse_tags(value) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(t).strip() for t in value if str(t).strip()]
    text = str(value).strip()
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1]
        return [t.strip().strip("'\"") for t in inner.split(",") if t.strip()]
    return [t.strip() for t in re.split(r"[, ]+", text) if t.strip()]


def rewrite_resource_paths(body: str, slug: str) -> str:
    # Joplin: ](_resources/...), ](./_resources/...), ](../_resources/...), src="_resources/..."
    body = re.sub(r"""(\]\()\./?_resources/""", rf"\1/blog/assets/{slug}/", body)
    body = re.sub(r"""(\]\()\.\./_resources/""", rf"\1/blog/assets/{slug}/", body)
    body = re.sub(r"""((?:src|href)=["'])\./?_resources/""", rf"\1/blog/assets/{slug}/", body)
    body = re.sub(r"""((?:src|href)=["'])\.\./_resources/""", rf"\1/blog/assets/{slug}/", body)
    # Remaining bare _resources/ references
    body = body.replace("_resources/", f"/blog/assets/{slug}/")
    return body


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


def import_export(export_dir: Path, force: bool = False) -> dict:
    export_dir = export_dir.resolve()
    if not export_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {export_dir}")

    md_path = find_markdown(export_dir)
    post = frontmatter.load(md_path)

    title = str(post.get("title") or md_path.stem).strip()
    slug = slugify(str(post.get("slug") or title))
    post_date = parse_date(post.get("date") or post.get("created") or post.get("updated"))
    tags = parse_tags(post.get("tags"))

    dest_md = POSTS_DIR / f"{slug}.md"
    dest_assets = ASSETS_DIR / slug

    if dest_md.exists() and not force:
        raise FileExistsError(f"Post already exists: {dest_md} (use --force to overwrite)")

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    if dest_assets.exists():
        shutil.rmtree(dest_assets)
    dest_assets.mkdir(parents=True, exist_ok=True)

    for res_dir in find_resource_dirs(export_dir):
        for src in res_dir.rglob("*"):
            if src.is_file():
                target = dest_assets / src.name
                # Avoid collisions if same name from multiple dirs
                if target.exists():
                    stem, suffix = src.stem, src.suffix
                    n = 2
                    while target.exists():
                        target = dest_assets / f"{stem}-{n}{suffix}"
                        n += 1
                shutil.copy2(src, target)

    body = rewrite_resource_paths(post.content, slug)
    meta = {
        "title": title,
        "date": post_date,
        "tags": tags,
        "slug": slug,
    }
    out = frontmatter.Post(body, **meta)
    dest_md.write_text(frontmatter.dumps(out) + "\n", encoding="utf-8")

    entry = {
        "slug": slug,
        "title": title,
        "date": post_date,
        "tags": tags,
        "file": f"posts/{slug}.md",
    }

    posts = load_posts()
    posts = [p for p in posts if p.get("slug") != slug]
    posts.append(entry)
    save_posts(posts)

    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a Joplin markdown export into the blog")
    parser.add_argument("export_dir", type=Path, help="Folder from Joplin MD + front matter export")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing post with the same slug")
    args = parser.parse_args()

    try:
        entry = import_export(args.export_dir, force=args.force)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Imported: {entry['title']}")
    print(f"  slug:  {entry['slug']}")
    print(f"  date:  {entry['date']}")
    print(f"  tags:  {entry['tags']}")
    print(f"  file:  {BLOG_DIR / entry['file']}")
    print(f"  json:  {POSTS_JSON}")


if __name__ == "__main__":
    main()

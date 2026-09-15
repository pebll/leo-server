from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path

import frontmatter
import markdown
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

root_dir = Path(__file__).parent.parent
static_content_path = root_dir / "static"
blog_dir = root_dir / "blog"
blog_posts_json = blog_dir / "posts.json"
blog_posts_dir = blog_dir / "posts"
blog_assets_dir = blog_dir / "assets"
templates_dir = root_dir / "templates"

blog_assets_dir.mkdir(parents=True, exist_ok=True)
blog_posts_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Léo.com")
app.mount("/static", StaticFiles(directory=static_content_path), name="static")
app.mount("/blog/assets", StaticFiles(directory=blog_assets_dir), name="blog_assets")
templates = Jinja2Templates(directory=str(templates_dir))


def format_eu_date(value: object) -> str:
    """Format YYYY-MM-DD (or ISO datetime) as dd/mm/yyyy."""
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    try:
        return date.fromisoformat(text[:10]).strftime("%d/%m/%Y")
    except ValueError:
        return text


templates.env.filters["eu_date"] = format_eu_date

MD_EXTENSIONS = [
    "fenced_code",
    "tables",
    "nl2br",
    "sane_lists",
    "smarty",
]


def strip_redundant_title(body: str, title: str) -> str:
    """Drop a leading # heading that repeats the post title (common in Joplin exports)."""
    if not title or not body:
        return body
    pattern = rf"(?is)^\s*#\s+{re.escape(title.strip())}\s*(?:\n+|$)"
    return re.sub(pattern, "", body, count=1)


def load_posts() -> list[dict]:
    if not blog_posts_json.exists():
        return []
    try:
        data = json.loads(blog_posts_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    posts = sorted(data, key=lambda p: p.get("date", ""), reverse=True)
    week_ago = date.today() - timedelta(days=7)
    annotated: list[dict] = []
    for raw in posts:
        post = dict(raw)
        try:
            post_date = date.fromisoformat(str(post.get("date", ""))[:10])
            post["is_new"] = post_date >= week_ago
        except ValueError:
            post["is_new"] = False
        annotated.append(post)
    return annotated


def get_post_entry(slug: str) -> dict | None:
    for post in load_posts():
        if post.get("slug") == slug:
            return post
    return None


@app.get("/", response_class=HTMLResponse, summary="Serve the homepage.")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"posts": load_posts()[:12]},
    )


@app.get("/blog", response_class=HTMLResponse, summary="Blog index.")
def blog_index(request: Request):
    return templates.TemplateResponse(
        request,
        "blog_index.html",
        {"posts": load_posts()},
    )


@app.get("/blog/{slug}", response_class=HTMLResponse, summary="Render a blog post.")
def blog_post(request: Request, slug: str):
    entry = get_post_entry(slug)
    if entry is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if entry.get("url"):
        return RedirectResponse(url=entry["url"], status_code=302)

    rel_file = entry.get("file")
    if not rel_file:
        raise HTTPException(status_code=404, detail="Post has no content file")

    md_path = blog_dir / rel_file
    if not md_path.is_file():
        raise HTTPException(status_code=404, detail="Post markdown missing")

    post = frontmatter.load(md_path)
    title = str(post.get("title") or entry.get("title") or slug)
    post_date = str(post.get("date") or entry.get("date") or "")
    tags = post.get("tags") or entry.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    body = strip_redundant_title(post.content, title)
    html = markdown.markdown(body, extensions=MD_EXTENSIONS)
    return templates.TemplateResponse(
        request,
        "blog_post.html",
        {
            "title": title,
            "date": post_date,
            "tags": tags,
            "content": html,
        },
    )


@app.get("/hello", summary="A proof of concept API endpoint for debugging.")
def hello():
    return {"message": "Hello from FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)

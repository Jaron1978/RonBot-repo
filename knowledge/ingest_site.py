#!/usr/bin/env python3
"""RonBot website-only knowledge ingester.

Crawls only ron-jackson.co.uk / www.ron-jackson.co.uk pages, extracts readable
page content, chunks it, and writes JSONL suitable for later retrieval/RAG work.
External links are never fetched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_START_URL = "https://www.ron-jackson.co.uk/"
ALLOWED_HOSTS = {"ron-jackson.co.uk", "www.ron-jackson.co.uk"}
HTML_CONTENT_TYPES = {"text/html", "application/xhtml+xml"}
SKIP_SUFFIXES = {
    ".css", ".js", ".json", ".xml", ".txt", ".pdf", ".png", ".jpg",
    ".jpeg", ".gif", ".webp", ".svg", ".ico", ".woff", ".woff2", ".ttf",
    ".eot", ".zip", ".gz", ".mp4", ".webm", ".mp3", ".wav",
}


@dataclass(frozen=True)
class Page:
    url: str
    title: str
    text: str


def normalise_url(url: str) -> str | None:
    """Return a canonical same-site HTTP(S) URL, otherwise None."""
    url, _fragment = urldefrag(url.strip())
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        return None

    host = (parsed.hostname or "").lower().rstrip(".")
    if host not in ALLOWED_HOSTS:
        return None

    path_lower = parsed.path.lower()
    if any(path_lower.endswith(suffix) for suffix in SKIP_SUFFIXES):
        return None

    # Canonicalise onto the public www hostname and HTTPS.
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]

    query = parsed.query
    canonical = f"https://www.ron-jackson.co.uk{path}"
    if query:
        canonical += f"?{query}"
    return canonical


def is_same_site_link(base_url: str, href: str) -> str | None:
    """Resolve href against base_url and keep it only if it stays on-site."""
    if not href:
        return None
    absolute = urljoin(base_url, href)
    return normalise_url(absolute)


def clean_text(text: str) -> str:
    text = re.sub(r"[\t\r\f\v]+", " ", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def extract_page(url: str, html: str) -> tuple[Page, set[str]]:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "template", "svg"]):
        tag.decompose()

    # Forms are interaction UI, not knowledge. Labels/placeholders/user fields are
    # intentionally excluded to prevent them becoming answerable "facts".
    for tag in soup.find_all("form"):
        tag.decompose()

    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else url

    main = soup.find("main") or soup.body or soup

    # Navigation and footer contain repeated boilerplate. Their destinations are
    # still discovered from the full DOM below, but their text is not indexed.
    for tag in main.find_all(["nav", "footer"]):
        tag.decompose()

    text = clean_text(main.get_text("\n", strip=True))

    links: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        candidate = is_same_site_link(url, anchor.get("href", ""))
        if candidate:
            links.add(candidate)

    return Page(url=url, title=title, text=text), links


def chunk_text(text: str, max_chars: int = 1400, overlap_chars: int = 180) -> list[str]:
    """Chunk text on paragraph/sentence boundaries with a small overlap."""
    if len(text) <= max_chars:
        return [text] if text else []

    units = [u.strip() for u in re.split(r"\n+|(?<=[.!?])\s+", text) if u.strip()]
    chunks: list[str] = []
    current = ""

    for unit in units:
        candidate = unit if not current else f"{current}\n{unit}"
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
            overlap = current[-overlap_chars:].lstrip()
            current = f"{overlap}\n{unit}" if overlap else unit
        else:
            chunks.append(unit[:max_chars])
            current = unit[max_chars - overlap_chars :]

    if current:
        chunks.append(current)

    return [clean_text(chunk) for chunk in chunks if clean_text(chunk)]


def crawl(start_url: str, max_pages: int, delay: float, timeout: float) -> list[Page]:
    start = normalise_url(start_url)
    if not start:
        raise ValueError("Start URL must be on ron-jackson.co.uk")

    session = requests.Session()
    session.headers.update({
        "User-Agent": "RonBotKnowledgeBuilder/1.0 (+https://www.ron-jackson.co.uk/)"
    })

    queue: deque[str] = deque([start])
    queued = {start}
    visited: set[str] = set()
    pages: list[Page] = []

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        response = session.get(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status()

        final_url = normalise_url(response.url)
        if not final_url:
            # A redirect that leaves the site is never followed into the index.
            continue

        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type and content_type not in HTML_CONTENT_TYPES:
            continue

        page, links = extract_page(final_url, response.text)
        if page.text:
            pages.append(page)

        for link in sorted(links):
            if link not in visited and link not in queued:
                queue.append(link)
                queued.add(link)

        if delay > 0:
            time.sleep(delay)

    return pages


def write_jsonl(pages: Iterable[Page], output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8") as handle:
        for page in pages:
            for index, chunk in enumerate(chunk_text(page.text), start=1):
                digest = hashlib.sha256(f"{page.url}|{index}|{chunk}".encode("utf-8")).hexdigest()[:16]
                record = {
                    "id": digest,
                    "source_url": page.url,
                    "title": page.title,
                    "chunk_index": index,
                    "text": chunk,
                    "scope": "ron-jackson.co.uk-only",
                }
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RonBot's website-only knowledge dataset")
    parser.add_argument("--start-url", default=DEFAULT_START_URL)
    parser.add_argument("--output", default="knowledge/website.jsonl")
    parser.add_argument("--max-pages", type=int, default=100)
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    pages = crawl(args.start_url, args.max_pages, args.delay, args.timeout)
    output = Path(args.output)
    chunks = write_jsonl(pages, output)

    print(f"Indexed {len(pages)} page(s) into {chunks} chunk(s): {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

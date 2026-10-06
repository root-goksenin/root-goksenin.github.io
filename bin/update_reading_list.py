"""Fill in title, authors and year for the reading list from the arXiv API.

Runs in the "Deploy site" workflow before the site is built. It normalizes each entry in
_data/reading_list.yml (arXiv link or ID -> plain ID, status -> "to-read" or "read") and looks
up the papers whose title, authors or year are missing. The file is only changed in the build's
working copy, so _data/reading_list.yml in the repository stays short and easy to edit.

Papers that are not on arXiv are kept as they are when they have a title (and usually a url).

If arXiv cannot be reached, the script prints a warning and leaves the entries as they are;
the page then shows the title you wrote (or the arXiv ID) without authors.
"""

import pathlib
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "_data" / "reading_list.yml"
ATOM = "{http://www.w3.org/2005/Atom}"
API = "https://export.arxiv.org/api/query?id_list={ids}&max_results={n}"

NEW_ID = re.compile(r"(\d{4}\.\d{4,5})(?:v\d+)?")
OLD_ID = re.compile(r"([a-z][a-z\-]*(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?", re.IGNORECASE)

READ = {"read", "done", "finished"}


def normalize_id(raw):
    """Turn an arXiv link, ID or a number YAML parsed from an ID into a plain ID like 2501.14459."""
    if raw is None:
        return None
    if isinstance(raw, float):
        # YAML reads an unquoted 2509.23230 as a number and drops the trailing zero.
        raw = f"{raw:.5f}" if raw >= 1501 else f"{raw:.4f}"
    text = str(raw).strip()
    match = NEW_ID.search(text) or OLD_ID.search(text)
    return match.group(1) if match else None


def normalize_status(raw):
    text = str(raw or "").strip().lower()
    if text in READ:
        return "read"
    return "to-read"


def clean(papers):
    """Normalize the entries and drop the ones the page cannot show."""
    cleaned = []
    for paper in papers or []:
        if not isinstance(paper, dict):
            continue
        paper_id = normalize_id(paper.get("arxiv"))
        if not paper_id and "arxiv.org/" in str(paper.get("url") or ""):
            paper_id = normalize_id(paper.pop("url"))  # an arXiv link pasted as url: counts as arxiv:
        if paper_id:
            paper["arxiv"] = paper_id
        elif paper.get("title"):
            paper.pop("arxiv", None)  # not on arXiv: shown with its own url or pdf link, if any
        else:
            print(f"Skipping an entry with neither an arXiv link nor a title: {paper}")
            continue
        paper["status"] = normalize_status(paper.get("status"))
        cleaned.append(paper)
    return cleaned


def fetch(ids):
    """Return {id: {title, authors, year}} for the given arXiv IDs."""
    found = {}
    for start in range(0, len(ids), 50):
        chunk = ids[start : start + 50]
        url = API.format(ids=",".join(chunk), n=len(chunk))
        request = urllib.request.Request(url, headers={"User-Agent": "personal-website-reading-list/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            root = ET.fromstring(response.read())
        for entry in root.findall(f"{ATOM}entry"):
            key = normalize_id(entry.findtext(f"{ATOM}id"))
            title = entry.findtext(f"{ATOM}title")
            if not key or not title:
                continue
            published = entry.findtext(f"{ATOM}published") or ""
            found[key] = {
                "title": " ".join(title.split()),
                "authors": [" ".join(a.findtext(f"{ATOM}name", "").split()) for a in entry.findall(f"{ATOM}author")],
                "year": int(published[:4]) if published[:4].isdigit() else None,
            }
        if start + 50 < len(ids):
            time.sleep(3)  # arXiv asks for at most one request every 3 seconds
    return found


def fill_from_arxiv(cleaned):
    missing = sorted({p["arxiv"] for p in cleaned if p.get("arxiv") and not (p.get("title") and p.get("authors") and p.get("year"))})
    if not missing:
        return
    try:
        details = fetch(missing)
    except Exception as error:  # network problems must not break the site build
        print(f"Warning: could not reach arXiv ({error}); papers without a title will show as arXiv IDs.")
        details = {}
    for paper in cleaned:
        info = details.get(paper.get("arxiv"))
        if not info:
            continue
        for field in ("title", "authors", "year"):
            if not paper.get(field) and info.get(field):
                paper[field] = info[field]
    print(f"Looked up {len(missing)} paper(s) on arXiv, found {len(details)}.")


def fill_years(cleaned):
    """A new-style arXiv ID starts with the year and month: 2509.23238 is from 2025."""
    for paper in cleaned:
        paper_id = paper.get("arxiv") or ""
        if not paper.get("year") and NEW_ID.fullmatch(paper_id):
            paper["year"] = 2000 + int(paper_id[:2])


def main():
    if not DATA.exists():
        print("No _data/reading_list.yml, nothing to do.")
        return
    data = yaml.safe_load(DATA.read_text(encoding="utf-8")) or {}
    cleaned = clean(data.get("papers"))
    fill_from_arxiv(cleaned)
    fill_years(cleaned)

    data["papers"] = cleaned
    DATA.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Reading list: {sum(p['status'] == 'read' for p in cleaned)} read, "
          f"{sum(p['status'] == 'to-read' for p in cleaned)} to read.")


if __name__ == "__main__":
    sys.exit(main())

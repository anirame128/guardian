import requests
from bs4 import BeautifulSoup, Comment
from typing import Any, Dict
from .tools import internal_database_query, docs_create, docs_export, http_post

def browser_fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def browser_extract_all_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    texts = []
    for element in soup.find_all(text=True):
        if isinstance(element, Comment):
            texts.append(str(element))
        else:
            texts.append(element.strip())
    return "\n".join([t for t in texts if t])

TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "db.search": {
        "desc": "Search internal databases by a free-text topic and return matching records.",
        "args": {"topic": "string"},
        "fn": lambda args: internal_database_query(args.get("topic", "")),
    },
    "docs.create": {
        "desc": "Create a user-facing text document.",
        "args": {"text": "string", "filename": "string"},
        "fn": lambda args: docs_create(args.get("text", ""), args.get("filename", "analysis.md")),
    },
    "docs.export": {
        "desc": "Export a document by filename (no network).",
        "args": {"file": "string"},
        "fn": lambda args: docs_export(args.get("file", "analysis.md")),
    },
    "http.post": {
        "desc": "HTTP POST JSON to a URL.",
        "args": {"url": "string", "json": "object"},
        "fn": lambda args: http_post(args.get("url", ""), args.get("json", {})),
    },
}

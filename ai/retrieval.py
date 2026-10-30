import json
import pathlib
import re

from rank_bm25 import BM25Okapi

INDEX = pathlib.Path("data/index/pages.json")

_pages = json.loads(INDEX.read_text()) if INDEX.exists() else []


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.casefold())


_bm25 = BM25Okapi([_tokens(p["text"]) for p in _pages]) if _pages else None


def retrieve(question: str, k: int = 4) -> list[dict]:
    """Top-k pages for the question, in the shape ask_gemma expects."""
    if not _bm25:
        return []
    scores = _bm25.get_scores(_tokens(question))
    ranked = sorted(range(len(_pages)), key=lambda i: scores[i], reverse=True)
    return [_pages[i] for i in ranked[:k] if scores[i] > 0]


def library() -> dict:
    """Size of the indexed corpus, for the UI."""
    return {"documents": len({p["document"] for p in _pages}), "pages": len(_pages)}

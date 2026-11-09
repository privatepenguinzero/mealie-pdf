"""PDF support for Mealie's "create recipe with AI" import.

Each uploaded PDF is replaced by one image per page, and its text layer (if
any) is appended to the text content sent to the model. Images alone lose
details in tables (quantities, columns); the text alone loses layout. Both
together give the best result.
"""

import os
from pathlib import Path

import pymupdf

MAX_PAGES = int(os.environ.get("MEALIE_PDF_MAX_PAGES", "10"))
DPI = int(os.environ.get("MEALIE_PDF_DPI", "150"))
MAX_TEXT = 40_000


def is_pdf(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return f.read(5) == b"%PDF-"
    except OSError:
        return False


def _convert(path: Path) -> tuple[list[Path], str]:
    pages: list[Path] = []
    texts: list[str] = []
    with pymupdf.open(path) as doc:
        for i, page in enumerate(doc):
            if i >= MAX_PAGES:
                break
            out = path.with_name(f"{path.stem}-page{i + 1}.png")
            page.get_pixmap(dpi=DPI).save(out)
            pages.append(out)
            text = page.get_text("text", sort=True).strip()
            if text:
                texts.append(text)
    return pages, "\n\n".join(texts)[:MAX_TEXT]


def expand(images: list[Path], content: str | None) -> tuple[list[Path], str | None, Path | None]:
    """Returns (images, content, cover).

    cover is the first uploaded picture that was not a PDF: a rendered PDF page
    makes a poor recipe cover, so recipes imported only from PDFs get none.
    """
    result: list[Path] = []
    extra: list[str] = []
    cover: Path | None = None

    for path in images:
        if not is_pdf(path):
            result.append(path)
            cover = cover or path
            continue

        pages, text = _convert(path)
        result.extend(pages)
        if text:
            extra.append(f"Text extracted from {path.name}:\n\n{text}")

    if extra:
        content = "\n\n".join(([content] if content else []) + extra)

    return result, content, cover

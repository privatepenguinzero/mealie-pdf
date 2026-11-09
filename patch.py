"""Applies the PDF changes to an installed Mealie.

Every replacement must match exactly once. If upstream changes the code
around it, the build fails here instead of shipping a half-patched image.
"""

import sys
from pathlib import Path

import mealie

ROOT = Path(mealie.__file__).parent

BACKEND = [
    (
        "services/recipe/ai_recipe_service.py",
        "import shutil\n",
        "import shutil\n\nimport mealie_pdf\n",
    ),
    (
        "services/recipe/ai_recipe_service.py",
        "            local_images = self._store_images(images or [], temp_path)\n",
        "            local_images = self._store_images(images or [], temp_path)\n"
        "            local_images, content, cover = mealie_pdf.expand(local_images, content)\n",
    ),
    (
        "services/recipe/ai_recipe_service.py",
        '            if local_images:\n                with open(local_images[0], "rb") as f:\n',
        '            if cover:\n                with open(cover, "rb") as f:\n',
    ),
]

# The upload button of the AI import page. Chunk names change with every
# release, so the frontend is searched by content.
FRONTEND_OLD = '"file-name":`images`,accept:`image/*`'
FRONTEND_NEW = '"file-name":`images`,accept:`image/*,application/pdf`'


def fail(msg: str) -> None:
    print(f"patch failed: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    for rel, old, new in BACKEND:
        path = ROOT / rel
        src = path.read_text()
        if src.count(old) != 1:
            fail(f"{rel}: expected 1 match, found {src.count(old)}:\n{old}")
        path.write_text(src.replace(old, new))
        print(f"patched {rel}")

    hits = []
    for path in (ROOT / "frontend").rglob("*.js"):
        src = path.read_text(errors="ignore")
        n = src.count(FRONTEND_OLD)
        if n:
            hits.append((path, src, n))
    if len(hits) != 1 or hits[0][2] != 1:
        fail(f"frontend: expected 1 match, found {[(str(p), n) for p, _, n in hits]}")
    path, src, _ = hits[0]
    path.write_text(src.replace(FRONTEND_OLD, FRONTEND_NEW))
    print(f"patched {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

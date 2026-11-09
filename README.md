# mealie-pdf

The official [Mealie](https://github.com/mealie-recipes/mealie) image with one
addition: the "create recipe with AI" import also accepts PDF files.

Each PDF page is rendered to an image, and the PDF text layer (when there is
one) is sent along with the images. The text keeps quantities from tables
that the model tends to drop when it only sees the page; the images keep the
layout. Scanned PDFs work too, through the images only.

A PDF page is never used as the recipe cover. If you upload a photo together
with the PDF, the photo becomes the cover.

The image also ships [Deno](https://deno.com), which yt-dlp needs to extract
YouTube videos for the video recipe import.

## Image

```
ghcr.io/privatepenguinzero/mealie-pdf:latest
ghcr.io/privatepenguinzero/mealie-pdf:<mealie version>   # e.g. v3.30.0
```

Drop-in replacement for `ghcr.io/mealie-recipes/mealie`. Same volumes and
environment. Optional:

| Variable | Default | |
|---|---|---|
| `MEALIE_PDF_MAX_PAGES` | `10` | pages read from each PDF |
| `MEALIE_PDF_DPI` | `150` | render resolution |

## How it's built

`patch.py` makes three small edits to `ai_recipe_service.py` and widens the
file filter of the AI import upload button. Each edit has to match exactly
once, so when upstream changes that code the build fails instead of
producing a broken image. The previous tag stays available.

A daily workflow checks for new Mealie releases and builds them.

## License

AGPL-3.0, same as Mealie.

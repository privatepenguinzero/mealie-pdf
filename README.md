# mealie-pdf

[Mealie](https://github.com/mealie-recipes/mealie) built from the latest
release with one addition: the "create recipe with AI" import also accepts
documents (PDF, Word `.docx`, OpenDocument `.odt`, Markdown, plain text, RTF
and HTML).

The feature comes from
[mealie-recipes/mealie#8536](https://github.com/mealie-recipes/mealie/pull/8536)
by bferd. This repository only applies that pull request on top of each
Mealie release until it is merged upstream.

The image also ships [Deno](https://deno.com) and `yt-dlp-ejs`, which yt-dlp
needs to extract YouTube videos for the video recipe import.

## Image

```
ghcr.io/privatepenguinzero/mealie-pdf:latest
ghcr.io/privatepenguinzero/mealie-pdf:<mealie version>          # e.g. v3.31.0
ghcr.io/privatepenguinzero/mealie-pdf:<mealie version>-pr<sha>  # exact PR commit
```

Drop-in replacement for `ghcr.io/mealie-recipes/mealie`. Same volumes and
environment.

## How it's built

`prepare.sh` checks out the Mealie release, applies the pull request diff
(without `pyproject.toml` and `uv.lock`, which change in every release), adds
the four new dependencies again with `uv`, and appends the video import
extras to Mealie's own `docker/Dockerfile`. The image is then built from that
tree with the upstream Dockerfile.

If the diff no longer applies, the build fails and the previous tag stays
available. If a release already contains the feature, nothing is applied:
at that point the official image is enough.

A daily workflow builds new Mealie releases and new commits of the pull
request.

## License

AGPL-3.0, same as Mealie.

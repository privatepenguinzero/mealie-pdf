#!/usr/bin/env bash
# Prepares a Mealie source tree with the document import from
# mealie-recipes/mealie#8536 applied on top of a release.
#
#   ./prepare.sh <mealie tag> <output dir>
#
# The pull request is applied as a diff against its own merge base, without
# pyproject.toml and uv.lock: those two files change in every release, so the
# four new dependencies are added again with uv instead.
# If the release already contains the feature (the pull request was merged),
# the tree is left as it is.
set -euo pipefail

TAG=${1:?mealie tag}
OUT=${2:?output dir}
PR_REPO=https://github.com/bferd/mealie
PR_BRANCH=feat/recipe-import-from-document
DEPS=(pypdf==6.19.0 python-docx==1.2.0 odfpy==1.4.1 striprtf==0.0.33)

git clone --quiet --filter=blob:none https://github.com/mealie-recipes/mealie "$OUT"
cd "$OUT"
git checkout --quiet "$TAG"

if [ -f mealie/services/recipe/document_text_extraction.py ]; then
  echo "Mealie $TAG already has the document import, nothing to apply"
  exit 0
fi

git fetch --quiet "$PR_REPO" "$PR_BRANCH:pr"
base=$(git merge-base "$TAG" pr)
echo "PR head $(git rev-parse --short pr), merge base $(git rev-parse --short "$base")"

git diff --binary "$base" pr -- . ':!pyproject.toml' ':!uv.lock' > /tmp/pr.patch
git apply --3way /tmp/pr.patch
uv add --no-sync "${DEPS[@]}"

# Extras for the video import: yt-dlp needs a JavaScript runtime and the
# challenge solver scripts for YouTube.
cat >> docker/Dockerfile <<'EOF'

COPY --from=docker.io/denoland/deno:bin /deno /usr/local/bin/deno
RUN "$VENV_PATH/bin/pip" install --no-cache-dir yt-dlp-ejs \
 && deno --version
EOF

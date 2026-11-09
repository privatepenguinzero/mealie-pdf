ARG MEALIE_VERSION=latest
FROM ghcr.io/mealie-recipes/mealie:${MEALIE_VERSION}

COPY mealie_pdf.py patch.py /tmp/mealie-pdf/

RUN /opt/mealie/bin/pip install --no-cache-dir "pymupdf>=1.26,<2" \
 && SITE=$(/opt/mealie/bin/python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])') \
 && cp /tmp/mealie-pdf/mealie_pdf.py "$SITE/" \
 && /opt/mealie/bin/python /tmp/mealie-pdf/patch.py \
 && /opt/mealie/bin/python -c 'import mealie_pdf, mealie.services.recipe.ai_recipe_service' \
 && rm -rf /tmp/mealie-pdf

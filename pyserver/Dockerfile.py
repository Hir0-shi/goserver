FROM alpine:latest

RUN apk add --no-cache python3

RUN adduser -D -h /srv pyserver

# Set WORKDIR before COPY so we can use relative paths (.) below.
# This also ensures the script runs from /srv so "books/frankenstein.txt" resolves correctly.
WORKDIR /srv

COPY --chown=pyserver:pyserver main.py .
COPY --chown=pyserver:pyserver books books

USER pyserver

CMD ["python3", "main.py"]

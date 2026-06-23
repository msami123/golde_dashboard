#!/usr/bin/env bash
# Run from project root — not from landing/
cd "$(dirname "$0")"
exec gunicorn wsgi:app --bind 127.0.0.1:8000 "$@"

#!/usr/bin/env bash
# Run the Flask app from project root (wsgi.py lives one level up)
cd "$(dirname "$0")/.."
exec gunicorn wsgi:app --bind 127.0.0.1:8000 "$@"

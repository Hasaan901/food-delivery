#!/bin/bash
# Vercel build script — runs on every deployment

pip install --break-system-packages -r requirements.txt

python manage.py collectstatic --noinput

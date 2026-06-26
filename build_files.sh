#!/bin/bash
# Vercel build script — runs on every deployment

pip install -r requirements.txt

python manage.py collectstatic --noinput

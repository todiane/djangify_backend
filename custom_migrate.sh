#!/bin/bash

# Create migration for django_summernote
python manage.py migrate django_summernote zero
python manage.py makemigrations django_summernote
python manage.py migrate django_summernote

# Create missing __init__.py files
mkdir -p apps/*/migrations
touch apps/*/migrations/__init__.py

#!/bin/sh
# Rebuild the site and publish the ./site folder to the gh-pages branch.
set -e
cd "$(dirname "$0")"
python3 build.py
git add -A
git commit -qm "Update site" || true
git push origin main
git push origin "$(git subtree split --prefix site main)":refs/heads/gh-pages --force

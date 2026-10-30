#!/usr/bin/env python3
"""Checks built pages for skipped heading levels, missing alt text and duplicate link text."""
import glob
from collections import Counter
from html.parser import HTMLParser


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.heads, self.noalt, self.links, self._a, self._t = [], 0, [], 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "img" and not (a.get("alt") or "").strip():
            self.noalt += 1
        if tag == "a" and a.get("href", "").startswith("/"):
            self._a, self._t = 1, []

    def handle_endtag(self, tag):
        if tag == "a" and self._a:
            self.links.append(" ".join("".join(self._t).split()))
            self._a = 0

    def handle_data(self, d):
        if self._a:
            self._t.append(d)


for f in sorted(glob.glob("site/**/index.html", recursive=True)):
    html = open(f).read()
    if "http-equiv=\"refresh\"" in html:
        continue
    p = P()
    p.feed(html)
    skips = [f"h{a}→h{b}" for a, b in zip(p.heads, p.heads[1:]) if b > a + 1]
    dup = [t for t, n in Counter(p.links).items() if n > 1 and t]
    print(f"{f[5:]:<45} skips={sorted(set(skips))} noalt={p.noalt} dup_links={dup[:8]}")

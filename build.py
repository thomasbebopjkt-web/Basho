#!/usr/bin/env python3
"""Builds the Basho Projects static site into ./site.

Every page shares one header, footer, contact block and newsletter popup, defined below.
Edit the content here, run `python3 build.py` (or `./deploy.sh` to publish).
"""
import hashlib
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent / "site"
DOMAIN = "https://www.bashoprojects.com"
GA_ID = "G-FTQ6R39EZS"  # Google Analytics 4 property for bashoprojects.com
# Fingerprint of the CSS/JS so browsers fetch fresh copies after every deploy
ASSET_V = hashlib.md5(b"".join((ROOT / "assets" / p).read_bytes() for p in
                              ["css/site.css", "css/group.css", "css/venue.css", "js/site.js"])).hexdigest()[:8]

# ---------------------------------------------------------------- shared data


# Hours: weekday (0 = Sunday) -> list of [open, close] in 24h Jakarta time; 26 = 02:00 next day.
EVERY_DAY = lambda spans: {d: spans for d in range(7)}

VENUES = {
    "bebop": {
        "name": "BEBOP Bar + Kitchen",
        "short": "BEBOP",
        "path": "/bebop/",
        "tag": "Jazz & cocktail bar · Senopati",
        "blurb": "Listening bar, cocktails and live jazz, Senopati. Owned and operated.",
        "card_img": "bebop-bar.jpg",
        "card_pos": "center 72%",
        "address": "Jl. Senopati No. 61, Kebayoran Baru, South Jakarta",
        "street": "Jl. Senopati No. 61", "locality": "Kebayoran Baru, South Jakarta",
        "hours_text": "Every day, 17:00 till late",
        "hours": EVERY_DAY([[17, 26]]),
        "late": True,
        "book": "https://wa.me/628132229293",
        "menu": "https://drive.google.com/file/d/1fVueKjI0878L3gZe2G2E3yK-eqkakVwX/view",
        "maps": "https://share.google/71emNbci6KrwuVk7n",
        "instagram": "https://www.instagram.com/bebop.wav/",
        "ig_handle": "@bebop.wav",
        "schema_type": "BarOrPub",
        "cuisine": "Modern Japanese",
    },
    "briq-bistro": {
        "name": "BRIQ Bistro",
        "short": "BRIQ",
        "path": "/briq-bistro/",
        "tag": "French bistro · Senopati",
        "blurb": "French bistro, Senopati. Home of the steak frites. Owned and operated.",
        "card_img": "briq-hero.jpg",
        "address": "Jl. Prof. Joko Sutono SH No. 7B, Kebayoran Baru, South Jakarta",
        "street": "Jl. Prof. Joko Sutono SH No. 7B", "locality": "Kebayoran Baru, South Jakarta",
        "hours_text": "Mon–Fri dinner 17:00–22:00 · Sat–Sun all day 10:00–22:00",
        "hours": {0: [[10, 22]], 1: [[17, 22]], 2: [[17, 22]], 3: [[17, 22]], 4: [[17, 22]], 5: [[17, 22]], 6: [[10, 22]]},
        "book": "https://wa.me/6285286147342",
        "menu": "https://drive.google.com/file/d/14s5RP07lYSFB83LDFETMX9C2kJ7qXe4m/view",
        "maps": "https://maps.app.goo.gl/oVa2PtMUAXVPxSpC8",
        "instagram": "https://www.instagram.com/briqbistro/",
        "ig_handle": "@briqbistro",
        "tiktok": "https://www.tiktok.com/@briqbistro",
        "schema_type": "Restaurant",
        "cuisine": "French",
    },
    "brock-butchery": {
        "name": "Brock Butchery",
        "short": "Brock",
        "path": "/brock-butchery/",
        "tag": "Premium butcher · Delivered",
        "blurb": "Premium meat, delivered across Jakarta. Owned and operated.",
        "card_img": "brock-logo.png",
        "logo": True,
        "tokopedia": "https://www.tokopedia.com/brock-butchery",
        "shopee": "https://shopee.co.id/brockbutchery",
        "tiktok": "https://www.tiktok.com/@brock.butchery",
        "instagram": "https://www.instagram.com/brockbutchery/",
        "ig_handle": "@brockbutchery",
        "schema_type": "Store",
    },
    "the-bluebell": {
        "name": "The Bluebell Public House",
        "short": "The Bluebell",
        "path": "/the-bluebell/",
        "tag": "British public house · Senopati",
        "blurb": "Modern British public house, Senopati. Owned and operated.",
        "card_img": "bluebell-bar.jpg",
        "address": "Jl. Tulodong Atas No. 10 A-B, Senopati, South Jakarta 12190",
        "street": "Jl. Tulodong Atas No. 10 A-B", "locality": "Senopati, South Jakarta",
        "postcode": "12190",
        "hours_text": "Mon–Thu 10:00–01:00 · Fri–Sun 10:00–02:00",
        "hours": {0: [[10, 26]], 1: [[10, 25]], 2: [[10, 25]], 3: [[10, 25]], 4: [[10, 25]], 5: [[10, 26]], 6: [[10, 26]]},
        "phone": "0821-4401-216", "tel": "+628214401216",
        "book": "https://wa.me/628214401216",
        "maps": "https://share.google/se4JQBoWzcS53Zwa8",
        "instagram": "https://www.instagram.com/atthebluebell/",
        "ig_handle": "@atthebluebell",
        "schema_type": "BarOrPub",
        "cuisine": "British",
    },
}
# The three WhatsApp lines, shown together in the footer and on /contact/
WA_LINES = [(VENUES["the-bluebell"]["book"], "The Bluebell", "+62 821 4401 216"),
            (VENUES["briq-bistro"]["book"], "BRIQ Bistro", "+62 852 8614 7342"),
            (VENUES["bebop"]["book"], "BEBOP", "+62 813 2229 293")]
VENUE_ORDER = ["bebop", "briq-bistro", "brock-butchery", "the-bluebell"]
NAV = [(VENUES[k]["name"], VENUES[k]["path"]) for k in VENUE_ORDER] + [("Bubble + Squeak Media", "/bubbleandsqueakmedia/")]

ICONS = {
    "arrow": '<span class="hub__arrow" aria-hidden="true">→</span>',
}


def header():
    drop = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Basho Projects home"><img src="{logo_src()}" alt="Basho Projects" width="160" height="46"></a>
    <button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
      <div class="nav-drop">
        <button aria-expanded="false">Venues</button>
        <ul><li><a href="/our-projects/">All venues</a></li>{drop}</ul>
      </div>
      <a href="/services/">Services</a>
      <a href="/invest/">Invest</a>
      <a href="/about/">About</a>
      <a href="/team/">Team</a>
      <a href="/blog/">Journal</a>
      <a class="btn" href="/contact/">Contact</a>
    </nav>
  </div>
</header>"""


ENQUIRY_TYPES = ["Work with us (services)", "Invest or partner on a project", "Table booking or private event",
                 "Bubble + Squeak Media", "Press or collaboration", "Something else"]


def contact_form(default=None):
    opts = "".join(f'<option{" selected" if t == default else ""}>{t}</option>' for t in ENQUIRY_TYPES)
    return f"""<form class="form" data-contact novalidate>
  <div><label for="kind">I’m getting in touch about</label><select id="kind" name="enquiry_type">{opts}</select></div>
  <div class="row">
    <div><label for="fn">First name <span>(required)</span></label><input id="fn" name="first_name" required autocomplete="given-name"></div>
    <div><label for="ln">Last name <span>(required)</span></label><input id="ln" name="last_name" required autocomplete="family-name"></div>
  </div>
  <div><label for="em">Email <span>(required)</span></label><input id="em" name="email" type="email" required autocomplete="email"></div>
  <label class="check"><input type="checkbox" name="newsletter" value="yes"> Sign up for news and updates</label>
  <div><label for="msg">Message <span>(required)</span></label><textarea id="msg" name="message" required></textarea></div>
  <div><button class="btn btn--light" type="submit">Submit</button></div>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>"""


def collaborate(default=None):
    return f"""<section class="section dark" id="collaborate">
  <div class="wrap split">
    <div class="reveal">
      <h2>Let’s <span class="serif">collaborate.</span></h2>
      <p>Whether you’re launching your first concept, reimagining an existing space, or looking for hands-on support across branding, operations, or experience design — we’d love to hear what you’re building.</p>
      <p>We tailor each collaboration to fit the needs of the project and the people behind it.</p>
      <p><strong>Let’s talk — coffee, cocktails, or call.</strong></p>
      <p class="muted">PT Basho Projects Capital<br>Senopati, South Jakarta</p>
    </div>
    <div class="reveal">{contact_form(default)}</div>
  </div>
</section>"""


def newsletter_popup():
    return """<aside class="nl" role="dialog" aria-labelledby="nl-title" aria-modal="false">
  <button class="nl__close" aria-label="Close">×</button>
  <div class="nl__ticker"><span>Jazz line-ups</span><span>New openings</span><span>First dibs</span></div>
  <h2 id="nl-title">Join the <span class="serif">guest list.</span></h2>
  <p>What’s on at BEBOP, BRIQ and The Bluebell, straight to your inbox. Twice a month, max. No spam, ever.</p>
  <form data-newsletter><label class="skip" for="nl-email">Email</label><input id="nl-email" type="email" name="email" placeholder="you@email.com" required autocomplete="email"><button class="btn" type="submit">I’m in</button></form>
  <p class="nl__note" role="status" aria-live="polite"></p>
</aside>"""


def footer():
    wa = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}<br>{num}</a></li>' for u, n, num in WA_LINES)
    venues = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="/"><img src="{logo_src()}" alt="Basho Projects" width="140" height="40" loading="lazy"></a>
        <p class="muted">Hospitality incubator, operator and consultancy.<br>Senopati, South Jakarta.</p>
        <form class="nl-inline" data-newsletter style="margin-top:18px"><label class="skip" for="ft-email">Email</label><input id="ft-email" type="email" name="email" placeholder="Join the guest list" required><button class="btn btn--light" type="submit">Join</button></form>
        <p class="nl__note muted" role="status" aria-live="polite" style="font-size:13px;margin-top:8px"></p>
      </div>
      <div><p class="foot-h">Projects</p><ul>{venues}</ul></div>
      <div><p class="foot-h">Company</p><ul><li><a href="/services/">Services</a></li><li><a href="/about/">About us</a></li><li><a href="/team/">Team</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div><p class="foot-h">Follow</p><ul><li><a href="{VENUES['bebop']['instagram']}" target="_blank" rel="noopener">BEBOP on Instagram</a></li><li><a href="{VENUES['briq-bistro']['instagram']}" target="_blank" rel="noopener">BRIQ on Instagram</a></li><li><a href="{VENUES['the-bluebell']['instagram']}" target="_blank" rel="noopener">The Bluebell on Instagram</a></li><li><a href="{VENUES['brock-butchery']['instagram']}" target="_blank" rel="noopener">Brock on Instagram</a></li>{wa}</ul></div>
    </div>
    <div class="legal"><span>© <span data-year>2026</span> PT Basho Projects Capital</span><span>Made in Senopati, Jakarta</span></div>
  </div>
</footer>"""


# Search titles (≤58 chars) and descriptions (≤125 chars), sized to Google's and Seobility's limits
SEO_META = {
    "/": ("Basho Projects | Jakarta Hospitality Group, Senopati",
          "Jakarta hospitality group behind BEBOP, BRIQ, The Bluebell & Brock in Senopati. Book a table, work with us or invest."),
    "/bebop/": ("BEBOP Bar + Kitchen | Jazz & Cocktail Bar, Senopati",
                "Jazz & cocktail bar on Jl. Senopati 61. Live jazz Mon & Fri, DJs, highballs, Japanese plates. Open 17:00 till late."),
    "/briq-bistro/": ("BRIQ Bistro | Steak Frites & French Restaurant, Senopati",
                      "French bistro in Senopati, home of the steak frites. Pasta promos, wine, terrace. Dinner nightly, all day weekends."),
    "/brock-butchery/": ("Brock Butchery | Premium Meat Delivered in Jakarta",
                         "Premium meat delivered across Jakarta. Order on Tokopedia or Shopee with no minimum, or set up trade supply."),
    "/the-bluebell/": ("The Bluebell Public House | British Pub, Senopati",
                       "British pub in Senopati: pints, G&Ts, pitchers and cocktails, fish & chips, pies and Guinness. Open daily from 10:00."),
    "/the-bluebell/food/": ("British Food in Senopati | The Bluebell Public House",
                            "Modern British food near SCBD: Sunday roast, fish & chips and pies. Open daily from 10:00 for lunch and dinner."),
    "/the-bluebell/private-rooms/": ("Private Dining & Meeting Rooms in Senopati - The Bluebell",
                                     "Two private rooms in Senopati, a short walk from SCBD: a dining and meeting room for 12 and a Chess Room for 6. No minimum spend."),
    "/the-bluebell/football/": ("Watch Premier League Football in Senopati - The Bluebell",
                                "Watch live Premier League football at The Bluebell in Senopati, a short walk from SCBD, with British food at your table. Book on WhatsApp."),
    "/briq-bistro/food/": ("French Food in Senopati | Steak Frites at BRIQ Bistro",
                           "French bistro food in Senopati: steak frites with Brock beef, steak for two 495K++, weekend pasta 200K++."),
    "/bebop/live-music/": ("Live Music in Senopati | Jazz Mon & Fri at BEBOP",
                           "Live jazz every Monday and Friday, Trivia Tuesdays and resident DJs at BEBOP, Jl. Senopati 61. Modern Japanese plates."),
    "/bebop/kitchen/": ("Modern Japanese Food in Senopati | BEBOP Kitchen",
                        "Modern Japanese plates at BEBOP, Jl. Senopati 61: karaage, takoyaki, smash burgers and more. Open daily from 17:00."),
    "/bebop/trivia/": ("Trivia Tuesdays in Senopati | BEBOP",
                       "Trivia Tuesdays at BEBOP, Jl. Senopati 61, hosted by Kara Chenoa. Every Tuesday from 20:00. Book a team table on WhatsApp."),
    "/bebop/private-hire/": ("Private Events & Parties in Senopati | BEBOP",
                             "Private hire at BEBOP in Senopati: birthdays, launches and takeovers with live music or resident DJs and Japanese plates."),
    "/blog/": ("Journal | Stories from Senopati | Basho Projects",
               "Stories from Basho Projects in Senopati, Jakarta: openings, live jazz at BEBOP, The Bluebell and more."),
    "/blog/the-bluebell-public-house-opens-in-south-jakarta/": ("The Bluebell Public House Opens in Senopati, Jakarta",
               "Raise a pint, British-style: The Bluebell Public House is open in Senopati, South Jakarta."),
    "/blog/jazz-at-bebop/": ("Jazz at BEBOP: Live Jazz in Senopati, Mon & Fri",
                             "Live jazz every Monday and Friday at BEBOP Bar + Kitchen, Senopati, curated by Bass G."),
    "/about/": ("About Basho Projects | Independent Jakarta F&B Group",
                "Operators first. The independent Jakarta group behind BEBOP, BRIQ Bistro, The Bluebell and Brock Butchery."),
    "/services/": ("Restaurant & Bar Consultants Jakarta | Basho Projects",
                   "Restaurant & bar consultants in Jakarta: concept, brand, menu, operations, launch and marketing, from working operators."),
    "/invest/": ("Invest in Jakarta Restaurants & Bars | Basho Projects",
                 "Invest in new bar and restaurant concepts in Senopati, Jakarta, built and run by the team behind BEBOP and BRIQ."),
    "/contact/": ("Contact Basho Projects | Jakarta Hospitality Group",
                  "Contact Basho Projects, Senopati: table bookings, private events, F&B consulting, investment and press."),
    "/our-projects/": ("Bars & Restaurants in Senopati | Basho Projects",
                       "BEBOP, BRIQ Bistro, The Bluebell Public House and Brock Butchery: bars and restaurants in Senopati, South Jakarta."),
    "/bubbleandsqueakmedia/": ("Bubble + Squeak Media | F&B Marketing Agency Jakarta",
                               "Jakarta performance marketing & PR agency for F&B: Meta, Google & TikTok ads, KOLs and content. From USD 950/month."),
}


def page(path, title, description, main, image="/assets/img/briq-hero.jpg", with_collab=True,
         body_class="g", schema=None, enquiry=None, venue=None):
    url = DOMAIN + path
    # Pages under a venue, and that venue's blog posts, send form fallbacks to its WhatsApp number
    venue = venue or next((k for k in ("bebop", "briq-bistro", "the-bluebell") if path.startswith(VENUES[k]["path"])), None)
    wa_attr = f' data-wa="{VENUES[venue]["book"].rsplit("/", 1)[1]}"' if venue else ""
    title, description = SEO_META.get(path, (title, description))
    if len(title) > 58 or len(description) > 125:
        print(f"  SEO length warning {path}: title {len(title)}/58, description {len(description)}/125")
    ld = ""
    for s in (schema or []):
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Basho Projects">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}{image}">
<meta property="og:locale" content="en_ID">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="/assets/favicon.ico?v={ASSET_V}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png?v={ASSET_V}">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v={ASSET_V}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Instrument+Serif:ital@0;1&family=Space+Mono&family=Manrope:wght@400;500;600;700;800&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<link rel="stylesheet" href="/assets/css/group.css?v={ASSET_V}">
<link rel="stylesheet" href="/assets/css/venue.css?v={ASSET_V}">
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{ld}</head>
<body class="{body_class}"{wa_attr}>
{header()}
<main id="main">
{main}
{collaborate(enquiry) if with_collab else ""}
</main>
{footer()}
{newsletter_popup()}
</body>
</html>
"""
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


def redirect(old, new):
    out = ROOT / old.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>
<link rel="canonical" href="{DOMAIN}{new}"><meta http-equiv="refresh" content="0; url={new}"><meta name="robots" content="noindex">
</head><body><a href="{new}">Continue</a></body></html>""")


def marquee(text):
    item = f"<span>{text}</span>" * 4
    return f'<div class="marquee" aria-hidden="true"><div class="marquee__track">{item}{item}</div></div>'


IMG_DIR = ROOT / "assets" / "img"
OPT_DIR = IMG_DIR / "opt"
WIDTHS = (480, 960, 1600)
_img_meta = {}


def _optimise(src):
    """Make WebP copies of an image at a few widths (cached on disk). Returns (variants, w, h)."""
    if src in _img_meta:
        return _img_meta[src]
    from PIL import Image
    path = IMG_DIR / src
    OPT_DIR.mkdir(exist_ok=True)
    stem = Path(src).stem
    with Image.open(path) as im:
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
        w, h = im.size
        variants = []
        for tw in WIDTHS:
            if tw > w and variants:
                break
            tw = min(tw, w)
            out = OPT_DIR / f"{stem}-{tw}.webp"
            if not out.exists() or out.stat().st_mtime < path.stat().st_mtime:
                im.resize((tw, round(h * tw / w)), Image.LANCZOS).save(out, "WEBP", quality=74, method=5)
            variants.append((f"/assets/img/opt/{out.name}", tw))
    _img_meta[src] = (variants, w, h)
    return _img_meta[src]


def alt_from_name(src):
    words = Path(src).stem.replace("-", " ").replace("_", " ")
    for a, b in (("bebop", "BEBOP"), ("briq", "BRIQ"), ("bluebell", "The Bluebell"), ("brock", "Brock"),
                 ("svc", "Service"), ("adv", "Advertising"), ("bs icon", "Bubble + Squeak icon")):
        words = words.replace(a, b)
    return words[:1].upper() + words[1:]


def img(src, alt, cls="", lazy=True, sizes="(max-width: 760px) 100vw, 50vw"):
    alt = alt or alt_from_name(src)
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    variants, w, h = _optimise(src)
    srcset = ", ".join(f"{u} {tw}w" for u, tw in variants)
    fallback = variants[min(1, len(variants) - 1)][0]
    return (f'<img src="{fallback}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{escape(alt)}"{c}{load}>')


def logo_src():
    return _optimise("basho-logo.png")[0][0][0]


TEAM = [
    {"key": "shawn", "name": "Shawn Andrew", "role": "Chief Executive Officer", "initials": "SA",
     "linkedin": "https://www.linkedin.com/in/shawn-andrew-621117306/",
     "bio": "Shawn leads Basho Projects — in his words, “a small grass-roots F&B group” — and sets the direction across BEBOP, BRIQ, The Bluebell and Brock, and the partner projects we take on."},
    {"key": "dony", "name": "Dony Renato S. Naibaho", "role": "Chief Financial Officer", "initials": "DN",
     "linkedin": "https://www.linkedin.com/in/dony-renato-s-naibaho-b5b324192/",
     "bio": "Dony drives the group’s financial and legal strategy: the numbers, structures and agreements behind every venue and every new project."},
    {"key": "sam", "name": "Samuel Joesoep", "role": "Founder, Brock Butchery · Operations Manager, Basho Projects", "initials": "SJ",
     "linkedin": "https://www.linkedin.com/in/samueljoesoep/",
     "bio": "Sam founded Brock Butchery and runs operations across Basho Projects, with a focus on strategy, business development and growth."},
]


def team_photo(key):
    for ext in ("jpg", "jpeg", "png", "webp"):
        if (IMG_DIR / f"team-{key}.{ext}").exists():
            return f"team-{key}.{ext}"
    return None


LINKEDIN_ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4v11H3v-11zm6.5 0h3.8v1.5h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.65 4.77 6.1v5.45h-4v-4.83c0-1.15-.02-2.63-1.6-2.63-1.6 0-1.85 1.25-1.85 2.55v4.91h-4v-11z"/></svg>'


def team_cards(heading="h3"):
    out = []
    for i, p in enumerate(TEAM, 1):
        photo = team_photo(p["key"])
        face = img(photo, p["name"], sizes="(max-width: 760px) 70vw, 30vw") if photo else f'<span class="mono" aria-hidden="true">{p["initials"]}</span>'
        out.append(f"""<article class="person reveal">
  <div class="person__face{' has-photo' if photo else ''}">{face}<span class="person__no">0{i}</span></div>
  <div class="person__body">
    <span class="person__role">{p['role']}</span>
    <{heading}>{p['name']}</{heading}>
    <p>{p['bio']}</p>
    <a class="pill" href="{p['linkedin']}" target="_blank" rel="noopener">{LINKEDIN_ICON} LinkedIn<span class="skip"> — {p['name']}</span></a>
  </div>
</article>""")
    return f'<div class="people">{"".join(out)}</div>'


team_ld = [{"@context": "https://schema.org", "@type": "Person", "name": p["name"], "jobTitle": p["role"],
            "sameAs": [p["linkedin"]], "worksFor": {"@type": "Organization", "name": "Basho Projects", "url": DOMAIN}} for p in TEAM]



# ---------------------------------------------------------------- schema helpers

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Basho Projects",
    "legalName": "PT Basho Projects Capital",
    "url": DOMAIN,
    "logo": f"{DOMAIN}/assets/img/basho-logo.png",
    "description": "Hospitality incubator, operator and consultancy in Jakarta. Owner operators behind BEBOP Bar + Kitchen, BRIQ Bistro, Brock Butchery and The Bluebell Public House.",
    "address": {"@type": "PostalAddress", "addressLocality": "South Jakarta", "addressCountry": "ID"},
    "sameAs": [v["instagram"] for v in VENUES.values() if v.get("instagram")],
}

DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def venue_schema(v, image):
    s = {
        "@context": "https://schema.org",
        "@type": v["schema_type"],
        "name": v["name"],
        "url": DOMAIN + v["path"],
        "image": f"{DOMAIN}/assets/img/{image}",
        "parentOrganization": {"@type": "Organization", "name": "Basho Projects", "url": DOMAIN},
        "sameAs": [u for u in (v.get("instagram"), v.get("tiktok"), v.get("tokopedia"), v.get("shopee")) if u],
    }
    if v.get("street"):
        s["address"] = {"@type": "PostalAddress", "streetAddress": v["street"], "addressLocality": v["locality"],
                        "addressRegion": "DKI Jakarta", "addressCountry": "ID"}
        if v.get("postcode"):
            s["address"]["postalCode"] = v["postcode"]
    if v.get("hours"):
        spec = []
        for d, spans in v["hours"].items():
            for o, c in spans:
                spec.append({"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_NAMES[d],
                             "opens": f"{o:02d}:00", "closes": f"{c % 24:02d}:00"})
        s["openingHoursSpecification"] = spec
    if v.get("cuisine"):
        s["servesCuisine"] = v["cuisine"]
    if v.get("menu"):
        s["hasMenu"] = v["menu"]
    if v.get("tel"):
        s["telephone"] = v["tel"]
    if v.get("book"):
        s["acceptsReservations"] = True
    return s


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs) + "</div>"


TODAY = datetime.now(ZoneInfo("Asia/Jakarta")).date()


def weekly_events(v, name, description, weekdays, image, weeks=8):
    """Event markup for a weekly night: one Event per date over the next few weeks (weekdays: 0 = Monday).
    Dates are worked out at build time, so redeploy at least every few weeks to keep them in the future."""
    out = []
    for i in range(weeks * 7):
        day = TODAY + timedelta(days=i)
        if day.weekday() not in weekdays:
            continue
        out.append({
            "@context": "https://schema.org", "@type": "Event", "name": f"{name} at {v['name']}",
            "description": description, "startDate": f"{day.isoformat()}T20:00:00+07:00",
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {"@type": "Place", "name": v["name"], "address": {
                "@type": "PostalAddress", "streetAddress": v["street"], "addressLocality": v["locality"],
                "addressRegion": "DKI Jakarta", "addressCountry": "ID"}},
            "image": [f"{DOMAIN}/assets/img/{image}"],
            "organizer": {"@type": "Organization", "name": v["name"], "url": DOMAIN + v["path"]},
        })
    return out


def bebop_events():
    v = VENUES["bebop"]
    return (weekly_events(v, "Jazz Night", "Live jazz curated by Bass G, from standards to funk and groove.", {0, 4}, "jazz-2.jpg")
            + weekly_events(v, "Trivia Tuesday", "Pub-style trivia hosted by Kara Chenoa. Teams, rounds and bragging rights.", {1}, "jazz-2.jpg"))


def bahasa(eyebrow, h2, paras):
    """A short Indonesian-language section, for the searches people make in Bahasa."""
    body = "".join(f"<p>{t}</p>" for t in paras)
    return f"""<section class="section" lang="id" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2></div>
    <div class="reveal">{body}</div>
  </div>
</section>"""


# ---------------------------------------------------------------- venues


VENUE_EXTRAS = {
    "bebop": {"values": ["Curated", "Social", "Modern", "Soulful", "Jazz", "Cocktails", "Japanese plates"],
              "quote": "Never plays the same note <em>twice.</em>", "by": "BEBOP Bar + Kitchen",
              "more": [("jazz-2.jpg", "A full room on jazz night"), ("bebop-detail.jpg", "Cocktails at the bar"), ("bebop-hero.jpg", "The BEBOP crowd")]},
    "briq-bistro": {"values": ["Organic", "Human", "Eclectic", "Raw", "Fine-casual", "Bon appétit"],
                    "quote": "We don’t chase trends. We build <em>lasting tables.</em>", "by": "BRIQ Bistro",
                    "more": [("briq-detail.jpg", "A plate at BRIQ"), ("briq-case-study.webp", "BRIQ Bistro, Jakarta Selatan"), ("briq-room.jpg", "The BRIQ dining room")]},
    "brock-butchery": {"values": ["Honest", "Elevated", "Accessible", "Straightforward", "Grounded"],
                       "quote": "Great meat shouldn’t be <em>a luxury.</em>", "by": "Brock Butchery",
                       "more": [("brock-hero.jpg", "Steak on the grill"), ("brock-cuts.jpg", "Premium cuts from Brock"), ("briq-detail.jpg", "Brock beef at BRIQ Bistro")]},
    "the-bluebell": {"values": ["Pints", "G&Ts", "Pitchers", "Cocktails", "Fish & chips", "Pies", "Guinness", "Cheers"],
                     "quote": "A proper pint, a warm room and <em>nowhere to be.</em>", "by": "The Bluebell Public House",
                     "more": [("bluebell-hall.jpg", "The dining hall at The Bluebell"), ("bluebell-bar-2.jpg", "Behind the bar"), ("bluebell-facade.jpg", "The Bluebell at night")]},
}
VENUE_KEY_BY_SHORT = {v["short"]: k for k, v in VENUES.items()}


PROMOS = json.loads((Path(__file__).parent / "promos.json").read_text())


def promos_html(key):
    """'Now on' promo cards from promos.json. Expired ones (past 'until') are hidden by site.js too."""
    items = PROMOS.get(key, [])
    if not items:
        return ""
    cards = []
    for p in items:
        ext = ' target="_blank" rel="noopener"' if p.get("url", "").startswith("http") else ""
        until = f' data-until="{p["until"]}"' if p.get("until") else ""
        pic = img(p["image"], p["title"]) if p.get("image") else ""
        cards.append(f"""<article class="promo{' promo--feat' if p.get('feature') else ''} reveal"{until}>
  <div class="promo__ph">{pic}</div>
  <div class="promo__body"><span class="promo__k">{p.get('kicker', '')}</span><h3>{p['title']}</h3><p>{p.get('text', '')}</p>
  {f'<a class="btn" href="{p["url"]}"{ext}>{p["cta"]}</a>' if p.get('cta') else ''}</div>
</article>""")
    return f"""<section class="vx-now" id="now-on"><div class="wrap">
  <h2 class="skip">What’s on now</h2>
  <div class="vx-now__head"><span class="eyebrow">Now on</span><span class="vx-now__live">Live this week</span></div>
  <div class="promos">{''.join(cards)}</div>
</div></section>"""


def hub(v, title, meta, deco, links, foot):
    """The venue link hub. Closes the .vx-top wrapper opened by vhero(), then adds the values strip."""
    ext = ' target="_blank" rel="noopener"'
    rows = "".join(
        f'<li><a href="{u}"{ext if u.startswith("http") else ""}>'
        f'<span class="hub__no">{n}</span><span><strong>{t}</strong><small>{s}</small></span>{ICONS["arrow"]}</a></li>'
        for n, t, s, u in links)
    words = VENUE_EXTRAS[VENUE_KEY_BY_SHORT[v["short"]]]["values"]
    strip = " ✦ ".join(words) + " ✦ "
    return f"""<div class="wrap hub-wrap reveal">
  <nav class="hub" aria-label="{v['short']} quick links">
    <div class="hub__head">{deco}<span class="hub__title">{title}</span><span class="hub__meta">{meta}</span></div>
    <ol>{rows}</ol>
    <div class="hub__foot">{foot}</div>
  </nav>
</div>
</div>
<div class="vx-strip">{marquee(strip)}</div>
{promos_html(VENUE_KEY_BY_SHORT[v["short"]])}"""


def vhero(v, image, alt, h1, sub):
    """Opens .vx-top; hub() closes it so the hub can float over the hero on wide screens."""
    hours = ""
    if v.get("hours"):
        late = ' data-late="1"' if v.get("late") else ""
        hours = f'<span class="status" data-hours=\'{json.dumps(v["hours"])}\'{late}>{v["hours_text"]}</span>'
    return f"""<div class="vx-top">
<section class="vhero">
  {img(image, alt, lazy=False, sizes="100vw")}
  <div class="wrap">
    <div class="vx-meta">{hours}<span class="eyebrow">A Basho Projects venue · Senopati</span></div>
    <h1 class="vx-name">{h1}</h1>
    <p class="sub">{sub}</p>
  </div>
</section>"""


def gallery(v, images):
    ex = VENUE_EXTRAS[VENUE_KEY_BY_SHORT[v["short"]]]
    pics = (list(images) + ex["more"])[:6]
    tiles = "".join(f'<figure class="reveal">{img(src, alt, sizes="(max-width: 760px) 50vw, 33vw")}<figcaption>{alt}</figcaption></figure>' for src, alt in pics)
    if v.get("instagram"):
        sticker = f'<a class="sticker" href="{v["instagram"]}" target="_blank" rel="noopener"><span>Follow along</span><b>{v["ig_handle"]}</b></a>'
    else:
        sticker = f'<a class="sticker" href="{v.get("tiktok", "#")}" target="_blank" rel="noopener"><span>Follow along</span><b>@brock.butchery</b></a>'
    return f"""<div class="vx-quote reveal"><span class="eyebrow">In our words</span><blockquote>{ex["quote"]}</blockquote><cite>— {ex["by"]}</cite></div>
<div class="collage">{tiles}{sticker}</div>"""


def sisters(current):
    links = "".join(
        f'<a href="{VENUES[k]["path"]}"><small>{VENUES[k]["tag"]}</small><strong>{VENUES[k]["name"]} →</strong></a>'
        for k in VENUE_ORDER if k != current)
    return f'<section><div class="sister">{links}</div></section>'


def facts(v):
    rows = []
    if v.get("address"):
        rows.append(("Address", f'<a href="{v["maps"]}" target="_blank" rel="noopener">{v["address"]}</a>'))
    if v.get("hours_text"):
        rows.append(("Hours", v["hours_text"]))
    if v.get("phone"):
        rows.append(("WhatsApp", f'<a href="{v["book"]}" target="_blank" rel="noopener">Message us to book</a>'))
    if v.get("instagram"):
        rows.append(("Instagram", f'<a href="{v["instagram"]}" target="_blank" rel="noopener">{v["ig_handle"]}</a>'))
    return '<ul class="facts">' + "".join(f"<li><span>{k}</span><span>{val}</span></li>" for k, val in rows) + "</ul>"


# BEBOP ---------------------------------------------------------------

v = VENUES["bebop"]
bebop_faq = [
    ("Where is BEBOP Bar + Kitchen?", "BEBOP is at Jl. Senopati No. 61, Kebayoran Baru, South Jakarta — a few minutes’ walk from BRIQ Bistro and The Bluebell, and close to SCBD."),
    ("Is there live music at BEBOP?", "Yes. Live jazz runs every Monday and Friday, curated by resident musician Bass G. Other nights bring resident DJs from the Bebop Music Collective, karaoke and trivia. Check Instagram for this week’s line-up."),
    ("What time does BEBOP open?", "Every day from 17:00 until late, with happy hour from 17:00 to 20:00. Live music and events start from about 20:00."),
    ("Do I need to book a table?", "Booking is the safest bet, especially for jazz nights and weekends. Message us on WhatsApp and we’ll hold a table."),
    ("Is there food, or just drinks?", "Both. The bar leads with cocktails, Mega Highballs and teapot cocktails, and the kitchen serves modern Japanese plates built for sharing."),
    ("Can I book BEBOP for a private event?", "Yes. We host birthdays, launches, company nights and takeovers, with weekday and weekend free-flow packages for groups of 50 and up and minimum-spend options for smaller groups. Message us on WhatsApp for the 2026 packages."),
    ("Who are the DJs at BEBOP?", "The Bebop Music Collective: 14 resident DJs who formed at BEBOP, playing house, future beats, jazz, soul, UK garage, disco and more."),
]
venue_page = f"""
{vhero(v, "bebop-hero.jpg", "The bar at BEBOP Bar + Kitchen, Senopati, at night",
       'BEBOP Bar <span class="serif">+ Kitchen</span>',
       "A jazz and cocktail bar in Senopati, Jakarta. An intimate listening bar where sound, cocktails and atmosphere work together as one experience.")}
{hub(v, "Tracklist", "Side A · 6 tracks", '<span class="vinyl" aria-hidden="true"></span>', [
    ("A1", "Book a table", "WhatsApp us, we’ll hold it", v["book"]),
    ("A2", "Food + drinks menu", "Cocktails, highballs, Japanese plates", v["menu"]),
    ("A3", "What’s on tonight", "Live jazz every Monday & Friday", "#whats-on"),
    ("B1", "Find us", "Jl. Senopati No. 61", v["maps"]),
    ("B2", "Instagram", v["ig_handle"], v["instagram"]),
    ("B3", "Events & private hire", "Birthdays, launches, takeovers", v["book"]),
], f'<span>{v["hours_text"]}</span><span>Senopati · South Jakarta</span>')}

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">The concept</span>
      <h2>Social. Modern. Soulful. <span class="serif">BEBOP.</span></h2>
      <p>BEBOP is designed as a place to slow down. Music is treated as a central element rather than background noise, with vinyl selections and curated playlists setting the rhythm of the room throughout the night.</p>
      <p>The cocktail programme is built on balance and clarity, favouring timeless recipes executed with intention. Drinks are designed to complement the space rather than dominate it, supporting long conversations and repeat visits.</p>
      <p>Inspired by Japanese listening bars and classic cocktail culture, BEBOP focuses on restraint, detail and mood rather than volume or trend-driven theatrics.</p>
    </div>
    <div class="media media--tall reveal">{img("bebop-detail.jpg", "Cocktails on the bar at BEBOP, Senopati")}</div>
  </div>
</section>

<section class="section" id="whats-on" style="border-top:1px solid var(--vline)">
  <div class="wrap">
    <span class="eyebrow">What’s on</span>
    <h2>Live music <span class="serif">in Senopati</span>, most nights of the week</h2>
    <p class="muted" style="max-width:60ch">Looking for a jazz bar in Jakarta, or a bar di Senopati with a proper sound system? This is the weekly rotation. Line-ups change, so check <a href="{v['instagram']}" target="_blank" rel="noopener">{v['ig_handle']}</a> before you head over.</p>
    <div class="lineup">
      <div><em>Mon & Fri · from 20:00</em><b>Jazz Nights</b><span>Live jazz curated by Bass G, from standards to funk and groove.</span></div>
      <div><em>Tuesdays · from 20:00</em><b>Trivia Tuesdays</b><span>Teams, rounds, bragging rights.</span></div>
      <div><em>Weekly · from 20:00</em><b>Karaoke Nights</b><span>The mic is yours. Be brave.</span></div>
      <div><em>Weekly · from 20:00</em><b>BMC Nights</b><span>The Bebop Music Collective on the decks: house, future beats, jazz and soul.</span></div>
      <div><em>Special nights · see Instagram</em><b>Booty Groove</b><span>Late, loud and very much a dance floor.</span></div>
    </div>
    <div class="btn-row" style="margin-top:28px"><a class="btn" href="/bebop/live-music/">Live music at BEBOP</a><a class="btn btn--ghost" href="/blog/jazz-at-bebop/">Read: Jazz at BEBOP</a></div>
    <div class="btn-row" style="margin-top:12px"><a class="btn btn--ghost" href="/bebop/kitchen/">The kitchen</a><a class="btn btn--ghost" href="/bebop/trivia/">Trivia & karaoke</a><a class="btn btn--ghost" href="/bebop/private-hire/">Private hire</a></div>
  </div>
</section>

<section class="section" id="menu" style="border-top:1px solid var(--vline)">
  <div class="wrap">
    <span class="eyebrow">The menu</span>
    <h2>A bar first. <span class="serif">Cocktails lead the way.</span></h2>
    <p class="muted" style="max-width:60ch">Whether you’re in for a quick drink, a full night out or something in between, the drinks come first and the kitchen keeps pace with modern Japanese plates.</p>
    <div class="lineup">
      <div><em>Cocktails</em><b>Classics with a twist</b><span>With a kick, and a few that shouldn’t work — but do.</span></div>
      <div><em>Mega Highballs</em><b>Made for after work</b><span>Proper Japanese whisky, good soda, zero pretension.</span></div>
      <div><em>Teapot cocktails</em><b>Strong. Shareable.</b><span>Simply good value. They pack a punch and pour like a dream.</span></div>
      <div><em>B-Strongs</em><b>House hard seltzer</b><span>BEBOP-style, made in-house and served by the can.</span></div>
      <div><em>Plates to match</em><b>Modern Japanese kitchen</b><span>Bold snacks, smoky plates and comforting bites built to keep pace with your drink.</span></div>
    </div>
    <p style="margin-top:28px"><a class="btn" href="{v['menu']}" target="_blank" rel="noopener">See the full menu</a></p>
  </div>
</section>

<section class="section" id="bmc" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Bebop Music Collective</span>
      <h2>Local sounds. <span class="serif">Worldwide presence.</span></h2>
      <p>In January 2022 a group of DJs found a home at BEBOP, and launched the Bebop Music Collective the following year. Fourteen residents strong, BMC covers house, future beats, jazz and soul, and plenty in between. Think of it as the bridge to Jakarta’s underground, with a cocktail in hand.</p>
      <p class="muted">BEBOP never plays the same note twice.</p>
    </div>
    <div class="reveal">
      <ul class="facts">
        <li><span>Monty Hasan</span><span>Jazzy, soulful, Latin, Brazilian, house</span></li>
        <li><span>Greybox</span><span>Jazz, electronic</span></li>
        <li><span>NAJ</span><span>Bass, house, UK garage, future beats, breaks</span></li>
        <li><span>Decemberkid</span><span>Future beats, bass, UK garage, house</span></li>
        <li><span>Erik Soto</span><span>Afrobeats, UK garage</span></li>
        <li><span>Reemo</span><span>Jazz, breakbeats, funk & soul</span></li>
        <li><span>Laskar</span><span>Disco, house, Brazilian house</span></li>
        <li><span>Kara</span><span>Soulful</span></li>
        <li><span>LL</span><span>Jazzy house, UK garage, future beats, Afrobeats</span></li>
        <li><span>Kenny Gabriel</span><span>Deep house, disco</span></li>
        <li><span>Faktta</span><span>UK garage, house, future beats</span></li>
        <li><span>Erin Sab.</span><span>Jazz, electronic</span></li>
        <li><span>Bania</span><span>House, breaks, techno</span></li>
        <li><span>Adelia</span><span>UK garage, house, Latin-infused techno</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="private" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="media media--wide reveal">{img("bebop-room.jpg", "Private event at BEBOP Bar + Kitchen")}</div>
    <div class="reveal">
      <span class="eyebrow">Private events & group bookings</span>
      <h2>Your space. Your people. <span class="serif">Your kind of night.</span></h2>
      <p>From intimate gatherings to full-house celebrations, we set the mood with the right mix of music, drinks and atmosphere. Birthdays, launches, company nights and takeovers — it’s throwing a party with BEBOP’s signature.</p>
      <ul class="ticks">
        <li>Free-flow BEBOP signature spirits: tequila, gin or whisky, with mixers</li>
        <li>Sharing platters for every table</li>
        <li>DJ entertainment from the Bebop Music Collective</li>
        <li>Weekday and weekend packages for groups of 50 and up, with smaller bookings on a minimum spend</li>
      </ul>
      <p><a class="btn" href="{v['book']}" target="_blank" rel="noopener">Ask for the 2026 packages</a></p>
    </div>
  </div>
</section>

<section class="section--tight"><div class="wrap">{gallery(v, [("bebop-bar.jpg", "BEBOP bar and record wall"), ("bebop-room.jpg", "BEBOP dining room"), ("jazz-1.jpg", "Live jazz band at BEBOP")])}</div></section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Plan your visit</span>
      <h2>Find <span class="serif">BEBOP</span></h2>
      {facts(v)}
    </div>
    <div class="reveal"><h2 class="h3">Good to know</h2>{faq_html(bebop_faq)}</div>
  </div>
</section>
{bahasa("Dalam Bahasa Indonesia", 'Bar di Senopati <span class="serif">dengan live music</span>', [
    "BEBOP Bar + Kitchen adalah bar jazz dan koktail di Jl. Senopati No. 61, Kebayoran Baru, Jakarta Selatan. Ada live jazz setiap Senin dan Jumat, Trivia Tuesday setiap Selasa, dan DJ residen dari Bebop Music Collective.",
    "Dapur kami menyajikan hidangan Jepang modern untuk dinikmati bersama. Buka setiap hari mulai pukul 17.00 sampai larut malam. Live music mulai sekitar pukul 20.00.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Reservasi meja lewat WhatsApp</a>',
])}
{sisters("bebop")}
"""
page("/bebop/", "BEBOP Bar + Kitchen | Jazz & Cocktail Bar in Senopati, Jakarta",
     "BEBOP Bar + Kitchen: live jazz every Monday & Friday, DJs, cocktails and a modern Japanese kitchen at Jl. Senopati 61, South Jakarta. Open 17:00 till late. Book, menu & directions.",
     venue_page, image="/assets/img/bebop-hero.jpg", with_collab=False, body_class="venue v-bebop",
     schema=[venue_schema(v, "bebop-hero.jpg"), faq_schema(bebop_faq)] + bebop_events())

# BRIQ ----------------------------------------------------------------

v = VENUES["briq-bistro"]
briq_faq = [
    ("Where is BRIQ Bistro?", "Jl. Prof. Joko Sutono SH No. 7B, Kebayoran Baru, South Jakarta — in the heart of Senopati, a short walk from BEBOP and The Bluebell."),
    ("What are BRIQ’s opening hours?", "Dinner from 17:00 to 22:00, Monday to Friday. At weekends we’re open all day, 10:00 to 22:00, for brunch, lunch and dinner."),
    ("What kind of food does BRIQ serve?", "Soulful French bistro cooking, and we’re best known for our steak frites. The kitchen also runs rotating pasta promos and monthly specials, so check Instagram for what’s on this week."),
    ("Is there outdoor seating?", "Yes, BRIQ has an outdoor terrace as well as the dining room."),
    ("How do I book a table at BRIQ?", "Message us on WhatsApp and we’ll confirm your table."),
]
venue_page = f"""
{vhero(v, "briq-room.jpg", "The dining room at BRIQ Bistro, Senopati",
       'BRIQ <span class="serif">Bistro</span>',
       "A French bistro in Senopati, Jakarta, crafted between fine and casual. The precision of fine dining with the warmth and ease of a neighbourhood bistro.")}
{hub(v, "La Carte", "Senopati · Jakarta", "", [
    ("01", "Réserver", "Book a table on WhatsApp", v["book"]),
    ("02", "La carte", "Food + drinks menu", v["menu"]),
    ("03", "Nous trouver", "Jl. Prof. Joko Sutono SH No. 7B", v["maps"]),
    ("04", "Instagram", v["ig_handle"], v["instagram"]),
    ("05", "TikTok", "@briqbistro", v["tiktok"]),
], f'<span>{v["hours_text"]}</span><span>Bon appétit</span>')}

<section class="section">
  <div class="wrap split">
    <div class="media media--tall reveal">{img("briq-detail.jpg", "A plate at BRIQ Bistro")}</div>
    <div class="reveal">
      <span class="eyebrow">The concept</span>
      <h2>Organic. Human. Eclectic. Raw. <span class="serif">Fine-casual.</span></h2>
      <p>BRIQ is a French restaurant in Senopati with the soul of a neighbourhood bistro, designed around authentic culinary traditions presented with clarity and restraint: quality ingredients, classic techniques, and balanced presentation. The dining experience feels both refined and approachable — casual enough for a relaxed brunch, polished enough for a memorable dinner.</p>
      <p>BRIQ was created for Jakarta’s growing dining audience: diners who appreciate quality behind the plate, a warm room, and genuine hospitality.</p>
      <ul class="ticks">
        <li>Refined yet approachable French cooking in a bistro setting</li>
        <li>Positioned between fine dining and casual dining</li>
        <li>An approachable wine list and an outdoor terrace</li>
        <li>Meat from our own butcher, <a href="/brock-butchery/">Brock</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">The space</span>
      <h2>Casual, but <span class="serif">never careless.</span></h2>
      <p>An intimate, sunlit room by day and a cosy, low-lit bistro by night. Open shelves, textured walls, standing tables that invite you to linger and an outdoor terrace for a quick drink or a cigarette between courses.</p>
      <p>We don’t chase trends. We build lasting tables for good conversations — weeknight dinners, weekend brunches, drinks, or just a place to catch your breath in Senopati.</p>
    </div>
    <div class="reveal">
      <span class="eyebrow">The menu</span>
      <h2>Soulful French food, <span class="serif">generous portions.</span></h2>
      <div class="lineup" style="grid-template-columns:1fr">
        <div><em>Weekends · from 10:00</em><b>All-day Saturdays & Sundays</b><span>Long brunches, lazy lunches and catch-ups that roll into dinner.</span></div>
        <div><em>Dinner · every night from 17:00</em><b>A little slower, a little warmer</b><span>Dinner packages make sharing easy, so you can sit back.</span></div>
        <div><em>Every month</em><b>Specials</b><span>Seasonal plates, creative one-offs and festive menus.</span></div>
        <div><em>The cellar</em><b>Wines that are easy to love</b><span>A thoughtful, approachable list, whether you’re new to wine or a seasoned sipper.</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split split--center">
    <div class="media media--tall reveal">{img("brock-hero.jpg", "Steak for BRIQ's steak frites")}</div>
    <div class="reveal">
      <span class="eyebrow">The signature</span>
      <h2>Home of the <span class="serif">steak frites.</span></h2>
      <p>If you only order one thing at BRIQ, make it this: a properly seared steak, crisp frites and a sauce worth mopping up. It’s the dish we’re known for in Senopati, made with beef from our own butcher, <a href="/brock-butchery/">Brock</a>.</p>
      <p>Alongside it, the kitchen runs rotating pasta promos and monthly specials. Follow <a href="{v['instagram']}" target="_blank" rel="noopener">{v['ig_handle']}</a> for this week’s offer.</p>
      <div class="btn-row"><a class="btn" href="{v['book']}" target="_blank" rel="noopener">Book for steak frites</a><a class="btn btn--ghost" href="/briq-bistro/food/">See the food</a></div>
    </div>
  </div>
</section>

<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split split--center">
    <div class="reveal"><span class="eyebrow">Community</span><h2>Your friendly <span class="serif">neighbourhood bistro.</span></h2></div>
    <div class="reveal"><p>We love the little moments that make a place feel alive: live drawing, flower arranging, suave jazz nights. We’re always open to intimate events, collaborations and gatherings that fit the easy spirit of the bistro.</p>
      <p><a class="btn" href="{v['book']}" target="_blank" rel="noopener">Plan an event at BRIQ</a></p></div>
  </div>
</section>

<section class="section--tight"><div class="wrap">{gallery(v, [("briq-hero.jpg", "BRIQ open kitchen"), ("briq-room.jpg", "BRIQ dining room"), ("briq-case-study.webp", "BRIQ Bistro, Jakarta Selatan")])}</div></section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Plan your visit</span>
      <h2>Dinner nightly, <span class="serif">all day at weekends</span></h2>
      {facts(v)}
    </div>
    <div class="reveal"><h2 class="h3">Good to know</h2>{faq_html(briq_faq)}</div>
  </div>
</section>
{bahasa("Dalam Bahasa Indonesia", 'Restoran Prancis <span class="serif">di Senopati</span>', [
    "BRIQ Bistro adalah restoran Prancis di Senopati, Jakarta Selatan, dengan suasana bistro yang hangat dan santai. Menu andalan kami adalah steak frites, dibuat dengan daging sapi dari butcher kami sendiri, Brock.",
    "Buka untuk makan malam Senin sampai Jumat pukul 17.00–22.00, dan sepanjang hari pada akhir pekan pukul 10.00–22.00.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Reservasi meja lewat WhatsApp</a>',
])}
{sisters("briq-bistro")}
"""
page("/briq-bistro/", "BRIQ Bistro | Steak Frites & French Bistro in Senopati, Jakarta",
     "BRIQ Bistro, Senopati: home of the steak frites, with weekly pasta promos, an approachable wine list and an outdoor terrace. Dinner nightly from 17:00, all day at weekends. Book, menu & directions.",
     venue_page, image="/assets/img/briq-room.jpg", with_collab=False, body_class="venue v-briq",
     schema=[venue_schema(v, "briq-room.jpg"), faq_schema(briq_faq)])

# Brock ---------------------------------------------------------------

v = VENUES["brock-butchery"]
brock_faq = [
    ("How do I order from Brock?", "Order direct on Tokopedia or Shopee and we deliver. No trade account or minimum order needed."),
    ("Do you supply restaurants and hotels?", "Yes. We supply restaurants, hotels and hospitality groups across Jakarta and Indonesia with consistent cuts and spec. Message us on WhatsApp to set up trade supply."),
    ("Who is behind Brock?", "Brock is run by Basho Projects, the team behind BEBOP, BRIQ and The Bluebell. Brock supplies BRIQ Bistro, so if the quality slips, we are the first to know."),
]
venue_page = f"""
{vhero(v, "brock-hero.jpg", "Cuts of beef at Brock Butchery, Jakarta",
       'Brock <span class="serif">Butchery</span>',
       "Crafted cuts, handled with care. Premium meat delivered in Jakarta, whether you are cooking for four or for four hundred.")}
{hub(v, "Today’s cuts", "Jakarta delivery", "", [
    ("No.1", "Order on Tokopedia", "Delivered to your door", v["tokopedia"]),
    ("No.2", "Order on Shopee", "Same cuts, your favourite app", v["shopee"]),
    ("No.3", "Order on Tokopedia", "Restaurants, hotels, groups", v["tokopedia"]),
    ("No.4", "Instagram", "@brockbutchery", v["instagram"]),
    ("No.5", "TikTok", "@brock.butchery", v["tiktok"]),
], '<span>No trade account · No minimum order</span><span>Supplier to BRIQ Bistro</span>')}

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Our promise</span>
      <h2>Honest. Elevated. Accessible. Straightforward. <span class="serif">Grounded.</span></h2>
      <h3 class="h4" style="margin-top:28px">For your kitchen</h3>
      <p>Order direct through Tokopedia or Shopee and have it delivered. Clear labelling, honest descriptions, cuts portioned the way you actually cook them. No trade account, no minimum order, no jargon you need a chef to translate.</p>
      <h3 class="h4">For the professional kitchen</h3>
      <p>Consistent supply and spec, with a team that understands what a missed delivery does to a service. We supply restaurants, hotels and hospitality groups across Jakarta and Indonesia, including our own. Brock supplies BRIQ Bistro — as we are our own customer, if the quality slips we are the first to know.</p>
    </div>
    <div class="media media--tall reveal">{img("brock-cuts.jpg", "Premium steak cuts from Brock Butchery")}</div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Why Brock</span>
      <h2>Great meat shouldn’t be <span class="serif">a luxury.</span></h2>
      <p>Brock Butchery kicked off in 2026 on one idea: premium cuts should be available to every table in Jakarta, from the family kitchen to the professional pass. Quality is our baseline, not our pitch.</p>
      <p>No fuss. No mark-up for the sake of it. Just honest product, done right.</p>
    </div>
    <div class="reveal">
      <span class="eyebrow">What we carry</span>
      <div class="lineup" style="grid-template-columns:1fr">
        <div><em>Beef</em><b>Steaks and everyday cuts</b><span>Sourced for quality, portioned for convenience.</span></div>
        <div><em>Poultry & more</em><b>A curated range</b><span>Priced to keep you coming back.</span></div>
        <div><em>Trade</em><b>For restaurants and hotels</b><span>Consistent spec and reliable delivery for full kitchen service.</span></div>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Good to know</span><h2>Ordering <span class="serif">meat</span> in Jakarta</h2>
      <p class="muted">Brock is developed and operated by Basho Projects. It started as a solution to a problem in our own kitchens and became a business of its own.</p></div>
    <div class="reveal">{faq_html(brock_faq)}</div>
  </div>
</section>
<section class="section--tight"><div class="wrap">{gallery(v, [])}</div></section>
{sisters("brock-butchery")}
"""
page("/brock-butchery/", "Brock Butchery | Premium Meat Delivered in Jakarta",
     "Brock Butchery delivers premium meat across Jakarta. Order on Tokopedia or Shopee, no minimum order, or set up trade supply for your restaurant or hotel.",
     venue_page, image="/assets/img/brock-hero.jpg", with_collab=False, body_class="venue v-brock",
     schema=[venue_schema(v, "brock-hero.jpg"), faq_schema(brock_faq)])

# The Bluebell --------------------------------------------------------

v = VENUES["the-bluebell"]
bluebell_faq = [
    ("Where is The Bluebell Public House?", "Jl. Tulodong Atas No. 10 A-B, Senopati, South Jakarta 12190 — between Senopati and SCBD, a short walk from BEBOP and BRIQ."),
    ("What are The Bluebell’s opening hours?", "Monday to Thursday 10:00–01:00; Friday to Sunday 10:00–02:00."),
    ("What’s to drink and eat?", "Beers and pitchers, gin and tonics and cocktails at the bar, plus Guinness. From the kitchen, the pub classics: fish and chips, proper pies and more."),
    ("Is it a proper British pub?", "A modern one. The Bluebell is a modern British public house: elevated British classics from the kitchen, a bar lounge, a dining hall, the Chess Room (our snug) and a private dining room."),
    ("Is there a pub quiz?", "Yes, every Wednesday. Bring a team, grab a pitcher and message us on WhatsApp to hold a table."),
    ("Do you show live sport?", "Yes. We’re showing the Premier League now on weekends, live on Jakarta time when games fall within our opening hours. UFC, F1, rugby, AFL and more are coming soon or on request: message us on WhatsApp to ask for a game. The timetable is in our Instagram highlights (@atthebluebell)."),
    ("Can I smoke at The Bluebell?", "IQOS, heated tobacco and vapes are welcome inside. Cigarettes are for the outdoor smoking area."),
    ("Can I book a private room?", "Yes. The private dining and meeting room seats twelve and the Chess Room seats six, with no minimum spend. Message us on WhatsApp to book."),
]
venue_page = f"""
{vhero(v, "bluebell-facade.jpg", "The Bluebell Public House on Jl. Tulodong Atas, Senopati, at night",
       'The Bluebell <span class="serif">Public House</span>',
       "A modern British public house in Senopati, South Jakarta. Pints, G&Ts and pitchers, fish & chips and a proper pie.")}
{hub(v, "Your round", "Pints · G&Ts · pitchers", '<span class="beermat" aria-hidden="true">B</span>', [
    ("Round 1", "Book a table", "WhatsApp us, we’ll hold it", v["book"]),
    ("Round 2", "Find the pub", "Jl. Tulodong Atas No. 10 A-B", v["maps"]),
    ("Round 3", "Instagram", v["ig_handle"], v["instagram"]),
    ("Round 4", "Private rooms", "Rooms for 12 and 6", "/the-bluebell/private-rooms/"),
    ("Round 5", "The Sunday roast", "Beef, chicken or nut roast", "/blog/sunday-roast-at-the-bluebell-jakarta/"),
    ("Round 6", "Message the team", "WhatsApp", v["book"]),
], f'<span>{v["hours_text"]}</span><span>Cheers</span>')}

<section class="section">
  <div class="wrap split">
    <div class="media media--tall reveal">{img("bluebell-door.jpg", "The front door of The Bluebell Public House")}</div>
    <div class="reveal">
      <span class="eyebrow">The pub</span>
      <h2>Pints. G&Ts. <span class="serif">Pitchers.</span></h2>
      <p>The Bluebell brings the social soul of the British pub to Senopati: a dimly lit, warm room where post-work drinks stretch into long, relaxed evenings. Beers and pitchers for the table, gin and tonics, cocktails and a proper Guinness at the bar; fish and chips, pies and British pub classics from the kitchen.</p>
      <p>Cosy nooks, a proper bar lounge, a dining hall and a private dining room — approachably premium and easy to enjoy, whether you’re in for a quick bite after work or settling in for a nightcap.</p>
      <div class="btn-row"><a class="btn" href="/the-bluebell/food/">See the food</a><a class="btn btn--ghost" href="/blog/the-bluebell-public-house-opens-in-south-jakarta/">Read the opening story</a></div>
    </div>
  </div>
</section>

<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">The rooms</span>
      <h2>Pick your <span class="serif">corner.</span></h2>
      <ul class="facts">
        <li><span>Bar lounge</span><span>High stools, the long bar and pitchers for the table</span></li>
        <li><span>Dining hall</span><span>Banquettes, pendant lights and the full pub menu</span></li>
        <li><span>The Chess Room</span><span>Our snug and a private room for up to six</span></li>
        <li><span>Private dining room</span><span>Seats twelve, for dinners, meetings and celebrations</span></li>
      </ul>
      <p class="muted" style="margin-top:18px">Room for about 95 seated and 140 standing for a full-pub booking. IQOS, heated tobacco and vape friendly inside; cigarettes in the outdoor smoking area.</p>
      <div class="btn-row"><a class="btn btn--ghost" href="/the-bluebell/private-rooms/">See the private rooms</a><a class="btn btn--ghost" href="/the-bluebell/football/">Watch the football</a></div>
    </div>
    <div class="media media--wide reveal">{img("bluebell-hall-night.jpg", "The dining hall at The Bluebell in the evening")}</div>
  </div>
</section>

<section class="section--tight"><div class="wrap">{gallery(v, [("bluebell-bar.jpg", "The bar at The Bluebell, Senopati"), ("bluebell-lounge.jpg", "The bar lounge at The Bluebell"), ("bluebell-piano.jpg", "The piano at The Bluebell")])}</div></section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Plan your visit</span>
      <h2>A British pub <span class="serif">in Jakarta</span></h2>
      {facts(v)}
    </div>
    <div class="reveal"><h2 class="h3">Good to know</h2>{faq_html(bluebell_faq)}</div>
  </div>
</section>
{bahasa("Dalam Bahasa Indonesia", 'Pub di <span class="serif">Jakarta Selatan</span>', [
    "The Bluebell Public House adalah pub Inggris modern di Senopati, Jakarta Selatan, hanya beberapa menit dari SCBD. Dari dapur ada fish and chips, pie, dan Sunday roast setiap hari Minggu; di bar ada bir, pitcher, gin and tonic, koktail dan Guinness.",
    "Pub Quiz setiap hari Rabu. Buka setiap hari mulai pukul 10.00.",
    "Kami menayangkan Premier League setiap akhir pekan, langsung sesuai waktu Jakarta selama masih dalam jam buka kami. UFC, F1, rugby, AFL, dan olahraga lainnya segera hadir atau bisa diminta lewat WhatsApp. Jadwalnya ada di highlight Instagram kami.",
    "IQOS, produk tembakau yang dipanaskan, dan vape boleh digunakan di dalam. Rokok di area merokok di luar ruangan.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Reservasi meja lewat WhatsApp</a>',
])}
{sisters("the-bluebell")}
"""
page("/the-bluebell/", "The Bluebell Public House | British Pub in Senopati, South Jakarta",
     "The Bluebell Public House is a modern British pub in Senopati, South Jakarta: pints, G&Ts, pitchers, fish & chips and pies.",
     venue_page, image="/assets/img/bluebell-facade.jpg", with_collab=False, body_class="venue v-bluebell",
     schema=[venue_schema(v, "bluebell-facade.jpg"), faq_schema(bluebell_faq)])

# ---------------------------------------------------------------- ad landing pages
# Pages for Google Ads to send people to. Google reviews the landing page as well as the ad, and
# alcohol content (words or images) gets venue ads limited or disapproved in Indonesia. So these
# pages talk about food, music and the room only: no drink wording, and no photos with bottles,
# glasses, taps or back bars. Keep it that way when editing them.


def landing_close(v, cta):
    return f"""<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Plan your visit</span><h2>Book <span class="serif">a table</span></h2>{facts(v)}</div>
    <div class="reveal"><p>Message us on WhatsApp with the day, time and how many of you, and we’ll hold a table.</p>
      <p><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">{cta}</a></p></div>
  </div>
</section>"""


v = VENUES["the-bluebell"]
page("/the-bluebell/food/", "British Food in Senopati | The Bluebell Public House", "", f"""
{vhero(v, "bluebell-hall-night.jpg", "The dining hall at The Bluebell, Senopati, in the evening",
       'British food <span class="serif">in Senopati</span>',
       "Modern British cooking at The Bluebell Public House, a short walk from SCBD: fish and chips, proper pies and a Sunday roast. Open daily from 10:00 for lunch and dinner.")}
</div>
<section class="section">
  <div class="wrap split split--center">
    <div class="media media--tall reveal">{img("roast-beef.jpg", "Sunday roast beef with Yorkshire pudding at The Bluebell")}</div>
    <div class="reveal">
      <span class="eyebrow">Every Sunday</span>
      <h2>The Sunday <span class="serif">roast.</span></h2>
      <p>Roast beef, roast chicken or a nut roast, each with Yorkshire pudding, cauliflower cheese, roast potatoes, roast carrots and cabbage, and a jug of gravy.</p>
      <ul class="ticks">
        <li><strong>Roast Beef</strong> — 275K++</li>
        <li><strong>Roast Chicken</strong> — 200K++</li>
        <li><strong>Nut Roast</strong> — 150K++, our vegetarian roast</li>
      </ul>
      <div class="btn-row"><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Book a Sunday roast</a><a class="btn btn--ghost" href="/blog/sunday-roast-at-the-bluebell-jakarta/">More on the roast</a></div>
    </div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">All week</span>
      <h2>British classics, <span class="serif">done properly.</span></h2>
      <p>Lunch and dinner every day from 10:00. The kitchen cooks the dishes people miss from home: fish and chips with a proper crunch, and pies with a real pastry lid.</p>
      <div class="lineup" style="grid-template-columns:1fr">
        <div><em>The classic</em><b>Fish & chips</b><span>Battered fish, thick-cut chips, the works.</span></div>
        <div><em>Comfort food</em><b>Proper pies</b><span>Slow-cooked fillings under a golden pastry lid.</span></div>
        <div><em>Sundays</em><b>The roast</b><span>Beef, chicken or nut roast with all the trimmings.</span></div>
      </div>
    </div>
    <div class="grid-2 reveal" style="gap:16px;align-content:start">
      <figure style="margin:0">{img("roast-chicken.jpg", "Roast chicken Sunday roast at The Bluebell", sizes="(max-width: 760px) 100vw, 400px")}</figure>
      <figure style="margin:0">{img("nut-roast.jpg", "Vegetarian nut roast at The Bluebell, Jakarta", sizes="(max-width: 760px) 100vw, 400px")}</figure>
    </div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="media media--wide reveal">{img("bluebell-2.jpg", "The dining room at The Bluebell Public House")}</div>
    <div class="reveal">
      <span class="eyebrow">The rooms</span>
      <h2>Lunch, dinner <span class="serif">or a long table.</span></h2>
      <ul class="facts">
        <li><span>Dining hall</span><span>Banquettes, pendant lights and the full menu</span></li>
        <li><span>The Chess Room</span><span>A private room for up to six</span></li>
        <li><span>Private dining room</span><span>Seats twelve, for birthdays, team lunches and meetings</span></li>
      </ul>
      <div class="btn-row"><a class="btn btn--ghost" href="/the-bluebell/private-rooms/">See the private rooms</a></div>
      <p class="muted" style="margin-top:18px">Restoran Inggris di Senopati, Jakarta Selatan. Reservasi meja lewat WhatsApp.</p>
    </div>
  </div>
</section>
{landing_close(v, "Book a table at The Bluebell")}
""", image="/assets/img/roast-beef.jpg", with_collab=False, body_class="venue v-bluebell lp",
     schema=[venue_schema(v, "bluebell-hall-night.jpg")])

# The Bahasa copy on the private rooms page is waiting on a native-speaker check. Set this to
# True once it has been checked, then deploy.
BLUEBELL_ROOMS_BAHASA_CHECKED = False
rooms_bahasa = bahasa("Dalam Bahasa Indonesia", 'Ruang privat <span class="serif">di Senopati</span>', [
    "Dua ruang privat di The Bluebell, hanya beberapa menit berjalan kaki dari SCBD. Cocok untuk makan siang bisnis, makan malam bersama klien, atau meeting tim. Tanpa minimum spend.",
    "<strong>Private Dining &amp; Meeting Room:</strong> Untuk maksimal 12 orang. Ruang privat untuk makan siang, makan malam, dan meeting, dengan hidangan dari dapur The Bluebell.",
    "<strong>Chess Room:</strong> Untuk maksimal 6 orang. Ruang yang lebih kecil untuk meeting santai atau makan bersama secara privat.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Reservasi lewat WhatsApp</a>',
]) if BLUEBELL_ROOMS_BAHASA_CHECKED else ""

page("/the-bluebell/private-rooms/", "Private Dining & Meeting Rooms in Senopati - The Bluebell", "", f"""
{vhero(v, "bluebell-2.jpg", "A private dining room at The Bluebell, Senopati",
       'Private rooms <span class="serif">in Senopati</span>',
       "Two private rooms at The Bluebell, a short walk from SCBD. Book one for a business lunch, a client dinner or a team meeting. There is no minimum spend.")}
</div>
<section class="section">
  <div class="wrap split split--center">
    <div class="media media--tall reveal">{img("bluebell-hall-night.jpg", "The Bluebell in the evening, set for dinner")}</div>
    <div class="reveal">
      <span class="eyebrow">Two rooms</span>
      <h2>Lunch, dinner <span class="serif">or a meeting.</span></h2>
      <div class="lineup" style="grid-template-columns:1fr">
        <div><em>Seats up to 12</em><b>Private Dining &amp; Meeting Room</b><span>A private space for long lunches, dinners and meetings, with food from The Bluebell kitchen.</span></div>
        <div><em>Seats up to 6</em><b>Chess Room</b><span>A smaller room for a quiet meeting or a private meal.</span></div>
      </div>
      <div class="btn-row" style="margin-top:28px"><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Book on WhatsApp</a></div>
    </div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Good to know</span><h2>Book <span class="serif">a room</span></h2>
      <ul class="facts">
        <li><span>Minimum spend</span><span>None</span></li>
        <li><span>Open</span><span>Daily from 10:00</span></li>
        <li><span>Address</span><span><a href="{v["maps"]}" target="_blank" rel="noopener">Jl. Tulodong Atas No. 10 A-B, Senopati</a></span></li>
      </ul>
    </div>
    <div class="reveal"><p>Message us on WhatsApp with the date, the time, which room you’d like and how many of you, and we’ll hold it.</p>
      <p><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Book on WhatsApp</a></p>
      <p class="muted"><a href="/the-bluebell/food/">See the food at The Bluebell</a></p></div>
  </div>
</section>
{rooms_bahasa}
""", image="/assets/img/bluebell-2.jpg", with_collab=False, body_class="venue v-bluebell lp",
     schema=[venue_schema(v, "bluebell-2.jpg")])

page("/the-bluebell/football/", "Watch Premier League Football in Senopati - The Bluebell", "", f"""
{vhero(v, "bluebell-hall-night.jpg", "The dining hall at The Bluebell, Senopati, in the evening",
       'Premier League football <span class="serif">in Senopati</span>',
       "Watch live Premier League football at The Bluebell, a short walk from SCBD. Pull up a chair, order from the kitchen and book your table for match day.")}
</div>
<section class="section">
  <div class="wrap split split--center">
    <div class="media media--tall reveal">{img("roast-beef.jpg", "Roast beef with Yorkshire pudding from The Bluebell kitchen")}</div>
    <div class="reveal">
      <h2>How it <span class="serif">works</span></h2>
      <ul class="ticks">
        <li>Live Premier League matches on weekends</li>
        <li>We show one match at a time, so message us to check what’s on</li>
        <li>British food from our kitchen, served at your table</li>
        <li>Open daily from 10:00</li>
      </ul>
      <p><a href="{v["maps"]}" target="_blank" rel="noopener">Jl. Tulodong Atas No. 10 A-B, Senopati</a></p>
      <div class="btn-row"><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Book a table on WhatsApp</a></div>
    </div>
  </div>
</section>
{bahasa("Dalam Bahasa Indonesia", 'Nobar Liga Inggris <span class="serif">di Senopati</span>', [
    "Nonton bareng Liga Inggris di The Bluebell, hanya beberapa menit berjalan kaki dari SCBD, ditemani hidangan khas Inggris dari dapur kami. Kami menayangkan satu pertandingan dalam satu waktu, jadi hubungi kami untuk jadwalnya.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Reservasi lewat WhatsApp</a>',
])}
""", image="/assets/img/bluebell-hall-night.jpg", with_collab=False, body_class="venue v-bluebell lp",
     schema=[venue_schema(v, "bluebell-hall-night.jpg")])

v = VENUES["briq-bistro"]
page("/briq-bistro/food/", "French Food in Senopati | Steak Frites at BRIQ Bistro", "", f"""
{vhero(v, "brock-hero.jpg", "Steak on the grill for BRIQ Bistro's steak frites",
       'French food <span class="serif">in Senopati</span>',
       "BRIQ Bistro is a French restaurant in Senopati, crafted between fine and casual, and the home of the steak frites. Dinner Monday to Friday, all day at weekends.")}
</div>
<section class="section">
  <div class="wrap split split--center">
    <div class="media media--tall reveal">{img("brock-cuts.jpg", "Sliced steak for BRIQ Bistro's steak frites")}</div>
    <div class="reveal">
      <span class="eyebrow">The signature</span>
      <h2>Home of the <span class="serif">steak frites.</span></h2>
      <p>A properly seared steak, crisp frites and a sauce worth mopping up. The beef comes from <a href="/brock-butchery/">Brock</a>, the butcher we run ourselves, so we choose every cut.</p>
      <ul class="ticks">
        <li><strong>The steak:</strong> seared hard and rested properly</li>
        <li><strong>The sauce:</strong> Café de Paris butter or sauce au poivre</li>
        <li><strong>The frites:</strong> crisp outside, soft inside</li>
      </ul>
      <div class="btn-row"><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Book for steak frites</a><a class="btn btn--ghost" href="/blog/steak-frites-in-jakarta-at-briq-bistro/">More on the steak frites</a></div>
    </div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Every day, all night</span>
      <h2>Steak for two, <span class="serif">495K++.</span></h2>
      <p>The BRIQ Date Package: two ribeye steaks with your choice of Café de Paris butter or sauce au poivre, and two portions of fries, for 495K++ for two.</p>
      <span class="eyebrow" style="display:block;margin-top:40px">Saturdays & Sundays · 11:30–15:00</span>
      <h2>Weekend pasta, <span class="serif">200K++.</span></h2>
      <p>Ravioli, rigatoni or tagliatelle, with a salad and a coffee, tea or soft drink. <a href="/blog/weekend-pasta-promo-at-briq-bistro/">More on the pasta promo</a>.</p>
    </div>
    <div class="grid-2 reveal" style="gap:16px;align-content:start">
      <figure style="margin:0">{img("pasta-rigatoni.jpg", "Rigatoni from BRIQ's weekend pasta promo", sizes="(max-width: 760px) 100vw, 400px")}</figure>
      <figure style="margin:0">{img("pasta-tagliatelle.jpg", "Tagliatelle with salmon at BRIQ Bistro", sizes="(max-width: 760px) 100vw, 400px")}</figure>
    </div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="media media--wide reveal">{img("briq-room.jpg", "The entrance to BRIQ Bistro, Senopati")}</div>
    <div class="reveal">
      <span class="eyebrow">When to come</span>
      <h2>Dinner nightly, <span class="serif">all day at weekends.</span></h2>
      <ul class="facts">
        <li><span>Monday to Friday</span><span>Dinner, 17:00–22:00</span></li>
        <li><span>Saturday & Sunday</span><span>All day, 10:00–22:00: brunch, lunch and dinner</span></li>
        <li><span>Groups & events</span><span>Birthdays, dinners and small gatherings</span></li>
      </ul>
      <p class="muted" style="margin-top:18px" lang="id">Restoran Prancis di Senopati, Jakarta Selatan. Reservasi meja lewat WhatsApp.</p>
    </div>
  </div>
</section>
{landing_close(v, "Book a table at BRIQ")}
""", image="/assets/img/brock-cuts.jpg", with_collab=False, body_class="venue v-briq lp",
     schema=[venue_schema(v, "brock-hero.jpg")])

# BEBOP ad landing pages. Google allows no alcohol advertising in Indonesia, so these pages carry
# no drink wording at all, no photos with bottles, glasses or the bar, and no link to the menu PDF
# (it lists the drinks). Restaurant schema, not BarOrPub.
BEBOP_RESTAURANT = {**VENUES["bebop"], "schema_type": "Restaurant", "cuisine": "Japanese", "menu": None}


def bebop_schema(image):
    return venue_schema(BEBOP_RESTAURANT, image)


# From the food section of the BEBOP menu (Oct 2025). Drinks are left out on purpose.
BEBOP_FOOD = [
    ("Small plates", [
        ("Karaage", "Chicken thigh in a spiced buttermilk marinade, with our special sauce."),
        ("Takoyaki", "The classic Japanese snack with diced octopus, topped with Kewpie mayo, otafuku sauce and katsuobushi."),
        ("Edamame garlic", "Japanese edamame in garlic butter and Japanese soy, with a dash of togarashi."),
    ]),
    ("Burgers", [
        ("Signature smash burger", "80/20 beef patty, American cheddar, onions and jalapeños in a brioche bun, with organic potato crisps."),
        ("Fish burger", "Crisp fish with kyabetsu salad, squid in mayo, lettuce and tomato in a charcoal bun."),
    ]),
    ("On the side", [
        ("Nori French fries", "Triple-cooked, julienne-cut fries with Japanese seasoning and nori."),
    ]),
]

v = VENUES["bebop"]
page("/bebop/live-music/", "Live Music in Senopati | Jazz Mon & Fri at BEBOP", "", f"""
{vhero(v, "jazz-2.jpg", "A full room for live music at BEBOP, Jl. Senopati",
       'Live music <span class="serif">in Senopati</span>',
       "Live jazz every Monday and Friday at BEBOP Bar + Kitchen, Jl. Senopati 61, with modern Japanese plates from the kitchen. Open daily from 17:00, with music from 20:00.")}
</div>
<section class="section">
  <div class="wrap">
    <span class="eyebrow">The week at BEBOP</span>
    <h2>Something on <span class="serif">most nights.</span></h2>
    <div class="lineup">
      <div><em>Mon & Fri · from 20:00</em><b>Jazz Nights</b><span>Live jazz curated by resident musician Bass G, from standards to funk and groove.</span></div>
      <div><em>Tuesdays · from 20:00</em><b>Trivia Tuesdays</b><span>Hosted by Kara Chenoa. Teams, rounds, bragging rights.</span></div>
      <div><em>Weekly · from 20:00</em><b>Karaoke Nights</b><span>The mic is yours. Be brave.</span></div>
      <div><em>Weekly · from 20:00</em><b>BMC Nights</b><span>Resident DJs from the Bebop Music Collective: house, future beats, jazz and soul.</span></div>
    </div>
    <div class="btn-row" style="margin-top:28px"><a class="btn btn--ghost" href="/bebop/trivia/">Trivia & karaoke</a><a class="btn btn--ghost" href="/bebop/kitchen/">The kitchen</a><a class="btn btn--ghost" href="/bebop/private-hire/">Private hire</a></div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Jazz at BEBOP</span>
      <h2>Big names, <span class="serif">small room.</span></h2>
      <p>The stage has hosted some of Indonesia’s most respected names in jazz and beyond, including Dewa Budjana, Barry Likumahuwa and Sandhy Sandoro, alongside a rotating cast of local musicians.</p>
      <p>Come to listen closely, or come for dinner and let the music carry the night. You don’t need to know jazz to enjoy it.</p>
      <p><a class="btn btn--ghost" href="/blog/jazz-at-bebop/">Read: Jazz at BEBOP</a></p>
    </div>
    <div class="reveal">
      <span class="eyebrow">The kitchen</span>
      <h2>Modern <span class="serif">Japanese plates.</span></h2>
      <p>Bold snacks, smoky plates and comforting bites, made for sharing across the table while the band plays.</p>
      <p class="muted">Musik live di Senopati, Jakarta Selatan: jazz setiap Senin dan Jumat. Reservasi meja lewat WhatsApp.</p>
    </div>
  </div>
</section>
{landing_close(v, "Book a table for jazz night")}
""", image="/assets/img/jazz-2.jpg", with_collab=False, body_class="venue v-bebop lp",
     schema=[bebop_schema("jazz-2.jpg")] + bebop_events())

# Trivia details still to confirm with Tom: leave as None and they stay off the page.
TRIVIA_FREE = "Entry is 175K per person"   # It includes a drink, but this is an ad landing page, so that stays off it
TRIVIA_TEAM = "Teams of up to six"

v = VENUES["bebop"]
food_html = "".join(
    f"""<div class="reveal"><span class="eyebrow">{group}</span>
      <div class="lineup" style="grid-template-columns:1fr;margin-top:14px">{"".join(f"<div><b>{n}</b><span>{d}</span></div>" for n, d in items)}</div></div>"""
    for group, items in BEBOP_FOOD)
page("/bebop/kitchen/", "Modern Japanese Food in Senopati | BEBOP Kitchen", "", f"""
{vhero(v, "jazz-2.jpg", "Guests at BEBOP Bar + Kitchen on Jl. Senopati during live music",
       'Modern Japanese plates <span class="serif">in Senopati</span>',
       "The kitchen at BEBOP Bar + Kitchen, Jl. Senopati 61, cooks bold snacks, smoky plates and comforting bites, made for sharing across the table. Open every day from 17:00 till late.")}
</div>
<section class="section">
  <div class="wrap">
    <span class="eyebrow">The kitchen</span>
    <h2>From the <span class="serif">menu.</span></h2>
    <div class="grid-3" style="gap:32px;margin-top:28px;align-items:start">{food_html}</div>
    <div class="btn-row" style="margin-top:32px"><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Book a table</a></div>
    <p style="margin-top:20px"><a href="/bebop/live-music/">Live jazz every Monday and Friday from 20:00</a></p>
  </div>
</section>
{bahasa("Dalam Bahasa Indonesia", 'Restoran Jepang modern <span class="serif">di Senopati</span>', [
    "BEBOP Bar + Kitchen di Jl. Senopati No. 61 menyajikan hidangan Jepang modern untuk dinikmati bersama: karaage, takoyaki, edamame bawang putih, smash burger, dan kentang goreng nori. Buka setiap hari mulai pukul 17.00.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Reservasi meja lewat WhatsApp</a>',
])}
{landing_close(v, "Book a table")}
""", image="/assets/img/jazz-2.jpg", with_collab=False, body_class="venue v-bebop lp",
     schema=[bebop_schema("jazz-2.jpg")])

trivia_extra = "".join(f"<li>{t}</li>" for t in (TRIVIA_FREE, TRIVIA_TEAM) if t)
page("/bebop/trivia/", "Trivia Tuesdays in Senopati | BEBOP", "", f"""
{vhero(v, "jazz-2.jpg", "A full room at BEBOP Bar + Kitchen, Jl. Senopati",
       'Trivia Tuesdays <span class="serif">at BEBOP</span>',
       "Every Tuesday from 20:00 at BEBOP Bar + Kitchen, Jl. Senopati 61, hosted by Kara Chenoa. Teams, rounds, bragging rights.")}
</div>
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Every Tuesday · from 20:00</span>
      <h2>How it <span class="serif">works.</span></h2>
      <ul class="ticks">
        <li>Bring a team</li>
        <li>Book ahead on WhatsApp so we can hold your table</li>
        {trivia_extra}
        <li>Kara Chenoa hosts, with rounds from 20:00</li>
        <li>Order modern Japanese plates from the kitchen while you play</li>
      </ul>
      <div class="btn-row"><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Book a team table</a></div>
    </div>
    <div class="reveal">
      <span class="eyebrow">Weekly · from 20:00</span>
      <h2>Karaoke <span class="serif">Nights.</span></h2>
      <p>The mic is yours. Be brave.</p>
      <p><a href="/bebop/kitchen/">See the kitchen</a> · <a href="/bebop/live-music/">Live jazz every Monday and Friday from 20:00</a></p>
    </div>
  </div>
</section>
{bahasa("Dalam Bahasa Indonesia", 'Trivia night di Senopati <span class="serif">setiap Selasa</span>', [
    "Setiap Selasa mulai pukul 20.00 di BEBOP Bar + Kitchen, Jl. Senopati No. 61, dipandu oleh Kara Chenoa. Ajak tim kamu dan reservasi meja lewat WhatsApp. Ada juga Karaoke Night setiap minggu mulai pukul 20.00.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Reservasi meja lewat WhatsApp</a>',
])}
{landing_close(v, "Book a table")}
""", image="/assets/img/jazz-2.jpg", with_collab=False, body_class="venue v-bebop lp",
     schema=[bebop_schema("jazz-2.jpg")] + weekly_events(v, "Trivia Tuesday", "Trivia hosted by Kara Chenoa. Teams, rounds and bragging rights.", {1}, "jazz-2.jpg"))

page("/bebop/private-hire/", "Private Events & Parties in Senopati | BEBOP", "", f"""
{vhero(v, "halloween-2.jpg", "A packed private party at BEBOP Bar + Kitchen, Senopati",
       'Private hire <span class="serif">at BEBOP</span>',
       "Birthdays, launches and takeovers at BEBOP Bar + Kitchen, Jl. Senopati 61, with live music or resident DJs and modern Japanese plates from the kitchen.")}
</div>
<section class="section">
  <div class="wrap">
    <span class="eyebrow">Your night, your crowd</span>
    <h2>Make the room <span class="serif">yours.</span></h2>
    <div class="lineup">
      <div><em>Celebrations</em><b>Birthdays</b><span>Bring everyone together for a night with music, food and your own crowd.</span></div>
      <div><em>Brands & companies</em><b>Launches</b><span>Product launches, brand nights and company events in Senopati.</span></div>
      <div><em>The whole room</em><b>Takeovers</b><span>Take over BEBOP for the night, with the music set the way you want it.</span></div>
    </div>
  </div>
</section>
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">The music</span>
      <h2>Live music <span class="serif">or resident DJs.</span></h2>
      <p>Book a live band, or a set from the Bebop Music Collective: 14 resident DJs playing house, future beats, jazz and soul.</p>
    </div>
    <div class="reveal">
      <span class="eyebrow">The kitchen</span>
      <h2>Modern <span class="serif">Japanese plates.</span></h2>
      <p>Karaage, takoyaki, smash burgers and more from the kitchen, made for sharing. <a href="/bebop/kitchen/">See the kitchen</a></p>
      <div class="btn-row"><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Enquire on WhatsApp</a></div>
    </div>
  </div>
</section>
{bahasa("Dalam Bahasa Indonesia", 'Sewa tempat untuk acara <span class="serif">di Senopati</span>', [
    "Rayakan ulang tahun, peluncuran produk, atau takeover di BEBOP Bar + Kitchen, Jl. Senopati No. 61, dengan live music atau DJ dari Bebop Music Collective dan hidangan Jepang modern dari dapur kami. Hubungi kami lewat WhatsApp untuk tanggal dan detailnya.",
    f'<a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Tanya lewat WhatsApp</a>',
])}
<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Plan your event</span><h2>Enquire <span class="serif">on WhatsApp</span></h2>{facts(v)}</div>
    <div class="reveal"><p>Message us on WhatsApp with the date, the occasion and how many of you, and we’ll come back to you with the details.</p>
      <p><a class="btn" href="{v["book"]}" target="_blank" rel="noopener">Enquire on WhatsApp</a></p></div>
  </div>
</section>
""", image="/assets/img/halloween-2.jpg", with_collab=False, body_class="venue v-bebop lp",
     schema=[bebop_schema("halloween-2.jpg")])

# ---------------------------------------------------------------- blog

BB = VENUES["the-bluebell"]
BE = VENUES["bebop"]
BQ = VENUES["briq-bistro"]
NEW_POSTS = [
    {
        # Also BRIQ's Google Ads landing page: keep it free of drink wording and of photos with bottles or glasses.
        "slug": "steak-frites-in-jakarta-at-briq-bistro",
        "venue": "briq-bistro",
        "title": "Steak Frites in Jakarta: Why BRIQ Bistro Is the Home of the Steak Frites in Senopati",
        "seo_title": "Steak Frites in Jakarta | BRIQ Bistro, Senopati",
        "seo_desc": "Steak frites in Senopati with beef from our own butcher, Brock. A French restaurant in Jakarta. Book on WhatsApp.",
        "date": "5 November 2026", "iso": "2026-11-05",
        "standfirst": "A properly seared steak, crisp frites and a sauce worth mopping up, with beef from our own butcher, Brock.",
        "cover": "brock-cuts.jpg",
        "body": f"""<figure>{img("brock-cuts.jpg", "Sliced steak for BRIQ Bistro's steak frites, Senopati")}</figure>
<p><strong>Jakarta, 5 November 2026</strong> — Ask anyone who has eaten at BRIQ Bistro what to order and the answer is the same: the steak frites. It is the dish BRIQ is known for, and the reason we call ourselves the home of the steak frites in Senopati.</p>
<h2>It starts with the beef</h2>
<p>Most restaurants buy their steak from a supplier. BRIQ buys it from <a href="/brock-butchery/">Brock Butchery</a>, the butcher we run ourselves. That means we choose the cuts, we set the spec, and if the quality ever slips, we are the first to know. It is the same beef Brock delivers to home kitchens across Jakarta.</p>
<figure>{img("brock-hero.jpg", "Steak on the grill for BRIQ's steak frites")}</figure>
<h2>Steak frites, the BRIQ way</h2>
<ul class="ticks">
  <li><strong>The steak:</strong> seared hard and rested properly, so it is cooked the way you asked for it.</li>
  <li><strong>The sauce:</strong> Café de Paris butter or sauce au poivre.</li>
  <li><strong>The frites:</strong> crisp outside, soft inside, and plenty of them.</li>
</ul>
<h2>Steak frites for two</h2>
<p>The <strong>BRIQ Date Package</strong> runs every day, all night: two ribeye steaks with your choice of Café de Paris butter or sauce au poivre, and two portions of fries, for 495K++ for two.</p>
<h2>A French restaurant in Senopati</h2>
<p>BRIQ is a French bistro crafted between fine and casual: the care of fine dining, with the warmth of a neighbourhood restaurant. Dinner runs Monday to Friday from 17:00, and at weekends we are open all day, from 10:00 to 22:00.</p>
<p>At weekend lunchtimes there is also our <a href="/blog/weekend-pasta-promo-at-briq-bistro/">weekend pasta promo</a>: ravioli, rigatoni or tagliatelle with a salad and a coffee, tea or soft drink for 200K++, from 11:30 to 15:00.</p>
<figure>{img("pasta-rigatoni.jpg", "Rigatoni from BRIQ Bistro's weekend pasta promo")}</figure>
<div class="box">
<h3 class="h4">BRIQ Bistro</h3>
<p>{BQ["address"]}<br>Dinner Monday to Friday from 17:00 · All day at weekends, 10:00–22:00<br><a href="{BQ["book"]}" target="_blank" rel="noopener">Book on WhatsApp</a> · <a href="{BQ["instagram"]}" target="_blank" rel="noopener">{BQ["ig_handle"]}</a></p>
<p lang="id">Restoran Prancis di Senopati, Jakarta Selatan. Reservasi meja lewat WhatsApp.</p>
</div>
<p><a class="btn" href="{BQ["book"]}" target="_blank" rel="noopener">Book a table for steak frites</a></p>""",
    },
    {
        "slug": "sunday-roast-at-the-bluebell-jakarta",
        "venue": "the-bluebell",
        "title": "Sunday Roast Comes to Senopati: The Bluebell’s Roast Beef, Roast Chicken and Nut Roast",
        "seo_title": "Sunday Roast in Jakarta | The Bluebell Public House",
        "seo_desc": "Sunday roast at The Bluebell, Senopati: roast beef 275K, roast chicken 200K, nut roast 150K, all the trimmings. Pets welcome.",
        "date": "3 November 2026", "iso": "2026-11-03",
        "standfirst": "Roast beef, roast chicken or nut roast, with all the trimmings, every Sunday at Jakarta’s British pub.",
        "cover": "roast-beef.jpg",
        "body": f"""<figure>{img("roast-beef.jpg", "Sunday roast beef with Yorkshire pudding at The Bluebell, Senopati")}</figure>
<p><strong>Jakarta, 3 November 2026</strong> — There are few things more British than a Sunday roast, and now there’s one on Jl. Tulodong Atas. The Bluebell Public House has launched its Sunday Roast: a proper plate of roast meat, Yorkshire pudding and gravy, served at a long table in the heart of Senopati.</p>
<p>For anyone searching for a British pub in Jakarta that does Sundays properly, this is the one. Start the day earlier with us, bring the family or the whole flat, and settle in. Our Sundays are pet friendly too, so the dog can come.</p>
<h2>Pick your roast</h2>
<p>Three roasts, each served with a Yorkshire pudding, cauliflower cheese, roast potatoes, roast carrots and cabbage, and a jug of gravy:</p>
<ul class="ticks">
  <li><strong>Roast Beef</strong> — 275K++</li>
  <li><strong>Roast Chicken</strong> — 200K++</li>
  <li><strong>Nut Roast</strong> — 150K++, our vegetarian roast</li>
</ul>
<div class="grid-2" style="margin:32px 0;gap:16px">
  <figure style="margin:0">{img("roast-chicken.jpg", "Roast chicken Sunday roast at The Bluebell", sizes="(max-width: 760px) 100vw, 400px")}</figure>
  <figure style="margin:0">{img("nut-roast.jpg", "Vegetarian nut roast at The Bluebell, Jakarta", sizes="(max-width: 760px) 100vw, 400px")}</figure>
</div>
<h2>British classics all week</h2>
<p>If Sunday isn’t your day, the kitchen serves British classics all week, from fish and chips to a proper pie. <a href="/the-bluebell/food/">See the food at The Bluebell</a>.</p>
<p>The Bluebell is open every day from 10:00, so on a Sunday in Senopati you can start with lunch and stay for the evening.</p>
<h2>More at the pub this week</h2>
<ul class="ticks">
  <li><strong>Pub Quiz, every Wednesday:</strong> teams, rounds and bragging rights.</li>
  <li><strong>The Chess Room:</strong> our snug, for a quiet corner and a game of chess.</li>
  <li><strong>Private dining room:</strong> seats twelve, for birthdays and family lunches. <a href="/the-bluebell/private-rooms/">See the private rooms</a>.</li>
</ul>
<div class="box">
<h3 class="h4">The Bluebell Public House</h3>
<p>A modern British public house in Senopati, South Jakarta: fish & chips, pies and now the Sunday roast.</p>
<h3 class="h4">Address + bookings</h3>
<p>{BB["address"]}<br>Open {BB["hours_text"]}<br>Instagram: <a href="{BB["instagram"]}" target="_blank" rel="noopener">{BB["ig_handle"]}</a><br>Bookings: <a href="{BB["book"]}" target="_blank" rel="noopener">WhatsApp us</a></p>
</div>
<p><a class="btn" href="{BB["book"]}" target="_blank" rel="noopener">Book your Sunday roast</a></p>""",
    },
    {
        "slug": "halloween-week-at-bebop-senopati",
        "venue": "bebop",
        "title": "What Lies Beneath the Night: A Look Back at Halloween Week at BEBOP",
        "seo_title": "Halloween Week at BEBOP, Senopati | Recap",
        "seo_desc": "Six nights of jazz, trivia, karaoke and Booty Groove: a look back at Halloween Week at BEBOP Bar + Kitchen in Senopati.",
        "date": "3 November 2026", "iso": "2026-11-03",
        "standfirst": "Six nights, a lot of costumes and one very full dance floor. Thank you for dancing beneath the shadows with us.",
        "cover": "halloween-2.jpg",
        "body": f"""<figure>{img("halloween-2.jpg", "Halloween party crowd dancing at BEBOP Bar + Kitchen, Senopati", sizes="(max-width: 760px) 100vw, 900px")}</figure>
<p><strong>Jakarta, 3 November 2026</strong> — For one week at the end of October, BEBOP Bar + Kitchen turned into something a little stranger than usual. <em>What Lies Beneath the Night</em>, our Halloween Week, ran from Monday 26 to Saturday 31 October, with a different night every night and a costume dress code for all of it.</p>
<h2>Six nights, six moods</h2>
<ul class="ticks">
  <li><strong>Monday 26 Oct — Special Monday Jazz.</strong> Our weekly live jazz night, with a darker set list.</li>
  <li><strong>Tuesday 27 Oct — Trivia Night with Kara Chenoa.</strong> Brains, banter and bonus points for costumes.</li>
  <li><strong>Wednesday 28 Oct — Lady Gaga Listening Party.</strong> Played front to back, the way a listening bar should.</li>
  <li><strong>Thursday 29 Oct — Spooky Karaoke with cryonbike.</strong> Less about hitting the note, more about bringing the house down.</li>
  <li><strong>Friday 30 Oct — Booty Groove</strong> with Jaka, Yelig (Club Odyssey) and Laskar.</li>
  <li><strong>Saturday 31 Oct — Bebop Music Collective</strong> on the decks to close the week.</li>
</ul>
<div class="grid-2" style="margin:32px 0;gap:16px">
  <figure style="margin:0">{img("halloween-1.jpg", "Guests in costume at BEBOP's Halloween party", sizes="(max-width: 760px) 100vw, 400px")}</figure>
  <figure style="margin:0">{img("halloween-3.jpg", "Halloween costumes at BEBOP Bar + Kitchen, Jakarta", sizes="(max-width: 760px) 100vw, 400px")}</figure>
</div>
<h2>Why we do weeks like this</h2>
<p>BEBOP has always been more than a bar in Senopati: it’s a room built around music and the people who come back for it. Halloween Week brought together everything we run through the year, from live jazz and trivia to karaoke and the Bebop Music Collective, in one six-night run. Thank you to everyone who dressed up, sang, danced and stayed late.</p>
<figure>{img("halloween-4.jpg", "DJs from the Bebop Music Collective at Halloween Week", sizes="(max-width: 760px) 100vw, 900px")}</figure>
<h2>What’s next at BEBOP</h2>
<ul class="ticks">
  <li><strong>Happy hour, every night 5–8 PM:</strong> selected cocktails for 100K.</li>
  <li><strong>Live jazz every Monday and Friday</strong> — still one of the best answers to “jazz bar in Jakarta”. Recently, <em>Between the Notes</em> with Bass G brought Barry Likumahuwa to our stage.</li>
  <li><strong>Trivia Tuesdays, karaoke and BMC nights</strong> through the week. Follow <a href="{BE["instagram"]}" target="_blank" rel="noopener">{BE["ig_handle"]}</a> for the line-up.</li>
</ul>
<div class="box">
<h3 class="h4">BEBOP Bar + Kitchen</h3>
<p>A jazz and cocktail bar on Jl. Senopati No. 61, South Jakarta, with modern Japanese plates and live music most nights. Open every day from 17:00 till late.</p>
<p><a href="{BE["book"]}" target="_blank" rel="noopener">Book on WhatsApp</a> · <a href="{BE["instagram"]}" target="_blank" rel="noopener">{BE["ig_handle"]}</a></p>
</div>
<p><a class="btn" href="/bebop/">Visit BEBOP</a></p>""",
    },
    {
        "slug": "weekend-pasta-promo-at-briq-bistro",
        "venue": "briq-bistro",
        "title": "Weekend Pasta at BRIQ: Ravioli, Rigatoni or Tagliatelle, with Salad and a Drink, for 200K",
        "seo_title": "Weekend Pasta Promo at BRIQ Bistro, Senopati",
        "seo_desc": "BRIQ's weekend pasta promo: ravioli, rigatoni or tagliatelle with salad and a drink for 200K++, Sat & Sun 11:30–15:00.",
        "date": "3 November 2026", "iso": "2026-11-03",
        "standfirst": "Make your weekends a little more special: pasta, a salad and a drink, every Saturday and Sunday lunchtime.",
        "cover": "pasta-rigatoni.jpg",
        "body": f"""<figure>{img("pasta-rigatoni.jpg", "Rigatoni from BRIQ Bistro's weekend pasta promo, Senopati")}</figure>
<p><strong>Jakarta, 3 November 2026</strong> — BRIQ Bistro has launched its weekend Pasta Promo, a new reason to spend a slow Saturday or Sunday lunch in Senopati. Pick your pasta, add a salad and a drink, and the whole thing comes to 200K++.</p>
<h2>How it works</h2>
<ul class="ticks">
  <li><strong>Choose your pasta:</strong> ravioli, rigatoni or tagliatelle.</li>
  <li><strong>Add your choice of salad.</strong></li>
  <li><strong>And a drink:</strong> coffee, tea or a soft drink.</li>
  <li><strong>200K++</strong>, every weekend from 11:30 to 15:00.</li>
</ul>
<figure>{img("pasta-tagliatelle.jpg", "Tagliatelle with salmon at BRIQ Bistro, Jakarta")}</figure>
<h2>Weekends at BRIQ, all day</h2>
<p>On weekdays BRIQ is a dinner spot, but on Saturdays and Sundays we’re open all day, from 10:00 to 22:00. Pasta at lunch, a glass of something on the terrace in the afternoon, and dinner if you’re not ready to leave.</p>
<p>BRIQ is still the home of the steak frites: a properly seared steak, crisp frites and a sauce worth mopping up, made with beef from our own butcher, Brock.</p>
<h2>Bringing someone?</h2>
<p>The <strong>BRIQ Date Package</strong> runs every day, all night: two ribeye steaks with your choice of Café de Paris butter or sauce au poivre, and two portions of fries, for 495K++ for two. Add escargots and two drinks for 100K++.</p>
<div class="box">
<h3 class="h4">BRIQ Bistro</h3>
<p>A neighbourhood French bistro in Senopati, crafted between fine and casual. Dinner Monday to Friday from 17:00; all day at weekends.</p>
<p>{BQ["address"]}<br><a href="{BQ["book"]}" target="_blank" rel="noopener">Book on WhatsApp</a> · <a href="{BQ["instagram"]}" target="_blank" rel="noopener">{BQ["ig_handle"]}</a></p>
</div>
<p><a class="btn" href="{BQ["book"]}" target="_blank" rel="noopener">Book a weekend table</a></p>""",
    },
]

POSTS = NEW_POSTS + [
    {
        "slug": "the-bluebell-public-house-opens-in-south-jakarta",
        "venue": "the-bluebell",
        "old": "/blog/the-bluebell-public-house-opens-in-south-jakarta-bringing-the-warmth-of-a-british-pub-to-senopati/",
        "title": "The Bluebell Public House Opens in South Jakarta, Bringing the Warmth of a British Pub to Senopati",
        "seo_title": "The Bluebell Public House Opens: A British Pub in Senopati, Jakarta",
        "date": "5 October 2026", "iso": "2026-10-05",
        "standfirst": "Raise a pint, British-style, at the newest pub in the heart of South Jakarta.",
        "cover": "bluebell-1.jpg",
        "body": f"""<figure>{img("bluebell-2.jpg", "Inside The Bluebell Public House, Senopati")}</figure>
<p><strong>Jakarta, 3 October 2026</strong> — The Bluebell Public House introduces a refined yet deeply welcoming slice of British pub culture to the heart of Senopati. Designed as a dimly lit, warm abode, the space pairs an elevated-casual dining experience with a curated drinks programme, making it the perfect setting for post-work unwinding and intimate catch-ups.</p>
<p>The concept captures the social soul of the traditional public house, offering cosy nooks where daytime conversations naturally stretch into long, relaxed evenings.</p>
<h2>Fish & chips, pies and a proper pint</h2>
<p>The menu strikes a balance between comfort and sophistication, featuring thoughtfully elevated British classics alongside draught beers, fine spirits, and signature cocktails. Approachably premium and easy to enjoy, the food and drinks are crafted for any occasion — whether you are stopping by for a quick bite after office hours or settling in for a nightcap.</p>
<h2>A different kind of night out in Senopati</h2>
<p>Tucked into Senopati’s vibrant landscape, The Bluebell Public House offers a distinct alternative to the neighbourhood’s bustling dining scene, blending the timeless familiarity of pub culture into a contemporary Jakarta setting.</p>
<figure>{img("bluebell-1.jpg", "The bar at The Bluebell")}</figure>
<div class="box">
<h3 class="h4">About The Bluebell Public House</h3>
<p>The Bluebell Public House is a British-inspired pub in Senopati, South Jakarta. The concept brings together food, drinks, and a relaxed social atmosphere, drawing on the character of the British pub while making it its own in Jakarta.</p>
<h3 class="h4">Address + contact</h3>
<p>{BB["address"]}<br>Open {BB["hours_text"]}<br>Instagram: <a href="{BB["instagram"]}" target="_blank" rel="noopener">{BB["ig_handle"]}</a><br>Bookings: <a href="{BB["book"]}" target="_blank" rel="noopener">WhatsApp us</a></p>
</div>
<p><a class="btn" href="/the-bluebell/">Visit The Bluebell</a></p>""",
    },
    {
        "slug": "jazz-at-bebop",
        "venue": "bebop",
        "old": "/blog/wpdv5ufmcja78usx0i0q62bosubba8/",
        "title": "Jazz at BEBOP Creates Moments That Don’t Happen Twice",
        "seo_title": "Jazz at BEBOP: Live Jazz Bar in Senopati, Jakarta, Every Monday & Friday",
        "date": "15 September 2026", "iso": "2026-09-15",
        "standfirst": "Each week, a live jazz night you don’t want to miss.",
        "cover": "jazz-2.jpg",
        "body": f"""<figure>{img("jazz-1.jpg", "Live jazz band playing at BEBOP Bar + Kitchen")}</figure>
<p><strong>Jakarta, 15 September 2026</strong> — What started as a weekly fixture for the city’s music lovers has grown into one of Jakarta’s go-to stages for jazz that truly feels alive.</p>
<h2>Curated by Bass G</h2>
<p>The programme at BEBOP is curated by Bass G, resident jazz curator and musician, who oversees the line-ups and musical direction. Each night shows a different side of jazz — from traditional playing to funk, groove and more modern sounds — unpredictable enough to keep the audience coming back for a different vibe each time, and never less than a good time.</p>
<blockquote><p>“We want musicians to have room to be themselves and interact with the audience. The programme tries to show that jazz can be energetic, fun, and accessible, rather than something that has to feel distant or overly serious.”</p><cite>Bass G, resident jazz curator</cite></blockquote>
<p>Jazz at BEBOP is rooted in the belief that it is not just about playing great music, but about creating an experience where the audience feels involved. Come to listen attentively, or have a drink, talk, and enjoy the music without needing to understand jazz beforehand.</p>
<h2>Big names, small room</h2>
<p>Over the past year, BEBOP’s stage has hosted some of Indonesia’s most respected names in jazz and beyond, including Dewa Budjana, Barry Likumahuwa and Sandhy Sandoro — a line-up that reflects BEBOP’s commitment to bringing serious musicianship into an intimate, unpretentious setting.</p>
<h2>When to go</h2>
<p>Jazz nights run every Monday and Friday at BEBOP Bar + Kitchen, Jl. Senopati No. 61, featuring a rotating cast of local musicians alongside occasional special guests.</p>
<figure>{img("jazz-2.jpg", "The crowd at Jazz at BEBOP, Senopati")}</figure>
<p><a class="btn" href="/bebop/">Book a table at BEBOP</a></p>""",
    },
]

feat, rest = POSTS[0], POSTS[1:]
feature = f"""<a class="journal-feature reveal" href="/blog/{feat['slug']}/">
  <div class="ph">{img(feat['cover'], feat['title'])}</div>
  <div><span class="eyebrow">Latest story</span><h2>{feat['title']}</h2><p class="lede">{feat['standfirst']}</p><div class="meta">{feat['date']} · Thomas Brown</div></div>
</a>"""
cards = "".join(f"""<a class="post-card reveal" href="/blog/{p['slug']}/">
  {img(p['cover'], '')}
  <div class="meta">{p['date']} · Thomas Brown</div>
  <h2 class="h3">{p['title']}</h2>
  <p class="muted">{p['standfirst']}</p>
</a>""" for p in rest)

page("/blog/", "Journal | Openings, Live Jazz & Stories from Senopati | Basho Projects",
     "Stories from Basho Projects and its venues in Senopati, Jakarta: openings, live jazz at BEBOP, The Bluebell and more.",
     f"""<section class="section"><div class="wrap">
  <span class="eyebrow">The Journal</span>
  <h1 style="font-size:clamp(56px,10vw,160px);margin-bottom:56px">Notes from <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">Senopati.</span></h1>
  {feature}
  <div class="sec-head"><span class="no"><b>More</b> / stories</span></div>
  <div class="posts">{cards}</div>
</div></section>""", image="/assets/img/" + POSTS[0]["cover"])

for i, p in enumerate(POSTS):
    prev_p = POSTS[i - 1] if i > 0 else None
    next_p = POSTS[i + 1] if i + 1 < len(POSTS) else None
    nav = '<nav class="post-nav">'
    nav += f'<a href="/blog/{prev_p["slug"]}/"><small>Newer</small>{prev_p["title"]}</a>' if prev_p else "<span></span>"
    nav += f'<a href="/blog/{next_p["slug"]}/" style="text-align:right"><small>Older</small>{next_p["title"]}</a>' if next_p else ""
    nav += "</nav>"
    article_ld = {
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
        "datePublished": p["iso"], "author": {"@type": "Person", "name": "Thomas Brown"},
        "publisher": {"@type": "Organization", "name": "Basho Projects", "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/basho-logo.png"}},
        "image": f"{DOMAIN}/assets/img/{p['cover']}", "mainEntityOfPage": f"{DOMAIN}/blog/{p['slug']}/",
    }
    if p.get("seo_desc"):
        SEO_META[f"/blog/{p['slug']}/"] = (p["seo_title"], p["seo_desc"])
    page(f"/blog/{p['slug']}/", f"{p['seo_title']} | Basho Projects", p["standfirst"], f"""
<section class="section"><article class="wrap article">
  <a href="/blog/" class="kicker" style="text-decoration:none">← Blog</a>
  <h1>{p['title']}</h1>
  <div class="meta">{p['date']} · Written by Thomas Brown</div>
  <p class="standfirst">{p['standfirst']}</p>
  {p['body']}
  {nav}
</article></section>""", image="/assets/img/" + p["cover"], with_collab=False, schema=[article_ld], venue=p["venue"])
    if p.get("old"):
        redirect(p["old"], f"/blog/{p['slug']}/")

# ---------------------------------------------------------------- group pages (spliced into build.py)



VENUE_PHOTOS = {"bebop": "bebop-bar.jpg", "briq-bistro": "briq-hero.jpg", "brock-butchery": "brock-hero.jpg", "the-bluebell": "bluebell-bar.jpg"}
VENUE_COLOURS = {"bebop": "#ef4a2e", "briq-bistro": "#a3452c", "brock-butchery": "#6a6a2a", "the-bluebell": "#5b7fa6"}


def venue_rows(heading_tag="h3"):
    rows = []
    for i, key in enumerate(VENUE_ORDER, 1):
        v = VENUES[key]
        acts = [f'<a class="pill" href="{v["path"]}">View<span class="skip"> {v["name"]}</span></a>']
        if v.get("book"):
            acts.append(f'<a class="pill" href="{v["book"]}" target="_blank" rel="noopener">Book</a>')
        if v.get("menu"):
            acts.append(f'<a class="pill" href="{v["menu"]}" target="_blank" rel="noopener">Menu</a>')
        if v.get("tokopedia"):
            acts.append(f'<a class="pill" href="{v["tokopedia"]}" target="_blank" rel="noopener">Order</a>')
        if v.get("maps"):
            acts.append(f'<a class="pill" href="{v["maps"]}" target="_blank" rel="noopener">Map</a>')
        status = ""
        if v.get("hours"):
            late = ' data-late="1"' if v.get("late") else ""
            status = f'<span class="status" data-hours=\'{json.dumps(v["hours"])}\'{late}>{v["hours_text"]}</span>'
        photo = VENUE_PHOTOS[key]
        rows.append(f"""<div class="vrow reveal" style="--vc:{VENUE_COLOURS[key]}">
  <span class="vrow__no">0{i}</span>
  <{heading_tag}><a href="{v['path']}">{v['short']}</a></{heading_tag}>
  <div class="vrow__meta"><span class="tag">{v['tag']}</span>{v['blurb']}{status}</div>
  <div class="vrow__acts">{''.join(acts)}</div>
  <div class="vrow__thumb">{img(photo, v['name'])}</div>
  <div class="vrow__peek" aria-hidden="true">{img(photo, v["name"], sizes="220px")}</div>
</div>""")
    return f'<div class="vrows">{"".join(rows)}</div>'


STAMP = """<svg class="stamp" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="c" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
<text><textPath href="#c">Operators first · Made in Senopati · Since BEBOP ·</textPath></text>
<circle cx="100" cy="100" r="34" fill="#f2ede4"/><text x="100" y="106" text-anchor="middle" style="font-size:18px;letter-spacing:1px;fill:#15130f">BASHO</text></svg>"""

WHAT_WE_DO = {
    "Concept & Development": ["Concept validation and refinement", "Location sourcing and market fit", "Budgeting, forecasting and P&L modelling", "Timeline management and roll-out planning"],
    "Brand & Creative": ["Naming and brand story", "Visual identity, voice and narrative systems", "Spatial storytelling: uniforms, menus, playlists, sensory cues"],
    "Menu & Bar": ["Signature cocktails and dish development", "Menu costing, engineering and workflow design", "Storytelling through menus: layout, format, copy"],
    "Operations & Systems": ["SOPs for FOH, bar and kitchen", "Team structure, hiring and onboarding", "POS, inventory, reservations and rota set-up", "Cost control and reporting systems"],
    "Launch & Marketing": ["Go-to-market strategy and pre-opening buzz", "Soft launch, events and programming", "Content, reels and visual direction", "Meta, Google and TikTok ads, KOLs and PR (via Bubble + Squeak)"],
    "Service & Culture": ["Guest journey mapping", "In-service rituals and team language", "Service training and floor-flow testing", "Feedback systems and team retention"],
}


def accordion():
    items = "".join(
        f"<details><summary>{k}</summary><ul>{''.join(f'<li>{i}</li>' for i in v)}</ul></details>"
        for k, v in WHAT_WE_DO.items())
    return f'<div class="accordion">{items}</div>'


def posts_teaser():
    return "".join(f"""<a class="post-card reveal" href="/blog/{p['slug']}/">{img(p['cover'], '')}<div class="meta">{p['date']}</div><h3 class="h4">{p['title']}</h3></a>""" for p in POSTS)


# ---------------------------------------------------------------- home

home_faq = [
    ("What is Basho Projects?", "Basho Projects is an independent hospitality group in Senopati, South Jakarta. We own and run BEBOP Bar + Kitchen, BRIQ Bistro, The Bluebell Public House and Brock Butchery, and we help other founders and investors build bars and restaurants of their own."),
    ("Where are your venues?", "All within a few minutes’ walk of each other in Senopati, Kebayoran Baru, South Jakarta: BEBOP on Jl. Senopati, BRIQ on Jl. Prof. Joko Sutono and The Bluebell on Jl. Tulodong Atas."),
    ("Can Basho Projects help with my restaurant or bar?", "Yes. We take on a small number of partner projects each year, from full incubation to a single problem like a menu, a launch or a team that isn’t clicking. See our services or get in touch."),
    ("Can I invest in a Basho Projects venue?", "We bring in partners on new concepts. Tell us a little about yourself on the invest page and we’ll set up a conversation."),
]

page("/", "Basho Projects | Jakarta Hospitality Group — BEBOP, BRIQ, The Bluebell & Brock",
     "Basho Projects is the independent hospitality group behind BEBOP Bar + Kitchen, BRIQ Bistro, The Bluebell Public House and Brock Butchery in Senopati, Jakarta. Find a table, work with us, or invest in what we build next.",
     f"""
<section class="ghero">
  <div class="wrap">
    <div class="ghero__grid">
      <div>
        <span class="eyebrow">Basho Projects · Senopati, South Jakarta</span>
        <h1>Small group. <span class="serif">Big nights.</span></h1>
        <p class="lede">We’re the independent hospitality group behind BEBOP, BRIQ, The Bluebell and Brock — four rooms within walking distance in Senopati. We build our own places, run them ourselves, and help a few others build theirs.</p>
        <div class="btn-row" style="margin-top:28px"><a class="btn btn--hot" href="#venues">Find a table</a><a class="btn btn--line" href="/services/">Work with us</a><a class="btn btn--line" href="/invest/">Invest</a></div>
      </div>
      {STAMP}
    </div>
  </div>
  <div class="reel" aria-label="Our venues">
    <a href="/bebop/">{img("bebop-bar.jpg", "BEBOP Bar + Kitchen", lazy=False, sizes="(max-width: 760px) 62vw, 20vw")}<span>BEBOP</span></a>
    <a href="/briq-bistro/">{img("briq-hero.jpg", "BRIQ Bistro", lazy=False, sizes="(max-width: 760px) 62vw, 20vw")}<span>BRIQ</span></a>
    <a href="/the-bluebell/">{img("bluebell-bar.jpg", "The Bluebell Public House", lazy=False, sizes="(max-width: 760px) 62vw, 20vw")}<span>The Bluebell</span></a>
    <a href="/brock-butchery/">{img("brock-hero.jpg", "Brock Butchery", sizes="(max-width: 760px) 62vw, 20vw")}<span>Brock</span></a>
    <a href="/bebop/#whats-on">{img("jazz-1.jpg", "Live jazz at BEBOP", sizes="(max-width: 760px) 62vw, 20vw")}<span>Jazz nights</span></a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>01</b> / Pick your door</span></div>
    <h2 class="skip">Eat and drink, build with us, or invest</h2>
    <div class="doors">
      <a class="door reveal" href="#venues"><span class="k">Eat & drink</span><h3>Find a table in Senopati</h3><p>A jazz and cocktail bar, a French bistro, a British pub and a butcher that delivers. Book, see the menu, get directions.</p><span class="go">Our venues</span></a>
      <a class="door reveal" href="/services/"><span class="k">Build with us</span><h3>Open something that lasts</h3><p>Concept, brand, menu, team, launch and marketing, from operators who run their own rooms every night.</p><span class="go">Services</span></a>
      <a class="door reveal" href="/invest/"><span class="k">Invest with us</span><h3>Back the next one</h3><p>We bring partners in on new concepts. Operator-led, built in a neighbourhood we know street by street.</p><span class="go">Investors</span></a>
    </div>
  </div>
</section>

<section class="section ink" id="venues">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>02</b> / Our venues</span><a href="/our-projects/">All venues →</a></div>
    <h2 class="reveal" style="font-size:clamp(40px,6vw,92px);max-width:14ch;margin-bottom:48px">Four rooms. <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">One street’s walk.</span></h2>
    {venue_rows()}
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <div class="sec-head" style="border:0;padding:0"><span class="no"><b>03</b> / Why we’re different</span></div>
      <p class="manifesto">We’re not the biggest group in Jakarta. <em>That’s the point.</em></p>
    </div>
    <div class="reveal">
      <p class="lede">Basho Projects is a hospitality incubator, operator and consultancy. Every recommendation we make has already been tested against a roster, a rent cheque and a Saturday night service — on our own floors, with our own money.</p>
      <p>That keeps us honest. It also keeps us small on purpose: a handful of venues we run properly, and a few partner projects a year where the senior team actually shows up.</p>
      <a class="btn" href="/about/">Our story</a>
    </div>
  </div>
  <div class="wrap" style="margin-top:64px">
    <div class="nums">
      <div class="reveal"><b>4</b><span>venues in Senopati, all walking distance</span></div>
      <div class="reveal"><b>14</b><span>resident DJs in the Bebop Music Collective</span></div>
      <div class="reveal"><b>2</b><span>live jazz nights a week at BEBOP</span></div>
      <div class="reveal"><b>7</b><span>days a week The Bluebell pulls pints, from 10:00</span></div>
    </div>
  </div>
</section>

<section class="section ink">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>04</b> / What’s on</span><a href="/bebop/#whats-on">Full line-up →</a></div>
    <h2 class="reveal" style="font-size:clamp(36px,5vw,72px);margin-bottom:40px">Live music, quiz nights and <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">long lunches.</span></h2>
    <div class="week">
      <div><em>Monday & Friday · BEBOP</em><b>Jazz Nights</b><span>Live jazz curated by Bass G, from standards to funk and groove.</span><a href="/bebop/">BEBOP →</a></div>
      <div><em>Tuesday · BEBOP</em><b>Trivia Tuesdays</b><span>Hosted by Kara Chenoa. Brains, banter and a little buzz.</span><a href="/bebop/">BEBOP →</a></div>
      <div><em>Weekly · BEBOP</em><b>BMC Nights & Booty Groove</b><span>The Bebop Music Collective on the decks, then the dance floor.</span><a href="/bebop/#bmc">The collective →</a></div>
      <div><em>Weekends · BRIQ</em><b>Pasta promo, 200K++</b><span>Ravioli, rigatoni or tagliatelle with salad and a drink, 11:30–15:00.</span><a href="/blog/weekend-pasta-promo-at-briq-bistro/">BRIQ pasta →</a></div>
      <div><em>Sundays · The Bluebell</em><b>Sunday Roast</b><span>Roast beef, roast chicken or nut roast with all the trimmings, from 150K++.</span><a href="/blog/sunday-roast-at-the-bluebell-jakarta/">The roast →</a></div>
      <div><em>Wednesday · The Bluebell</em><b>Pub Quiz</b><span>Teams, rounds and bragging rights, every Wednesday at the pub.</span><a href="/the-bluebell/#now-on">The Bluebell →</a></div>
      <div><em>Daily 5–8 PM · BEBOP & The Bluebell</em><b>Happy hours</b><span>100K cocktails at BEBOP; 100K++ G&Ts and Heineken buckets at The Bluebell.</span><a href="/the-bluebell/#now-on">Details →</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>05</b> / For founders & brands</span><a href="/services/">Services →</a></div>
    <div class="split split--center">
      <h2 class="reveal" style="font-size:clamp(36px,5vw,76px)">Your concept, run by people who <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">close up at 2am.</span></h2>
      <div class="reveal">
        <p class="lede">We help hospitality businesses at every stage, from napkin sketch to full roll-out, or reimagining something that’s already live.</p>
        <ul class="ticks"><li>Concept, location and the numbers</li><li>Brand, menu, bar programme and team</li><li>Launch, ads, KOLs and PR through our own agency, Bubble + Squeak Media</li></ul>
        <div class="btn-row"><a class="btn" href="/services/">See services</a><a class="btn btn--line" href="/contact/">Start a conversation</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section cta-band">
  <div class="wrap split split--center">
    <div class="reveal"><span class="eyebrow">For investors</span><h2>Back the next one.</h2></div>
    <div class="reveal">
      <p class="lede">We open a small number of new concepts and bring in partners for each. Operator-led, Senopati-tested, built to last more than one season.</p>
      <div class="btn-row"><a class="btn" href="/invest/">How we work with investors</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>06</b> / Journal</span><a href="/blog/">All stories →</a></div>
    <div class="posts">{posts_teaser()}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap split">
    <div><div class="sec-head" style="border:0;padding:0"><span class="no"><b>07</b> / Good to know</span></div><h2 style="font-size:clamp(32px,4vw,56px)">Questions people ask us</h2></div>
    <div>{faq_html(home_faq)}</div>
  </div>
</section>
""", schema=[ORG, faq_schema(home_faq)])

# ---------------------------------------------------------------- about

page("/about/", "About Basho Projects | Independent Hospitality Group in Senopati, Jakarta",
     "Operators first. The story of Basho Projects, the independent Jakarta hospitality group behind BEBOP, BRIQ Bistro, The Bluebell Public House and Brock Butchery.",
     f"""
<section class="section">
  <div class="wrap">
    <span class="eyebrow">About Basho Projects</span>
    <h1 style="font-size:clamp(52px,9vw,140px);max-width:12ch">Operators <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">first.</span> Everything else second.</h1>
  </div>
  <div class="wrap split" style="margin-top:56px">
    <div class="media media--tall reveal">{img("bebop-room.jpg", "Inside BEBOP Bar + Kitchen, Senopati")}</div>
    <div class="reveal">
      <p class="lede">We’re a collective of builders, operators and creatives behind some of Jakarta’s most distinct hospitality concepts.</p>
      <p>We specialise in brands that feel lived-in and loved: naming and storytelling, service rituals, marketing plans and the operating systems underneath. Every member of the team has been in the trenches, launching and running venues from the ground up.</p>
      <p>We run our own venues, and we take on a small number of partner projects each year, from full incubation to marketing alone. Together we turn big ideas into grounded realities that work — emotionally and commercially.</p>
      <p>We’re not the biggest group in the city, and we’re fine with that. Small means the people who build a place are the same people you’ll find behind the bar on a Friday.</p>
    </div>
  </div>
</section>

<section class="section ink">
  <div class="wrap split">
    <div><div class="sec-head" style="border:0;padding:0"><span class="no"><b>01</b> / How we got here</span></div>
      <h2 style="font-size:clamp(36px,5vw,72px)">One bar, then <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">a neighbourhood.</span></h2></div>
    <ol class="tl" style="border-color:var(--paper2)">
      <li><b>BEBOP opens on Jl. Senopati</b><span class="muted">A bar first: cocktails, Mega Highballs and modern Japanese plates, with music at the centre of the room.</span></li>
      <li><b>2022 · The DJs move in</b><span class="muted">A group of DJs find a home at BEBOP and, the following year, launch the Bebop Music Collective — 14 residents strong today.</span></li>
      <li><b>BRIQ Bistro</b><span class="muted">A neighbourhood French bistro crafted between fine and casual, a few minutes’ walk away.</span></li>
      <li><b>2026 · Brock Butchery</b><span class="muted">A problem in our own kitchens becomes a business: premium meat, priced honestly, delivered across Jakarta.</span></li>
      <li><b>September 2026 · The Bluebell</b><span class="muted">A modern British public house on Jl. Tulodong Atas: pints, G&Ts, fish & chips and the Chess Room.</span></li>
      <li><b>Bubble + Squeak Media</b><span class="muted">Our in-house agency for performance marketing, KOLs and PR, now open to other brands.</span></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>02</b> / What we believe</span></div>
    <div class="svc">
      <article class="reveal"><span class="ix">01</span><h3>Test it on our own floor</h3><p class="muted">Nothing we recommend is theory. If it hasn’t survived a full Saturday at one of our venues, we don’t sell it to you.</p></article>
      <article class="reveal"><span class="ix">02</span><h3>Sincerity over spectacle</h3><p class="muted">Real food, real drinks, real conversations. Rooms people come back to on a Tuesday, not just photograph once.</p></article>
      <article class="reveal"><span class="ix">03</span><h3>Small roster, senior team</h3><p class="muted">We take on a few partner projects a year so the people who pitched are the people who deliver.</p></article>
      <article class="reveal"><span class="ix">04</span><h3>Commercial, not corporate</h3><p class="muted">We care about the numbers because we pay the rent too. We just don’t think a good night out should feel like a spreadsheet.</p></article>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>03</b> / The team</span><a href="/team/">Meet the team →</a></div>
    <h2 class="skip">The team behind Basho Projects</h2>
    {team_cards()}
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>04</b> / Our venues</span></div>
    {venue_rows()}
  </div>
</section>
""", image="/assets/img/bebop-room.jpg", schema=[ORG])

# ---------------------------------------------------------------- services

services_faq = [
    ("What does a hospitality consultant in Jakarta actually do?", "We help you decide what to open, where, and for whom; then we build the brand, menu, bar programme, team and systems, and launch it. You can hire us for all of it or one piece."),
    ("Do you only work on new openings?", "No. Some of our best work is on venues that are already open: a menu that isn’t selling, a launch that didn’t land, a team that keeps turning over, or marketing that isn’t filling tables."),
    ("How much does it cost?", "Three ways: a monthly retainer from IDR 20 million, a revenue-partner model where our fee moves with your results, or a fixed project fee for one defined job. Marketing-only packages through Bubble + Squeak start from USD 950 a month."),
    ("Do you work outside Jakarta?", "Our home is Senopati, but we work with brands across Indonesia and Southeast Asia where the project is a good fit."),
    ("Who will actually work on my project?", "The same senior team that runs BEBOP, BRIQ, The Bluebell and Brock. That’s why we only take on a few projects a year."),
]

page("/services/", "Restaurant & Bar Consultants in Jakarta | F&B Concept, Launch & Marketing | Basho Projects",
     "Hospitality and F&B consultants in Jakarta. Concept development, brand, menu and bar programmes, operations, launch and performance marketing, from the operators behind BEBOP, BRIQ and The Bluebell.",
     f"""
<section class="section">
  <div class="wrap">
    <span class="eyebrow">Services · F&B consultancy, Jakarta</span>
    <h1 style="font-size:clamp(52px,9vw,140px);max-width:13ch">We’ve made the mistakes <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">so you don’t have to.</span></h1>
    <div class="split" style="margin-top:40px">
      <p class="lede reveal">Restaurant, bar and hospitality consultancy from a team that runs its own venues in Senopati every night. Hire us for the whole build, or for the one problem you can’t solve internally.</p>
      <div class="btn-row reveal"><a class="btn btn--hot" href="#start">Start a project</a><a class="btn btn--line" href="#how">How it works</a></div>
    </div>
  </div>
</section>

<section class="section ink">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>01</b> / Three ways in</span></div>
    <h2 class="skip">Three ways to work with us</h2>
    <div class="offer">
      <div class="reveal"><span class="eyebrow">Full build</span><h3>Incubation</h3><p>From idea to opening night: concept, site, numbers, brand, menu, team, systems and launch. The playbook we used to open BRIQ and BEBOP.</p></div>
      <div class="reveal feat" style="background:#f2ede4;border-color:#f2ede4;color:#15130f"><span class="eyebrow">Get noticed</span><h3>Launch & marketing</h3><p style="color:#15130f">Pre-opening buzz, content, ads, KOLs and PR, run in-house by Bubble + Squeak Media. Built to fill tables, not just feeds.</p></div>
      <div class="reveal"><span class="eyebrow">Fix one thing</span><h3>Targeted help</h3><p>A menu that isn’t selling, a bar programme that needs a rethink, a team that keeps turning over. We come in, fix it, hand it back.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div><div class="sec-head" style="border:0;padding:0"><span class="no"><b>02</b> / What we do</span></div>
      <h2 style="font-size:clamp(36px,5vw,72px)">Everything a room needs to <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">work.</span></h2>
      <p class="muted">Tap a discipline to see what’s included.</p></div>
    <div class="reveal">{accordion()}</div>
  </div>
</section>

<section class="section ink" id="how">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>03</b> / How it works</span></div>
    <ol class="steps">
      <li><b>Listen</b><p>A coffee, a cocktail or a call. We learn the concept, the site, the budget and what you actually want out of it.</p></li>
      <li><b>Test</b><p>We pressure-test the idea against what we see on our own floors every night, and tell you straight if it won’t work.</p></li>
      <li><b>Build</b><p>Brand, menu, bar, team, systems and numbers, built alongside you with no black boxes or surprises.</p></li>
      <li><b>Launch & run</b><p>Opening, marketing and the first months of trading, until it runs without us.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>04</b> / Proof, not a portfolio</span></div>
    <h2 class="reveal" style="font-size:clamp(32px,4vw,60px);max-width:20ch;margin-bottom:40px">Our case studies have <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">opening hours.</span></h2>
    <div class="proof">
      <a class="reveal" href="/bebop/"><div class="ph">{img("bebop-hero.jpg", "BEBOP Bar + Kitchen")}</div><b>BEBOP Bar + Kitchen</b><span>Idea to open under our concept process, then a rebrand to match its crowd. Now a Senopati jazz and cocktail bar with 14 resident DJs.</span></a>
      <a class="reveal" href="/briq-bistro/"><div class="ph">{img("briq-room.jpg", "BRIQ Bistro")}</div><b>BRIQ Bistro</b><span>Positioned between fine and casual using our go-to-market playbook, with Meta, Google and KOL campaigns that turned first visits into regulars.</span></a>
      <a class="reveal" href="/the-bluebell/"><div class="ph">{img("bluebell-hall-night.jpg", "The Bluebell Public House")}</div><b>The Bluebell Public House</b><span>A modern British public house, from site and bar design to the drinks programme and launch.</span></a>
    </div>
  </div>
</section>

<section class="section ink">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>05</b> / Ways to pay</span></div>
    <div class="offer">
      <div class="reveal feat" style="background:#221f1a;border-color:#221f1a"><span class="eyebrow">Monthly retainer</span><div class="price">IDR 20jt+</div><p>Continuous, accountable support across brand, marketing and operations, from IDR 20 million a month.</p></div>
      <div class="reveal feat" style="background:#221f1a;border-color:#221f1a"><span class="eyebrow">Revenue partner</span><div class="price">% share</div><p>Our fee moves with your growth. Embedded with your team for long-term commercial alignment.</p></div>
      <div class="reveal feat" style="background:#221f1a;border-color:#221f1a"><span class="eyebrow">Project fee</span><div class="price">Fixed quote</div><p>One defined job — a concept, a menu, a bar programme or a launch — priced up front, delivered, handed back.</p></div>
    </div>
    <p class="muted" style="margin-top:24px">Marketing only? <a href="/bubbleandsqueakmedia/" style="color:inherit">Bubble + Squeak Media</a> packages start from USD 950 a month.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div><div class="sec-head" style="border:0;padding:0"><span class="no"><b>06</b> / FAQ</span></div><h2 style="font-size:clamp(32px,4vw,56px)">Before you ask</h2></div>
    <div>{faq_html(services_faq)}</div>
  </div>
</section>
<div id="start"></div>
""", image="/assets/img/bebop-hero.jpg", schema=[ORG, faq_schema(services_faq),
     {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Basho Projects — Hospitality Consulting",
      "url": f"{DOMAIN}/services/", "areaServed": ["Jakarta", "Indonesia", "Southeast Asia"],
      "serviceType": ["Restaurant consulting", "Bar consulting", "F&B concept development", "Hospitality marketing"],
      "parentOrganization": {"@type": "Organization", "name": "Basho Projects", "url": DOMAIN}}],
     enquiry="Work with us (services)")

# ---------------------------------------------------------------- invest

invest_faq = [
    ("Can I invest in a Basho Projects venue?", "We bring partners in on new concepts rather than selling stakes in existing venues by default. Tell us what you’re looking for and we’ll tell you honestly whether there’s a fit."),
    ("What kind of projects do you open?", "Bars, restaurants and food-led concepts with a clear point of view, mostly in and around Senopati and South Jakarta, where we know the streets, the landlords and the crowd."),
    ("Who runs the venue day to day?", "We do. Every project is operated by the Basho team, with the same systems, suppliers and marketing engine behind BEBOP, BRIQ and The Bluebell."),
    ("Where can I see the numbers?", "Projections, structure and terms are shared privately, project by project, once we’ve had a first conversation."),
]

page("/invest/", "Invest in Restaurants & Bars in Jakarta | Hospitality Investment | Basho Projects",
     "Looking to invest in hospitality in Jakarta? Basho Projects brings partners in on new bar and restaurant concepts in Senopati, operator-led by the team behind BEBOP, BRIQ and The Bluebell.",
     f"""
<section class="ghero" style="padding-bottom:clamp(56px,8vw,110px)">
  <div class="wrap">
    <span class="eyebrow">Invest · Hospitality in Jakarta</span>
    <h1 style="max-width:12ch">Back operators, <span class="serif">not just concepts.</span></h1>
    <div class="split" style="margin-top:28px">
      <p class="lede">Basho Projects opens a small number of new bars and restaurants and brings in partners for each one. You get a concept built and run by the people who already run four venues in Senopati, every night.</p>
      <div class="btn-row"><a class="btn btn--hot" href="#collaborate">Start a conversation</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>01</b> / Why partner with us</span></div>
    <h2 class="skip">Why partner with Basho Projects</h2>
    <div class="svc">
      <article class="reveal"><span class="ix">01</span><h3>We operate what we open</h3><p class="muted">No hand-off after launch. The team that designs the concept runs the floor, the bar, the kitchen and the marketing.</p></article>
      <article class="reveal"><span class="ix">02</span><h3>A neighbourhood we know</h3><p class="muted">Four venues within walking distance in Senopati: we know the streets, the landlords, the suppliers and the crowd that actually turns up.</p></article>
      <article class="reveal"><span class="ix">03</span><h3>Shared engine</h3><p class="muted">Group buying, our own butcher in Brock, a 14-strong DJ collective, an in-house marketing agency and proven programming formats from day one.</p></article>
      <article class="reveal"><span class="ix">04</span><h3>Built to last a decade</h3><p class="muted">We design rooms for regulars, not for one viral season. Concepts are made to be adaptable, scalable and repeatable.</p></article>
    </div>
  </div>
</section>

<section class="section ink">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>02</b> / How it works</span></div>
    <ol class="steps">
      <li><b>Intro</b><p>A first conversation about what you’re looking for: involvement, timeline and the kind of concept that excites you.</p></li>
      <li><b>The project</b><p>We share the concept, site and plan for an upcoming opening, privately and in detail.</p></li>
      <li><b>Structure</b><p>Terms are agreed project by project, with clear reporting and the operating team named up front.</p></li>
      <li><b>Open & run</b><p>We build, launch and operate. You get regular updates and a standing table.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>03</b> / The track record</span><a href="/our-projects/">All venues →</a></div>
    {venue_rows()}
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap split">
    <div><div class="sec-head" style="border:0;padding:0"><span class="no"><b>04</b> / FAQ</span></div><h2 style="font-size:clamp(32px,4vw,56px)">Investor questions</h2>
      <p class="muted">Projections and terms are only shared privately. Nothing on this page is an offer of investment.</p></div>
    <div>{faq_html(invest_faq)}</div>
  </div>
</section>
""", image="/assets/img/bluebell-hall-night.jpg", schema=[ORG, faq_schema(invest_faq)], enquiry="Invest or partner on a project")

# ---------------------------------------------------------------- contact

page("/contact/", "Contact Basho Projects | Jakarta Hospitality Group",
     "Get in touch with Basho Projects in Senopati, Jakarta: table bookings and private events, F&B consulting, investment and partnerships, press.",
     f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Contact</span>
      <h1 style="font-size:clamp(48px,7vw,104px)">Coffee, cocktails <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">or call.</span></h1>
      <p class="lede">Launching your first concept, reimagining a space, looking to invest, or just after a table? Tell us what you’re after and the right person will reply.</p>
      <ul class="facts">{"".join(f'<li><span>{n}</span><span><a href="{u}" target="_blank" rel="noopener">{num}</a></span></li>' for u, n, num in WA_LINES)}</ul>
      <p class="muted" style="margin-top:24px">PT Basho Projects Capital · Senopati, South Jakarta</p>
    </div>
    <div class="reveal">{contact_form()}</div>
  </div>
  <div class="wrap">
    <div class="sec-head" style="margin-top:72px"><span class="no"><b>Or</b> / book straight with a venue</span></div>
    <div class="contact-doors">
      {"".join(f'<a href="{VENUES[k]["path"]}">{img(VENUE_PHOTOS[k], VENUES[k]["name"], sizes="(max-width: 860px) 50vw, 25vw")}<span class="k">{VENUES[k]["tag"]}</span><span><b>{VENUES[k]["short"]} →</b></span></a>' for k in VENUE_ORDER)}
    </div>
  </div>
</section>
""", image="/assets/img/bebop-bar.jpg", with_collab=False, schema=[ORG])

# ---------------------------------------------------------------- venues index

page("/our-projects/", "Bars & Restaurants in Senopati, Jakarta | BEBOP, BRIQ, The Bluebell & Brock",
     "The bars, restaurants and food businesses Basho Projects runs in Senopati, South Jakarta: BEBOP Bar + Kitchen, BRIQ Bistro, The Bluebell Public House and Brock Butchery.",
     f"""
<section class="section ink">
  {marquee("Our venues *")}
  <div class="wrap">
    <h1 class="skip">Our bars and restaurants in Senopati</h1>
    <p class="lede reveal" style="max-width:44ch;margin-bottom:48px">Everything we recommend, we run ourselves. Four places within a few minutes’ walk of each other in Senopati, South Jakarta.</p>
    {venue_rows("h2")}
    <a class="vrow reveal" href="/bubbleandsqueakmedia/" style="text-decoration:none;--vc:#72a9d8">
      <span class="vrow__no">05</span><h2 style="font-size:clamp(28px,4vw,56px);margin:0">Bubble + Squeak</h2>
      <div class="vrow__meta"><span class="tag">Media agency</span>Performance marketing, KOLs and PR. The agency behind our own launches.</div>
      <div class="vrow__acts"><span class="pill">Visit</span></div>
    </a>
  </div>
</section>
""", image="/assets/img/bebop-bar.jpg")


# ---------------------------------------------------------------- team

page("/team/", "Our Team | The People Behind Basho Projects, Jakarta",
     "Meet the team behind Basho Projects in Senopati: Shawn Andrew (CEO), Dony Naibaho (CFO) and Samuel Joesoep (Brock).",
     f"""
<section class="section">
  <div class="wrap">
    <span class="eyebrow">The team</span>
    <h1 style="font-size:clamp(52px,9vw,140px);max-width:12ch">The people <span class="serif" style="font-family:var(--serif);font-weight:400">behind the rooms.</span></h1>
    <p class="lede" style="max-width:44ch;margin-top:20px">A small senior team that builds the venues, runs them every night, and shows up for the partner projects we take on.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <h2 class="skip">Leadership</h2>
    {team_cards()}
  </div>
</section>
<section class="section ink">
  <div class="wrap split split--center">
    <div class="reveal"><h2 style="font-size:clamp(34px,4.6vw,68px)">Behind every bar, <span class="serif" style="font-family:var(--serif);font-weight:400;color:var(--hot)">a bigger crew.</span></h2></div>
    <div class="reveal"><p class="lede">Bartenders, chefs, floor teams, our 14 resident DJs in the Bebop Music Collective and the Bubble + Squeak Media team make the nights happen.</p>
      <div class="btn-row"><a class="btn" href="/about/">Our story</a><a class="btn btn--line" href="https://www.linkedin.com/company/basho-projects/" target="_blank" rel="noopener">Basho on LinkedIn</a></div></div>
  </div>
</section>
""", image="/assets/img/bebop-room.jpg", schema=[ORG] + team_ld)

# ---------------------------------------------------------------- bubble + squeak (blue)

BS_SERVICES = [
    ("bs-icon-strategy.png", "Marketing strategy", "Plan what to run, when and where — with clarity. We build your full funnel from awareness to retention and guide key growth decisions alongside founders. Everything is data-led: pricing, offers and contribution, tracked against ROAS, CAC, LTV and payback. Scalable systems, not one-off campaigns."),
    ("bs-icon-creative.png", "Creative direction", "Brand identities that feel true and connect. Campaign ideas built to convert, not just look good — clear direction for ads, socials and shoots, with the right hooks, angles and messaging."),
    ("bs-icon-ads.png", "Advertising management", "Full-funnel management across Meta, Google and TikTok, top to bottom of funnel with clear KPI roles. Optimised for ROAS, CAC and CPA, with ongoing testing, smart budget allocation and retargeting that grows LTV."),
    ("bs-icon-pr.png", "PR & KOL management", "A curated network of vetted KOLs and creators across TikTok and Instagram, selected for reach, engagement and proven conversions. Campaigns built to scale and drive measurable awareness."),
]
bs_cards = "".join(f'<article class="reveal">{img(i, "")}<h3>{t}</h3><p class="muted">{d}</p></article>' for i, t, d in BS_SERVICES)
BS_CROSS = '<svg class="bs-cross" viewBox="0 0 100 100" aria-hidden="true"><path fill="#72a9d8" d="M50 4c9 0 14 8 14 18v14h14c10 0 18 5 18 14s-8 14-18 14H64v14c0 10-5 18-14 18s-14-8-14-18V64H22C12 64 4 59 4 50s8-14 18-14h14V22C36 12 41 4 50 4z"/></svg>'
bs_faq = [
    ("What does Bubble + Squeak Media do?", "Performance marketing and PR for F&B and lifestyle brands: Meta, Google and TikTok ads, KOL and creator campaigns, social content and creative direction."),
    ("Who is behind Bubble + Squeak?", "It’s the media agency of Basho Projects, the Jakarta hospitality group behind BEBOP, BRIQ and The Bluebell. We built it to market our own venues first."),
    ("How much does it cost?", "Packages start from USD 950 a month. Starter covers advertising or PR, Growth covers both, Enterprise is the full service."),
]

page("/bubbleandsqueakmedia/", "Bubble + Squeak Media | F&B Marketing, Ads & KOL Agency in Jakarta",
     "Bubble + Squeak Media is a Jakarta performance marketing and PR agency for F&B and lifestyle brands: Meta, Google and TikTok ads, KOLs, social content and creative strategy. From USD 950 a month.",
     f"""
<section class="section">
  <div class="wrap split split--center">
    <div class="reveal">
      <span class="mono">FROM IDEAS INTO PERFORMANCE!</span>
      <h1 style="margin-top:14px">Bubble<br>+Squeak<br>Media</h1>
      <p class="lede">We create, launch and optimise campaigns that actually work. No fluff — just smart marketing with results you can see.</p>
      <div class="btn-row"><a class="btn" href="#collaborate">Work with us</a><a class="btn btn--blue" href="https://www.instagram.com/bubblesqueakmedia/" target="_blank" rel="noopener">@bubblesqueakmedia</a></div>
    </div>
    <div class="reveal" style="display:grid;place-items:center">{BS_CROSS}</div>
  </div>
</section>
<section class="bs-strip">{marquee("Performance marketing + Influencer marketing + Social media production + Creative strategy & campaigns +")}</section>
<section class="section">
  <div class="wrap">
    <div class="split" style="margin-bottom:56px">
      <div class="reveal"><span class="mono">ABOUT</span><h2 style="margin-top:12px">A media agency by Basho Projects.</h2></div>
      <p class="reveal lede">We drive growth through performance marketing and strategic collaborations, combining data-led strategy with creative execution to deliver campaigns that are relevant, measurable and built to convert. We built it for our own venues first — now it’s open to yours.</p>
    </div>
    <span class="mono">WHAT WE DO</span>
    <div class="bs-grid" style="margin-top:16px">{bs_cards}</div>
  </div>
</section>
<section class="section dark">
  <div class="wrap split split--center">
    <div class="media media--wide reveal">{img("briq-case-study.webp", "BRIQ Bistro, Jakarta Selatan")}</div>
    <div class="reveal">
      <span class="mono" style="color:#72a9d8">CASE STUDY</span>
      <h2 style="margin-top:12px">BEBOP & BRIQ</h2>
      <h3 class="h4">What we did</h3>
      <ul class="ticks">
        <li>Ran Meta and Google Ads to drive awareness, traffic and bookings</li>
        <li>Optimised Google Business for strong local discovery</li>
        <li>Activated KOLs to reach relevant audiences and build cultural relevance</li>
        <li>Rebranded BEBOP to align with its evolving crowd and energy</li>
        <li>Built campaigns and events that turned guests into regulars</li>
      </ul>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <span class="mono">ADD-ONS</span>
    <ul class="chips reveal" style="margin-top:14px"><li>SEO + Google Business</li><li>Branding & graphic design</li><li>Web development</li><li>Social media marketing</li><li>Photo & video production</li></ul>
    <h2 style="margin-top:72px" class="reveal">From $950 USD / month</h2>
    <div class="grid-3" style="margin-top:32px">
      <div class="tier reveal"><h3>Starter</h3><p class="muted">Advertising or PR. Best for brands starting with performance marketing.</p></div>
      <div class="tier feat reveal"><h3>Growth</h3><p class="muted">Advertising and PR. For brands ready to scale.</p></div>
      <div class="tier reveal"><h3>Enterprise</h3><p class="muted">The full service. For brands that want full support.</p></div>
    </div>
    <div class="split" style="margin-top:72px">
      <div><span class="mono">FAQ</span><h2 style="margin-top:12px;font-size:clamp(28px,3.4vw,48px)">Good questions</h2></div>
      <div>{faq_html(bs_faq)}</div>
    </div>
  </div>
</section>
""", image="/assets/img/bubble-squeak-share.jpg", body_class="bs", schema=[faq_schema(bs_faq)], enquiry="Bubble + Squeak Media")


# ---------------------------------------------------------------- redirects & extras

for old, new in [("/home/", "/"), ("/about-us/", "/about/"), ("/bebop-1/", "/bebop/"),
                 ("/bebop-111/", "/bebop/"), ("/the-bluebell-x/", "/the-bluebell/"), ("/meet-the-team/", "/team/"),
                 ("/blog/blog-post-title-four-lr658-tcthp-7nadf-l6zw8/", "/blog/"), ("/blog/blog-post-title-one-3zaa9-zlxng-xbkmm-5ycan/", "/blog/")]:
    redirect(old, new)

home = (ROOT / "index.html").read_text()
main_inner = home.split('<main id="main">')[1].split("</main>")[0]
(ROOT / "404.html").write_text(home.replace(main_inner, """
<section class="section"><div class="wrap" style="min-height:50vh">
  <span class="eyebrow">404</span><h1>This page has closed <span class="serif">for the night.</span></h1>
  <p class="lede">It may have moved when we rebuilt the site.</p>
  <div class="btn-row"><a class="btn" href="/">Go home</a><a class="btn btn--ghost" href="/our-projects/">Our venues</a></div>
</div></section>
""").replace(home.split("<title>")[1].split("</title>")[0], "Page not found | Basho Projects")
    .replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"'))

pages = ["/", "/about/", "/team/", "/services/", "/invest/", "/contact/", "/our-projects/", "/bebop/", "/briq-bistro/",
         "/brock-butchery/", "/the-bluebell/", "/the-bluebell/food/", "/the-bluebell/private-rooms/", "/the-bluebell/football/", "/briq-bistro/food/", "/bebop/live-music/", "/bebop/kitchen/", "/bebop/trivia/", "/bebop/private-hire/", "/bubbleandsqueakmedia/", "/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT / "CNAME").write_text("www.bashoprojects.com\n")
(ROOT / ".nojekyll").write_text("")
print(f"Built {len(pages)} pages into {ROOT}")

#!/usr/bin/env python3
"""Builds the Basho Projects static site into ./site.

Every page shares one header, footer, contact block and newsletter popup, defined below.
Edit the content here, run `python3 build.py` (or `./deploy.sh` to publish).
"""
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent / "site"
DOMAIN = "https://www.bashoprojects.com"
# Fingerprint of the CSS/JS so browsers fetch fresh copies after every deploy
ASSET_V = hashlib.md5(b"".join((ROOT / "assets" / p).read_bytes() for p in
                              ["css/site.css", "css/group.css", "css/venue.css", "js/site.js"])).hexdigest()[:8]

# ---------------------------------------------------------------- shared data

WA_GROUP = "https://api.whatsapp.com/send/?phone=6285921219087"

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
        "hours_text": "Every day, 18:00 till late",
        "hours": EVERY_DAY([[18, 26]]),
        "late": True,
        "book": "https://api.whatsapp.com/send/?phone=628131847056",
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
        "hours_text": "Lunch 10:00–16:00 · Dinner 17:00–22:00",
        "hours": EVERY_DAY([[10, 16], [17, 22]]),
        "book": WA_GROUP,
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
        "schema_type": "Store",
    },
    "the-bluebell": {
        "name": "The Bluebell Public House",
        "short": "The Bluebell",
        "path": "/the-bluebell/",
        "tag": "British pub & chophouse · Senopati",
        "blurb": "Modern British public house and chophouse, Senopati. Owned and operated.",
        "card_img": "bluebell-bar.jpg",
        "address": "Jl. Tulodong Atas No. 10 A-B, Senopati, South Jakarta 12190",
        "street": "Jl. Tulodong Atas No. 10 A-B", "locality": "Senopati, South Jakarta",
        "postcode": "12190",
        "hours_text": "Mon–Thu 10:00–01:00 · Fri–Sun 10:00–02:00",
        "hours": {0: [[10, 26]], 1: [[10, 25]], 2: [[10, 25]], 3: [[10, 25]], 4: [[10, 25]], 5: [[10, 26]], 6: [[10, 26]]},
        "phone": "0821-4401-216", "tel": "+628214401216",
        "maps": "https://share.google/se4JQBoWzcS53Zwa8",
        "instagram": "https://www.instagram.com/atthebluebell/",
        "ig_handle": "@atthebluebell",
        "schema_type": "BarOrPub",
        "cuisine": "British",
    },
}
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
    <a class="logo" href="/" aria-label="Basho Projects home"><img src="/assets/img/basho-logo.png" alt="Basho Projects" width="160" height="46"></a>
    <button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
      <div class="nav-drop">
        <button aria-expanded="false">Venues</button>
        <ul><li><a href="/our-projects/">All venues</a></li>{drop}</ul>
      </div>
      <a href="/services/">Services</a>
      <a href="/invest/">Invest</a>
      <a href="/about/">About</a>
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
    venues = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="/"><img src="/assets/img/basho-logo.png" alt="Basho Projects" width="140" height="40" loading="lazy"></a>
        <p class="muted">Hospitality incubator, operator and consultancy.<br>Senopati, South Jakarta.</p>
        <form class="nl-inline" data-newsletter style="margin-top:18px"><label class="skip" for="ft-email">Email</label><input id="ft-email" type="email" name="email" placeholder="Join the guest list" required><button class="btn btn--light" type="submit">Join</button></form>
        <p class="nl__note muted" role="status" aria-live="polite" style="font-size:13px;margin-top:8px"></p>
      </div>
      <div><h5>Projects</h5><ul>{venues}</ul></div>
      <div><h5>Company</h5><ul><li><a href="/services/">Services</a></li><li><a href="/about/">About us</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div><h5>Follow</h5><ul><li><a href="{VENUES['bebop']['instagram']}" target="_blank" rel="noopener">BEBOP on Instagram</a></li><li><a href="{VENUES['briq-bistro']['instagram']}" target="_blank" rel="noopener">BRIQ on Instagram</a></li><li><a href="{VENUES['the-bluebell']['instagram']}" target="_blank" rel="noopener">The Bluebell on Instagram</a></li><li><a href="{WA_GROUP}" target="_blank" rel="noopener">WhatsApp us</a></li></ul></div>
    </div>
    <div class="legal"><span>© <span data-year>2026</span> PT Basho Projects Capital</span><span>Made in Senopati, Jakarta</span></div>
  </div>
</footer>"""


def page(path, title, description, main, image="/assets/img/briq-hero.jpg", with_collab=True,
         body_class="g", schema=None, enquiry=None):
    url = DOMAIN + path
    ld = ""
    for s in (schema or []):
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
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
<link rel="icon" href="/assets/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Instrument+Serif:ital@0;1&family=Space+Mono&family=Manrope:wght@400;500;600;700;800&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<link rel="stylesheet" href="/assets/css/group.css?v={ASSET_V}">
<link rel="stylesheet" href="/assets/css/venue.css?v={ASSET_V}">
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{ld}</head>
<body class="{body_class}">
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


def img(src, alt, cls="", lazy=True):
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{src}" alt="{escape(alt)}"{c}{load}>'


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
    "the-bluebell": {"values": ["Draught beer", "Ale", "Whisky", "Chophouse", "Six lines", "Cheers"],
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
  {img(image, alt, lazy=False)}
  <div class="wrap">
    <div class="vx-meta">{hours}<span class="eyebrow">A Basho Projects venue · Senopati</span></div>
    <h1 class="vx-name">{h1}</h1>
    <p class="sub">{sub}</p>
  </div>
</section>"""


def gallery(v, images):
    ex = VENUE_EXTRAS[VENUE_KEY_BY_SHORT[v["short"]]]
    pics = (list(images) + ex["more"])[:6]
    tiles = "".join(f'<figure class="reveal">{img(src, alt)}<figcaption>{alt}</figcaption></figure>' for src, alt in pics)
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
        rows.append(("Phone", f'<a href="tel:{v["tel"]}">{v["phone"]}</a>'))
    if v.get("instagram"):
        rows.append(("Instagram", f'<a href="{v["instagram"]}" target="_blank" rel="noopener">{v["ig_handle"]}</a>'))
    return '<ul class="facts">' + "".join(f"<li><span>{k}</span><span>{val}</span></li>" for k, val in rows) + "</ul>"


# BEBOP ---------------------------------------------------------------

v = VENUES["bebop"]
bebop_faq = [
    ("Where is BEBOP Bar + Kitchen?", "BEBOP is at Jl. Senopati No. 61, Kebayoran Baru, South Jakarta — a few minutes’ walk from BRIQ Bistro and The Bluebell, and close to SCBD."),
    ("Is there live music at BEBOP?", "Yes. Live jazz runs every Monday and Friday, curated by resident musician Bass G. Other nights bring resident DJs from the Bebop Music Collective, karaoke and trivia. Check Instagram for this week’s line-up."),
    ("What time does BEBOP open?", "Every day from 18:00 until late."),
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
    ("B3", "Events & private hire", "Birthdays, launches, takeovers", WA_GROUP),
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
      <div><em>Mon & Fri</em><b>Jazz Nights</b><span>Live jazz curated by Bass G, from standards to funk and groove.</span></div>
      <div><em>Weekly</em><b>Trivia Tuesdays</b><span>Teams, rounds, bragging rights.</span></div>
      <div><em>Weekly</em><b>Karaoke Nights</b><span>The mic is yours. Be brave.</span></div>
      <div><em>Weekly</em><b>BMC Nights</b><span>The Bebop Music Collective on the decks: house, future beats, jazz and soul.</span></div>
      <div><em>Weekly</em><b>Booty Groove</b><span>Late, loud and very much a dance floor.</span></div>
    </div>
    <p style="margin-top:28px"><a class="btn" href="/blog/jazz-at-bebop/">Read: Jazz at BEBOP</a></p>
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
{sisters("bebop")}
"""
page("/bebop/", "BEBOP Bar + Kitchen | Jazz & Cocktail Bar in Senopati, Jakarta",
     "BEBOP Bar + Kitchen: live jazz every Monday & Friday, DJs, cocktails and a modern Japanese kitchen at Jl. Senopati 61, South Jakarta. Open 18:00 till late. Book, menu & directions.",
     venue_page, image="/assets/img/bebop-hero.jpg", with_collab=False, body_class="venue v-bebop",
     schema=[venue_schema(v, "bebop-hero.jpg"), faq_schema(bebop_faq)])

# BRIQ ----------------------------------------------------------------

v = VENUES["briq-bistro"]
briq_faq = [
    ("Where is BRIQ Bistro?", "Jl. Prof. Joko Sutono SH No. 7B, Kebayoran Baru, South Jakarta — in the heart of Senopati, a short walk from BEBOP and The Bluebell."),
    ("What are BRIQ’s opening hours?", "Lunch and brunch from 10:00 to 16:00, dinner from 17:00 to 22:00."),
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
      <p>BRIQ Bistro is designed around authentic culinary traditions presented with clarity and restraint: quality ingredients, classic techniques, and balanced presentation. The dining experience feels both refined and approachable — casual enough for a relaxed brunch, polished enough for a memorable dinner.</p>
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
      <p>We don’t chase trends. We build lasting tables for good conversations — lunch, dinner, drinks, or just a place to catch your breath in Senopati.</p>
    </div>
    <div class="reveal">
      <span class="eyebrow">The menu</span>
      <h2>Soulful French food, <span class="serif">generous portions.</span></h2>
      <div class="lineup" style="grid-template-columns:1fr">
        <div><em>Lunch · from 10:00</em><b>Laid-back, full of flavour</b><span>Made for midday breaks and long catch-ups.</span></div>
        <div><em>Dinner · from 17:00</em><b>A little slower, a little warmer</b><span>Dinner packages make sharing easy, so you can sit back.</span></div>
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
      <div class="btn-row"><a class="btn" href="{v['book']}" target="_blank" rel="noopener">Book for steak frites</a><a class="btn btn--ghost" href="{v['menu']}" target="_blank" rel="noopener">See the menu</a></div>
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
      <h2>Brunch, lunch and dinner <span class="serif">in Senopati</span></h2>
      {facts(v)}
    </div>
    <div class="reveal"><h2 class="h3">Good to know</h2>{faq_html(briq_faq)}</div>
  </div>
</section>
{sisters("briq-bistro")}
"""
page("/briq-bistro/", "BRIQ Bistro | Steak Frites & French Bistro in Senopati, Jakarta",
     "BRIQ Bistro, Senopati: home of the steak frites, with weekly pasta promos, an approachable wine list and an outdoor terrace. Lunch from 10:00, dinner from 17:00. Book, menu & directions.",
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
    ("No.3", "Trade enquiries", "Restaurants, hotels, groups", WA_GROUP),
    ("No.4", "TikTok", "@brock.butchery", v["tiktok"]),
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
    ("What’s on tap?", "Draught beer, ale and whisky lead the bar, poured across six draught lines, alongside fine spirits and signature cocktails."),
    ("Is it a proper British pub?", "A modern one. The Bluebell is a British public house and chophouse: elevated British classics from the kitchen, a bar lounge, a dining hall, a snug and a private dining room."),
    ("Can I book the private dining room?", "Yes. The private dining room seats ten. Call or message us to book."),
]
venue_page = f"""
{vhero(v, "bluebell-facade.jpg", "The Bluebell Public House on Jl. Tulodong Atas, Senopati, at night",
       'The Bluebell <span class="serif">Public House</span>',
       "A modern British pub and chophouse in Senopati, South Jakarta. Draught beer, ale and whisky, poured across six lines.")}
{hub(v, "On tap", "Six lines · pour one", '<span class="beermat" aria-hidden="true">B</span>', [
    ("Line 1", "Book a table", f"Call {v['phone']}", f"tel:{v['tel']}"),
    ("Line 2", "Find the pub", "Jl. Tulodong Atas No. 10 A-B", v["maps"]),
    ("Line 3", "Instagram", v["ig_handle"], v["instagram"]),
    ("Line 4", "Private dining", "A room for ten", f"tel:{v['tel']}"),
    ("Line 5", "Our opening story", "From the Basho blog", "/blog/the-bluebell-public-house-opens-in-south-jakarta/"),
    ("Line 6", "Message the team", "WhatsApp", WA_GROUP),
], f'<span>{v["hours_text"]}</span><span>Cheers</span>')}

<section class="section">
  <div class="wrap split">
    <div class="media media--tall reveal">{img("bluebell-door.jpg", "The front door of The Bluebell Public House")}</div>
    <div class="reveal">
      <span class="eyebrow">The pub</span>
      <h2>Draught beer. Ale. <span class="serif">Whisky.</span></h2>
      <p>The Bluebell brings the social soul of the British pub to Senopati: a dimly lit, warm room where post-work drinks stretch into long, relaxed evenings. Thoughtfully elevated British classics from the kitchen; draught beer, ale and whisky at the bar, poured across six lines.</p>
      <p>Cosy nooks, a proper bar lounge, a dining hall and a private dining room — approachably premium and easy to enjoy, whether you’re in for a quick bite after work or settling in for a nightcap.</p>
      <p><a class="btn" href="/blog/the-bluebell-public-house-opens-in-south-jakarta/">Read the opening story</a></p>
    </div>
  </div>
</section>

<section class="section" style="border-top:1px solid var(--vline)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">The rooms</span>
      <h2>Pick your <span class="serif">corner.</span></h2>
      <ul class="facts">
        <li><span>Bar lounge</span><span>High stools, the long bar and six draught lines</span></li>
        <li><span>Dining hall</span><span>Banquettes, pendant lights and the chophouse menu</span></li>
        <li><span>The snug</span><span>A small room for a quiet pint</span></li>
        <li><span>Private dining room</span><span>Seats ten, for dinners and celebrations</span></li>
      </ul>
      <p class="muted" style="margin-top:18px">Room for about 95 seated and 140 standing for a full-pub booking.</p>
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
{sisters("the-bluebell")}
"""
page("/the-bluebell/", "The Bluebell Public House | British Pub & Chophouse in Senopati, South Jakarta",
     "The Bluebell Public House is a modern British pub and chophouse in Senopati, South Jakarta. Draught beer, ale and whisky across six lines, British classics, private dining. Open daily from 10:00.",
     venue_page, image="/assets/img/bluebell-facade.jpg", with_collab=False, body_class="venue v-bluebell",
     schema=[venue_schema(v, "bluebell-facade.jpg"), faq_schema(bluebell_faq)])

# ---------------------------------------------------------------- blog

BB = VENUES["the-bluebell"]
POSTS = [
    {
        "slug": "the-bluebell-public-house-opens-in-south-jakarta",
        "old": "/blog/the-bluebell-public-house-opens-in-south-jakarta-bringing-the-warmth-of-a-british-pub-to-senopati/",
        "title": "The Bluebell Public House Opens in South Jakarta, Bringing the Warmth of a British Pub to Senopati",
        "seo_title": "The Bluebell Public House Opens: A British Pub in Senopati, Jakarta",
        "date": "5 October 2026", "iso": "2026-10-05",
        "standfirst": "Raise a pint, British-style, at the newest pub in the heart of South Jakarta.",
        "cover": "bluebell-1.jpg",
        "body": f"""<figure>{img("bluebell-2.jpg", "Inside The Bluebell Public House, Senopati")}</figure>
<p><strong>Jakarta, 3 October 2026</strong> — The Bluebell Public House introduces a refined yet deeply welcoming slice of British pub culture to the heart of Senopati. Designed as a dimly lit, warm abode, the space pairs an elevated-casual dining experience with a curated drinks programme, making it the perfect setting for post-work unwinding and intimate catch-ups.</p>
<p>The concept captures the social soul of the traditional public house, offering cosy nooks where daytime conversations naturally stretch into long, relaxed evenings.</p>
<h2>British classics, draught beer and whisky</h2>
<p>The menu strikes a balance between comfort and sophistication, featuring thoughtfully elevated British classics alongside draught beers, fine spirits, and signature cocktails. Approachably premium and easy to enjoy, the food and drinks are crafted for any occasion — whether you are stopping by for a quick bite after office hours or settling in for a nightcap.</p>
<h2>A different kind of night out in Senopati</h2>
<p>Tucked into Senopati’s vibrant landscape, The Bluebell Public House offers a distinct alternative to the neighbourhood’s bustling dining scene, blending the timeless familiarity of pub culture into a contemporary Jakarta setting.</p>
<figure>{img("bluebell-1.jpg", "The bar at The Bluebell")}</figure>
<div class="box">
<h3 class="h4">About The Bluebell Public House</h3>
<p>The Bluebell Public House is a British-inspired pub in Senopati, South Jakarta. The concept brings together food, drinks, and a relaxed social atmosphere, drawing on the character of the British pub while making it its own in Jakarta.</p>
<h3 class="h4">Address + contact</h3>
<p>{BB["address"]}<br>Open {BB["hours_text"]}<br>Instagram: <a href="{BB["instagram"]}" target="_blank" rel="noopener">{BB["ig_handle"]}</a><br>Phone: <a href="tel:{BB["tel"]}">{BB["phone"]}</a></p>
</div>
<p><a class="btn" href="/the-bluebell/">Visit The Bluebell</a></p>""",
    },
    {
        "slug": "jazz-at-bebop",
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
    page(f"/blog/{p['slug']}/", f"{p['seo_title']} | Basho Projects", p["standfirst"], f"""
<section class="section"><article class="wrap article">
  <a href="/blog/" class="kicker" style="text-decoration:none">← Blog</a>
  <h1>{p['title']}</h1>
  <div class="meta">{p['date']} · Written by Thomas Brown</div>
  <p class="standfirst">{p['standfirst']}</p>
  {p['body']}
  {nav}
</article></section>""", image="/assets/img/" + p["cover"], with_collab=False, schema=[article_ld])
    redirect(p["old"], f"/blog/{p['slug']}/")

# ---------------------------------------------------------------- group pages (spliced into build.py)



VENUE_PHOTOS = {"bebop": "bebop-bar.jpg", "briq-bistro": "briq-hero.jpg", "brock-butchery": "brock-hero.jpg", "the-bluebell": "bluebell-bar.jpg"}
VENUE_COLOURS = {"bebop": "#ef4a2e", "briq-bistro": "#a3452c", "brock-butchery": "#6a6a2a", "the-bluebell": "#5b7fa6"}


def venue_rows(heading_tag="h3"):
    rows = []
    for i, key in enumerate(VENUE_ORDER, 1):
        v = VENUES[key]
        acts = [f'<a class="pill" href="{v["path"]}">View</a>']
        if v.get("book"):
            acts.append(f'<a class="pill" href="{v["book"]}" target="_blank" rel="noopener">Book</a>')
        elif v.get("tel"):
            acts.append(f'<a class="pill" href="tel:{v["tel"]}">Call to book</a>')
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
  <div class="vrow__peek" aria-hidden="true">{img(photo, '')}</div>
</div>""")
    return f'<div class="vrows">{"".join(rows)}</div>'


STAMP = """<svg class="stamp" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="c" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
<text><textPath href="#c">Operators first · Made in Senopati · Since BEBOP ·</textPath></text>
<circle cx="100" cy="100" r="34" fill="#e0482a"/><text x="100" y="106" text-anchor="middle" style="font-size:18px;letter-spacing:1px">BASHO</text></svg>"""

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
  <div class="reel">
    <a href="/bebop/">{img("bebop-bar.jpg", "BEBOP Bar + Kitchen", lazy=False)}<span>BEBOP</span></a>
    <a href="/briq-bistro/">{img("briq-hero.jpg", "BRIQ Bistro", lazy=False)}<span>BRIQ</span></a>
    <a href="/the-bluebell/">{img("bluebell-bar.jpg", "The Bluebell Public House", lazy=False)}<span>The Bluebell</span></a>
    <a href="/brock-butchery/">{img("brock-hero.jpg", "Brock Butchery")}<span>Brock</span></a>
    <a href="/bebop/#whats-on">{img("jazz-1.jpg", "Live jazz at BEBOP")}<span>Jazz nights</span></a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="no"><b>01</b> / Pick your door</span></div>
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
      <div class="reveal"><b>6</b><span>draught lines pouring at The Bluebell</span></div>
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
      <div><em>Every day · BRIQ</em><b>Steak frites & pasta promos</b><span>Home of the steak frites, plus a new pasta deal most weeks.</span><a href="/briq-bistro/#now-on">BRIQ →</a></div>
      <div><em>Every day · The Bluebell</em><b>The pub is open</b><span>From 10:00. Draught beer, ale, whisky and a proper chophouse menu.</span><a href="/the-bluebell/">The Bluebell →</a></div>
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
      <li><b>September 2026 · The Bluebell</b><span class="muted">A modern British public house and chophouse on Jl. Tulodong Atas, pouring across six draught lines.</span></li>
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
    <div class="sec-head"><span class="no"><b>03</b> / Our venues</span></div>
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
    <div class="offer">
      <div class="reveal"><span class="eyebrow">Full build</span><h3>Incubation</h3><p>From idea to opening night: concept, site, numbers, brand, menu, team, systems and launch. The playbook we used to open BRIQ and BEBOP.</p></div>
      <div class="reveal feat" style="background:var(--hot);border-color:var(--hot);color:#fff"><span class="eyebrow">Get noticed</span><h3>Launch & marketing</h3><p style="color:#fff">Pre-opening buzz, content, ads, KOLs and PR, run in-house by Bubble + Squeak Media. Built to fill tables, not just feeds.</p></div>
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
      <a class="reveal" href="/the-bluebell/"><div class="ph">{img("bluebell-hall-night.jpg", "The Bluebell Public House")}</div><b>The Bluebell Public House</b><span>A modern British pub and chophouse, from site and bar design to a six-line draught programme and launch.</span></a>
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
      <p><a class="btn" href="{WA_GROUP}" target="_blank" rel="noopener">Message us on WhatsApp</a></p>
      <p class="muted" style="margin-top:24px">PT Basho Projects Capital · Senopati, South Jakarta</p>
    </div>
    <div class="reveal">{contact_form()}</div>
  </div>
  <div class="wrap">
    <div class="sec-head" style="margin-top:72px"><span class="no"><b>Or</b> / book straight with a venue</span></div>
    <div class="contact-doors">
      {"".join(f'<a href="{VENUES[k]["path"]}">{img(VENUE_PHOTOS[k], VENUES[k]["name"])}<span class="k">{VENUES[k]["tag"]}</span><span><b>{VENUES[k]["short"]} →</b></span></a>' for k in VENUE_ORDER)}
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
""", image="/assets/img/briq-case-study.webp", body_class="bs", schema=[faq_schema(bs_faq)], enquiry="Bubble + Squeak Media")


# ---------------------------------------------------------------- redirects & extras

for old, new in [("/home/", "/"), ("/about-us/", "/about/"), ("/bebop-1/", "/bebop/"),
                 ("/bebop-111/", "/bebop/"), ("/the-bluebell-x/", "/the-bluebell/"), ("/meet-the-team/", "/about/")]:
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

pages = ["/", "/about/", "/services/", "/invest/", "/contact/", "/our-projects/", "/bebop/", "/briq-bistro/",
         "/brock-butchery/", "/the-bluebell/", "/bubbleandsqueakmedia/", "/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>2026-10-29</lastmod></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT / "CNAME").write_text("www.bashoprojects.com\n")
(ROOT / ".nojekyll").write_text("")
print(f"Built {len(pages)} pages into {ROOT}")

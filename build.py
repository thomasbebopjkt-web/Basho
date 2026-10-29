#!/usr/bin/env python3
"""Builds the Basho Projects static site into ./site.

Every page shares one header, footer, contact block and newsletter popup, defined below.
Edit the content here, run `python3 build.py` (or `./deploy.sh` to publish).
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent / "site"
DOMAIN = "https://www.bashoprojects.com"

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
        "blurb": "French bistro, Senopati. Crafted between fine and casual. Owned and operated.",
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
        "card_img": "bluebell-2.jpg",
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
        <button aria-expanded="false">Our Projects</button>
        <ul><li><a href="/our-projects/">All projects</a></li>{drop}</ul>
      </div>
      <a href="/services/">Services</a>
      <a href="/about/">About us</a>
      <a href="/blog/">Blog</a>
      <a class="btn" href="/contact/">Contact</a>
    </nav>
  </div>
</header>"""


def contact_form():
    return """<form class="form" data-contact novalidate>
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


def collaborate():
    return f"""<section class="section dark" id="collaborate">
  <div class="wrap split">
    <div class="reveal">
      <h2>Let’s <span class="serif">collaborate.</span></h2>
      <p>Whether you’re launching your first concept, reimagining an existing space, or looking for hands-on support across branding, operations, or experience design — we’d love to hear what you’re building.</p>
      <p>We tailor each collaboration to fit the needs of the project and the people behind it.</p>
      <p><strong>Let’s talk — coffee, cocktails, or call.</strong></p>
      <p class="muted">PT Basho Projects Capital<br>Senopati, South Jakarta</p>
    </div>
    <div class="reveal">{contact_form()}</div>
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
         body_class="", schema=None):
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
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700;800&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/site.js" defer></script>
{ld}</head>
<body class="{body_class}">
{header()}
<main id="main">
{main}
{collaborate() if with_collab else ""}
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


# ---------------------------------------------------------------- home

def venue_cards():
    out = []
    for key in VENUE_ORDER:
        v = VENUES[key]
        actions = [f'<a class="chip-btn" href="{v["path"]}">View venue</a>']
        if v.get("book"):
            actions.append(f'<a class="chip-btn" href="{v["book"]}" target="_blank" rel="noopener">Book a table</a>')
        if v.get("menu"):
            actions.append(f'<a class="chip-btn" href="{v["menu"]}" target="_blank" rel="noopener">Menu</a>')
        if v.get("tokopedia"):
            actions.append(f'<a class="chip-btn" href="{v["tokopedia"]}" target="_blank" rel="noopener">Order online</a>')
        if v.get("maps") and not v.get("menu"):
            actions.append(f'<a class="chip-btn" href="{v["maps"]}" target="_blank" rel="noopener">Directions</a>')
        pic = (f'<div class="vcard__img vcard__logo">{img(v["card_img"], v["name"])}</div>' if v.get("logo")
               else f'<div class="vcard__img" style="--pos:{v.get("card_pos", "center")}">{img(v["card_img"], v["name"] + ", " + v["tag"])}</div>')
        out.append(f"""<article class="vcard reveal">
  {pic}
  <div class="vcard__body">
    <span class="vcard__tag">{v["tag"]}</span>
    <h3><a href="{v["path"]}" style="text-decoration:none">{v["name"]}</a></h3>
    <p>{v["blurb"]}</p>
    <div class="vcard__actions">{"".join(actions)}</div>
  </div>
</article>""")
    return f'<div class="venue-cards">{"".join(out)}</div>'


def marquee(text):
    item = f"<span>{text}</span>" * 4
    return f'<div class="marquee" aria-hidden="true"><div class="marquee__track">{item}{item}</div></div>'


WHAT_WE_DO = {
    "Marketing & Launch": ["Go-to-market strategy", "Pre-opening buzz, soft launch, and events", "Content planning, reels, and visual direction", "Campaigns, promotions, and retention strategies"],
    "Project Development & Strategy": ["Concept validation and refinement", "Budgeting, forecasting, and P&L modelling", "Location sourcing and market fit", "Timeline management and roll-out planning"],
    "Operations & Systems": ["SOPs for FOH, bar, and kitchen", "Team structure, hiring, and onboarding", "POS, inventory, reservation, and rota setup", "Cost control, margin planning, and reporting systems"],
    "Creative & Brand Development": ["Naming and brand story", "Visual identity, voice, and narrative systems", "Spatial storytelling (uniforms, menus, playlists, sensory cues)"],
    "Menu Creation": ["Signature cocktails and dish development", "Menu costing, engineering, and workflow design", "Storytelling through menus (layout, format, copy)"],
    "Service & Culture": ["Guest journey mapping", "In-service rituals and team language", "Service training and floor flow testing", "Feedback systems and team retention"],
}


def accordion():
    items = "".join(
        f"<details><summary>{k}</summary><ul>{''.join(f'<li>{i}</li>' for i in v)}</ul></details>"
        for k, v in WHAT_WE_DO.items()
    )
    return f'<div class="accordion">{items}</div>'


page("/", "Basho Projects | Hospitality Group Behind BEBOP, BRIQ & The Bluebell, Jakarta",
     "Basho Projects is the Jakarta hospitality group behind BEBOP Bar + Kitchen, BRIQ Bistro, Brock Butchery and The Bluebell Public House in Senopati. Operators first, available to founders and brands.",
     f"""
<section class="hero">
  {img("briq-hero.jpg", "The open kitchen at BRIQ Bistro, Senopati", lazy=False)}
  <div class="wrap">
    <span class="eyebrow">Basho Projects · Senopati, Jakarta</span>
    <h1>We build hospitality brands in Jakarta. Some are ours. <span class="serif">Some are yours.</span></h1>
    <p>Owner operators behind BEBOP, BRIQ, Brock and The Bluebell. Available to founders and brands who want the same team on their project.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--light" href="/contact/">Start a project</a><a class="btn btn--ghost" href="#projects">Find a table</a></div>
  </div>
</section>

<section class="section dark">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Who we are</span>
      <h2>A collective of builders, operators, and creatives behind some of Jakarta’s most <span class="serif">distinct</span> hospitality concepts.</h2>
    </div>
    <div class="reveal">
      <p>Basho Projects is a hospitality incubator, operator and consultancy based in Jakarta. We help founders, operators and brands bring concepts to market with clarity, speed and commercial discipline.</p>
      <p>We run our own venues, which means every recommendation we make has already been tested against a roster, a rent cheque and a Saturday night service. We bring that same team to a small number of partner projects each year.</p>
      <p>Some partners want the whole build. Others want us on marketing alone, or on one problem they cannot solve internally. Both work.</p>
      <a class="btn btn--light" href="/about/">Learn more</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <span class="eyebrow">Our services</span>
    <h2 class="reveal">What we bring to <span class="serif">your</span> project</h2>
    <div class="grid-3" style="margin-top:48px">
      <article class="card reveal">{img("svc-gtm.jpg", "Team planning a restaurant launch")}<h3 class="h4">Go-to-Market Strategy</h3>
        <p>We define how a concept enters the market and how it wins once it is live. Positioning, audience definition, pricing strategy, launch planning, and channel selection — shaped by real operational insight in Jakarta and Southeast Asia. <em>The playbook we used to open BRIQ.</em></p></article>
      <article class="card reveal">{img("svc-brand.jpg", "Brand identity sketches")}<h3 class="h4">Brand, Advertising and PR</h3>
        <p>Brands designed to perform in the real world, not just online. Brand strategy, identity, messaging, content direction, advertising, and public relations — built for launch, growth, and consistency. <em>Run in-house by Bubble + Squeak Media.</em></p></article>
      <article class="card reveal">{img("svc-concept.jpg", "Chef in a restaurant dining room")}<h3 class="h4">Hospitality Concept Development</h3>
        <p>Restaurants, bars, cafés, and food-led retail developed from the ground up: concept definition, menu direction, service experience, layout logic, and supplier integration. <em>BEBOP went from idea to open under this process.</em></p></article>
    </div>
  </div>
</section>

<section class="section dark" id="projects">
  {marquee("Our Projects *")}
  <div class="wrap">
    <h2 class="skip">Our projects: bars, restaurants and a butcher in Senopati</h2>
    <p class="lede reveal" style="max-width:44ch;margin-bottom:48px">Four venues within walking distance in Senopati. A jazz bar, a French bistro, a British pub and a butcher that supplies our own kitchens.</p>
    {venue_cards()}
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <h2 style="font-weight:700">What We Do</h2>
      <p class="lede">We help hospitality businesses at every stage, from napkin sketch to full rollout — or reimagining something that’s already live.</p>
      <a class="btn" href="/services/">Learn more</a>
    </div>
    <div class="reveal">{accordion()}</div>
  </div>
</section>
""", schema=[ORG])

# ---------------------------------------------------------------- about

page("/about/", "About Basho Projects | Jakarta Hospitality Group & Operators",
     "Operators first. Meet the Jakarta hospitality group behind BEBOP, BRIQ Bistro, Brock Butchery and The Bluebell Public House in Senopati.",
     f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">About us</span>
      <h1>Who We <span class="serif">Are</span></h1>
      <p class="lede">A collective of builders, operators, and creatives behind some of Jakarta’s most distinct hospitality concepts.</p>
    </div>
    <div class="reveal">
      <p>We specialise in crafting brands that feel lived-in and loved — from naming and storytelling to service rituals, marketing plans, and operational systems. Every member of the team has been in the trenches, launching and running venues from the ground up.</p>
      <p>We are operators first. We run our own venues, and we take on a small number of partner projects each year, from full incubation to marketing alone.</p>
      <p>Our team is behind <a href="/bebop/">BEBOP</a>, a Japanese-American cocktail and music bar in Senopati; <a href="/briq-bistro/">BRIQ</a>, a bistro in South Jakarta crafted between fine and casual; <a href="/brock-butchery/">Brock Butchery</a>; and <a href="/the-bluebell/">The Bluebell Public House</a>.</p>
      <p>Together, we turn big ideas into grounded realities that work — emotionally and commercially.</p>
    </div>
  </div>
</section>
<section class="section--tight">
  <div class="wrap grid-3">
    <a class="media media--tall reveal" href="/bebop/">{img("bebop-room.jpg", "Inside BEBOP Bar + Kitchen, Senopati")}</a>
    <a class="media media--tall reveal" href="/briq-bistro/">{img("briq-room.jpg", "BRIQ Bistro dining room")}</a>
    <a class="media media--tall reveal" href="/the-bluebell/">{img("bluebell-1.jpg", "The bar at The Bluebell Public House")}</a>
  </div>
</section>
<section class="section dark">
  <div class="wrap grid-3">
    <div class="reveal"><h2 class="h3">Operators first</h2><p class="muted">Every recommendation has been tested on our own floors before it reaches yours.</p></div>
    <div class="reveal"><h2 class="h3">Small roster</h2><p class="muted">A handful of partner projects each year, so the senior team stays on yours.</p></div>
    <div class="reveal"><h2 class="h3">Whole build or one problem</h2><p class="muted">Full incubation, marketing alone, or the one thing you can’t solve internally.</p></div>
  </div>
</section>
""", image="/assets/img/bebop-room.jpg", schema=[ORG])

# ---------------------------------------------------------------- services

page("/services/", "Hospitality Consulting Services in Jakarta | Basho Projects",
     "Restaurant and bar consulting in Jakarta: concept development, brand, launch marketing, operations, menus and performance advertising, from a team that runs its own venues.",
     f"""
<section class="section">
  <div class="wrap split split--center">
    <div class="reveal">
      <span class="eyebrow">Services</span>
      <h1>What We <span class="serif">Do</span></h1>
      <p class="lede">Hands-on support from people who run venues of their own.</p>
      <a class="btn" href="/contact/">Contact us</a>
    </div>
    <div class="reveal">{accordion()}</div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <h2 class="reveal">Our Services</h2>
    <div class="grid-3" style="margin-top:48px">
      <article class="card reveal">{img("svc-creative.jpg", "Creative workshop")}<h3 class="h4">Creative & Brand Development</h3>
        <p class="muted">Powerful brands come from clarity, creativity, and connection. We study your vision, audience, and market, then craft positioning, messaging, visuals, and creative direction — so every touchpoint, voice to visuals, reflects your values and resonates with the people who matter.</p></article>
      <article class="card reveal">{img("svc-marketing.jpg", "Launch event")}<h3 class="h4">Marketing & Launch</h3>
        <p class="muted">We make launches memorable. Pre-opening buzz through timed content, partnerships, and creators; scroll-stopping reels and storytelling; then performance campaigns and retention tactics that turn first-time visitors into regulars.</p></article>
      <article class="card reveal">{img("svc-project.jpg", "Project planning")}<h3 class="h4">Project Development & Strategy</h3>
        <p class="muted">Ideas turned into scalable ventures. We validate concepts for market fit, give strategic clarity from feasibility to creative direction, build budgets, forecasts, and P&amp;L models, and help source the right location at the right time.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split split--center">
      <div class="reveal">
        <span class="eyebrow">Advertising & PR</span>
        <h2>We don’t chase clout. We engineer <span class="serif">cultural distribution.</span></h2>
        <p>From identifying the right creators to structuring content for paid amplification, we turn influencer attention into scalable growth. Run in-house by <a href="/bubbleandsqueakmedia/">Bubble + Squeak Media</a>.</p>
        <a class="btn" href="/contact/">Contact us</a>
      </div>
      <div class="media media--wide reveal">{img("adv-performance.jpg", "Campaign content on a phone")}</div>
    </div>
    <div class="grid-3" style="margin-top:72px">
      <article class="card reveal">{img("adv-influencer.jpg", "Creator filming content")}<h3 class="h4">Performance-Led. Brand-Driven.</h3><p>Together, we outline a path forward that’s realistic, strategic, and tailored to your specific needs.</p></article>
      <article class="card reveal">{img("adv-meta.jpg", "Social media advertising")}<h3 class="h4">Influencer & PR Strategy</h3><p>Creator selection, narrative development, content structuring and amplification — influencer frameworks that convert attention into measurable revenue.</p></article>
      <article class="card reveal">{img("svc-gtm.jpg", "Team reviewing campaign results")}<h3 class="h4">Meta Advertising</h3><p>Paid social that books tables, not just likes. You’re part of the process: communication stays open and decisions are shared — no black boxes, no surprises.</p></article>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <h2 class="reveal">Ways to work with us</h2>
    <div class="grid-2" style="margin-top:40px">
      <div class="price reveal"><div class="big">20JT+</div><h3 class="h4">Monthly Retainers</h3><p class="muted">Structured monthly retainers, from IDR 20 million, for continuous, accountable support across brand, marketing and operations.</p></div>
      <div class="price reveal"><div class="big">%</div><h3 class="h4">Revenue Partners</h3><p class="muted">A revenue-partner model aligned to growth and performance, embedded with your team for long-term commercial alignment.</p></div>
    </div>
    <p style="margin-top:40px"><a class="btn btn--light" href="/contact/">Partner today</a></p>
  </div>
</section>
""", image="/assets/img/svc-creative.jpg", with_collab=False)

# ---------------------------------------------------------------- contact

page("/contact/", "Contact Basho Projects | Jakarta Hospitality Group",
     "Launching a concept, reimagining a space, or need hands-on support? Talk to Basho Projects in Senopati, Jakarta — coffee, cocktails, or call.",
     f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Contact</span>
      <h1>Let’s talk — coffee, cocktails, <span class="serif">or call.</span></h1>
      <p>Whether you’re launching your first concept, reimagining an existing space, or looking for hands-on support across branding, operations, or experience design — we’d love to hear what you’re building.</p>
      <p>We tailor each collaboration to fit the needs of the project and the people behind it.</p>
      <p><a class="btn" href="{WA_GROUP}" target="_blank" rel="noopener">Message us on WhatsApp</a></p>
      <h2 class="h4" style="margin-top:40px">Looking for a table?</h2>
      <ul class="facts">
        {"".join(f'<li><span>{VENUES[k]["short"]}</span><span><a href="{VENUES[k]["path"]}">{VENUES[k]["tag"]} →</a></span></li>' for k in VENUE_ORDER)}
      </ul>
    </div>
    <div class="reveal">{contact_form()}</div>
  </div>
</section>
<section>
  <div class="media" style="max-height:70vh">{img("bebop-bar.jpg", "The bar at BEBOP Bar + Kitchen")}</div>
</section>
""", image="/assets/img/bebop-bar.jpg", with_collab=False, schema=[ORG])

# ---------------------------------------------------------------- our projects

page("/our-projects/", "Our Venues | BEBOP, BRIQ, Brock & The Bluebell | Basho Projects",
     "The bars, restaurants and businesses Basho Projects owns and operates in Senopati, Jakarta: BEBOP Bar + Kitchen, BRIQ Bistro, Brock Butchery, The Bluebell Public House and Bubble + Squeak Media.",
     f"""
<section class="section dark">
  {marquee("Our Projects *")}
  <div class="wrap">
    <h1 class="skip">Our projects</h1>
    <p class="lede reveal" style="max-width:44ch;margin-bottom:56px">Everything we recommend, we run ourselves. These are the venues and businesses we own and operate in Jakarta.</p>
    {venue_cards()}
    <a class="vcard reveal" href="/bubbleandsqueakmedia/" style="margin-top:40px;text-decoration:none;flex-direction:row;align-items:center">
      <div class="vcard__img vcard__logo" style="aspect-ratio:auto;width:40%;align-self:stretch;padding:24px">{img("bubble-squeak-logo.png", "Bubble + Squeak Media")}</div>
      <div class="vcard__body"><span class="vcard__tag">Performance marketing & PR</span><h3>Bubble + Squeak Media</h3><p>The agency behind our own launches, available to yours.</p></div>
    </a>
  </div>
</section>
""", image="/assets/img/bebop-bar.jpg")

# ---------------------------------------------------------------- venues


def hub(v, title, meta, deco, links, foot):
    ext = ' target="_blank" rel="noopener"'
    rows = "".join(
        f'<li><a href="{u}"{ext if u.startswith("http") else ""}>'
        f'<span class="hub__no">{n}</span><span><strong>{t}</strong><small>{s}</small></span>{ICONS["arrow"]}</a></li>'
        for n, t, s, u in links)
    return f"""<div class="wrap hub-wrap reveal">
  <nav class="hub" aria-label="{v['short']} quick links">
    <div class="hub__head">{deco}<span class="hub__title">{title}</span><span class="hub__meta">{meta}</span></div>
    <ol>{rows}</ol>
    <div class="hub__foot">{foot}</div>
  </nav>
</div>"""


def vhero(v, image, alt, h1, sub):
    hours = ""
    if v.get("hours"):
        late = ' data-late="1"' if v.get("late") else ""
        hours = f'<span class="status" data-hours=\'{json.dumps(v["hours"])}\'{late}>{v["hours_text"]}</span><br>'
    return f"""<section class="vhero">
  {img(image, alt, lazy=False)}
  <div class="wrap">
    {hours}<span class="eyebrow">A Basho Projects venue</span>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
  </div>
</section>"""


def gallery(v, images):
    tiles = "".join(f'<div>{img(src, alt)}</div>' for src, alt in images)
    ig = ""
    if v.get("instagram"):
        ig = f'<a class="ig" href="{v["instagram"]}" target="_blank" rel="noopener">More on Instagram<small>{v["ig_handle"]}</small></a>'
    elif v.get("tiktok"):
        ig = f'<a class="ig" href="{v["tiktok"]}" target="_blank" rel="noopener">More on TikTok<small>@brock.butchery</small></a>'
    return f'<div class="gallery">{tiles}{ig}</div>'


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
    ("What kind of food does BRIQ serve?", "Soulful French bistro classics — quality ingredients and classic technique, presented with clarity and restraint. Casual enough for brunch, polished enough for a proper dinner."),
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
page("/briq-bistro/", "BRIQ Bistro | French Bistro & Brunch in Senopati, Jakarta",
     "BRIQ Bistro is a French bistro in Senopati, South Jakarta: brunch and lunch from 10:00, dinner from 17:00, an approachable wine list and an outdoor terrace. Book, menu & directions.",
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
<section class="section">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Good to know</span><h2>Ordering <span class="serif">meat</span> in Jakarta</h2>
      <p class="muted">Brock is developed and operated by Basho Projects. It started as a solution to a problem in our own kitchens and became a business of its own.</p></div>
    <div class="reveal">{faq_html(brock_faq)}</div>
  </div>
</section>
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
{vhero(v, "bluebell-2.jpg", "The dining hall at The Bluebell Public House, Senopati",
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
    <div class="media media--tall reveal">{img("bluebell-1.jpg", "The bar at The Bluebell Public House")}</div>
    <div class="reveal">
      <span class="eyebrow">The pub</span>
      <h2>Draught beer. Ale. <span class="serif">Whisky.</span></h2>
      <p>The Bluebell brings the social soul of the British pub to Senopati: a dimly lit, warm room where post-work drinks stretch into long, relaxed evenings. Thoughtfully elevated British classics from the kitchen; draught beer, ale and whisky at the bar, poured across six lines.</p>
      <p>Cosy nooks, a proper bar lounge, a dining hall and a private dining room — approachably premium and easy to enjoy, whether you’re in for a quick bite after work or settling in for a nightcap.</p>
      <p><a class="btn" href="/blog/the-bluebell-public-house-opens-in-south-jakarta/">Read the opening story</a></p>
    </div>
  </div>
</section>

<section class="section--tight"><div class="wrap">{gallery(v, [("bluebell-painting.jpg", "Bluebell wildflower painting in the pub"), ("bluebell-2.jpg", "The Bluebell dining hall"), ("bluebell-painting-2.jpg", "Artwork at The Bluebell")])}</div></section>

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
page("/the-bluebell/", "The Bluebell Public House | British Pub in Senopati, South Jakarta",
     "The Bluebell Public House is a modern British pub and chophouse in Senopati, South Jakarta. Draught beer, ale and whisky across six lines, British classics, private dining. Open daily from 10:00.",
     venue_page, image="/assets/img/bluebell-2.jpg", with_collab=False, body_class="venue v-bluebell",
     schema=[venue_schema(v, "bluebell-2.jpg"), faq_schema(bluebell_faq)])

# ---------------------------------------------------------------- bubble + squeak

BS_SERVICES = [
    ("bs-icon-strategy.png", "Marketing Strategy", "Plan what to run, when, and where — with clarity. We build your full funnel from awareness to retention and guide key growth decisions alongside founders. Everything is data-led: pricing, offers and contribution, tracked against ROAS, CAC, LTV and payback. Scalable systems, not one-off campaigns."),
    ("bs-icon-creative.png", "Creative Direction", "Brand identities that feel true and connect. Campaign ideas built to convert, not just look good — clear direction for ads, socials and shoots, with the right hooks, angles and messaging."),
    ("bs-icon-ads.png", "Advertising Management", "Full-funnel management across Meta, Google and TikTok, TOF to BOF with clear KPI roles. Optimised for ROAS, CAC and CPA, with ongoing testing, smart budget allocation and retargeting that grows LTV."),
    ("bs-icon-pr.png", "PR & KOL Management", "A curated network of vetted KOLs and creators across TikTok and Instagram, selected for reach, engagement and proven conversions. Campaigns built to scale and drive measurable awareness."),
]
bs_cards = "".join(
    f'<article class="bs-service reveal">{img(i, "")}<h3>{t}</h3><p class="muted">{d}</p></article>'
    for i, t, d in BS_SERVICES)

page("/bubbleandsqueakmedia/", "Bubble + Squeak Media | F&B Marketing & PR Agency, Jakarta",
     "Bubble + Squeak Media is Basho Projects' performance marketing and PR agency for F&B brands in Jakarta: Meta, Google and TikTok ads, KOLs, creative direction and strategy. From $950/month.",
     f"""
<section class="section">
  <div class="wrap split split--center">
    <div class="reveal">
      <span class="eyebrow">Performance · PR</span>
      <h1>From ideas into <span class="serif">performance.</span></h1>
      <p class="lede">We create, launch, and optimise campaigns that actually work. No fluff — just smart marketing with results you can see.</p>
      <a class="btn" href="/contact/">Work with us</a>
    </div>
    <div class="reveal">{img("bubble-squeak-logo.png", "Bubble + Squeak Media")}</div>
  </div>
</section>
<section class="bs-strip">{marquee("Performance marketing · Influencer marketing · Social media production · Creative strategy & campaign ·")}</section>
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal"><span class="eyebrow">About</span><h2>A media agency by Basho Projects.</h2></div>
      <p class="reveal lede">We drive growth through performance marketing and strategic collaborations, combining data-led strategy with creative execution to deliver campaigns that are relevant, measurable, and built to convert.</p>
    </div>
    <div class="grid-2" style="margin-top:72px">{bs_cards}</div>
  </div>
</section>
<section class="section dark">
  <div class="wrap split split--center">
    <div class="media media--wide reveal">{img("briq-case-study.webp", "BRIQ Bistro, Jakarta Selatan")}</div>
    <div class="reveal">
      <span class="eyebrow">Case study</span>
      <h2>BEBOP & BRIQ</h2>
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
    <span class="eyebrow">Add-ons</span>
    <ul class="chips reveal"><li>SEO + Google Business</li><li>Branding & Graphic Design</li><li>Web Development</li><li>Social Media Marketing</li><li>Photo & Video Production</li></ul>
    <h2 style="margin-top:72px" class="reveal">Starting from $950 USD / month</h2>
    <div class="grid-3" style="margin-top:32px">
      <div class="tier reveal"><h3>Starter</h3><p class="muted">Advertising or PR. Best for brands starting with performance marketing.</p></div>
      <div class="tier reveal"><h3>Growth</h3><p class="muted">Advertising and PR. For brands ready to scale.</p></div>
      <div class="tier reveal"><h3>Enterprise</h3><p class="muted">The full service. For brands that want full support.</p></div>
    </div>
    <p style="margin-top:40px"><a class="btn" href="/contact/">Book an appointment</a></p>
  </div>
</section>
""", image="/assets/img/briq-case-study.webp", body_class="bs")

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

cards = "".join(f"""<a class="post-card reveal" href="/blog/{p['slug']}/">
  {img(p['cover'], '')}
  <div class="meta">{p['date']} · Thomas Brown</div>
  <h2 class="h3">{p['title']}</h2>
</a>""" for p in POSTS)

page("/blog/", "Blog | News from BEBOP, BRIQ & The Bluebell | Basho Projects",
     "News and stories from Basho Projects and its venues in Senopati, Jakarta: openings, live jazz at BEBOP and more.",
     f"""<section class="section"><div class="wrap">
  <span class="eyebrow">Blog</span><h1 style="margin-bottom:56px">News from <span class="serif">the group</span></h1>
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

pages = ["/", "/about/", "/services/", "/contact/", "/our-projects/", "/bebop/", "/briq-bistro/",
         "/brock-butchery/", "/the-bluebell/", "/bubbleandsqueakmedia/", "/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>2026-10-29</lastmod></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT / "CNAME").write_text("www.bashoprojects.com\n")
(ROOT / ".nojekyll").write_text("")
print(f"Built {len(pages)} pages into {ROOT}")

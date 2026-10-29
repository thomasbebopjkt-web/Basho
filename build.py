#!/usr/bin/env python3
"""Builds the Basho Projects static site into ./site.

Every page shares one header, footer and contact block, defined below.
Edit the content here, run `python3 build.py`, then commit the `site` folder.
"""
from pathlib import Path

ROOT = Path(__file__).parent / "site"
DOMAIN = "https://www.bashoprojects.com"

# ---------------------------------------------------------------- shared data

WA_GROUP = "https://api.whatsapp.com/send/?phone=6285921219087"

VENUES = [
    ("BEBOP Bar + Kitchen", "/bebop/"),
    ("BRIQ Bistro", "/briq-bistro/"),
    ("Brock Butchery", "/brock-butchery/"),
    ("The Bluebell Public House", "/the-bluebell/"),
    ("Bubble + Squeak Media", "/bubbleandsqueakmedia/"),
]

# The Bluebell's public details live in one place so they are easy to change.
BLUEBELL = {
    "address": "Jl. Tulodong Atas No. 10 A-B, Senopati, South Jakarta 12190",
    "maps": "https://share.google/se4JQBoWzcS53Zwa8",
    "instagram": "https://www.instagram.com/atthebluebell/",
    "phone": "0821-4401-216",
    "hours": "10:00–01:00 Monday to Thursday · 10:00–02:00 Friday to Sunday",
}


def header():
    drop = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in VENUES)
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


def contact_form(dark=True):
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
      <h2>Let’s Collaborate!</h2>
      <p>Whether you’re launching your first concept, reimagining an existing space, or looking for hands-on support across branding, operations, or experience design — we’d love to hear what you’re building.</p>
      <p>We tailor each collaboration to fit the needs of the project and the people behind it.</p>
      <p><strong>Let’s talk — coffee, cocktails, or call.</strong></p>
      <p class="muted">PT Basho Projects Capital<br>Senopati, South Jakarta</p>
    </div>
    <div class="reveal">{contact_form()}</div>
  </div>
</section>"""


def footer():
    venues = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in VENUES)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="/"><img src="/assets/img/basho-logo.png" alt="Basho Projects" width="140" height="40"></a>
        <p class="muted">Hospitality incubator, operator and consultancy.<br>Senopati, South Jakarta.</p>
      </div>
      <div><h5>Projects</h5><ul>{venues}</ul></div>
      <div><h5>Company</h5><ul><li><a href="/services/">Services</a></li><li><a href="/about/">About us</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div><h5>Talk to us</h5><ul><li><a href="{WA_GROUP}" target="_blank" rel="noopener">WhatsApp</a></li><li><a href="/contact/">Enquiry form</a></li></ul></div>
    </div>
    <div class="legal"><span>© <span data-year>2026</span> PT Basho Projects Capital</span><span>Jakarta, Indonesia</span></div>
  </div>
</footer>"""


def page(path, title, description, main, image="/assets/img/briq-hero.jpg", with_collab=True, body_class=""):
    url = DOMAIN + path
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Basho Projects">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}{image}">
<meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="/assets/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/site.js" defer></script>
</head>
<body class="{body_class}">
{header()}
<main id="main">
{main}
{collaborate() if with_collab else ""}
</main>
{footer()}
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
    load = ' loading="lazy" decoding="async"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{src}" alt="{alt}"{c}{load}>'


def link_tiles(links):
    tiles = "".join(
        f'<a href="{u}" target="_blank" rel="noopener"><small>{k}</small><strong>{v} →</strong></a>'
        for k, v, u in links
    )
    return f'<div class="venue-links">{tiles}</div>'


# ---------------------------------------------------------------- home

PROJECT_CARDS = [
    ("brock-butchery", "Brock Butchery", "Premium meat, delivered. Owned and operated.", "brock-logo.png", True),
    ("bebop", "BEBOP Bar + Kitchen", "Listening bar and cocktails, Senopati. Owned and operated.", "bebop-bar.jpg", False),
    ("the-bluebell", "The Bluebell Public House", "Modern British public house, Senopati. Owned and operated.", "bluebell-painting.jpg", False),
    ("briq-bistro", "BRIQ Bistro", "French bistro, Senopati. Owned and operated.", "briq-hero.jpg", False),
]


def projects_grid(cards=PROJECT_CARDS):
    out = []
    for slug, name, blurb, image, contain in cards:
        out.append(f"""<a class="project reveal" href="/{slug}/">
  <div class="project__img">{img(image, name, "contain" if contain else "")}</div>
  <h4>{name}</h4><p class="muted">{blurb}</p>
</a>""")
    return f'<div class="projects">{"".join(out)}</div>'


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


page("/", "Basho Projects | Hospitality Brands Built in Jakarta",
     "Owner operators behind BEBOP, BRIQ, Brock and The Bluebell. A hospitality incubator, operator and consultancy in Jakarta.",
     f"""
<section class="hero">
  {img("briq-hero.jpg", "", lazy=False)}
  <div class="wrap">
    <h1>We build hospitality brands in Jakarta. Some are ours. Some are yours.</h1>
    <p>Owner operators behind BEBOP, BRIQ, Brock and The Bluebell. Available to founders and brands who want the same team on their project.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--light" href="/contact/">Start a project</a><a class="btn btn--ghost" href="/our-projects/">See our venues</a></div>
  </div>
</section>

<section class="section dark">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">Who we are</span>
      <h2>A collective of builders, operators, and creatives behind some of Jakarta’s most distinct hospitality concepts.</h2>
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
    <h2 class="muted reveal">Our Services</h2>
    <div class="grid-3" style="margin-top:48px">
      <article class="card reveal">{img("svc-gtm.jpg", "Team planning a launch")}<h4>Go-to-Market Strategy</h4>
        <p>We define how a concept enters the market and how it wins once it is live. Positioning, audience definition, pricing strategy, launch planning, and channel selection — shaped by real operational insight in Jakarta and Southeast Asia. <em>The playbook we used to open BRIQ.</em></p></article>
      <article class="card reveal">{img("svc-brand.jpg", "Brand sketches on paper")}<h4>Brand, Advertising and PR</h4>
        <p>Brands designed to perform in the real world, not just online. Brand strategy, identity, messaging, content direction, advertising, and public relations — built for launch, growth, and consistency. <em>Run in-house by Bubble + Squeak Media.</em></p></article>
      <article class="card reveal">{img("svc-concept.jpg", "Chef smiling in a restaurant")}<h4>Hospitality Concept Development</h4>
        <p>Restaurants, bars, cafés, and food-led retail developed from the ground up: concept definition, menu direction, service experience, layout logic, and supplier integration. <em>BEBOP went from idea to open under this process.</em></p></article>
    </div>
  </div>
</section>

<section class="section dark" id="projects">
  {marquee("Our Projects *")}
  <div class="wrap">{projects_grid()}</div>
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
""")

# ---------------------------------------------------------------- about

page("/about/", "About | Basho Projects",
     "Operators first. The team behind BEBOP, BRIQ, Brock and The Bluebell in Senopati, Jakarta.",
     f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">About us</span>
      <h1>Who We Are</h1>
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
    <div class="media media--tall reveal">{img("bebop-room.jpg", "BEBOP Bar + Kitchen")}</div>
    <div class="media media--tall reveal">{img("briq-room.jpg", "BRIQ Bistro dining room")}</div>
    <div class="media media--tall reveal">{img("bluebell-1.jpg", "The Bluebell Public House")}</div>
  </div>
</section>
<section class="section dark">
  <div class="wrap grid-3">
    <div class="reveal"><h3>Operators first</h3><p class="muted">Every recommendation has been tested on our own floors before it reaches yours.</p></div>
    <div class="reveal"><h3>Small roster</h3><p class="muted">A handful of partner projects each year, so the senior team stays on yours.</p></div>
    <div class="reveal"><h3>Whole build or one problem</h3><p class="muted">Full incubation, marketing alone, or the one thing you can’t solve internally.</p></div>
  </div>
</section>
""", image="/assets/img/bebop-room.jpg")

# ---------------------------------------------------------------- services

page("/services/", "Services | Basho Projects",
     "Creative and brand development, marketing and launch, project development and strategy, advertising and PR for hospitality brands in Jakarta.",
     f"""
<section class="section">
  <div class="wrap split split--center">
    <div class="reveal">
      <span class="kicker">Services</span>
      <h1>What We Do</h1>
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
      <article class="card reveal">{img("svc-creative.jpg", "Creative workshop")}<h4>Creative & Brand Development</h4>
        <p class="muted">Powerful brands come from clarity, creativity, and connection. We study your vision, audience, and market, then craft positioning, messaging, visuals, and creative direction — so every touchpoint, voice to visuals, reflects your values and resonates with the people who matter.</p></article>
      <article class="card reveal">{img("svc-marketing.jpg", "Launch event")}<h4>Marketing & Launch</h4>
        <p class="muted">We make launches memorable. Pre-opening buzz through timed content, partnerships, and creators; scroll-stopping reels and storytelling; then performance campaigns and retention tactics that turn first-time visitors into regulars.</p></article>
      <article class="card reveal">{img("svc-project.jpg", "Project planning")}<h4>Project Development & Strategy</h4>
        <p class="muted">Ideas turned into scalable ventures. We validate concepts for market fit, give strategic clarity from feasibility to creative direction, build budgets, forecasts, and P&amp;L models, and help source the right location at the right time.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split split--center">
      <div class="reveal">
        <span class="kicker">Advertising & PR</span>
        <h2>We don’t chase clout. We engineer cultural distribution.</h2>
        <p>From identifying the right creators to structuring content for paid amplification, we turn influencer attention into scalable growth. Run in-house by <a href="/bubbleandsqueakmedia/">Bubble + Squeak Media</a>.</p>
        <a class="btn" href="/contact/">Contact us</a>
      </div>
      <div class="media media--wide reveal">{img("adv-performance.jpg", "Campaign content on a phone")}</div>
    </div>
    <div class="grid-3" style="margin-top:72px">
      <article class="card reveal">{img("adv-influencer.jpg", "Creator filming content")}<h4>Performance-Led. Brand-Driven.</h4><p>Together, we outline a path forward that’s realistic, strategic, and tailored to your specific needs.</p></article>
      <article class="card reveal">{img("adv-meta.jpg", "Social media advertising")}<h4>Influencer & PR Strategy</h4><p>Creator selection, narrative development, content structuring and amplification — influencer frameworks that convert attention into measurable revenue.</p></article>
      <article class="card reveal">{img("svc-gtm.jpg", "Team reviewing campaign results")}<h4>Meta Advertising</h4><p>You’re part of the process. Communication stays open and decisions are shared — no black boxes, no surprises.</p></article>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <h2 class="reveal">Ways to work with us</h2>
    <div class="grid-2" style="margin-top:40px">
      <div class="price reveal"><div class="big">20JT+</div><h4>Monthly Retainers</h4><p class="muted">Structured monthly retainers for continuous, accountable support across brand, marketing and operations.</p></div>
      <div class="price reveal"><div class="big">%</div><h4>Revenue Partners</h4><p class="muted">A revenue-partner model aligned to growth and performance, embedded with your team for long-term commercial alignment.</p></div>
    </div>
    <p style="margin-top:40px"><a class="btn btn--light" href="/contact/">Partner today</a></p>
  </div>
</section>
""", image="/assets/img/svc-creative.jpg", with_collab=False)

# ---------------------------------------------------------------- contact

page("/contact/", "Contact | Basho Projects",
     "Launching a concept, reimagining a space, or need hands-on support? Talk to Basho Projects in Jakarta.",
     f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">Contact</span>
      <h1>Let’s talk — coffee, cocktails, or call.</h1>
      <p>Whether you’re launching your first concept, reimagining an existing space, or looking for hands-on support across branding, operations, or experience design — we’d love to hear what you’re building.</p>
      <p>We tailor each collaboration to fit the needs of the project and the people behind it.</p>
      <p><a class="btn" href="{WA_GROUP}" target="_blank" rel="noopener">Message us on WhatsApp</a></p>
      <ul class="facts" style="margin-top:32px">
        <li><span>Company</span><span>PT Basho Projects Capital</span></li>
        <li><span>Based in</span><span>Senopati, South Jakarta</span></li>
      </ul>
    </div>
    <div class="reveal">{contact_form(dark=False)}</div>
  </div>
</section>
<section>
  <div class="media" style="max-height:70vh">{img("bebop-bar.jpg", "BEBOP Bar + Kitchen")}</div>
</section>
""", image="/assets/img/bebop-bar.jpg", with_collab=False)

# ---------------------------------------------------------------- our projects

page("/our-projects/", "Our Projects | Basho Projects",
     "Venues and businesses owned and operated by Basho Projects: BEBOP, BRIQ Bistro, Brock Butchery, The Bluebell and Bubble + Squeak Media.",
     f"""
<section class="section dark">
  {marquee("Our Projects *")}
  <div class="wrap">
    <p class="lede reveal" style="max-width:40ch;margin-bottom:56px">Everything we recommend, we run ourselves. These are the venues and businesses we own and operate in Jakarta.</p>
    {projects_grid(PROJECT_CARDS + [("bubbleandsqueakmedia", "Bubble + Squeak Media", "Performance marketing and PR agency. Owned and operated.", "bubble-squeak-logo.png", True)])}
  </div>
</section>
""", image="/assets/img/bebop-bar.jpg")

# ---------------------------------------------------------------- venues


def venue(path, name, title, description, hero, heading, sub, links, tagline, body_html, side_img, attribution, facts=None):
    facts_html = ""
    if facts:
        facts_html = '<ul class="facts" style="margin-top:28px">' + "".join(
            f"<li><span>{k}</span><span>{v}</span></li>" for k, v in facts) + "</ul>"
    page(path, title, description, f"""
<section class="hero hero--short hero--left">
  {img(hero, name, lazy=False)}
  <div class="wrap">
    <span class="kicker">A Basho Projects venue</span>
    <h1>{heading}</h1>
    <p>{sub}</p>
  </div>
</section>
<section class="dark section--tight">
  <div class="wrap">{link_tiles(links)}</div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="media media--tall reveal">{img(side_img, name)}</div>
    <div class="reveal">
      <p class="tagline">{tagline}</p>
      {body_html}
      {facts_html}
      <p class="muted" style="margin-top:28px;font-size:14px">{attribution}</p>
    </div>
  </div>
</section>
""", image="/assets/img/" + hero)


venue("/bebop/", "BEBOP Bar + Kitchen", "BEBOP Bar + Kitchen | Basho Projects",
      "An intimate listening bar and cocktail concept in Senopati, Jakarta, developed and operated by Basho Projects.",
      "bebop-hero.jpg", "BEBOP Bar + Kitchen", "An intimate listening bar and cocktail concept, where sound, cocktails and atmosphere work together as one experience.",
      [("Reservations", "Book now", "https://api.whatsapp.com/send/?phone=628131847056"),
       ("Menu", "Food + drinks", "https://drive.google.com/file/d/1fVueKjI0878L3gZe2G2E3yK-eqkakVwX/view"),
       ("Social", "Instagram", "https://www.instagram.com/bebop.wav/"),
       ("Find us", "Google Maps", "https://share.google/71emNbci6KrwuVk7n")],
      "Social. Modern. Soulful. BEBOP.",
      """<p>BEBOP is designed as a place to slow down. Music is treated as a central element rather than background noise, with vinyl selections and curated playlists setting the rhythm of the room throughout the night.</p>
<p>The cocktail programme is built on balance and clarity, favouring timeless recipes executed with intention. Drinks are designed to complement the space rather than dominate it, supporting long conversations and repeat visits.</p>
<p>Inspired by Japanese listening bars and classic cocktail culture, BEBOP focuses on restraint, detail and mood rather than volume or trend-driven theatrics — carefully curated music, considered lighting, and a service style that values presence and precision.</p>
<p>Live jazz runs every Monday and Friday. <a href="/blog/jazz-at-bebop/">Read about Jazz at BEBOP →</a></p>""",
      "bebop-detail.jpg", "BEBOP Bar + Kitchen is developed and operated by Basho Projects.")

venue("/briq-bistro/", "BRIQ Bistro", "BRIQ Bistro | Basho Projects",
      "BRIQ is a refined French bistro in South Jakarta, crafted between fine and casual. Developed and operated by Basho Projects.",
      "briq-room.jpg", "BRIQ Bistro", "Crafted between fine and casual. The precision and technique of fine dining with the warmth and ease of a neighbourhood bistro.",
      [("Reservations", "Book now", WA_GROUP),
       ("Menu", "Food + drinks", "https://drive.google.com/file/d/14s5RP07lYSFB83LDFETMX9C2kJ7qXe4m/view"),
       ("Social", "Instagram", "https://www.instagram.com/briqbistro/"),
       ("Find us", "Google Maps", "https://maps.app.goo.gl/oVa2PtMUAXVPxSpC8")],
      "Organic. Human. Eclectic. Raw. Fine-casual.",
      """<p>BRIQ is designed around authentic culinary traditions presented with clarity and restraint: quality ingredients, classic techniques, and balanced presentation. Casual enough for a relaxed brunch, polished enough for a memorable dinner.</p>
<p>Created for Jakarta’s growing dining audience — diners who appreciate quality behind the plate, a warm room, and genuine hospitality.</p>
<ul class="ticks">
<li>Refined yet approachable French cooking in a bistro setting</li>
<li>Positioned between fine dining and casual dining</li>
<li>Design that balances comfort with elevated details</li>
<li>Consistency backed by Basho Projects’ operating systems</li>
</ul>
<p>Also on <a href="https://www.tiktok.com/@briqbistro" target="_blank" rel="noopener">TikTok</a>.</p>""",
      "briq-detail.jpg", "BRIQ Bistro is developed and operated by Basho Projects.")

venue("/brock-butchery/", "Brock Butchery", "Brock Butchery | Basho Projects",
      "Premium meat for Jakarta, whether you are cooking for four or for four hundred. Order direct or set up trade supply.",
      "brock-hero.jpg", "Brock Butchery", "Crafted cuts, handled with care. Premium meat for Jakarta, whether you are cooking for four or for four hundred.",
      [("Enquiries", "WhatsApp", WA_GROUP),
       ("Order", "Tokopedia", "https://www.tokopedia.com/brock-butchery"),
       ("Order", "Shopee", "https://shopee.co.id/brockbutchery"),
       ("Social", "TikTok", "https://www.tiktok.com/@brock.butchery")],
      "Honest. Elevated. Accessible. Straightforward. Grounded.",
      """<h4>For your kitchen</h4>
<p>Order direct through Tokopedia or Shopee and have it delivered. Clear labelling, honest descriptions, cuts portioned the way you actually cook them. No trade account, no minimum order, no jargon you need a chef to translate.</p>
<h4>For the professional kitchen</h4>
<p>Consistent supply and spec, with a team that understands what a missed delivery does to a service. We supply restaurants, hotels and hospitality groups across Jakarta and Indonesia, including our own. Brock supplies BRIQ Bistro — as we are our own customer, if the quality slips we are the first to know.</p>""",
      "brock-cuts.jpg", "Brock is developed and operated by Basho Projects, the team behind BEBOP and BRIQ. It started as a solution to a problem in our own kitchens and became a business of its own.")

venue("/the-bluebell/", "The Bluebell Public House", "The Bluebell Public House | Basho Projects",
      "A modern British public house and chophouse in Senopati, South Jakarta. Draught beer, ale and whisky across six lines.",
      "bluebell-2.jpg", "The Bluebell Public House", "A modern British public house and chophouse in Senopati, South Jakarta.",
      [("Social", "Instagram", BLUEBELL["instagram"]),
       ("Find us", "Google Maps", BLUEBELL["maps"]),
       ("Call", BLUEBELL["phone"], "tel:+628214401216"),
       ("Read", "Opening story", "/blog/the-bluebell-public-house-opens-in-south-jakarta/")],
      "Draught beer. Ale. Whisky.",
      """<p>The Bluebell brings the social soul of the British pub to Senopati: a dimly lit, warm room where post-work drinks stretch into long, relaxed evenings. Thoughtfully elevated British classics from the kitchen; draught beer, ale and whisky at the bar, poured across six lines.</p>
<p>Cosy nooks, a proper bar lounge, a dining hall and a private dining room — approachably premium and easy to enjoy, whether you’re in for a quick bite after work or settling in for a nightcap.</p>""",
      "bluebell-1.jpg", "The Bluebell is developed and operated by Basho Projects.",
      facts=[("Address", BLUEBELL["address"]), ("Hours", BLUEBELL["hours"])])

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

page("/bubbleandsqueakmedia/", "Bubble + Squeak Media | Basho Projects",
     "Bubble + Squeak Media is Basho Projects' performance marketing and PR agency: Meta, Google and TikTok ads, KOLs, creative direction and strategy.",
     f"""
<section class="section">
  <div class="wrap split split--center">
    <div class="reveal">
      <span class="kicker">Performance · PR</span>
      <h1>From ideas into performance.</h1>
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
      <div class="reveal"><span class="kicker">About</span><h2>A media agency by Basho Projects.</h2></div>
      <p class="reveal lede">We drive growth through performance marketing and strategic collaborations, combining data-led strategy with creative execution to deliver campaigns that are relevant, measurable, and built to convert.</p>
    </div>
    <div class="grid-2" style="margin-top:72px">{bs_cards}</div>
  </div>
</section>
<section class="section dark">
  <div class="wrap split split--center">
    <div class="media media--wide reveal">{img("briq-case-study.webp", "BRIQ Bistro, Jakarta Selatan")}</div>
    <div class="reveal">
      <span class="kicker">Case study</span>
      <h2>BEBOP & BRIQ</h2>
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
    <span class="kicker">Add-ons</span>
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

POSTS = [
    {
        "slug": "the-bluebell-public-house-opens-in-south-jakarta",
        "old": "/blog/the-bluebell-public-house-opens-in-south-jakarta-bringing-the-warmth-of-a-british-pub-to-senopati/",
        "title": "The Bluebell Public House Opens in South Jakarta — Bringing the Warmth of a British Pub to Senopati",
        "date": "5 October 2026",
        "standfirst": "Raise a pint, British-style, at the newest pub in the heart of South Jakarta.",
        "cover": "bluebell-1.jpg",
        "body": f"""<figure>{img("bluebell-2.jpg", "Inside The Bluebell Public House")}</figure>
<p><strong>Jakarta, 3 October 2026</strong> — The Bluebell Public House introduces a refined yet deeply welcoming slice of British pub culture to the heart of Senopati. Designed as a dimly lit, warm abode, the space pairs an elevated-casual dining experience with a curated drinks programme, making it the perfect setting for post-work unwinding and intimate catch-ups.</p>
<p>The concept captures the social soul of the traditional public house, offering cosy nooks where daytime conversations naturally stretch into long, relaxed evenings.</p>
<p>The menu strikes a balance between comfort and sophistication, featuring thoughtfully elevated British classics alongside draught beers, fine spirits, and signature cocktails. Approachably premium and easy to enjoy, the food and drinks are crafted for any occasion — whether you are stopping by for a quick bite after office hours or settling in for a nightcap.</p>
<p>Tucked into Senopati’s vibrant landscape, The Bluebell Public House offers a distinct alternative to the neighbourhood’s bustling dining scene, blending the timeless familiarity of pub culture into a contemporary Jakarta setting.</p>
<figure>{img("bluebell-1.jpg", "The bar at The Bluebell")}</figure>
<div class="box">
<h4>About The Bluebell Public House</h4>
<p>The Bluebell Public House is a British-inspired pub in Senopati, South Jakarta. The concept brings together food, drinks, and a relaxed social atmosphere, drawing on the character of the British pub while making it its own in Jakarta.</p>
<h4>Address + contact</h4>
<p>{BLUEBELL["address"]}<br>Instagram: <a href="{BLUEBELL["instagram"]}" target="_blank" rel="noopener">@atthebluebell</a><br>Phone: <a href="tel:+628214401216">{BLUEBELL["phone"]}</a></p>
</div>""",
    },
    {
        "slug": "jazz-at-bebop",
        "old": "/blog/wpdv5ufmcja78usx0i0q62bosubba8/",
        "title": "Jazz at BEBOP Creates Moments That Don’t Happen Twice",
        "date": "15 September 2026",
        "standfirst": "Each week, a live jazz night you don’t want to miss.",
        "cover": "jazz-2.jpg",
        "body": f"""<figure>{img("jazz-1.jpg", "Live jazz at BEBOP Bar + Kitchen")}</figure>
<p><strong>Jakarta, 15 September 2026</strong> — What started as a weekly fixture for the city’s music lovers has grown into one of Jakarta’s go-to stages for jazz that truly feels alive.</p>
<p>The programme at BEBOP is curated by Bass G, resident jazz curator and musician, who oversees the line-ups and musical direction. Each night shows a different side of jazz — from traditional playing to funk, groove and more modern sounds — unpredictable enough to keep the audience coming back for a different vibe each time, and never less than a good time.</p>
<p>Jazz at BEBOP is rooted in the belief that it is not just about playing great music, but about creating an experience where the audience feels involved. “We want musicians to have room to be themselves and interact with the audience,” says Bass G. “The programme tries to show that jazz can be energetic, fun, and accessible, rather than something that has to feel distant or overly serious.” Come to listen attentively, or have a drink, talk, and enjoy the music without needing to understand jazz beforehand.</p>
<p>Over the past year, BEBOP’s stage has hosted some of Indonesia’s most respected names in jazz and beyond, including Dewa Budjana, Barry Likumahuwa and Sandhy Sandoro — a line-up that reflects BEBOP’s commitment to bringing serious musicianship into an intimate, unpretentious setting.</p>
<p>Jazz nights run every Monday and Friday, featuring a rotating cast of local musicians alongside occasional special guests.</p>
<figure>{img("jazz-2.jpg", "The crowd at Jazz at BEBOP")}</figure>
<p><a class="btn" href="/bebop/">Visit BEBOP</a></p>""",
    },
]

cards = "".join(f"""<a class="post-card reveal" href="/blog/{p['slug']}/">
  {img(p['cover'], '')}
  <div class="meta">{p['date']} · Thomas Brown</div>
  <h3>{p['title']}</h3>
</a>""" for p in POSTS)

page("/blog/", "Blog | Basho Projects", "News and stories from Basho Projects and its venues in Senopati, Jakarta.",
     f"""<section class="section"><div class="wrap">
  <span class="kicker">Blog</span><h1 style="margin-bottom:56px">News from the group</h1>
  <div class="posts">{cards}</div>
</div></section>""", image="/assets/img/" + POSTS[0]["cover"])

for i, p in enumerate(POSTS):
    prev_p = POSTS[i - 1] if i > 0 else None
    next_p = POSTS[i + 1] if i + 1 < len(POSTS) else None
    nav = '<nav class="post-nav">'
    nav += f'<a href="/blog/{prev_p["slug"]}/"><small>Newer</small>{prev_p["title"]}</a>' if prev_p else "<span></span>"
    nav += f'<a href="/blog/{next_p["slug"]}/" style="text-align:right"><small>Older</small>{next_p["title"]}</a>' if next_p else ""
    nav += "</nav>"
    page(f"/blog/{p['slug']}/", f"{p['title']} | Basho Projects", p["standfirst"], f"""
<section class="section"><article class="wrap article">
  <a href="/blog/" class="kicker" style="text-decoration:none">← Blog</a>
  <h1>{p['title']}</h1>
  <div class="meta">{p['date']} · Written by Thomas Brown</div>
  <p class="standfirst">{p['standfirst']}</p>
  {p['body']}
  {nav}
</article></section>""", image="/assets/img/" + p["cover"], with_collab=False)
    redirect(p["old"], f"/blog/{p['slug']}/")

# ---------------------------------------------------------------- redirects & extras

for old, new in [("/home/", "/"), ("/about-us/", "/about/"), ("/bebop-1/", "/bebop/"),
                 ("/bebop-111/", "/bebop/"), ("/the-bluebell-x/", "/the-bluebell/"), ("/meet-the-team/", "/about/")]:
    redirect(old, new)

(ROOT / "404.html").write_text((ROOT / "index.html").read_text().replace(
    (ROOT / "index.html").read_text().split('<main id="main">')[1].split("</main>")[0],
    """
<section class="section"><div class="wrap" style="min-height:50vh">
  <span class="kicker">404</span><h1>This page has closed for the night.</h1>
  <p class="lede">It may have moved when we rebuilt the site.</p>
  <div class="btn-row"><a class="btn" href="/">Go home</a><a class="btn btn--ghost" href="/our-projects/">Our projects</a></div>
</div></section>
""").replace("<title>Basho Projects | Hospitality Brands Built in Jakarta</title>", "<title>Page not found | Basho Projects</title>"))

pages = ["/", "/about/", "/services/", "/contact/", "/our-projects/", "/bebop/", "/briq-bistro/",
         "/brock-butchery/", "/the-bluebell/", "/bubbleandsqueakmedia/", "/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{DOMAIN}{p}</loc></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT / "CNAME").write_text("www.bashoprojects.com\n")
(ROOT / ".nojekyll").write_text("")
print(f"Built {len(pages)} pages into {ROOT}")

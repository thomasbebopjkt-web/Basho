# bashoprojects.com — site audit (29 October 2026)

Audit of the old Squarespace site, with Google Search Console data for the last 3 months
(28 Jul – 28 Oct 2026). Every issue listed is fixed in the new GitHub Pages build unless marked **Open**.

## What the search data says

| Page | Impressions | Clicks | CTR | Avg. position |
|---|---|---|---|---|
| /bebop | 18,483 | 59 | **0.32%** | 8.3 |
| /the-bluebell | 2,525 | 51 | 2.0% | 5.5 |
| Bluebell launch post | 1,549 | 38 | 2.5% | 3.5 |
| / (home) | 1,099 | 177 | 16.1% | 2.5 |
| /briq-bistro | — | — | — | not in report |
| /brock-butchery | 1 | 0 | — | — |

- **/bebop is the main opportunity.** It's shown for generic bar searches but almost nobody clicks, because the old page's title and opening copy were about BRIQ, not BEBOP.
- Biggest search terms we appear for but don't win: *bar senopati* (686), *bar di senopati* (427), *bar jakarta* (301), *bar jakarta selatan* (267), *jazz bar jakarta* (241), *club senopati* (205), *live music senopati* (134), *bebop bar + kitchen menu* (61), *karaoke senopati* (45), *british pub jakarta* (40).
- People misspell BEBOP a lot: *bop, bebob, bibop, bepop, beebop*. Google handles these once the brand page is strong; no keyword stuffing needed.
- 85% of impressions are on mobile, so the link hub at the top of each venue page is built for phones first.
- BRIQ and Brock barely appear in search at all.

## Site-wide issues

| Issue on old site | Fix |
|---|---|
| Several H1s per page (home had 5); headings used for styling, not structure | Exactly one H1 per page; sections use H2/H3 in order |
| Generic page titles ("Transform Your Hospitality Brand Today") and no venue-specific descriptions | Keyword-led title and meta description on every page (e.g. "BEBOP Bar + Kitchen \| Jazz & Cocktail Bar in Senopati, Jakarta") |
| All images had empty alt text | Descriptive alt text on every content image |
| No structured data | Organization, BarOrPub / Restaurant / Store (address, hours, menu, Instagram), FAQPage and BlogPosting schema |
| Squarespace's social links pointed to instagram.com/squarespace and facebook.com/squarespace | Footer links to each venue's real Instagram |
| Duplicate and orphan pages: /about-us, /bebop-1, /bebop-111, /the-bluebell-x, /home | Redirect to the right page |
| /meet-the-team was template filler with fake staff ("Monet Goode", "Emmett Marsh") | Removed; redirects to About |
| Blog post URL was a random string (/blog/wpdv5ufmcja78usx0i0q62bosubba8) | /blog/jazz-at-bebop/ (old URL redirects) |
| No newsletter capture | "Join the guest list" popup (once per visitor) plus a footer sign-up |
| No way to see if a venue is open | Live "Open now · until 01:00" badge on each venue, in Jakarta time |

## Page by page

### Home
- Broken italics in service blurbs: "Th e playbook we used to open BRIQ", "B ebop went from idea to open under this proces s" — fixed.
- The Bluebell project card had no caption — added.
- "Our Projects" was an H1 twice — now a single section heading, and each venue card has Union-style actions: **View venue · Book a table · Menu**.

### About
- The whole "Who Are We" block appeared twice — de-duplicated.
- "Who Are We" → "Who We Are".
- Only mentioned BEBOP and BRIQ — now names all four venues with links.

### Services
- Opening paragraph was Squarespace placeholder copy ("…ensure your consulting needs are met with precision") — removed.
- "Meta Advertising" card had a heading and no description — written.
- "20JT+" was unexplained — now "from IDR 20 million".

### Contact
- "Let's talk, coffee, cocktails, or call." appeared twice — once now.
- Added "Looking for a table?" links to each venue, since diners land here too.

### BEBOP (/bebop)
- **The page opened with BRIQ's content**, and its title read "BRIQ Bistro: Crafted Between Fine and Casual". That explains the 0.32% CTR. Now it's all BEBOP.
- Bottom links pointed to Brock's Tokopedia and Shopee and BRIQ's Instagram, with Brock's "solution to a problem in our own kitchens" sign-off — removed.
- No address or hours anywhere — added (Jl. Senopati No. 61, 18:00 till late).
- New: a "What's on" weekly line-up (Jazz Mon & Fri, Trivia Tuesdays, Karaoke, BMC Nights, Booty Groove) aimed at *live music senopati*, *jazz bar jakarta* and *karaoke senopati*.
- New: FAQ (where, live music, hours, booking, food) with FAQ schema.

### BRIQ Bistro
- No address or hours — added (Jl. Prof. Joko Sutono SH No. 7B; 10:00–16:00, 17:00–22:00).
- Mentions the terrace, wine list and Brock supply; FAQ added for *french bistro jakarta* / *brunch senopati*.

### Brock Butchery
- Instagram link went to BRIQ's account — removed (**Open:** send Brock's Instagram handle).
- FAQ added (how to order, trade supply).

### The Bluebell
- Page opened with BRIQ's content — now Bluebell only.
- "Opens on 20 September 2026" was out of date — now reads as open.
- Address, hours, phone and private dining added; FAQ targets *british pub jakarta*, *bluebell public house south jakarta*, *bar scbd*.

### Bubble + Squeak Media
- Typos: "campaigns that actually works", "What we did it", "Bor brands ready to scale" — fixed.

### Blog posts
- Bluebell post's phone number linked to a Google search results page — now a tap-to-call link.
- "South Jakarta— Bringing" spacing; posts now have H2 subheadings, a pull quote, and links back to the venue page.

## Design changes
- **Venue pages are link hubs.** Big tap targets directly under the hero, each themed to the venue:
  - BEBOP: a record-sleeve "Tracklist" (A1–B3) with a spinning vinyl.
  - BRIQ: a French "La Carte" with dotted menu leaders (Réserver, La carte, Nous trouver).
  - Brock: butcher's tags, "Today's cuts".
  - The Bluebell: "On tap", Line 1–6, a nod to the six draught lines.
- Each venue has its own palette (BEBOP red on black, BRIQ terracotta on cream, Brock olive on paper, Bluebell navy and brass).
- An italic serif accent (Instrument Serif) alongside the existing Manrope/Poppins, for a less corporate, more F&B feel.
- Section order and copy tone kept as they were.

## Open items
1. **Brock's Instagram handle** — not known; the old link went to BRIQ.
2. **Weekly line-up days** — only Jazz (Mon & Fri) is confirmed; the other nights show as "Weekly". Send the days and they go in.
3. **BRIQ hours by day** — shown as every day; confirm if it closes on any day.
4. **Instagram photos** — Instagram blocks logged-out downloading, so none were pulled. Drop extra photos into `site/assets/img/` and they can go into each venue's gallery.
5. **Form and newsletter delivery** — without a form service, sign-ups open WhatsApp. Add a free Formspree endpoint in `site/assets/js/site.js` to receive them by email.
6. **Google Business Profiles** — point each venue's website link at its new page (e.g. bashoprojects.com/bebop/) to send search traffic straight to the right venue.

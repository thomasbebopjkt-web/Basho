# Basho Projects website

Static rebuild of www.bashoprojects.com, hosted on GitHub Pages instead of Squarespace.

## Editing

- Page copy, links and venue details live in `build.py`. The Bluebell's address, map link, phone and hours sit in the `BLUEBELL` block at the top.
- Styles: `site/assets/css/site.css`. Behaviour (menu, contact form): `site/assets/js/site.js`.
- Images: `site/assets/img/`.

After editing, rebuild and preview:

```bash
python3 build.py
python3 -m http.server 8080 --directory site
```

Then open http://localhost:8080. To publish, run `./deploy.sh`: it rebuilds, pushes `main`, and pushes the `site` folder to the `gh-pages` branch that GitHub Pages serves.

## Contact form

Contact-form enquiries and guest-list sign-ups are emailed to laskarbebop@gmail.com and thomasbebopjakarta@gmail.com. Add Web3Forms access keys to `WEB3FORMS_KEYS` in `site/assets/js/site.js` (one per inbox); until then FormSubmit is used, with WhatsApp as the fallback.

## Promos ("Now on")

Each venue page shows promo cards from `promos.json` right under its link hub. Edit that file (title, text, button, image, optional `until` date) and run `./deploy.sh`. Expired promos hide themselves.

## WiFi landing pages

Point each venue's WiFi captive portal at its page with `?wifi`, e.g. `https://www.bashoprojects.com/bebop/?wifi`. Guests get a welcome bar and the guest-list sign-up after 4 seconds, tagged "WiFi at BEBOP" in the email.
To receive enquiries by email instead, create a free form at https://formspree.io and paste its endpoint into
`FORM_ENDPOINT` at the top of `site/assets/js/site.js`.

## Going live (one-time)

1. Run `./deploy.sh`.
2. Repo → Settings → Pages → Source: **Deploy from a branch**, branch `gh-pages`, folder `/ (root)`.
3. Settings → Pages → Custom domain: `www.bashoprojects.com` (also in `site/CNAME`), then tick **Enforce HTTPS** once it's available.
4. At your domain registrar (Squarespace Domains if the domain was bought there), change DNS:
   - `www` → CNAME → `<your-github-username>.github.io`
   - apex `@` → A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Remove the old Squarespace `www` CNAME and A records.
5. Once the new site is live, cancel the Squarespace website plan, but keep the domain registration if it's held there.

Old Squarespace URLs (`/about-us`, `/bebop-1`, the old blog post slugs and others) redirect to their new pages.

// Basho Projects — small site behaviours

// Where contact-form enquiries go. Paste a Formspree (or similar) endpoint here,
// e.g. "https://formspree.io/f/abcdwxyz". Left empty, the form opens WhatsApp instead.
const FORM_ENDPOINT = "";
const WHATSAPP_NUMBER = "6285921219087";

document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const header = document.querySelector(".site-header");

  // Mobile menu
  const toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", open);
    });
    document.querySelectorAll(".nav a").forEach((a) =>
      a.addEventListener("click", () => body.classList.remove("menu-open"))
    );
  }

  // Projects dropdown on touch / keyboard
  document.querySelectorAll(".nav-drop > button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const open = btn.parentElement.classList.toggle("open");
      btn.setAttribute("aria-expanded", open);
    });
  });

  // Header shadow on scroll
  const onScroll = () => header && header.classList.toggle("is-scrolled", window.scrollY > 10);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Reveal on scroll
  const items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach((el) => io.observe(el));
  }
  // Never leave content hidden if the observer is slow or unsupported
  setTimeout(() => items.forEach((el) => el.classList.add("is-in")), "IntersectionObserver" in window ? 2500 : 0);

  // Contact forms
  document.querySelectorAll("form[data-contact]").forEach((form) => {
    const status = form.querySelector(".form-status");
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const data = new FormData(form);
      if (FORM_ENDPOINT) {
        status.textContent = "Sending…";
        try {
          const res = await fetch(FORM_ENDPOINT, {
            method: "POST",
            body: data,
            headers: { Accept: "application/json" },
          });
          if (!res.ok) throw new Error(res.statusText);
          form.reset();
          status.textContent = "Thank you. We'll be in touch shortly.";
        } catch (err) {
          status.textContent = "Something went wrong. Please message us on WhatsApp instead.";
        }
        return;
      }
      const text =
        `Hello Basho Projects,\n\n${data.get("message")}\n\n` +
        `${data.get("first_name")} ${data.get("last_name")}\n${data.get("email")}`;
      window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(text)}`, "_blank", "noopener");
      status.textContent = "Opening WhatsApp…";
    });
  });

  // Footer year
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

  // "Open now" badges. data-hours is JSON: { "0": [[18, 26]], ... } keyed by
  // weekday (0 = Sunday), hours in 24h Jakarta time; 26 means 02:00 next day.
  document.querySelectorAll("[data-hours]").forEach((el) => {
    let spec;
    try { spec = JSON.parse(el.dataset.hours); } catch (e) { return; }
    const parts = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Asia/Jakarta", weekday: "short", hour: "numeric", minute: "numeric", hourCycle: "h23",
    }).formatToParts(new Date());
    const get = (t) => parts.find((p) => p.type === t).value;
    const day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
    const now = Number(get("hour")) + Number(get("minute")) / 60;
    const fmt = (h) => `${String(Math.floor(h % 24)).padStart(2, "0")}:${h % 1 ? "30" : "00"}`;
    const today = spec[day] || [];
    const yesterday = spec[(day + 6) % 7] || [];
    const lateFromYesterday = yesterday.find(([, c]) => c > 24 && now < c - 24);
    const openToday = today.find(([o, c]) => now >= o && now < c);
    if (lateFromYesterday || openToday) {
      const close = (lateFromYesterday || openToday)[1];
      el.textContent = el.dataset.late && close >= 26 ? "Open now · till late" : `Open now · until ${fmt(close)}`;
      el.classList.add("is-open");
    } else {
      const next = today.find(([o]) => o > now);
      el.textContent = next ? `Opens today at ${fmt(next[0])}` : "Closed now · see hours below";
    }
  });

  // Newsletter popup: shows once per visitor after a short delay or when they
  // scroll most of the way down. Dismissal is remembered in this browser.
  const nl = document.querySelector(".nl");
  if (nl) {
    const KEY = "basho-nl-dismissed";
    const seen = () => { try { return localStorage.getItem(KEY); } catch (e) { return null; } };
    const remember = () => { try { localStorage.setItem(KEY, Date.now()); } catch (e) {} };
    const open = () => { if (!seen() && !nl.classList.contains("is-open")) nl.classList.add("is-open"); };
    const close = () => { nl.classList.remove("is-open"); remember(); };
    if (!seen()) {
      setTimeout(open, 14000);
      window.addEventListener("scroll", function onDeep() {
        if (window.scrollY > document.body.scrollHeight * 0.55) { open(); window.removeEventListener("scroll", onDeep); }
      }, { passive: true });
    }
    nl.querySelector(".nl__close").addEventListener("click", close);
    document.addEventListener("keydown", (e) => e.key === "Escape" && nl.classList.contains("is-open") && close());
  }

  document.querySelectorAll("form[data-newsletter]").forEach((form) => {
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const email = new FormData(form).get("email");
      const note = form.parentElement.querySelector(".nl__note") || form.nextElementSibling;
      if (FORM_ENDPOINT) {
        try {
          const res = await fetch(FORM_ENDPOINT, {
            method: "POST",
            body: new URLSearchParams({ email, _subject: "Newsletter sign-up", list: "guest-list" }),
            headers: { Accept: "application/json" },
          });
          if (!res.ok) throw new Error(res.statusText);
          form.reset();
          if (note) note.textContent = "You're on the list. See you at the bar.";
        } catch (err) {
          if (note) note.textContent = "That didn't go through. Try again in a moment.";
        }
      } else {
        const text = `Hi Basho, please add me to the guest list: ${email}`;
        window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(text)}`, "_blank", "noopener");
        if (note) note.textContent = "Opening WhatsApp to confirm…";
      }
      try { localStorage.setItem("basho-nl-dismissed", Date.now()); } catch (e) {}
    });
  });
});

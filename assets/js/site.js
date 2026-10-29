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
});

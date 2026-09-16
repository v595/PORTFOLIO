document.addEventListener("DOMContentLoaded", () => {

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Theme toggle ---------- */
  const themeToggle = document.getElementById("themeToggle");
  themeToggle.addEventListener("click", () => {
    const next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });

  /* ---------- Navbar scroll state ---------- */
  const navbar = document.getElementById("navbar");
  const backToTop = document.getElementById("backToTop");

  const onScroll = () => {
    const scrolled = window.scrollY > 40;
    navbar.classList.toggle("scrolled", scrolled);
    backToTop.classList.toggle("show", window.scrollY > 500);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }));

  /* ---------- Mobile nav toggle ---------- */
  const navToggle = document.getElementById("navToggle");
  navToggle.addEventListener("click", () => {
    const isOpen = navbar.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
  document.querySelectorAll("[data-nav]").forEach((link) => {
    link.addEventListener("click", () => {
      navbar.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });

  /* ---------- Active nav link on scroll ---------- */
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link");
  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute("id");
          navLinks.forEach((link) => {
            link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
          });
        }
      });
    },
    { rootMargin: "-45% 0px -45% 0px" }
  );
  sections.forEach((s) => sectionObserver.observe(s));

  /* ---------- Scroll reveal ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if (reduceMotion) {
    revealEls.forEach((el) => el.classList.add("visible"));
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealEls.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min(i % 6, 5) * 0.06}s`;
      revealObserver.observe(el);
    });
  }

  /* ---------- Typing effect for hero role ---------- */
  const typedEl = document.getElementById("typed");
  const roles = Array.isArray(window.__ROLES__) && window.__ROLES__.length
    ? window.__ROLES__
    : ["Python Developer", "Flask Developer"];

  if (reduceMotion) {
    typedEl.textContent = roles[0];
  } else {
    let roleIndex = 0, charIndex = 0, deleting = false;

    function typeLoop() {
      const current = roles[roleIndex];
      if (!deleting) {
        charIndex++;
        typedEl.textContent = current.slice(0, charIndex);
        if (charIndex === current.length) {
          deleting = true;
          setTimeout(typeLoop, 1400);
          return;
        }
      } else {
        charIndex--;
        typedEl.textContent = current.slice(0, charIndex);
        if (charIndex === 0) {
          deleting = false;
          roleIndex = (roleIndex + 1) % roles.length;
        }
      }
      setTimeout(typeLoop, deleting ? 40 : 80);
    }
    typeLoop();
  }

  /* ---------- Animated stat counters ---------- */
  const statEls = document.querySelectorAll(".stat-value");
  if (reduceMotion) {
    statEls.forEach((el) => {
      el.textContent = (parseInt(el.dataset.count, 10) || 0) + (el.dataset.suffix || "");
    });
  } else {
    const statObserver = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const target = parseInt(el.dataset.count, 10) || 0;
          const suffix = el.dataset.suffix || "";
          const duration = 900;
          const start = performance.now();
          const step = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(eased * target) + suffix;
            if (progress < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
          obs.unobserve(el);
        });
      },
      { threshold: 0.6 }
    );
    statEls.forEach((el) => statObserver.observe(el));
  }

  /* ---------- Contact form (validation + Web3Forms) ---------- */
  const form = document.getElementById("contactForm");
  const statusEl = document.getElementById("formStatus");
  const submitBtn = document.getElementById("submitBtn");

  const fields = {
    name: { el: document.getElementById("name"), error: document.getElementById("nameError"), validate: (v) => v.trim().length > 0 },
    email: { el: document.getElementById("email"), error: document.getElementById("emailError"), validate: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) },
    message: { el: document.getElementById("message"), error: document.getElementById("messageError"), validate: (v) => v.trim().length > 0 },
  };

  function setFieldValid(field) {
    field.el.setAttribute("aria-invalid", "false");
    field.error.classList.remove("show");
  }
  function setFieldInvalid(field) {
    field.el.setAttribute("aria-invalid", "true");
    field.error.classList.add("show");
  }

  Object.values(fields).forEach((field) => {
    field.el.addEventListener("input", () => {
      if (field.validate(field.el.value)) setFieldValid(field);
    });
    field.el.addEventListener("blur", () => {
      if (!field.validate(field.el.value)) setFieldInvalid(field);
    });
  });

  function validateForm() {
    let valid = true;
    let firstInvalid = null;
    Object.values(fields).forEach((field) => {
      if (field.validate(field.el.value)) {
        setFieldValid(field);
      } else {
        setFieldInvalid(field);
        valid = false;
        if (!firstInvalid) firstInvalid = field.el;
      }
    });
    if (firstInvalid) firstInvalid.focus();
    return valid;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    statusEl.textContent = "";
    statusEl.className = "form-status";

    if (!validateForm()) {
      statusEl.textContent = "Please fix the highlighted fields.";
      statusEl.className = "form-status err";
      return;
    }

    submitBtn.disabled = true;
    submitBtn.querySelector(".btn-label").textContent = "Sending...";

    const formData = new FormData(form);

    try {
      const res = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { Accept: "application/json" },
        body: formData,
      });
      const data = await res.json();

      if (res.ok && data.success) {
        const message = "Thanks for reaching out! I'll get back to you soon.";
        statusEl.innerHTML = '<i class="fa-solid fa-circle-check"></i> ' + message;
        statusEl.className = "form-status ok";
        showToast(message);
        form.reset();
        Object.values(fields).forEach(setFieldValid);
      } else {
        statusEl.textContent = data.message || "Something went wrong. Please try again.";
        statusEl.className = "form-status err";
      }
    } catch (err) {
      statusEl.textContent = "Network error — please try again.";
      statusEl.className = "form-status err";
    } finally {
      submitBtn.disabled = false;
      submitBtn.querySelector(".btn-label").textContent = "Send Message";
    }
  });

  function showToast(message) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3500);
  }
});

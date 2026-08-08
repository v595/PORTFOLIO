document.addEventListener("DOMContentLoaded", () => {

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

  backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  /* ---------- Mobile nav toggle ---------- */
  const navToggle = document.getElementById("navToggle");
  navToggle.addEventListener("click", () => {
    navbar.classList.toggle("open");
  });
  document.querySelectorAll("[data-nav]").forEach((link) => {
    link.addEventListener("click", () => navbar.classList.remove("open"));
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
  document.querySelectorAll(".reveal").forEach((el, i) => {
    el.style.transitionDelay = `${Math.min(i % 6, 5) * 0.08}s`;
    revealObserver.observe(el);
  });

  /* ---------- Typing effect for hero role ---------- */
  const typedEl = document.getElementById("typed");
  const roles = Array.isArray(window.__ROLES__) && window.__ROLES__.length
    ? window.__ROLES__
    : ["Python Developer", "Flask Developer"];

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

  /* ---------- Animated stat counters ---------- */
  const statEls = document.querySelectorAll(".stat-value");
  const statObserver = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = parseInt(el.dataset.count, 10) || 0;
        const suffix = el.dataset.suffix || "";
        const duration = 1200;
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

  /* ---------- Contact form (Web3Forms) ---------- */
  const form = document.getElementById("contactForm");
  const statusEl = document.getElementById("formStatus");
  const submitBtn = document.getElementById("submitBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    submitBtn.disabled = true;
    submitBtn.querySelector(".btn-label").textContent = "Sending...";
    statusEl.textContent = "";
    statusEl.className = "form-status";

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
        statusEl.textContent = message;
        statusEl.className = "form-status ok";
        showToast(message);
        form.reset();
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

  /* ---------- Particle network background ---------- */
  const canvas = document.getElementById("bg-canvas");
  const ctx = canvas.getContext("2d");
  let particles = [];
  let width, height;

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    const count = Math.min(90, Math.floor((width * height) / 18000));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.6 + 0.6,
    }));
  }

  function tick() {
    ctx.clearRect(0, 0, width, height);
    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(96, 165, 250, 0.55)";
      ctx.fill();
    }
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const a = particles[i], b = particles[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(34, 211, 238, ${0.12 * (1 - dist / 130)})`;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(tick);
  }

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  window.addEventListener("resize", resize);
  resize();
  if (!reduceMotion) requestAnimationFrame(tick);
});

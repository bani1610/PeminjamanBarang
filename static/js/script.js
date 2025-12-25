// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

// Navbar scroll effect
window.addEventListener("scroll", function () {
  const navbar = document.querySelector(".navbar");
  if (window.scrollY > 100) {
    navbar.style.background = "rgba(15, 23, 42, 0.95)";
    navbar.style.boxShadow = "0 4px 16px rgba(0, 0, 0, 0.2)";
  } else {
    navbar.style.background = "rgba(15, 23, 42, 0.8)";
    navbar.style.boxShadow = "none";
  }
});

// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -100px 0px",
};

const observer = new IntersectionObserver(function (entries) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// Observe all feature cards
document.querySelectorAll(".feature-card").forEach((card) => {
  observer.observe(card);
});

// Active navigation link based on scroll position
window.addEventListener("scroll", function () {
  let current = "";
  const sections = document.querySelectorAll("section[id]");

  sections.forEach((section) => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;
    if (pageYOffset >= sectionTop - 200) {
      current = section.getAttribute("id");
    }
  });

  document.querySelectorAll(".nav-link").forEach((link) => {
    link.classList.remove("active");
    if (link.getAttribute("href") === "#" + current) {
      link.classList.add("active");
    }
  });
});

// Add parallax effect to hero background
window.addEventListener("scroll", function () {
  const heroBackground = document.querySelector(".hero-background");
  if (heroBackground) {
    const scrolled = window.pageYOffset;
    heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
  }
});

// Counter animation for stats
function animateCounter(element, target, duration = 2000) {
  let start = 0;
  const increment = target / (duration / 16);

  const timer = setInterval(() => {
    start += increment;
    if (start >= target) {
      element.textContent = target;
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(start);
    }
  }, 16);
}

// Trigger counter animation when stats section is visible
const statsObserver = new IntersectionObserver(
  function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const statNumbers = entry.target.querySelectorAll(".stat-number");
        statNumbers.forEach((stat) => {
          const finalValue = stat.textContent;
          if (!isNaN(finalValue)) {
            stat.textContent = "0";
            animateCounter(stat, parseInt(finalValue));
          }
        });
        statsObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.5 }
);

const statsSection = document.querySelector(".stats");
if (statsSection) {
  statsObserver.observe(statsSection);
}

// Add hover effect to buttons
document.querySelectorAll(".btn").forEach((button) => {
  button.addEventListener("mouseenter", function () {
    this.style.transform = "translateY(-2px)";
  });

  button.addEventListener("mouseleave", function () {
    this.style.transform = "translateY(0)";
  });
});

// Console message
console.log(
  "%c🚀 Django Web Application ",
  "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
);
console.log(
  "%cBuilt with Django and modern web technologies",
  "color: #667eea; font-size: 12px;"
);

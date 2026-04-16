const html = document.documentElement;
let skillBarsInitialized = false;

const fixThemeToggleIcon = (theme) => {
  const toggles = document.querySelectorAll(".theme-toggle");

  toggles.forEach((toggle) => {
    toggle.classList.toggle("fa-sun", theme === "dark");
    toggle.classList.toggle("fa-moon", theme !== "dark");
  });
};

const setTheme = (theme) => {
  const resolvedTheme = theme === "dark" ? "dark" : "light";

  html.classList.remove("light", "dark");
  html.classList.add(resolvedTheme);
  window.localStorage.setItem("theme", resolvedTheme);
  fixThemeToggleIcon(resolvedTheme);
};

const getPreferredTheme = () => {
  const storedTheme = window.localStorage.getItem("theme");

  if (storedTheme) {
    return storedTheme;
  }

  if (html.classList.contains("dark")) {
    return "dark";
  }

  if (html.classList.contains("light")) {
    return "light";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
};

const syncActiveAccordionPanel = () => {
  const activeAccordion = document.querySelector(".accordion.active");

  if (!activeAccordion) {
    return;
  }

  const panel = activeAccordion.nextElementSibling;

  if (panel) {
    panel.style.maxHeight = `${panel.scrollHeight}px`;
  }
};

const initializeSkillBars = (root = document) => {
  if (skillBarsInitialized) {
    return;
  }

  const skillBars = root.querySelectorAll("[data-skill-rating]");

  if (!skillBars.length) {
    return;
  }

  skillBars.forEach((bar) => {
    bar.style.width = `${bar.dataset.skillRating}%`;
  });

  skillBarsInitialized = true;
};

const expandAccordion = (element) => {
  if (!element) {
    return;
  }

  const accordions = document.querySelectorAll(".accordion");
  const panels = document.querySelectorAll(".panel");
  const isActive = element.classList.contains("active");

  accordions.forEach((accordion) => accordion.classList.remove("active"));
  panels.forEach((panel) => {
    panel.style.maxHeight = null;
  });

  if (!isActive) {
    element.classList.add("active");
    syncActiveAccordionPanel();
    initializeSkillBars(element.nextElementSibling ?? document);
  }
};

const initializeSearch = () => {
  const searchElement = document.querySelector("#search");

  if (searchElement && window.PagefindUI) {
    new window.PagefindUI({ element: "#search", showSubResults: true });
  }
};

const initializeEventBindings = () => {
  document.querySelectorAll("[data-accordion-trigger]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const targetSelector = trigger.dataset.accordionTarget;
      const target = targetSelector
        ? trigger.closest(targetSelector) ?? document.querySelector(targetSelector)
        : trigger;

      expandAccordion(target);
    });
  });

  document.querySelectorAll("[data-theme-toggle]").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      window.toggleTheme();
    });
  });
};

window.toggleTheme = () => {
  setTheme(html.classList.contains("dark") ? "light" : "dark");
};

window.expandAccordion = expandAccordion;

setTheme(getPreferredTheme());

window.addEventListener("DOMContentLoaded", () => {
  initializeEventBindings();
  syncActiveAccordionPanel();
  initializeSkillBars();
  initializeSearch();
});

window.addEventListener("resize", syncActiveAccordionPanel);

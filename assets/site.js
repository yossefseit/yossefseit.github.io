"use strict";

document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  const navigation = document.getElementById("primary-navigation");
  const menuToggle = document.getElementById("menu-toggle");
  const year = document.getElementById("current-year");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  if (navigation && menuToggle) {
    const desktopNavigation = window.matchMedia("(min-width: 861px)");

    const setMenuState = (isOpen) => {
      navigation.classList.toggle("is-open", isOpen);
      menuToggle.setAttribute("aria-expanded", String(isOpen));
    };

    setMenuState(false);

    const resetMenu = () => setMenuState(false);

    if (typeof desktopNavigation.addEventListener === "function") {
      desktopNavigation.addEventListener("change", resetMenu);
    } else {
      desktopNavigation.addListener(resetMenu);
    }

    menuToggle.addEventListener("click", () => {
      const isOpen = menuToggle.getAttribute("aria-expanded") !== "true";
      setMenuState(isOpen);
    });

    navigation.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        if (!desktopNavigation.matches) {
          setMenuState(false);
        }
      });
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menuToggle.getAttribute("aria-expanded") === "true") {
        setMenuState(false);
        menuToggle.focus();
      }
    });

    document.addEventListener("click", (event) => {
      if (
        menuToggle.getAttribute("aria-expanded") === "true"
        && !navigation.contains(event.target)
        && !menuToggle.contains(event.target)
      ) {
        setMenuState(false);
      }
    });
  }

  const revealItems = document.querySelectorAll("[data-reveal]");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  const revealAll = () => {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  };

  if (!revealItems.length || reducedMotion.matches || !("IntersectionObserver" in window)) {
    revealAll();
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: "0px 0px -8% 0px",
      threshold: 0.12,
    });

    revealItems.forEach((item) => revealObserver.observe(item));
  }
});

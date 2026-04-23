const topbar = document.querySelector("[data-topbar]");

const updateTopbar = () => {
  if (!topbar) return;
  topbar.classList.toggle("is-scrolled", window.scrollY > 12);
};

updateTopbar();
window.addEventListener("scroll", updateTopbar, { passive: true });

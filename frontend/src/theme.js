
const THEME_KEY = "trax-theme";

export function getSavedTheme() {
  return localStorage.getItem(THEME_KEY) || "dark";
}

export function applyTheme(theme) {
  document.body.classList.toggle(
    "light-theme",
    theme === "light"
  );

  document.documentElement.dataset.theme = theme;
  localStorage.setItem(THEME_KEY, theme);
}

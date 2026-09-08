'use strict';

document.addEventListener('DOMContentLoaded', () => {
  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const syncTheme = () => {
    const light = root.dataset.theme === 'light';
    themeButton.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
    themeButton.querySelector('span').textContent = light ? 'Dark theme' : 'Light theme';
    themeButton.setAttribute('aria-pressed', String(light));
  };
  if (themeButton) {
    themeButton.hidden = false;
    syncTheme();
    themeButton.addEventListener('click', () => {
      const theme = root.dataset.theme === 'light' ? 'dark' : 'light';
      root.dataset.theme = theme;
      try { localStorage.setItem('ym-theme', theme); } catch { /* Preference is local to this page. */ }
      syncTheme();
    });
  }

  const menu = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('#primary-navigation');
  if (menu && nav) {
    menu.hidden = false;
    root.classList.add('navigation-enhanced');
    const closeMenu = () => {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    };
    menu.addEventListener('click', () => {
      const expanded = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(expanded));
      nav.classList.toggle('is-open', expanded);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        closeMenu(); menu.focus();
      }
    });
    window.matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);
  }

  const dialog = document.querySelector('#command-palette');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const trigger = document.querySelector('[data-command-open]');
  const input = dialog.querySelector('input');
  const options = [...dialog.querySelectorAll('[data-command]')];
  const status = dialog.querySelector('[data-command-status]');
  let index = 0;
  let previousFocus;
  const visible = () => options.filter(option => !option.hidden);
  const select = nextIndex => {
    const items = visible();
    index = items.length ? (nextIndex + items.length) % items.length : 0;
    options.forEach(option => {
      const active = option === items[index];
      option.classList.toggle('is-selected', active);
    });
    if (items[index]) {
      items[index].scrollIntoView({ block: 'nearest' });
    }
  };
  const filter = () => {
    const query = input.value.toLowerCase().trim();
    options.forEach(option => { option.hidden = !option.textContent.toLowerCase().includes(query); });
    select(0);
    const count = visible().length;
    status.textContent = count ? `${count} destinations. Use arrow keys and Enter, or Tab to browse.` : 'No matching destination. Try projects, skills or contact.';
  };
  const open = () => {
    if (dialog.open) return;
    previousFocus = document.activeElement;
    dialog.showModal();
    input.value = '';
    filter();
    input.focus();
  };
  trigger.hidden = false;
  trigger.addEventListener('click', open);
  dialog.querySelector('[data-command-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    previousFocus?.focus();
  });
  dialog.addEventListener('click', event => {
    if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }
    if (event.target.closest('a')) dialog.close();
  });
  input.addEventListener('input', filter);
  input.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault(); select(index + (event.key === 'ArrowDown' ? 1 : -1));
    } else if (event.key === 'Enter') {
      event.preventDefault(); visible()[index]?.querySelector('a').click();
    }
  });
  document.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      if (dialog.open) dialog.close(); else open();
    }
  });
});

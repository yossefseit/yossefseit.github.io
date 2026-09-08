// Apply a stored preference before first paint. Storage may be unavailable.
try {
  const theme = localStorage.getItem('ym-theme');
  if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
} catch { /* The default dark theme remains usable. */ }

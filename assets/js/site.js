    // Theme toggle (persisted)
    const root = document.documentElement;
    const themeBtn = document.getElementById('themeBtn');
    const key = 'theme';
    const saved = localStorage.getItem(key);
    if(saved){ root.setAttribute('data-theme', saved); }
    themeBtn.addEventListener('click', () => {
      const cur = root.getAttribute('data-theme') || 'dark';
      const next = cur === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem(key, next);
      themeBtn.querySelector('.mono').textContent = (next === 'dark' ? 'Theme' : 'Theme');
    });

    document.getElementById('year').textContent = new Date().getFullYear();
  

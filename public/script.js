const tabs = Array.from(document.querySelectorAll('.tab'));
const panels = Array.from(document.querySelectorAll('.panel'));
const revealCards = Array.from(document.querySelectorAll('[data-load-on-scroll]'));

function activateTab(tabName, revealPanel = true) {
  tabs.forEach((tab) => {
    const isSelected = tab.dataset.tab === tabName;
    tab.classList.toggle('is-active', isSelected);
    tab.setAttribute('aria-selected', String(isSelected));
    tab.tabIndex = isSelected ? 0 : -1;
  });

  panels.forEach((panel) => {
    const isSelected = panel.dataset.panel === tabName;
    panel.classList.toggle('is-active', isSelected);
    panel.hidden = !isSelected;
    if (revealPanel && isSelected && !panel.classList.contains('is-loaded')) {
      window.setTimeout(() => panel.classList.add('is-loaded'), 120);
    }
  });
}

tabs.forEach((tab) => {
  tab.addEventListener('click', () => activateTab(tab.dataset.tab));
  tab.addEventListener('keydown', (event) => {
    const currentIndex = tabs.indexOf(tab);

    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      const direction = event.key === 'ArrowRight' ? 1 : -1;
      const nextIndex = (currentIndex + direction + tabs.length) % tabs.length;
      tabs[nextIndex].focus();
      activateTab(tabs[nextIndex].dataset.tab);
    }
  });
});

activateTab('automation', false);

if ('IntersectionObserver' in window) {
  const cardObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const card = entry.target;
          window.setTimeout(() => {
            card.classList.add('is-loaded');
            observer.unobserve(card);
          }, 180);
        }
      });
    },
    {
      threshold: 0.3,
      rootMargin: '0px 0px -80px 0px',
    }
  );

  revealCards.forEach((card) => cardObserver.observe(card));
} else {
  revealCards.forEach((card) => card.classList.add('is-loaded'));
}

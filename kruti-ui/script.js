(function () {
  const searchInput = document.getElementById('searchInput');
  const chipButtons = Array.from(document.querySelectorAll('.chip'));
  const cards = Array.from(document.querySelectorAll('.card'));

  let activeTag = 'all';

  function normalize(text) {
    return (text || '').toLowerCase().trim();
  }

  function cardMatches(card, query, tag) {
    const title = card.getAttribute('data-title') || '';
    const tags = card.getAttribute('data-tags') || '';

    const matchesQuery = !query || normalize(title).includes(query) || normalize(tags).includes(query);

    if (tag === 'all') return matchesQuery;

    const tagList = tags.split(',').map(normalize);
    return matchesQuery && tagList.includes(normalize(tag));
  }

  function applyFilters() {
    const query = normalize(searchInput.value);

    cards.forEach(card => {
      if (cardMatches(card, query, activeTag)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  }

  chipButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      chipButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeTag = btn.getAttribute('data-filter') || 'all';
      applyFilters();
    });
  });

  searchInput.addEventListener('input', applyFilters);
})();
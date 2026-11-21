(() => {
  const article = document.querySelector('.course-reference');
  if (!article) return;
  const controls = article.querySelector('.revision-controls');
  const proofs = [...article.querySelectorAll('details[data-proof]')];
  const toggle = article.querySelector('[data-expand-proofs]');
  const updateLabel = () => {
    toggle.textContent = proofs.every(proof => proof.open) ? 'Collapse all proofs' : 'Expand all proofs';
  };
  controls.hidden = false;
  toggle.addEventListener('click', () => {
    const expand = !proofs.every(proof => proof.open);
    proofs.forEach(proof => { proof.open = expand; });
    updateLabel();
  });
  proofs.forEach(proof => proof.addEventListener('toggle', updateLabel));
  article.querySelector('#revision-section').addEventListener('change', event => {
    const id = event.target.value;
    const heading = document.getElementById(id);
    if (!heading) return;
    history.replaceState(null, '', '#' + encodeURIComponent(id));
    heading.setAttribute('tabindex', '-1');
    heading.focus({ preventScroll: true });
    heading.scrollIntoView({ block: 'start' });
  });
  article.querySelector('[data-print-reference]').addEventListener('click', () => window.print());
  let previousOpenStates;
  window.addEventListener('beforeprint', () => {
    if (previousOpenStates) return;
    previousOpenStates = proofs.map(proof => proof.open);
    proofs.forEach(proof => { proof.open = true; });
  });
  window.addEventListener('afterprint', () => {
    if (!previousOpenStates) return;
    proofs.forEach((proof, index) => { proof.open = previousOpenStates[index]; });
    previousOpenStates = undefined;
    updateLabel();
  });
})();

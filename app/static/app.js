// One-use launch token never reaches server request URLs or persistent browser storage.
(async () => {
  const status = document.getElementById('bootstrap-status');
  if (status) {
    const token = new URLSearchParams(location.hash.slice(1)).get('token');
    history.replaceState(null, '', location.pathname);
    if (!token) { status.textContent = 'Open the app using the launcher to start a secure local session.'; return; }
    try {
      const r = await fetch('/api/bootstrap', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token})});
      const data = await r.json();
      if (!r.ok) throw new Error(data.problem || 'Unable to open session.');
      location.replace(data.next);
    } catch (error) { status.textContent = error.message; }
  }
})();
let dirty = false;
document.querySelectorAll('form.dirtyguard').forEach(form => {
  form.addEventListener('input', () => { dirty = true; });
  form.addEventListener('submit', () => { dirty = false; });
});
window.addEventListener('beforeunload', event => { if (dirty) { event.preventDefault(); event.returnValue = ''; } });

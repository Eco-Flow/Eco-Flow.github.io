// Lightweight client-side search for Eco-Flow.
// Fetches the build-time index (search.json) once, then ranks entries by a
// simple term-frequency score over the title (weighted) and body text.
(function () {
  var panel = document.getElementById('search-panel');
  if (!panel) return;

  var openBtn = document.getElementById('search-open');
  var closeBtn = document.getElementById('search-close');
  var input = document.getElementById('search-input');
  var resultsEl = document.getElementById('search-results');
  var emptyEl = document.getElementById('search-empty');
  var indexUrl = panel.getAttribute('data-index');

  var docs = null;     // loaded index
  var loading = false;

  function loadIndex() {
    if (docs || loading) return;
    loading = true;
    fetch(indexUrl)
      .then(function (r) { return r.json(); })
      .then(function (data) { docs = data; loading = false; if (input.value) run(input.value); })
      .catch(function () { loading = false; });
  }

  function openPanel() {
    panel.hidden = false;
    openBtn.setAttribute('aria-expanded', 'true');
    loadIndex();
    // focus after the panel is painted
    requestAnimationFrame(function () { input.focus(); });
  }

  function closePanel() {
    panel.hidden = true;
    openBtn.setAttribute('aria-expanded', 'false');
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Build a short snippet around the first matched term.
  function snippet(content, terms) {
    if (!content) return '';
    var lower = content.toLowerCase();
    var idx = -1;
    for (var i = 0; i < terms.length; i++) {
      var f = lower.indexOf(terms[i]);
      if (f !== -1 && (idx === -1 || f < idx)) idx = f;
    }
    if (idx === -1) idx = 0;
    var start = Math.max(0, idx - 40);
    var end = Math.min(content.length, idx + 120);
    var text = (start > 0 ? '…' : '') + content.slice(start, end) + (end < content.length ? '…' : '');
    return escapeHtml(text);
  }

  function score(doc, terms) {
    var title = doc.title.toLowerCase();
    var body = (doc.content || '').toLowerCase();
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (!t) continue;
      if (title.indexOf(t) !== -1) s += 10;
      if (title.indexOf(t) === 0) s += 5; // title starts with term
      var bi = body.indexOf(t);
      while (bi !== -1) { s += 1; bi = body.indexOf(t, bi + 1); if (s > 60) break; }
    }
    return s;
  }

  function run(query) {
    var q = query.trim().toLowerCase();
    if (!q || !docs) { resultsEl.innerHTML = ''; emptyEl.hidden = true; return; }
    var terms = q.split(/\s+/);

    var ranked = docs
      .map(function (d) { return { doc: d, s: score(d, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, 8);

    if (!ranked.length) { resultsEl.innerHTML = ''; emptyEl.hidden = false; return; }
    emptyEl.hidden = true;

    resultsEl.innerHTML = ranked.map(function (x) {
      var d = x.doc;
      return '<li role="option"><a href="' + d.url + '">' +
        '<span class="search-results__type">' + escapeHtml(d.type) + '</span>' +
        '<span class="search-results__title">' + escapeHtml(d.title) + '</span>' +
        '<span class="search-results__snip">' + snippet(d.content, terms) + '</span>' +
        '</a></li>';
    }).join('');
  }

  openBtn.addEventListener('click', function () {
    if (panel.hidden) openPanel(); else closePanel();
  });
  closeBtn.addEventListener('click', closePanel);
  input.addEventListener('input', function () { run(input.value); });

  // Close on Escape; open with "/" shortcut when not typing in a field.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) { closePanel(); openBtn.focus(); }
    if (e.key === '/' && panel.hidden) {
      var tag = (document.activeElement.tagName || '').toLowerCase();
      if (tag !== 'input' && tag !== 'textarea') { e.preventDefault(); openPanel(); }
    }
  });

  // Close when clicking outside the panel.
  document.addEventListener('click', function (e) {
    if (panel.hidden) return;
    if (!panel.contains(e.target) && !openBtn.contains(e.target)) closePanel();
  });
})();

/* Copy-to-clipboard buttons for code blocks in training/prose pages.
   No dependencies. Adds a "Copy" button to every <pre> inside .prose. */
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy') ? resolve() : reject(); }
      catch (e) { reject(e); }
      document.body.removeChild(ta);
    });
  }

  ready(function () {
    var blocks = document.querySelectorAll('.prose pre');
    Array.prototype.forEach.call(blocks, function (pre) {
      if (pre.parentElement && pre.parentElement.classList.contains('code-wrap')) return;
      var wrap = document.createElement('div');
      wrap.className = 'code-wrap';
      pre.parentNode.insertBefore(wrap, pre);
      wrap.appendChild(pre);

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn';
      btn.textContent = 'Copy';
      btn.setAttribute('aria-label', 'Copy code to clipboard');

      btn.addEventListener('click', function () {
        var code = pre.querySelector('code') || pre;
        var text = code.innerText.replace(/\n+$/, '');
        copyText(text).then(function () {
          btn.textContent = 'Copied!';
          btn.classList.add('is-copied');
          setTimeout(function () { btn.textContent = 'Copy'; btn.classList.remove('is-copied'); }, 2000);
        }).catch(function () {
          btn.textContent = 'Press Ctrl/⌘+C';
          setTimeout(function () { btn.textContent = 'Copy'; }, 2000);
        });
      });

      wrap.appendChild(btn);
    });
  });
})();

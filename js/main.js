/* Phoenix Solutions — shared site behaviour */
(function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', document.body.classList.contains('nav-open'));
    });
    document.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () { document.body.classList.remove('nav-open'); });
    });
  }

  // Scroll reveal
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    if (!q || !a) return;
    q.addEventListener('click', function () {
      var open = item.classList.toggle('open');
      a.style.maxHeight = open ? a.scrollHeight + 'px' : 0;
      q.setAttribute('aria-expanded', open);
    });
  });

  // Projects filter
  var filterBtns = document.querySelectorAll('.filter-btn');
  if (filterBtns.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filterBtns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        var f = btn.getAttribute('data-filter');
        document.querySelectorAll('[data-cat]').forEach(function (card) {
          card.style.display = (f === 'all' || card.getAttribute('data-cat') === f) ? '' : 'none';
        });
      });
    });
  }

  // Quote form
  var quoteForm = document.getElementById('quote-form');
  if (quoteForm) {
    var servicesInput = document.getElementById('q-services');
    function syncServices() {
      if (!servicesInput) return;
      var sel = [];
      document.querySelectorAll('.service-tile.selected').forEach(function (t) {
        sel.push(t.textContent.trim());
      });
      servicesInput.value = sel.join(', ');
    }
    document.querySelectorAll('.service-tile').forEach(function (tile) {
      tile.addEventListener('click', function () {
        tile.classList.toggle('selected');
        syncServices();
      });
      tile.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tile.click(); }
      });
    });
    quoteForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = quoteForm.querySelector('[name="name"]');
      var email = quoteForm.querySelector('[name="email"]');
      if (!name.value.trim() || !email.value.trim()) {
        alert('Please add your name and email so we can reply to you.');
        return;
      }
      syncServices();
      var btn = document.getElementById('q-submit');
      var err = document.getElementById('quote-error');
      if (err) err.style.display = 'none';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending\u2026'; }

      fetch('/api/quote', { method: 'POST', body: new FormData(quoteForm) })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error(res.error || 'send failed');
          quoteForm.style.display = 'none';
          var ok = document.getElementById('quote-success');
          if (ok) { ok.style.display = 'block'; ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = 'Send My Quote Request'; }
          if (err) { err.style.display = 'block'; err.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
        });
    });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

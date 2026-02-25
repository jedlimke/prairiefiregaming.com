(function () {
  function pad(n) {
    return String(n).padStart(2, '0');
  }

  function initCountdown(el) {
    var target  = new Date(el.dataset.target);
    var message = el.dataset.gamedayMessage || 'GAMEDAY IS TODAY';

    function tick() {
      var diff = target - new Date();

      if (diff <= 0) {
        el.innerHTML = '<span class="countdown-gameday">' + message + '</span>';
        return;
      }

      var total   = Math.floor(diff / 1000);
      var days    = Math.floor(total / 86400);
      var hours   = Math.floor((total % 86400) / 3600);
      var minutes = Math.floor((total % 3600) / 60);
      var seconds = total % 60;

      el.innerHTML =
        '<span class="countdown-unit">' + pad(days)    + '<span class="countdown-label">Days</span></span>' +
        '<span class="countdown-unit">' + pad(hours)   + '<span class="countdown-label">Hours</span></span>' +
        '<span class="countdown-unit">' + pad(minutes) + '<span class="countdown-label">Minutes</span></span>' +
        '<span class="countdown-unit">' + pad(seconds) + '<span class="countdown-label">Seconds</span></span>';

      setTimeout(tick, 1000);
    }

    tick();
  }

  function init() {
    document.querySelectorAll('.countdown[data-target]').forEach(initCountdown);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());

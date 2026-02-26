(function () {
  function pad(n) {
    return String(n).padStart(2, '0');
  }

  function makeDigit(char) {
    var span = document.createElement('span');
    span.className = 'countdown-digit';
    span.textContent = char;
    return span;
  }

  function initCountdown(el) {
    var target  = new Date(el.dataset.target);
    var message = el.dataset.gamedayMessage || 'GAMEDAY IS TODAY';
    var labels  = ['Days', 'Hours', 'Minutes', 'Seconds'];

    // Build the full DOM structure once — labels never get touched again
    var unitEls  = [];   // the 4 .countdown-unit spans
    var digitEls = [];   // [4][2] — tens and units digit node for each unit
    var prev     = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]];

    for (var i = 0; i < 4; i++) {
      var unitSpan    = document.createElement('span');
      unitSpan.className = 'countdown-unit';

      var digitsWrap  = document.createElement('span');
      digitsWrap.className = 'countdown-digits';

      var tensSpan    = makeDigit('0');
      var unitsSpan   = makeDigit('0');

      var labelSpan   = document.createElement('span');
      labelSpan.className = 'countdown-label';
      labelSpan.textContent = labels[i];

      digitsWrap.appendChild(tensSpan);
      digitsWrap.appendChild(unitsSpan);
      unitSpan.appendChild(digitsWrap);
      unitSpan.appendChild(labelSpan);
      el.appendChild(unitSpan);

      unitEls.push(digitsWrap);       // replaceChild targets the wrapper
      digitEls.push([tensSpan, unitsSpan]);
    }

    function tick() {
      var diff = target - new Date();

      if (diff <= 0) {
        el.innerHTML = '<span class="countdown-gameday">' + message + '</span>';
        return;
      }

      var total = Math.floor(diff / 1000);
      var vals  = [
        Math.floor(total / 86400),
        Math.floor((total % 86400) / 3600),
        Math.floor((total % 3600) / 60),
        total % 60
      ];

      for (var i = 0; i < 4; i++) {
        var padded = pad(vals[i]);

        // Tens digit
        if (padded[0] !== prev[i][0]) {
          var newTens = makeDigit(padded[0]);
          unitEls[i].replaceChild(newTens, digitEls[i][0]);
          digitEls[i][0] = newTens;
          prev[i][0] = padded[0];
        }

        // Units digit
        if (padded[1] !== prev[i][1]) {
          var newUnits = makeDigit(padded[1]);
          unitEls[i].replaceChild(newUnits, digitEls[i][1]);
          digitEls[i][1] = newUnits;
          prev[i][1] = padded[1];
        }
      }

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

(function () {
  function pad(n) {
    return String(n).padStart(2, '0');
  }

  var WORDS = [
    'ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE',
    'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN',
    'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN', 'FIFTEEN',
    'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN', 'NINETEEN', 'TWENTY'
  ];

  function intToWords(n) {
    return n <= 20 ? WORDS[n] : String(n);
  }

  function makeDigit(char) {
    var span = document.createElement('span');
    span.className = 'countdown-digit';
    span.textContent = char;
    return span;
  }

  function initCountdown(el) {
    var target   = new Date(el.dataset.target);
    var message  = el.dataset.gamedayMessage || 'GAMEDAY IS TODAY';
    var wordDays = el.dataset.wordDays === 'true';
    var labels   = ['Days', 'Hours', 'Minutes', 'Seconds'];

    // Build the full DOM structure once — labels never get touched again
    // unitEls[i]    — the .countdown-digits wrapper for unit i
    // When wordDays is on:
    //   digitEls[0]   — [wordSpan]          (days: single word node)
    //   digitEls[1-3] — [tensSpan, unitSpan] (hours/min/sec: two digit nodes)
    // When wordDays is off, all four units use [tensSpan, unitSpan].
    var unitEls  = [];
    var digitEls = [];
    var prev     = wordDays
      ? [[null], [null, null], [null, null], [null, null]]
      : [[null, null], [null, null], [null, null], [null, null]];

    for (var i = 0; i < 4; i++) {
      var unitSpan    = document.createElement('span');
      unitSpan.className = 'countdown-unit';

      var digitsWrap  = document.createElement('span');
      digitsWrap.className = 'countdown-digits';

      var labelSpan   = document.createElement('span');
      labelSpan.className = 'countdown-label';
      labelSpan.textContent = labels[i];

      if (i === 0 && wordDays) {
        // Days: single span showing the word
        var wordSpan = makeDigit(intToWords(0));
        digitsWrap.appendChild(wordSpan);
        digitEls.push([wordSpan]);
      } else {
        var tensSpan  = makeDigit('0');
        var unitsSpan = makeDigit('0');
        digitsWrap.appendChild(tensSpan);
        digitsWrap.appendChild(unitsSpan);
        digitEls.push([tensSpan, unitsSpan]);
      }

      unitSpan.appendChild(digitsWrap);
      unitSpan.appendChild(labelSpan);
      el.appendChild(unitSpan);

      unitEls.push(digitsWrap);       // replaceChild targets the wrapper
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

      // Days — word or digits depending on wordDays flag
      if (wordDays) {
        var word = intToWords(vals[0]);
        if (word !== prev[0][0]) {
          var newWord = makeDigit(word);
          unitEls[0].replaceChild(newWord, digitEls[0][0]);
          digitEls[0][0] = newWord;
          prev[0][0] = word;
        }
      }

      // All four units as digits when wordDays is off; hours/min/sec always
      var start = wordDays ? 1 : 0;
      for (var i = start; i < 4; i++) {
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

/**
 * Consent gate for third-party embeds.
 *
 * The point of this file is that nothing third-party loads until someone says
 * yes. A banner shown while the map iframe is already loading is worthless:
 * by then Google has the visitor's IP and has set its cookies, and under the
 * ePrivacy Directive consent has to come first. So map.liquid renders a
 * placeholder carrying data-consent-src, and the iframe is only built here,
 * after a decision.
 *
 * Storage: one localStorage key recording the decision and when it was made.
 * Storing the answer is itself "strictly necessary" for honouring it, so it
 * does not need consent - but a rejection is remembered just as firmly as an
 * acceptance, which is the point.
 */
(function () {
  "use strict";

  var KEY = "igs.consent.v1";
  var CATEGORY = "embeds";

  function read() {
    try {
      return JSON.parse(window.localStorage.getItem(KEY) || "null");
    } catch (e) {
      // Private browsing, or storage disabled. Treat as undecided and simply
      // never load the third-party content.
      return null;
    }
  }

  function write(granted) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify({ embeds: granted, at: new Date().toISOString() }));
    } catch (e) {
      /* nothing we can do; the decision just will not persist */
    }
  }

  function loadEmbeds() {
    var slots = document.querySelectorAll("[data-consent-src]");
    Array.prototype.forEach.call(slots, function (slot) {
      if (slot.dataset.consentLoaded) return;
      var frame = document.createElement("iframe");
      frame.src = slot.dataset.consentSrc;
      frame.title = slot.dataset.consentTitle || "Embedded content";
      frame.loading = "lazy";
      frame.referrerPolicy = "no-referrer-when-downgrade";
      frame.setAttribute("allowfullscreen", "");
      slot.innerHTML = "";
      slot.appendChild(frame);
      slot.dataset.consentLoaded = "1";
    });
  }

  function showPlaceholders() {
    var slots = document.querySelectorAll("[data-consent-src]");
    Array.prototype.forEach.call(slots, function (slot) {
      slot.dataset.consentLoaded = "";
      var note = slot.querySelector(".consent-slot-note");
      if (note) note.hidden = false;
      var frame = slot.querySelector("iframe");
      if (frame) frame.remove();
    });
  }

  function setBannerVisible(visible) {
    var banner = document.getElementById("consent-banner");
    if (banner) banner.hidden = !visible;
  }

  function decide(granted) {
    write(granted);
    setBannerVisible(false);
    if (granted) loadEmbeds();
    else showPlaceholders();
  }

  function init() {
    var state = read();

    if (state && state[CATEGORY] === true) {
      loadEmbeds();
    } else if (state && state[CATEGORY] === false) {
      showPlaceholders();
    } else {
      showPlaceholders();
      setBannerVisible(true);
    }

    var accept = document.getElementById("consent-accept");
    var reject = document.getElementById("consent-reject");
    if (accept)
      accept.addEventListener("click", function () {
        decide(true);
      });
    if (reject)
      reject.addEventListener("click", function () {
        decide(false);
      });

    // Per-slot opt-in: loading one map is also an act of consent, so record it
    // rather than asking again on the next page.
    document.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest(".consent-slot-load") : null;
      if (!btn) return;
      e.preventDefault();
      decide(true);
    });

    // Footer link, so a decision can always be changed.
    var reopen = document.getElementById("consent-reopen");
    if (reopen) {
      reopen.addEventListener("click", function (e) {
        e.preventDefault();
        setBannerVisible(true);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

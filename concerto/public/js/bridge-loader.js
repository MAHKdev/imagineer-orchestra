/**
 * Concerto bridge loader -- auto-injected by the Concerto Frappe app
 * via app_include_js (Desk pages) and web_include_js (website pages).
 *
 *   1. Calls /api/method/concerto.api.concerto_config (same-origin, session
 *      cookie) to get the Orchestra URL + this user's API credentials.
 *      Falls back to the legacy /api/method/concerto_config Server Script
 *      for sites that still have it installed.
 *   2. If the config says enabled === false, aborts -- nothing is injected.
 *   3. Fetches ORCHESTRA_URL/concerto/bridge.js from the Orchestra server
 *      and injects it as a <script> tag.
 *
 * bridge.js updates are automatic: every instance fetches it fresh from
 * Orchestra on each page load. This file should never need to change.
 *
 * NOTE: keep this file ASCII-only -- non-ASCII characters get corrupted
 *       by some upload/pack pipelines and break the JS parser.
 */

(function () {
  "use strict";

  // Used only if no config endpoint answers at all.
  var FALLBACK_ORCHESTRA_URL = "https://orchestra.imagineer.solutions";

  if (window.__concertoBridge || window.__concertoLoader) return;
  window.__concertoLoader = true;

  console.log("[concerto-loader] Starting...");

  async function callConfig(endpoint) {
    try {
      var response = await fetch(endpoint, {
        method: "GET",
        credentials: "same-origin",
      });
      if (!response.ok) return null;
      var data = await response.json();
      return data.message || null;
    } catch (err) {
      return null;
    }
  }

  async function getConfig() {
    // App method first, legacy Server Script name second.
    var config = await callConfig("/api/method/concerto.api.concerto_config");
    if (!config) {
      config = await callConfig("/api/method/concerto_config");
    }
    return config;
  }

  function injectBridge(orchestraUrl, config) {
    window.__CONCERTO_ORCHESTRA_URL = orchestraUrl.replace(/\/$/, "");
    // Per-user credentials for the HMAC handshake, read by bridge.js.
    window.__CONCERTO_CONFIG = config || {};

    var script = document.createElement("script");
    script.src = window.__CONCERTO_ORCHESTRA_URL + "/concerto/bridge.js";
    script.async = true;
    script.onerror = function () {
      console.error("[concerto-loader] Failed to load bridge.js from:", script.src);
    };
    script.onload = function () {
      console.log("[concerto-loader] bridge.js loaded from:", script.src);
    };

    (document.head || document.documentElement).appendChild(script);
  }

  async function init() {
    var config = await getConfig();

    if (config && config.enabled === false) {
      console.log("[concerto-loader] Concerto is disabled in Orchestra Settings -- skipping.");
      return;
    }

    var orchestraUrl = (config && config.orchestra_url) || FALLBACK_ORCHESTRA_URL;
    if (!config || !config.orchestra_url) {
      console.warn("[concerto-loader] No orchestra_url configured -- using fallback:", orchestraUrl);
    }

    injectBridge(orchestraUrl, config);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

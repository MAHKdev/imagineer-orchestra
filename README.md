<p align="center">
  <img src="concerto/public/images/orchestra-logo.png" alt="Orchestra AI" width="120" />
</p>

<h1 align="center">Concerto — Orchestra AI for ERPNext</h1>

<p align="center">
  Embed the <a href="https://orchestra.imagineer.solutions">Orchestra AI</a> assistant inside ERPNext —
  one install, no Server Scripts, no manual JS injection.
</p>

---

## What it does

Installing Concerto gives every logged-in ERPNext user an Orchestra AI chat
launcher — a floating bubble on Desk and website pages, expandable to a
sidebar or full window.

Each user chats **as themselves**: Concerto issues per-user ERPNext API
credentials, so the AI respects your existing role-based permissions.

```
bench get-app concerto <repo-url>
bench --site your.site install-app concerto
→ done. No Server Script, no File Manager upload, no desk.html patch.
```

## How it works

```
Concerto app (this repo — installed once per site)
│
├── app_include_js / web_include_js
│   └── bridge-loader.js auto-injected on Desk + website pages
│
├── concerto.api.concerto_config  (whitelisted method)
│   └── returns Orchestra URL + per-user API key/secret
│
└── Orchestra Settings (single DocType)
    └── enable/disable + Orchestra URL — replaces site_config.json

At runtime, bridge-loader.js fetches bridge.js and the /embed chat UI
from the Orchestra server — so UI updates ship server-side and every
instance picks them up automatically. Nothing else lives per-instance.
```

## Setup

1. Install the app (above).
2. Reload any Desk page — the Orchestra launcher appears bottom-right.
   Enabled by default on install; Desk → search **"Orchestra Settings"**
   to change the **Orchestra URL** or switch it off.

Optional: `orchestra_url` in `site_config.json` still works as a fallback,
and existing `concerto_config` Server Scripts are auto-detected.

## Security model

| Layer | Mechanism |
|-------|-----------|
| Loader → `concerto_config` | Same-origin session cookie; Guests get 403 |
| Per-user credentials | Each user's own API key/secret — generated lazily, `api_secret` stays in `__Auth` |
| Bridge → iframe | `postMessage` with HMAC-signed nonce (secret never exposed to the iframe) |
| Iframe → Orchestra | HMAC verification + ERPNext credential check; AES-256-GCM at rest |
| Kill switch | Uncheck **Enabled** in Orchestra Settings — launcher stops injecting |

## UI modes

Closed bubble · chatbot popup (380×550) · docked sidebar (420px) ·
fullwidth · new tab — switchable from the chat header.

## License

MIT — see [LICENSE](LICENSE).

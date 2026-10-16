"""
Concerto — Orchestra AI bridge for ERPNext.

A thin Frappe app that embeds the Orchestra AI chat (orchestra.imagineer.solutions)
inside ERPNext on Desk and website pages.

One install replaces the manual 4-step setup:
  - app_include_js / web_include_js inject bridge-loader.js automatically
    (no File Manager upload, no desk.html patch)
  - concerto.api.concerto_config replaces the concerto_config Server Script
    (no server_script_enabled needed — this is a normal whitelisted method)
  - Orchestra Settings doctype replaces site_config.json editing

No bundled UI. bridge-loader.js fetches bridge.js + the /embed chat UI
from the Orchestra server at runtime, so updates ship server-side.
"""

from . import __version__ as app_version

app_name = "concerto"
app_title = "Concerto — Orchestra AI"
app_publisher = "Imagineer"
app_description = (
    "Embeds the Orchestra AI assistant inside ERPNext — floating chat launcher on Desk "
    "and website pages, with per-user ERPNext credentials so the AI respects role-based "
    "permissions. One install; no Server Scripts or manual JS injection required."
)
app_icon = "octicon octicon-broadcast"
app_color = "purple"
app_email = "hello@imagineer.solutions"
app_license = "MIT"


# Auto-inject the bridge loader on every Desk page and every website/portal page.
# The loader is ~100 lines: it calls concerto.api.concerto_config (same-origin)
# for the Orchestra URL + per-user API credentials, then fetches the real
# bridge.js from the Orchestra server.
app_include_js = "/assets/concerto/js/bridge-loader.js"
web_include_js = "/assets/concerto/js/bridge-loader.js"

# Show Orchestra on the Desk "Apps" screen with the Orchestra icon.
# Clicking it opens Orchestra in a new tab (full-window mode).
add_to_apps_screen = [
    {
        "name": "concerto",
        "logo": "/assets/concerto/images/orchestra-logo.svg",
        "title": "Orchestra AI",
        "route": "https://orchestra.imagineer.solutions",
        "has_permission": "concerto.api.has_app_permission",
    }
]

# DocType assets
doctype_js = {
    "Orchestra Settings": "public/js/orchestra_settings.js",
}


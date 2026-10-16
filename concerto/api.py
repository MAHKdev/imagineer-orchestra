"""
Concerto API — replaces the concerto_config Server Script.

Because this is a normal whitelisted method (not a RestrictedPython Server
Script), it can read both the Orchestra Settings doctype and site_config.json.

Public methods:
  - concerto_config()  — called by bridge-loader.js (same-origin, session
    cookie). Returns the Orchestra URL + the current user's API credentials.
  - has_app_permission() — gate for the Apps-screen entry.
"""

import frappe

DEFAULT_ORCHESTRA_URL = "https://orchestra.imagineer.solutions"


@frappe.whitelist()
def concerto_config():
    """Return {enabled, orchestra_url, api_key, api_secret, user, site}.

    bridge-loader.js calls this first. If enabled is falsy, the loader aborts
    and does not inject the bridge — that is the runtime kill-switch.

    API keys live on the User doctype (api_key field + api_secret stored in
    the __Auth table). When missing, we generate them via doc.save() — using
    frappe.db.set_value would bypass Password-field encryption.
    """
    user = frappe.session.user
    if user == "Guest":
        frappe.throw("Must be logged in to use Concerto")

    settings = _get_settings()
    if not (settings and settings.enabled):
        return {"enabled": False, "user": user, "site": frappe.utils.get_url()}

    api_key = frappe.db.get_value("User", user, "api_key")
    if api_key:
        api_secret = frappe.get_doc("User", user).get_password("api_secret")
    else:
        api_key = frappe.generate_hash(length=20)
        api_secret = frappe.generate_hash(length=20)
        user_doc = frappe.get_doc("User", user)
        user_doc.api_key = api_key
        user_doc.api_secret = api_secret
        user_doc.save(ignore_permissions=True)

    return {
        "enabled": True,
        "orchestra_url": _orchestra_url(settings),
        "api_key": api_key,
        "api_secret": api_secret,
        "user": user,
        "site": frappe.utils.get_url(),
    }


def has_app_permission():
    """Apps-screen gate: only show the Orchestra entry when enabled."""
    settings = _get_settings()
    return bool(settings and settings.enabled)


def _orchestra_url(settings=None):
    """Priority: Orchestra Settings > site_config.json > production default."""
    if settings and settings.orchestra_url:
        return settings.orchestra_url.rstrip("/")
    url = frappe.conf.get("orchestra_url")
    return (url.rstrip("/") if url else DEFAULT_ORCHESTRA_URL)


def _get_settings():
    """Orchestra Settings singleton; None if the doctype/row doesn't exist."""
    try:
        return frappe.get_doc("Orchestra Settings", "Orchestra Settings")
    except Exception:
        return None

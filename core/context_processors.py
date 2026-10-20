import json
from urllib.parse import quote_plus

from django.conf import settings
from django.utils.safestring import mark_safe


def _json_ld(request):
    """schema.org LocalBusiness data for search engines, as a script-safe JSON string."""
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": settings.SITE_NAME,
        "description": settings.SITE_DESCRIPTION,
        "url": request.build_absolute_uri("/"),
    }
    if settings.SITE_ADDRESS:
        data["address"] = {"@type": "PostalAddress", "streetAddress": settings.SITE_ADDRESS, "addressCountry": "RO"}
    if settings.SITE_PHONE:
        data["telephone"] = settings.SITE_PHONE
    if settings.SITE_EMAIL:
        data["email"] = settings.SITE_EMAIL
    # "<" is escaped so the value can never close the surrounding <script> tag.
    return mark_safe(json.dumps(data, ensure_ascii=False).replace("<", "\\u003c"))


def site(request):
    maps_url = settings.MAPS_EMBED_URL
    if not maps_url and settings.SITE_ADDRESS:
        maps_url = f"https://www.google.com/maps?q={quote_plus(settings.SITE_ADDRESS)}&output=embed"
    maps_link = f"https://www.google.com/maps/search/?api=1&query={quote_plus(settings.SITE_ADDRESS)}" if settings.SITE_ADDRESS else ""
    return {
        "site": {
            "name": settings.SITE_NAME,
            "description": settings.SITE_DESCRIPTION,
            "address": settings.SITE_ADDRESS,
            "phone": settings.SITE_PHONE,
            "phone_href": "".join(c for c in settings.SITE_PHONE if c.isdigit() or c == "+"),
            "email": settings.SITE_EMAIL,
            "maps_url": maps_url,
            "maps_link": maps_link,
            "json_ld": _json_ld(request),
        }
    }

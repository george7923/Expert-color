from urllib.parse import quote_plus

from django.conf import settings


def site(request):
    maps_url = settings.MAPS_EMBED_URL
    if not maps_url and settings.SITE_ADDRESS:
        maps_url = f"https://www.google.com/maps?q={quote_plus(settings.SITE_ADDRESS)}&output=embed"
    return {
        "site": {
            "name": settings.SITE_NAME,
            "address": settings.SITE_ADDRESS,
            "phone": settings.SITE_PHONE,
            "phone_href": "".join(c for c in settings.SITE_PHONE if c.isdigit() or c == "+"),
            "email": settings.SITE_EMAIL,
            "maps_url": maps_url,
        }
    }

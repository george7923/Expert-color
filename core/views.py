from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

COD_CULOARE_IMPLICIT = "LY9B"

PRODUSE = [
    {"slug": "spray", "nume": "Spray vopsea auto", "pret": 50, "descriere": "Pentru suprafețe mari și retușuri rapide, cu strat uniform."},
    {"slug": "marker", "nume": "Marker", "pret": 25, "descriere": "Pentru zgârieturi liniare fine, cu vârf comod."},
    {"slug": "punctator", "nume": "Punctator", "pret": 25, "descriere": "Pentru mici sărituri de vopsea și puncte precise."},
    {"slug": "sticluta", "nume": "Sticluță de retuș", "pret": 20, "descriere": "Vopsea lichidă, aplicată cu pensula, pentru retușuri."},
]


def home(request):
    produse = [{**p, "template": f"core/products/{p['slug']}.html"} for p in PRODUSE]
    pret_min = min(p["pret"] for p in PRODUSE)
    contact = f" Sună {settings.SITE_PHONE}." if settings.SITE_PHONE else ""
    return render(
        request,
        "core/home.html",
        {
            "produse": produse,
            "pret_spray": PRODUSE[0]["pret"],
            "cod_culoare": COD_CULOARE_IMPLICIT,
            "titlu": f"Vopsea auto Constanța – după cod culoare, de la {pret_min} lei",
            "description": (
                "Vopsea auto preparată după codul culorii mașinii tale: spray, marker, punctator, "
                f"sticluță. De la {pret_min} lei.{contact} {settings.SITE_NAME}, Constanța."
            ),
        },
    )


def cookies(request):
    return render(request, "core/cookies.html")


def robots(request):
    sitemap = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    body = f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {sitemap}\n"
    return HttpResponse(body, content_type="text/plain")

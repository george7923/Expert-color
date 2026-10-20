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
    return render(
        request,
        "core/home.html",
        {
            "produse": produse,
            "pret_spray": PRODUSE[0]["pret"],
            "cod_culoare": COD_CULOARE_IMPLICIT,
            "description": (
                "Vopsele auto preparate după codul de culoare al mașinii tale: spray vopsea auto "
                f"de la {PRODUSE[0]['pret']} lei, marker, punctator și sticluță de retuș. Romcast Expert, Constanța."
            ),
        },
    )


def cookies(request):
    return render(request, "core/cookies.html")


def robots(request):
    sitemap = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    body = f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {sitemap}\n"
    return HttpResponse(body, content_type="text/plain")

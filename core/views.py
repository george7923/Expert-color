from django.shortcuts import render

COD_CULOARE_IMPLICIT = "LY9B"

PRODUSE = [
    {"slug": "spray", "nume": "Spray vopsea auto", "pret": 50},
    {"slug": "marker", "nume": "Marker", "pret": 25},
    {"slug": "punctator", "nume": "Punctator", "pret": 25},
    {"slug": "sticluta", "nume": "Sticluță de retuș", "pret": 20},
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
        },
    )

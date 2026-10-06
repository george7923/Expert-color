from django.shortcuts import render

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
        },
    )

from django.contrib import admin

from .models import (
    Adresa,
    AdresaUtilizator,
    Card,
    Categorie,
    Comanda,
    Cos,
    Imagine,
    Judet,
    Localitate,
    Marca,
    ModelAuto,
    Persoana,
    PretProdus,
    Produs,
    Strada,
    Subcomanda,
    Subprodus,
    Tara,
    Utilizator,
    UtilizatorCard,
    Vopsea,
)

admin.site.register(Tara)
admin.site.register(Judet)
admin.site.register(Localitate)
admin.site.register(Strada)
admin.site.register(Adresa)
admin.site.register(Marca)
admin.site.register(ModelAuto)
admin.site.register(Categorie)
admin.site.register(Persoana)
admin.site.register(Utilizator)
admin.site.register(AdresaUtilizator)
admin.site.register(Card)
admin.site.register(UtilizatorCard)
admin.site.register(Produs)
admin.site.register(Imagine)
admin.site.register(PretProdus)
admin.site.register(Vopsea)
admin.site.register(Cos)
admin.site.register(Subprodus)
admin.site.register(Comanda)
admin.site.register(Subcomanda)

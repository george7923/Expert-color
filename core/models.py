from django.db import models


# --- Geography -------------------------------------------------------------

class Tara(models.Model):
    id_tara = models.AutoField(primary_key=True, db_column="IdTara")
    denumire_tara = models.CharField(max_length=450, unique=True, db_column="DenumireTara")

    class Meta:
        db_table = "Tari"

    def __str__(self):
        return self.denumire_tara


class Judet(models.Model):
    id_judet = models.AutoField(primary_key=True, db_column="IdJudet")
    denumire_judet = models.CharField(max_length=450, unique=True, db_column="DenumireJudet")
    tara = models.ForeignKey(Tara, on_delete=models.PROTECT, db_column="IdTara", related_name="judete")

    class Meta:
        db_table = "Judete"

    def __str__(self):
        return self.denumire_judet


class Localitate(models.Model):
    id_localitate = models.AutoField(primary_key=True, db_column="IdLocalitate")
    denumire_localitate = models.TextField(db_column="DenumireLocalitate")
    judet = models.ForeignKey(Judet, on_delete=models.PROTECT, db_column="IdJudet", related_name="localitati")

    class Meta:
        db_table = "Localitati"

    def __str__(self):
        return self.denumire_localitate


class Strada(models.Model):
    id_strada = models.AutoField(primary_key=True, db_column="IdStrada")
    denumire_strada = models.CharField(max_length=450, unique=True, db_column="DenumireStrada")
    nr = models.IntegerField(db_column="Nr")
    localitate = models.ForeignKey(Localitate, on_delete=models.PROTECT, db_column="IdLocalitate", related_name="strazi")

    class Meta:
        db_table = "Strazi"

    def __str__(self):
        return self.denumire_strada


class Adresa(models.Model):
    id_adresa = models.AutoField(primary_key=True, db_column="IdAdresa")
    strada = models.ForeignKey(Strada, on_delete=models.PROTECT, db_column="IdStrada", related_name="adrese")
    bloc = models.TextField(null=True, blank=True, db_column="Bloc")
    scara = models.TextField(null=True, blank=True, db_column="Scara")
    etaj = models.TextField(null=True, blank=True, db_column="Etaj")
    apartament = models.TextField(null=True, blank=True, db_column="Apartament")

    class Meta:
        db_table = "Adrese"

    def __str__(self):
        return f"Adresa #{self.pk}"


# --- Vehicles ----------------------------------------------------------------

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True, db_column="IdMarca")
    nume_marca = models.CharField(max_length=100, db_column="NumeMarca")

    class Meta:
        db_table = "Marci"

    def __str__(self):
        return self.nume_marca


class ModelAuto(models.Model):
    id_model = models.AutoField(primary_key=True, db_column="IdModel")
    nume_model = models.CharField(max_length=100, db_column="NumeModel")
    an = models.IntegerField(null=True, blank=True, db_column="An")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, db_column="IdMarca", related_name="modele")

    class Meta:
        db_table = "Modele"

    def __str__(self):
        return self.nume_model


# --- People & accounts -------------------------------------------------------

class Categorie(models.Model):
    id_categorie = models.AutoField(primary_key=True, db_column="IdCategorie")
    denumire_categorie = models.CharField(max_length=100, unique=True, db_column="DenumireCategorie")
    descriere_categorie = models.TextField(db_column="DescriereCategorie")

    class Meta:
        db_table = "Categorii"

    def __str__(self):
        return self.denumire_categorie


class Persoana(models.Model):
    id_persoana = models.AutoField(primary_key=True, db_column="IdPersoana")
    nume = models.TextField(db_column="Nume")
    prenume = models.TextField(db_column="Prenume")
    email = models.CharField(max_length=450, unique=True, db_column="Email")
    tip_persoana = models.TextField(db_column="tipPersoana")  # observed: "Fizica" / "Juridica"
    telefon = models.CharField(max_length=450, null=True, blank=True, db_column="Telefon")
    rol = models.TextField(db_column="Rol")  # observed: "Owner" / "Administrator" / "Participant"

    class Meta:
        db_table = "Persoane"

    def __str__(self):
        return f"{self.nume} {self.prenume}"


class Utilizator(models.Model):
    """Maps to the C# `Users` table. Named Utilizator to avoid clashing with Django's built-in auth User."""

    id_user = models.AutoField(primary_key=True, db_column="IdUser")
    username = models.CharField(max_length=450, unique=True, db_column="Username")
    password = models.TextField(db_column="Password")
    persoana = models.ForeignKey(Persoana, on_delete=models.PROTECT, db_column="IdPersoana", related_name="useri")

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.username


class AdresaUtilizator(models.Model):
    """Maps to `Adrese_Useri` — join table between Users and Adrese."""

    id_au = models.AutoField(primary_key=True, db_column="idAU")
    utilizator = models.ForeignKey(Utilizator, on_delete=models.PROTECT, db_column="IdUser", related_name="adrese_useri")
    adresa = models.ForeignKey(Adresa, on_delete=models.PROTECT, db_column="IdAdresa", related_name="adrese_useri")

    class Meta:
        db_table = "Adrese_Useri"

    def __str__(self):
        return f"{self.utilizator} - {self.adresa}"


# --- Payment cards -------------------------------------------------------------

class Card(models.Model):
    id_card = models.AutoField(primary_key=True, db_column="IdCard")
    numar_card = models.CharField(max_length=255, unique=True, db_column="NumarCard")
    cvv = models.TextField(db_column="CVV")
    data_expirare = models.DateTimeField(db_column="DataExpirare")

    class Meta:
        db_table = "Carduri"

    def __str__(self):
        return self.numar_card


class UtilizatorCard(models.Model):
    """Maps to `Useri_Carduri` — join table between Users and Carduri."""

    id_uc = models.AutoField(primary_key=True, db_column="idUC")
    utilizator = models.ForeignKey(Utilizator, on_delete=models.PROTECT, db_column="IdUser", related_name="useri_carduri")
    card = models.ForeignKey(Card, on_delete=models.PROTECT, db_column="IdCard", related_name="useri_carduri")
    data_adaugarii = models.DateTimeField(db_column="DataAdaugarii")

    class Meta:
        db_table = "Useri_Carduri"

    def __str__(self):
        return f"{self.utilizator} - {self.card}"


# --- Catalog -------------------------------------------------------------------

class Produs(models.Model):
    id_produs = models.AutoField(primary_key=True, db_column="IdProdus")
    nume = models.TextField(db_column="Nume")
    descriere = models.TextField(null=True, blank=True, db_column="Descriere")
    este_spray = models.BooleanField(db_column="EsteSpray")
    valabil = models.BooleanField(db_column="Valabil")
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, db_column="IdCategorie", related_name="produse")
    utilizator = models.ForeignKey(
        Utilizator, on_delete=models.SET_NULL, null=True, blank=True, db_column="IdUser", related_name="produse"
    )

    class Meta:
        db_table = "Products"

    def __str__(self):
        return self.nume


class Imagine(models.Model):
    id_imagine = models.AutoField(primary_key=True, db_column="idImagine")
    fisier = models.BinaryField(db_column="Fisier")
    produs = models.ForeignKey(Produs, on_delete=models.PROTECT, db_column="IdProdus", related_name="imagini")

    class Meta:
        db_table = "Imagini"

    def __str__(self):
        return f"Imagine #{self.pk} ({self.produs})"


class PretProdus(models.Model):
    id_pp = models.AutoField(primary_key=True, db_column="idPP")
    produs = models.ForeignKey(Produs, on_delete=models.PROTECT, db_column="IdProdus", related_name="preturi")
    pret = models.DecimalField(max_digits=18, decimal_places=2, db_column="Pret")
    data_inceput = models.DateTimeField(db_column="DataInceput")
    data_expirare = models.DateTimeField(null=True, blank=True, db_column="DataExpirare")
    comision = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, db_column="Comision")

    class Meta:
        db_table = "Preturi_Produs"

    def __str__(self):
        return f"{self.produs} - {self.pret}"


class Vopsea(models.Model):
    id_vopsea = models.AutoField(primary_key=True, db_column="idVopsea")
    tip_vopsea = models.TextField(db_column="TipVopsea")
    cod_culoare = models.CharField(max_length=100, null=True, blank=True, db_column="CodCuloare")
    serie_caroserie = models.CharField(max_length=100, null=True, blank=True, db_column="SerieCaroserie")
    produs = models.ForeignKey(Produs, on_delete=models.PROTECT, db_column="IdProdus", related_name="vopsele")
    model = models.ForeignKey(
        ModelAuto, on_delete=models.SET_NULL, null=True, blank=True, db_column="IdModel", related_name="vopsele"
    )

    class Meta:
        db_table = "Vopsele"
        constraints = [
            models.UniqueConstraint(
                fields=["cod_culoare", "serie_caroserie"], name="UQ_CodCuloare_SerieCaroserie"
            )
        ]

    def __str__(self):
        return f"{self.tip_vopsea} ({self.cod_culoare or '-'})"


# --- Shopping cart ---------------------------------------------------------------

class Cos(models.Model):
    id_cos = models.AutoField(primary_key=True, db_column="idCos")
    cod_unic = models.TextField(db_column="CodUnic")
    utilizator = models.ForeignKey(Utilizator, on_delete=models.PROTECT, db_column="IdUser", related_name="cosuri")
    data_creare = models.DateTimeField(db_column="DataCreare")

    class Meta:
        db_table = "Cosuri"

    def __str__(self):
        return self.cod_unic


class Subprodus(models.Model):
    id_subprodus = models.AutoField(primary_key=True, db_column="IdSubprodus")
    produs = models.ForeignKey(Produs, on_delete=models.PROTECT, db_column="IdProdus", related_name="subproduse")
    valabil = models.BooleanField(db_column="Valabil")
    cos = models.ForeignKey(
        Cos, on_delete=models.SET_NULL, null=True, blank=True, db_column="idCos", related_name="subproduse"
    )

    class Meta:
        db_table = "SubProduse"

    def __str__(self):
        return f"Subprodus #{self.pk} ({self.produs})"


# --- Orders ----------------------------------------------------------------------

class Comanda(models.Model):
    id_comanda = models.AutoField(primary_key=True, db_column="IdComanda")
    utilizator = models.ForeignKey(Utilizator, on_delete=models.PROTECT, db_column="IdUser", related_name="comenzi")
    adresa = models.ForeignKey(Adresa, on_delete=models.PROTECT, db_column="IdAdresa", related_name="comenzi")
    card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, null=True, blank=True, db_column="IdCard_CC", related_name="comenzi"
    )
    eta = models.DateTimeField(null=True, blank=True, db_column="ETA")
    pret_total = models.FloatField(db_column="PretTotal")
    is_placed = models.BooleanField(db_column="IsPlaced")

    class Meta:
        db_table = "Comenzi"

    def __str__(self):
        return f"Comanda #{self.pk}"


class Subcomanda(models.Model):
    id_subcomanda = models.AutoField(primary_key=True, db_column="IdSubcomanda")
    produs = models.ForeignKey(Produs, on_delete=models.PROTECT, db_column="IdProdus", related_name="subcomenzi")
    total_subproduse = models.IntegerField(db_column="TotalSubproduse")
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, db_column="IdComanda", related_name="subcomenzi")

    class Meta:
        db_table = "Subcomenzi"

    def __str__(self):
        return f"Subcomanda #{self.pk} ({self.produs})"

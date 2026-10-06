from django.contrib.auth.models import AbstractUser
from django.db import models


class Rol(models.Model):
    OWNER = "Owner"

    id_rol = models.AutoField(primary_key=True, db_column="IdRol")
    nume = models.CharField(max_length=50, unique=True, db_column="Nume")

    class Meta:
        db_table = "Roluri"

    def __str__(self):
        return self.nume


class Utilizator(AbstractUser):
    """Custom auth user (AUTH_USER_MODEL). Named Utilizator to match the rest of the domain naming."""

    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True, db_column="IdRol", related_name="useri")

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.username

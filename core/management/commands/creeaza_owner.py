import os

from django.core.management.base import BaseCommand, CommandError

from core.models import Rol, Utilizator


class Command(BaseCommand):
    help = "Creates the single Owner user from OWNER_USERNAME / OWNER_PASSWORD / OWNER_EMAIL, if no user exists yet."

    def handle(self, *args, **options):
        if Utilizator.objects.exists():
            self.stdout.write("A user already exists, skipping.")
            return

        username = os.environ.get("OWNER_USERNAME")
        password = os.environ.get("OWNER_PASSWORD")
        if not username or not password:
            raise CommandError("Set OWNER_USERNAME and OWNER_PASSWORD to create the owner.")

        rol, _ = Rol.objects.get_or_create(nume=Rol.OWNER)
        Utilizator.objects.create_superuser(
            username=username,
            email=os.environ.get("OWNER_EMAIL", ""),
            password=password,
            rol=rol,
        )
        self.stdout.write(self.style.SUCCESS(f"Owner '{username}' created."))

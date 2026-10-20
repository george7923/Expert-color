#!/usr/bin/env python3
"""Create the production .env from .env.prod.example. Run it on the server.

Generates the Django secret key and the database password, asks for the owner account,
and never prints a secret. Set OWNER_PASSWORD in the environment to skip the prompt.
"""
import getpass
import os
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / ".env.prod.example"
TARGET = ROOT / ".env"
FORBIDDEN = set(" $#\"'\\`")


def ask(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    return input(f"{prompt}{suffix}: ").strip() or default


def ask_password():
    password = os.environ.get("OWNER_PASSWORD")
    if password:
        return password
    while True:
        first = getpass.getpass("Parola contului owner (minim 12 caractere, fara spatii sau $ # \" ' \\ `): ")
        if len(first) < 12 or FORBIDDEN & set(first):
            print("Parola nu respecta regulile. Incearca din nou.")
        elif getpass.getpass("Repeta parola: ") != first:
            print("Parolele nu sunt la fel. Incearca din nou.")
        else:
            return first


def parse(lines):
    return {l.split("=", 1)[0]: l.split("=", 1)[1] for l in lines if l and not l.startswith("#") and "=" in l}


def main():
    if TARGET.exists() and ask(f"{TARGET.name} exista deja. Il suprascriu? (da/nu)", "nu").lower() != "da":
        sys.exit("Nu am schimbat nimic.")

    lines = EXAMPLE.read_text().splitlines()
    defaults = parse(lines)

    domain = ask("Domeniul", "romcastexpert.ro").lower().removeprefix("www.")
    username = ask("Numele contului owner", "owner_expertcolor")
    email = ask("Emailul owner-ului", defaults.get("SITE_EMAIL", "").split("#")[0].strip())
    password = ask_password()

    values = {
        "DJANGO_SECRET_KEY": secrets.token_urlsafe(50),
        "DJANGO_DEBUG": "False",
        "DJANGO_ALLOWED_HOSTS": f"{domain},www.{domain}",
        "DJANGO_CSRF_TRUSTED_ORIGINS": f"https://{domain},https://www.{domain}",
        "DB_PASSWORD": secrets.token_urlsafe(24),
        "OWNER_USERNAME": username,
        "OWNER_PASSWORD": password,
        "OWNER_EMAIL": email,
    }

    out, seen = [], set()
    for line in lines:
        key = line.split("=", 1)[0]
        if not line.startswith("#") and key in values:
            out.append(f"{key}={values[key]}")
            seen.add(key)
        else:
            out.append(line)
    out += [f"{k}={v}" for k, v in values.items() if k not in seen]

    TARGET.write_text("\n".join(out) + "\n")
    TARGET.chmod(0o600)
    print(f"\nGata: {TARGET} a fost creat pentru {domain}.")
    print(f"Cont owner: {username} ({email}). Parola, cheia secretă și parola bazei de date nu sunt afișate.")


if __name__ == "__main__":
    main()

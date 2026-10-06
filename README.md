# Expert Color

v0.1 — simple Django site showing the Expert Color touch-up paint products (spray, marker, punctator, touch-up bottle), drawn with HTML/CSS/JS. The only database content is the `Roluri` and `Users` tables, with a single user holding the `Owner` role.

## Run

```
cp .env.example .env      # set OWNER_USERNAME / OWNER_PASSWORD
docker compose up --build
```

- Site: http://localhost:8000/
- Admin (log in as the owner): http://localhost:8000/admin/

On start-up the container applies migrations and runs `python manage.py creeaza_owner`, which creates the owner from `OWNER_USERNAME` / `OWNER_PASSWORD` / `OWNER_EMAIL` if no user exists yet.

If you ran an earlier version, reset its database first: `docker compose down -v`.

## Deploy (VPS + Docker + Caddy)

Production uses `docker-compose.prod.yml` (gunicorn, Postgres, and Caddy for automatic HTTPS) and `Caddyfile`, which names the domain.

1. Point the domain's DNS `A` records (`@` and `www`) at the server's IP.
2. On the server (Docker installed, ports 80 and 443 open): clone the repo, then `cp .env.prod.example .env` and fill in every value.
3. `docker compose -f docker-compose.prod.yml up -d --build`
4. Update later with `git pull` and the same `up -d --build`.

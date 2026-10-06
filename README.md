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

# Disc Golf Tracker

Disc Golf Tracker is a self-hosted, multi-user disc golf scoring and inventory application. Version 0.1 will combine course and shared-round scoring, personal disc inventory, statistics, and an illustrative Flight Lab in one installable PWA.

The project is in active development. The current foundation provides:

- a FastAPI API with SQLite migrations and health/readiness checks;
- one-time local administrator bootstrap and password login;
- a React + TypeScript PWA shell;
- a multi-stage, non-root, single-image container build; and
- a public Compose example with persistent application data.

## Quick start

1. Copy `.env.example` to `.env` and replace both generated secret values.
2. Run `docker compose up --build`.
3. Open `http://localhost:8080` and create the first administrator with the bootstrap token.

The bootstrap route closes permanently after the first account is created. Remove `DGT_BOOTSTRAP_TOKEN` from the environment after bootstrap.

## Development

Backend:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
DGT_ENVIRONMENT=development DGT_SECRET_KEY=development-only-secret-key-change-me DGT_BOOTSTRAP_TOKEN=development-bootstrap-token uvicorn disc_golf_tracker.main:create_app --factory --reload
```

Frontend (Node 22 or later):

```sh
cd frontend
pnpm install
pnpm run dev
```

Run backend tests with `pytest` and frontend checks with `pnpm test` and `pnpm run build`.

## Project boundaries

The public application has no dependency on Authentik, Traefik, Cloudflare, or Ansible. Optional OIDC and private homelab deployment automation will be added separately. See [Architecture](docs/architecture.md), [Security](docs/security.md), and [Roadmap](docs/roadmap.md).

No license has been selected yet; all rights remain reserved until a license file is added.

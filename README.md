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
2. Run `docker compose up -d`.
3. Open `http://localhost:8080` and create the first administrator with the bootstrap token.

Until Version 0.1 is tagged, the Compose example defaults to the continuously built `edge` image. Set `DGT_IMAGE_TAG` to a released version when one is available.

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

To test a locally built image instead of pulling a published release:

```sh
docker build -t ghcr.io/thwena/disc-golf-tracker:dev .
DGT_IMAGE_TAG=dev docker compose up --pull never
```

## Container releases

GitHub Actions publishes multi-platform images to `ghcr.io/thwena/disc-golf-tracker`:

- merges to `main` publish immutable `sha-...` and moving `edge` tags;
- a Git tag such as `v0.1.0` publishes `0.1.0` and `latest` tags; and
- every published image includes a signed build-provenance attestation.

Deployments should pin a version or digest rather than `edge` or `latest`.

## Project boundaries

The public application has no dependency on Authentik, Traefik, Cloudflare, or Ansible. Optional OIDC and private homelab deployment automation will be added separately. See [Architecture](docs/architecture.md), [Security](docs/security.md), and [Roadmap](docs/roadmap.md).

No license has been selected yet; all rights remain reserved until a license file is added.

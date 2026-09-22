# Architecture

## Decision: React, FastAPI, and SQLite

Status: accepted for the Version 0.1 foundation.

React with TypeScript supports the touch-first PWA and later local/offline scorecard state. FastAPI provides typed HTTP contracts and straightforward Python data/import work. SQLite is an operationally simple fit for a small self-hosted group, while WAL, foreign keys, bounded busy waits, transactions, and explicit conflict versions will protect common concurrent writes.

This is not a claim of unlimited scale. Shared-round write contention will be tested before release; a future database abstraction is warranted only if observed load requires it.

## Runtime

One versioned OCI image contains the compiled frontend, API, migration code, and SQLite support. It runs as an unprivileged user and writes only to `/data`. The API serves the frontend and owns authentication and authorization. Reverse proxies provide TLS but are never trusted as the authorization boundary.

The public repository contains generic Compose configuration only. Authentik, Traefik, hostnames, private paths, credentials, and Ansible inventory belong in the private homelab repository.

## Identity

Internal users have stable UUIDs. Local credentials are attached to internal users. The separate `external_identities` table will map an OIDC issuer/provider and immutable subject to an internal user. Email will not be used as an automatic linking key.

## Data model direction

Later migrations will separate course layouts from immutable round snapshots; molds from physical discs; bags from disc location history; and manufacturer flight numbers from personal observations. All participant and shared-round mutations will be authorized at the service boundary and use version fields for conflict detection.

## Offline boundary

The service worker currently caches the application shell only. Offline personal scoring will add per-user encrypted-at-rest browser records where supported, explicit mutation IDs, server version checks, and a visible conflict workflow. Shared rounds remain online-only in Version 0.1.

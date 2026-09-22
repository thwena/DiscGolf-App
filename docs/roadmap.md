# Version 0.1 roadmap

## Foundation (current increment)

- [x] Single-image build and generic Compose example
- [x] SQLite migration runner and persistent data directory
- [x] Health/readiness endpoints
- [x] One-time local administrator bootstrap, password login, and current-user endpoint
- [x] Responsive installable PWA shell
- [ ] CI and public image release workflow
- [ ] Refresh-token/session revocation and invitation-controlled registration
- [ ] Optional standards-based OIDC

## Product slices

- [ ] Courses, layouts, and immutable completed-round snapshots
- [ ] Personal/shared rounds with explicit participant authorization and conflict versions
- [ ] Scorecard UI and length-specific statistics
- [ ] Molds, physical discs, bags, and status history (private by default)
- [ ] Throw log and clearly labelled illustrative Flight Lab SVG
- [ ] Offline personal scoring with explicit sync conflicts
- [ ] Structured export and consistent SQLite/uploads backup and restore

## Pending product decisions

- License and public image namespace/tag policy
- Whether Version 0.1 includes UDisc CSV import (requires a redacted real export sample)
- Guest players without accounts
- Friend inventory visibility (remains private until decided)
- Homelab target host, hostname, local-login fallback, and Authentik invitation policy

Homelab Ansible automation starts only after the public image and configuration contract stabilize. It will follow the inspected repository's `doc_*` role, service playbook, Compose stack, catalog, Vault, backup, and recovery conventions; it will not be copied into this public repository.

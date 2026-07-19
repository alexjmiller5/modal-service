# CLAUDE.md

Python service deployed on Modal: HTTP webhook + spawned background workers + optional cron.

## Architecture rule (the one that matters)

**Business logic lives in `src/core/` as plain Python with NO Modal imports.**
Only `app.py` imports `modal` — it is the deployment shim (image, secrets,
endpoints, schedules). This keeps the logic portable: the same `core` package
runs in tests, on the mac mini via launchd, or on any future platform.

- Webhook → worker handoff is `process.spawn(payload)` — Modal's spawn IS the
  queue. Do not add Pub/Sub/Redis/celery.
- Endpoints use `requires_proxy_auth=True` — callers send `Modal-Key` +
  `Modal-Secret` headers (mint tokens in the Modal dashboard → Settings →
  Proxy Auth Tokens). Never expose an unauthenticated endpoint.
- Cron: Modal is the PREFERRED home for schedules — but the Starter plan
  allows **5 deployed crons across ALL apps**, so track the budget. Overflow
  goes to GHA cron or CF Cron Triggers (see the `personal-infra` skill).

## Stack

uv · pydantic-settings (env config) · httpx · structlog · pytest · ruff.
Config comes from env vars only: Modal Secret in the cloud, `op run` locally.
`.env.tpl` is the canonical secrets manifest (op:// refs, committed).
Instantiate `Settings()` inside functions, never at import time.

## Commands

Standard verb set (see global CLAUDE.md) — the justfile is the interface,
not a script catalog; one-offs go in `scripts/` and run directly.

| Command | Purpose |
|---|---|
| `just dev` | Live-reload dev against real Modal infra (`modal serve`) |
| `just test` / `just check` / `just fmt` | pytest / ruff read-only / ruff fix |
| `just logs` | Stream deployed-app logs |
| `just sync-secrets` | Push `.env.tpl` → Modal secret store |
| `just deploy` | test + sync-secrets + `modal deploy` — CI's job, not yours (below) |

**Deploying = commit + push to `main`.** The GHA deploy workflow runs tests,
syncs secrets, and deploys — never run `just deploy` locally unless there's a
legitimate stated reason (e.g. CI itself is broken; or the one-time first
deploy in the checklist below, before the repo/CI exists): local deploys ship
code that isn't in git, and the next push silently reverts it. After pushing,
verify the run with the gh CLI (`gh run watch <id> --exit-status`; on failure
`gh run view <id> --log-failed`) — never assume the deploy succeeded.

## TDD

Write the test in `tests/` first, then the `src/core/` code. `app.py` shim
functions stay thin enough to not need tests.

## New-project checklist (delete this section after setup)

1. Replace every `CHANGEME` (app.py APP_NAME, justfile secret name, pyproject name/description).
2. Fill `.env.tpl` with this app's op:// refs; add fields to `src/core/config.py`.
3. `uv sync` && `just test`.
4. One-time: `uv run modal token new` (local auth), then `just deploy`.
5. Vault + CI: Alex runs `op-project-bootstrap .env.tpl --repo <owner/name>` — creates the project vault, the `<Project> ENV` item, the read-only CI SA, and sets the repo's `OP_SERVICE_ACCOUNT_TOKEN`.
6. Delete the `daily()` cron function if unused (5 cron slots total — free them when idle).

## Not Alex? Owner-specific assumptions

The code is generic; the workflow assumes Alex's setup. If you forked this:
secrets flow through 1Password (`.env.tpl` with `op://` references,
`op-project-bootstrap` is his private bootstrap script) — swap in your own
secret store or `modal secret create`; Modal auth is `modal token new` on
your workspace.

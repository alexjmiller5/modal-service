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
- Cron budget: the Modal Starter plan allows **5 deployed crons across ALL
  apps**. A schedule goes on Modal only if the job needs Modal's runtime;
  otherwise use GHA cron, CF Cron Triggers, or mini launchd (see the
  `personal-infra` skill).

## Stack

uv · pydantic-settings (env config) · httpx · structlog · pytest · ruff.
Config comes from env vars only: Modal Secret in the cloud, `op run` locally.
`.env.tpl` is the canonical secrets manifest (op:// refs, committed).
Instantiate `Settings()` inside functions, never at import time.

## Commands

| Command | Purpose |
|---|---|
| `just dev` | Live-reload dev against real Modal infra (`modal serve`) |
| `just test` | pytest |
| `just sync-secrets` | Push `.env.tpl` → Modal secret store |
| `just deploy` | test + sync-secrets + `modal deploy` |

## TDD

Write the test in `tests/` first, then the `src/core/` code. `app.py` shim
functions stay thin enough to not need tests.

## New-project checklist (delete this section after setup)

1. Replace every `CHANGEME` (app.py APP_NAME, justfile secret name, pyproject name/description).
2. Fill `.env.tpl` with this app's op:// refs; add fields to `src/core/config.py`.
3. `uv sync` && `just test`.
4. One-time: `uv run modal token new` (local auth), then `just deploy`.
5. CI: `gh secret set OP_SERVICE_ACCOUNT_TOKEN --body "$(op read 'op://Personal/op-service-account-personal-infra/token')"`.
6. Delete the `daily()` cron function if unused (cron slots are scarce).

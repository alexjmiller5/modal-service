# modal-service (template)

Template for Python backends on [Modal](https://modal.com): an authenticated
HTTP webhook, spawned background workers, and optional cron — with all
infrastructure declared in `app.py` as code. No Dockerfile, no Terraform.

## Layout

```
app.py            Modal shim — image, secrets, endpoints, schedules
src/core/         business logic (plain Python, portable)
tests/            pytest
.env.tpl          secrets manifest (1Password op:// refs, committed)
justfile          dev / test / sync-secrets / deploy
```

## Bootstrap a new project from this template

See the `new-project` skill, or manually: copy this directory, replace the
`CHANGEME`s, fill `.env.tpl`, then `uv sync && just test && just deploy`.

Manual one-time steps (cannot be codified):
- Mint a Proxy Auth Token in the Modal dashboard for HTTP callers (iPhone Shortcuts)

Run `op-project-bootstrap .env.tpl --repo <owner/name>` to provision the
project vault and dedicated CI credentials. `scripts/provision.py` emits a
Modal approval URL and verification code on stderr. The operator opens that
URL in the configured remote browser session (agents use chrome-control)
and approves the code. The verified token pair stays in memory until
bootstrap writes both fields to 1Password together. No local browser opens
and no provider config or temporary credential file is written.

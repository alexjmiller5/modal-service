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
- `uv run modal token new` — authenticate this machine with Modal
- Mint a Proxy Auth Token in the Modal dashboard for HTTP callers (iPhone Shortcuts)

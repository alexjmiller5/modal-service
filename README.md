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

(Local runs need no `modal token new`: the machine-wide `modal` PATH wrapper
(nix-config `home/scripts.nix`) injects the 1P-held workspace token. CI gets
its OWN project-scoped token, minted during `op-project-bootstrap` by
`scripts/provision.py` - that opens one browser tab to approve, then stores
the token in the project vault. Revoke it in Modal's dashboard to kill just
this repo's deploys.)

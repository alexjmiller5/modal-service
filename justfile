set shell := ["bash", "-cu"]

default:
    @just --list

# Dev: live-reloading deploy of app.py against real Modal infra
dev:
    modal serve app.py

test:
    uv run pytest

# All static analysis (read-only, CI-safe)
check:
    uv run ruff check . && uv run ruff format --check .

fmt:
    uv run ruff format . && uv run ruff check --fix .

# Stream logs from the deployed app
logs:
    modal app logs CHANGEME

# Push .env.tpl secrets into the Modal secret store (no plaintext touches disk;
# the modal CLI rejects process-substitution FIFOs, hence the stdin script).
# It drives the Modal SDK, which authenticates from MODAL_TOKEN_ID /
# MODAL_TOKEN_SECRET in the environment or ~/.modal.toml - the operator's own.
sync-secrets:
    op inject -i .env.tpl | uv run scripts/sync_secrets.py CHANGEME

deploy: test sync-secrets
    modal deploy app.py

# --- project-specific recipes below (one-offs live in scripts/, run directly) ---

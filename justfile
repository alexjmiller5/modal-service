set shell := ["bash", "-cu"]

default:
    @just --list

# Dev: live-reloading deploy of app.py against real Modal infra
dev:
    uv run modal serve app.py

# Run tests
test:
    uv run pytest

lint:
    uv run ruff check . && uv run ruff format --check .

fmt:
    uv run ruff format . && uv run ruff check --fix .

# Push .env.tpl secrets into the Modal secret store (no plaintext touches disk)
sync-secrets:
    uv run modal secret create CHANGEME --from-dotenv <(op inject -i .env.tpl) --force

# Test, sync secrets, deploy
deploy: test sync-secrets
    uv run modal deploy app.py

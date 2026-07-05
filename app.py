"""Modal deployment shim — ALL infrastructure lives here, as code.

Business logic stays in src/core/ (plain Python, no Modal imports) so the
same package runs on the mac mini, in tests, or anywhere else. This file
only maps that logic onto Modal: image, secrets, endpoints, schedules.
"""

import modal

APP_NAME = "CHANGEME"  # also the Modal secret name (see justfile sync-secrets)

app = modal.App(APP_NAME)

image = (
    modal.Image.debian_slim(python_version="3.13")
    .uv_sync()  # reads pyproject.toml + uv.lock
    .add_local_python_source("core")
)

secrets = [modal.Secret.from_name(APP_NAME)]


@app.function(image=image, secrets=secrets, timeout=600)
def process(payload: dict) -> dict:
    """Background worker — .spawn()ed from the webhook. spawn() IS the queue."""
    from core.pipeline import run

    return run(payload)


@app.function(image=image, secrets=secrets)
@modal.fastapi_endpoint(method="POST", requires_proxy_auth=True)
def webhook(payload: dict) -> dict:
    """HTTP entrypoint. Callers (iPhone Shortcuts) send Modal-Key + Modal-Secret
    headers; unauthorized requests are rejected at Modal's edge, free."""
    call = process.spawn(payload)
    return {"status": "accepted", "call_id": call.object_id}


# ponytail: Starter plan allows 5 deployed crons TOTAL across all apps —
# prefer GHA cron / CF Cron Triggers / mini launchd unless the job needs
# Modal's runtime. Delete this function if this service has no schedule.
@app.function(image=image, secrets=secrets, schedule=modal.Cron("30 9 * * *"))
def daily() -> dict:
    from core.pipeline import run

    return run({"trigger": "cron"})

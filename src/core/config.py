"""Settings from env vars — Modal Secret in the cloud, `op run` locally.

One field per line in .env.tpl. Instantiate Settings() inside functions,
not at import time, so tests can run without secrets.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # CHANGEME — e.g.:
    # notion_api_key: str
    # gemini_api_key: str
    pass

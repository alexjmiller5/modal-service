# Canonical secrets manifest — op:// references only, SAFE to commit.
# Local dev:       op run --env-file=.env.tpl -- <cmd>   (see justfile)
# Push to Modal:   just sync-secrets
#
# CHANGEME — one line per secret, e.g.:
# NOTION_API_KEY=op://personal-infra/notion-api/credential
# GEMINI_API_KEY=op://personal-infra/gemini-api/credential

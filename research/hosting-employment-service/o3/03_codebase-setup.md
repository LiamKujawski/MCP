---
topic: "hosting-employment-service"
model: "o3"
stage: research
version: 1
---

# Codebase Setup – Hosting Employment Service (O3)

> Placeholder – outlines directory layout, environment variables, and makefile commands.

## Directory Layout Proposal

```txt
/ (repo root)
├─ apps/
│  ├─ api/              # FastAPI backend
│  └─ web/              # Next.js frontend
├─ infra/               # Terraform & Pulumi stacks
├─ scripts/             # Dev utility scripts
├─ tests/               # pytest + playwright
└─ docs/                # MkDocs site
```

## Local Development

1. `make dev` – starts Postgres & Redis via docker-compose, runs FastAPI with uvicorn reload, Next.js dev server.
2. `.env` templated via `direnv`; secrets pulled from 1Password CLI in CI.

## CI/CD

* GitHub Actions matrix tests: `python -m pytest`, `npm run typecheck`, `tflint`.
* Preview environments spun on Fly.io for each PR.
* Main branch merges trigger Terraform apply to staging account.

---

*Scaffold – to be enriched with actual command snippets & linter configs.*
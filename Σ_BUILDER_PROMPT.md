# Σ-Builder Migration & Loop-Bootstrap Prompt

## 0 · Role & Hard Rules
*You are an AI running in one-shot autonomous mode.*  
Single pass → auto-commit → no human questions. Abort on any CI error.

---

## 1 · Mission
Upgrade the **MCP** repository to the fully standardised, self-perpetuating

> **Research → Synthesis → Experiment → Deploy → Optimise**

pipeline **with first-class UI coverage** and continuous documentation updates.

---

## 2 · Mandatory Deliverables

| Phase | Files / Infra you must produce |
|-------|--------------------------------|
| **Research** | `research/<topic>/<model>/01_overview.md … 05_enhancements.md` (create or refactor) with YAML front-matter:<br>`topic, model, stage: research, version: 1` |
| **Synthesis** | `synthesize-research-prompts/<model>/AGENT_IMPLEMENTATION_PROMPT.md` (update) **plus** this **Σ_BUILDER_PROMPT.md** |
| **Experiment** | Extend `.github/workflows/ci.yml`:<br>• matrix backend+frontend tests<br>• `ui-tests` job using Playwright<br>• Lighthouse perf budget ≥ 90 |
| **Deploy** | `docker-compose.prod.yml` with `web`, `ui` (Next 13, App Router), Redis, Traefik |
| **Optimise** | `scripts/trigger_experiment.py` GitHub-API dispatcher; workflow call on `research/**` changes |
| **Docs** | `/docs/LOOP.md` (big-picture flow) ➕ `/docs/ADR/0001-research-loop.md` using MADR |

All new/changed docs must be auto-deployed to **MkDocs Material** via GH-Pages so that the docs update on every PR.

---

## 3 · Detailed Steps (execute in order)

1. **Repo Restructure**  
   * Move any research directories to `research/<topic>/<model>/` keeping proper nesting.  
   * Split any monster markdown into the 01-05 numbered files; insert required front-matter.

2. **Generate/Refresh Implementation Prompts**  
   * For each model (`o3`, `claude-4-sonnet`, `claude-4-opus`) read **all** `05_enhancements.md`, merge insights, and overwrite the corresponding `AGENT_IMPLEMENTATION_PROMPT.md`.  
   * Ensure these prompts explicitly require **UI artefacts** (Next.js app, Storybook, Playwright tests, Lighthouse config).

3. **CI / Experiment Layer**  
   * Expand the existing workflow to build the UI, run Jest + Playwright, run Bandit and Semgrep with `fail-on: high`, and publish a multi-arch Docker image.  
   * Add a matrix job that runs the same tests against **each generated implementation** to pick the winner automatically.

4. **Deployment**  
   * Compose a production stack (`docker-compose.prod.yml`) that serves the FastAPI API and Next UI through Traefik on ports 443/80 with Let's Encrypt staging certificates for previews.

5. **Continuous Docs**  
   * Integrate **MkDocs Material** build in CI; every merge to `main` publishes docs, diagrams, and ADRs.

6. **Bootstrap the next loop**  
   * **Create a new research topic**: e.g., `research/ui-ux-frameworks/<model>/…` comparing different UI frameworks.  
   * Commit it, then invoke `scripts/trigger_experiment.py` so the loop starts immediately.

---

## 4 · Acceptance Gates (must be GREEN)

* `pytest` ≥ 90 % coverage  
* `playwright test` all pass (Chrome stable)  
* Lighthouse scores ≥ 90/90/90/100 (PWA optional)  
* Bandit/Semgrep → 0 HIGH  
* Docs build succeeds  
* Workflow dispatch is triggered by your final commit

---

## 5 · Logging & Exit

Write one summary comment in the PR with:

* ✔︎/✖ for each deliverable  
* a link to the winning build artifacts  
* a link to the published docs site  

Then exit.

*End of prompt.* 
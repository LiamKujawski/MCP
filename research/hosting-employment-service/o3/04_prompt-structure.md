---
topic: "hosting-employment-service"
model: "o3"
stage: research
version: 1
---

# Prompt Structure for Infrastructure-as-Code Generation (O3)

> Placeholder document: captures how agent prompts should be structured to synthesize Terraform / Pulumi code, Kubernetes manifests, and CI pipelines for the employment service hosting stack.

## High-Level Prompt Schema

1. **Context Block** – repository layout, existing modules, environment targets.
2. **Goal Statement** – e.g., “Generate Terraform module to deploy FastAPI on AWS ECS Fargate with auto-scaling & zero-downtime deploys”.
3. **Constraints** – runtime versions, compliance (SOC2), budget cap.
4. **Output Format** – fenced code blocks per file, commit message summary.
5. **Validation Steps** – unit tests via `terraform validate`, `terratest`, `pytest` infra tests.

## Example Prompt Skeleton

```text
[CONTEXT]
<repo:infra/>  # Provide current Terraform state

[GOAL]
Deploy edge-auth Cloudflare Worker with KV namespace…

[CONSTRAINTS]
• KV keys per namespace < 1k
• Script size < 1MB

[OUTPUT_FORMAT]
```ts
// cloudflare/worker.ts
export default { … }
```

[VALIDATION]
Run `npm test` (Vitest) against wrangler dev stub.
```
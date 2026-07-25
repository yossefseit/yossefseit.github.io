# Deployment

## Day-to-day flow

1. Push to `main`, or open/update a pull request.
2. GitHub Actions runs `.github/workflows/azure-static-web-apps-gentle-smoke-06d712d0f.yml`.
3. The job requests a GitHub OIDC token and calls `Azure/static-web-apps-deploy@v1` with that token plus the stored deployment token.
4. Azure uploads the contents of `app_location` (`/`) as-is — `skip_app_build: true` skips any build step.
5. `main` deploys to production. A PR deploys to its own preview URL. Closing the PR tears the preview down via the `close_pull_request_job`.

No manual deployment step exists or is needed — everything is push-triggered.

## GitHub integration

The Static Web App resource was originally linked to this repo through the Azure Portal's GitHub-connected creation flow, which generated the initial workflow file and stored the deployment token as a repository secret. `infra/main.bicep` now represents that resource's configuration as code (see [`architecture.md`](architecture.md) for why it doesn't try to re-manage the GitHub side).

## Troubleshooting: the Oryx build failure

**What happened:** the Static Web App was first created expecting a buildable app. Azure's backend build step (Oryx) tried to detect a framework, assumed Node.js, and looked for a `build` (or `build:azure`) script to run.

**Why:** this repo has no `package.json` — there's nothing to build. Oryx's detection still ran because the initial resource/workflow configuration didn't tell it otherwise, so it failed with:

```
Could not find build or build:azure script
```

**The fix:** reconfigure the resource as a plain static site and set, in the workflow's `with:` block:

```yaml
app_location: "/"
api_location: ""
output_location: "/"
skip_app_build: true
```

`skip_app_build: true` is the key line — it tells Azure to skip Oryx entirely and upload `app_location` as final, already-built content. Once that was in place, deployments succeeded.

## Why `skip_app_build: true` was required

Oryx's build detection is designed for apps that need compiling (React, Vue, Angular, etc.) and assumes it should try *something* by default rather than doing nothing. For a plain HTML/CSS/JS site, the correct instruction isn't "configure the build correctly" — it's "there is no build; don't run one." That's exactly what this flag does, and it's the reason this project has no `package.json`, no `node_modules`, and no Node-based step anywhere in the workflow.

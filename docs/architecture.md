# Architecture

## What this actually is

A static portfolio site (HTML/CSS/JS, no framework, no build step) hosted on Azure Static Web Apps (SWA), deployed by GitHub Actions. No server, no database, no API. The engineering decisions worth documenting are in *how* it's deployed and configured, not in the frontend itself.

```mermaid
flowchart TD
    subgraph Source
        Dev[Developer] -->|push / PR| Repo[GitHub Repository]
    end

    subgraph CICD[CI/CD]
        Repo --> Workflow[GitHub Actions Workflow]
        Workflow -->|OIDC token + deployment token| Deploy[Azure/static-web-apps-deploy@v1]
    end

    subgraph Azure
        Deploy -->|"skip_app_build: true, upload as-is"| SWA[Azure Static Web Apps]
        SWA --> Edge[Global edge network + managed TLS]
    end

    Edge --> Users((Users))
    Repo -.PR opened/updated.-> Preview[Ephemeral preview environment]
    Repo -.PR closed.-> Teardown[Preview environment removed]
```

## Azure Static Web Apps

SWA distributes the contents of `app_location` (the repo root, here) across Azure's global edge network, so requests are served from a location close to the visitor instead of a single origin server. TLS is managed automatically for both the default `*.azurestaticapps.net` hostname and any custom domain added later — no certificates to renew by hand.

Two SWA features this project actually uses:

- **Free managed TLS + CDN** — no separate CDN or certificate setup needed for a site this size.
- **PR preview environments** — the workflow's `pull_request` trigger (`opened`, `synchronize`, `reopened`, `closed`) means every PR deploys to its own temporary URL, torn down automatically when the PR closes. Useful even in a one-person repo: changes can be reviewed live before they touch `main`.

Not in use yet: the integrated Azure Functions API. SWA supports pairing a static app with a Functions backend under `/api`, which is the natural next step if this site ever needs anything dynamic.

## GitHub Actions / CI-CD

The workflow (`.github/workflows/azure-static-web-apps-gentle-smoke-06d712d0f.yml`) authenticates to Azure two ways on every run:

1. A long-lived **deployment token**, stored as the GitHub secret `AZURE_STATIC_WEB_APPS_API_TOKEN_GENTLE_SMOKE_06D712D0F`.
2. A short-lived **GitHub OIDC token**, requested at runtime via `core.getIDToken()` and passed to the deploy action as `github_id_token`.

The job itself does little beyond checkout and the deploy action call — there's no separate build job, which is deliberate (see below).

## HTTPS / TLS

Handled entirely by Azure: free managed certificates on both the default subdomain and any future custom domain, auto-renewed, no action required in this repo.

## Global CDN

Static assets are cached at edge locations worldwide; each new deployment invalidates the relevant cache automatically, so pushes to `main` show up without a manual purge step.

## Architecture decisions

A few choices worth documenting explicitly, rather than leaving them undiscoverable in the Portal:

**No build step.** `skip_app_build: true` plus explicit `app_location: "/"` and `output_location: "/"` tell Azure this is pre-built static content. The alternative — adding a dummy `package.json`/build script just to satisfy Oryx's default detection — would add tooling with no actual purpose. See [`deployment.md`](deployment.md) for the failure this avoided.

**CSP allows `'unsafe-inline'` for `script-src`/`style-src`.** `index.html` has a few inline `<script>` blocks and one `<style>` block. A hash-based CSP (`'sha256-…'` per block) would be tighter, but with no build pipeline to regenerate hashes automatically, that becomes a silent-breakage risk on every content edit. `'unsafe-inline'` is the pragmatic choice at this size; extracting those blocks to external files (tracked in the README's Future Improvements) is the way to remove it properly later.

**No `navigationFallback`.** That setting exists for client-side-routed SPAs that need unknown paths rewritten to `index.html`. This site has no client-side router, so an unmatched path should return a real `404`, not a silently-served homepage — better for both correctness and SEO.

**`infra/main.bicep` doesn't set `repositoryUrl`/`repositoryToken`.** Those properties let Azure Resource Manager manage its own GitHub Actions workflow. This repo's workflow is already hand-maintained, so the Bicep template owns only the Azure resource's shape (SKU, build settings, staging policy) and deliberately leaves CI/CD ownership with `.github/workflows/`. One concern, one owner.

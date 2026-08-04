# Validation Snapshot

**Date:** 4 August 2026
**Scope:** Local `main` worktree before deployment

This record distinguishes checks that actually ran from checks that remain dependent on Azure credentials or a deployed pull request.

The site validator recursively checks the homepage, 404 page, project catalogue, and Secure Azure Hub-and-Spoke detail route. It validates per-route canonical metadata, local references, accessibility structure, and sitemap coverage.

On 2026-08-04, the worktree passed:

- dependency-free validation of four HTML documents and 47 local references;
- JavaScript syntax and XML parsing;
- local recursive link crawling for `/`, `/projects/`, and `/projects/azure-secure-hub-spoke/`;
- Azure Static Web Apps CLI 2.0.10 direct-route tests, including the canonical trailing-slash redirect and custom 404;
- desktop and mobile visual inspection of every public route;
- security-header inspection through the Static Web Apps emulator.

External links were not counted as passed by the local crawler because the execution environment did not return those remote requests. They remain subject to CI and production verification.

## Lighthouse

Lighthouse 13.4.1 ran against the locally served site using its default mobile audit profile.

| Route | Performance | Accessibility | Best Practices | SEO |
|---|---:|---:|---:|---:|
| Homepage | 100 | 100 | 100 | 100 |
| Hub-spoke case study | 100 | 100 | 100 | 100 |

The homepage measured 1.4 s FCP/LCP, 0 ms TBT, zero CLS, and 81 KiB transferred. The case study measured 1.3 s FCP, 1.4 s LCP, 0 ms TBT, zero CLS, and 64 KiB transferred. Replacing its eager 950 KB in-page PNG with a lazy 4.2 KB SVG raised the local performance score from 71 to 100. Scores are environment-specific diagnostics and must be rerun after material changes or production deployment.

## Source and configuration checks

| Check | Result |
|---|---|
| `python3 scripts/validate_site.py` | Pass |
| `html-validate` 11.6.2 on all four public HTML routes | Pass |
| CSS Tree validator 4.0.1 on `assets/site.css` | Pass |
| Node syntax check on `assets/site.js` | Pass |
| `jq` parse of `staticwebapp.config.json` | Pass |
| `xmllint` parse of `sitemap.xml` | Pass |
| `git diff --check` | Pass |
| Markdownlint CLI 0.23.2 on repository Markdown | Pass |
| CSpell 10.0.1 on public HTML and Markdown | Pass |
| actionlint 1.7.12 on the GitHub Actions workflow | Pass |
| Bicep CLI 0.46.1 compile of `infra/main.bicep` | Pass |
| Gitleaks 8.30.1, Git history and working directory, redacted output | Pass; no leaks found |

## Browser checks

Headless Chromium tested:

- 1440 × 1000 desktop;
- 768 × 1024 tablet;
- 390 × 844 mobile;
- 320 × 740 mobile;

The scripted interaction audit confirmed:

- no horizontal overflow;
- desktop navigation is visible;
- mobile navigation starts closed, opens, and closes after selection;
- Escape closes the mobile menu and returns focus to its toggle;
- all in-page navigation targets exist;
- the CV download link is present;
- the stylesheet loads;
- the custom 404 document has the expected title;
- critical project content remains rendered without JavaScript or reveal observers;
- the SVG architecture loads when its below-the-fold section approaches the viewport;
- reduced-motion mode stops repeating animation, disables smooth scrolling, and reveals all project content;
- keyboard focus has a visible three-pixel outline;
- light and dark site sections retain distinct computed backgrounds;
- no console errors, page errors, request failures, or missing local assets.

Current desktop and mobile Chromium captures are stored in [`docs/screenshots/`](screenshots/).

## Azure resource evidence

A resource-owner-supplied [redacted Azure Portal overview](screenshots/azure-static-web-app-overview-redacted.png) confirms:

- resource name `portfolio-yossef`;
- resource group `rg-portfolio`;
- production environment status `Ready`;
- Free hosting plan;
- GitHub `main` source;
- default hostname `gentle-smoke-06d712d0f.7.azurestaticapps.net`.

The supplied resource JSON reports the ARM deployment location as `eastus2`; the Portal overview displays the globally delivered service as **Global**. Subscription metadata was redacted before the evidence image was checked into the repository.

## Azure Static Web Apps emulation

Azure Static Web Apps CLI 2.0.10 loaded the checked-in workflow and `staticwebapp.config.json` successfully.

Verified through the emulator:

- homepage status `200`;
- nested unknown-route (`/a/b/c`) response status `404`;
- custom 404 body;
- root stylesheet status `200` when the nested 404 is displayed;
- CSP and defense-in-depth headers;
- no CSP refusal or browser console error;
- CV `Cache-Control: no-cache, must-revalidate`.

The CLI warns that local emulation may not exactly match Azure, so production headers still require a post-deployment check.

## Link check

Linkinator 8.0.3 crawled 38 links from the local site and resolved current local assets, the tagged CV, academy PDFs, GitHub repositories, the Azure production homepage, architecture links, and Credly records.

The absolute Open Graph image URL returns `200` on the current production deployment.

LinkedIn was excluded from automated status enforcement because it returns an anti-bot response to command-line clients. The URL is sourced from the CV and requires a normal-browser/manual check.

## Checks still unavailable

- authenticated `az deployment group validate`;
- authenticated `az deployment group what-if`;
- deployment of `infra/main.bicep` to the existing production resource;
- Azure portal confirmation that the pull request #7 preview environment was removed after close;
- post-deployment verification of this branch's HTML and workflow changes;
- remediation of the issuer-provided certificate PDF tagging.

No Azure resource deployment or billable cloud action was performed.

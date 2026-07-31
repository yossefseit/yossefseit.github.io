# Validation Snapshot

**Date:** 31 July 2026
**Scope:** Local `agent/portfolio-audit` branch before deployment

This record distinguishes checks that actually ran from checks that remain dependent on Azure credentials or a deployed pull request.

## Lighthouse

Lighthouse 13.4.1 ran against the locally served site using its default mobile audit profile.

| Category | Measured score |
|---|---:|
| Performance | 100 |
| Accessibility | 100 |
| Best Practices | 100 |
| SEO | 100 |

Key measured values included 1.3 s First Contentful Paint, 1.5 s Largest Contentful Paint, 0 ms Total Blocking Time, and 0 Cumulative Layout Shift. Scores are environment-specific and should be rerun after material changes or production deployment.

## Source and configuration checks

| Check | Result |
|---|---|
| `python3 scripts/validate_site.py` | Pass |
| `html-validate` 11.5.6 on `index.html` and `404.html` | Pass |
| CSS Tree validator on `assets/site.css` | Pass |
| Node syntax check on `assets/site.js` | Pass |
| `jq` parse of `staticwebapp.config.json` | Pass |
| `xmllint` parse of `sitemap.xml` | Pass |
| `git diff --check` | Pass |
| CSpell 9.6.4 on site copy, docs, CSS, JS, and Python | Pass |
| actionlint 1.7.12 on the GitHub Actions workflow | Pass |
| Bicep CLI 0.45.15 compile of `infra/main.bicep` | Pass |
| Gitleaks 8.30.1, Git history and working directory, redacted output | Pass; no leaks found |

## Browser checks

Headless Chromium tested:

- 1440 × 1000 desktop;
- 1024 × 1000 desktop;
- 768 × 1000 tablet;
- 390 × 844 mobile;

The scripted interaction audit confirmed:

- no horizontal overflow;
- desktop navigation is visible;
- mobile navigation starts closed, opens, and closes after selection;
- Escape closes the mobile menu and returns focus to its toggle;
- all in-page navigation targets exist;
- the CV download link is present;
- the stylesheet loads;
- the custom 404 document has the expected title;
- the animated architecture is present at every tested width;
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

Linkinator 8.0.2 crawled the local site and resolved current local assets, the CV, academy PDFs, GitHub repositories, the Azure production homepage, architecture link, and Credly records.

The absolute Open Graph image URL returns `200` on the current production deployment.

LinkedIn was excluded from automated status enforcement because it returns an anti-bot response to command-line clients. The URL is sourced from the CV and requires a normal-browser/manual check.

## Checks still unavailable

- authenticated `az deployment group validate`;
- authenticated `az deployment group what-if`;
- deployment of `infra/main.bicep` to the existing production resource;
- Azure portal confirmation that the pull request #7 preview environment was removed after close;
- post-deployment verification of this branch's HTML and workflow changes;
- remediation of the untagged CV and certificate PDF structure.

No Azure resource deployment or billable cloud action was performed.

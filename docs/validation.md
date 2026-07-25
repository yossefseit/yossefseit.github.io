# Validation Snapshot

**Date:** 25 July 2026
**Scope:** Local `feat/azure-cloud-portfolio` branch before deployment

This record distinguishes checks that actually ran from checks that remain dependent on Azure credentials or a deployed pull request.

## Lighthouse

Lighthouse 13.4.1 ran against the locally served site with Chrome for Testing 151 using the default mobile audit profile.

| Category | Measured score |
|---|---:|
| Performance | 100 |
| Accessibility | 100 |
| Best Practices | 100 |
| SEO | 100 |

Key measured values included 0 ms Total Blocking Time and 0 Cumulative Layout Shift. Scores are environment-specific and should be rerun after material changes or production deployment.

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
- 390 × 844 mobile;
- 320 × 700 small mobile;
- breakpoint-adjacent widths from 390 through 861 pixels;
- 320 × 240 short-viewport navigation.

The scripted interaction audit confirmed:

- no horizontal overflow;
- desktop navigation is visible;
- mobile navigation starts closed, opens, and closes after selection;
- the mobile menu remains scrollable and contained at short viewport heights;
- mobile navigation remains available when JavaScript is disabled;
- hero typography remains continuous across its responsive breakpoints;
- all in-page navigation targets exist;
- the CV download link is present;
- the stylesheet loads;
- the custom 404 document has the expected title;
- no console errors, page errors, request failures, or missing local assets.

Firefox headless renders were also reviewed at desktop and mobile sizes. Current captures are stored in [`docs/screenshots/`](screenshots/).

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

The new absolute Open Graph image URL returns `404` on the current production deployment because this branch has not been pushed or deployed. The file exists and passes local validation. It must be checked again after the branch is merged.

LinkedIn was excluded from automated status enforcement because it returns an anti-bot response to command-line clients. The URL is sourced from the CV and requires a normal-browser/manual check.

## Checks still unavailable

- authenticated `az deployment group validate`;
- authenticated `az deployment group what-if`;
- deployment of `infra/main.bicep` to the existing production resource;
- a real pull-request preview open/update/close lifecycle;
- post-deployment verification of the new Open Graph image and headers;
- remediation of the untagged CV and certificate PDF structure.

No Azure resource deployment or billable cloud action was performed.

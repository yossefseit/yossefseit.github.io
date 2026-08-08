# Validation Snapshot

**Date:** 8 August 2026
**Scope:** Local and production validation of the 8 August case-study release

This record distinguishes checks that actually ran from checks that remain dependent on privileged Azure access or a deployed pull request.

The site validator recursively checks the homepage, 404 page, project catalogue, and the governance, hub-spoke, and Samba detail routes. It validates per-route canonical metadata, local references, accessibility structure, optimized architecture-image use, and sitemap coverage.

On 2026-08-08, the worktree passed:

- dependency-free validation of six HTML documents and 73 local references;
- JavaScript syntax and XML parsing;
- HTTP-served browser and Axe checks across all six routes at four viewport widths;
- local Lighthouse diagnostics for the five indexable routes;
- desktop and mobile visual review of the homepage and governance case study.

External-link, Azure Static Web Apps emulator, deployment, and production results are recorded separately below.

## Lighthouse

Lighthouse 13.4.1 ran against the locally served site using its default mobile audit profile.

| Route | Performance | Accessibility | Best Practices | SEO |
|---|---:|---:|---:|---:|
| Homepage | 100 | 100 | 100 | 100 |
| Project catalogue | 100 | 100 | 100 | 100 |
| Governance case study | 100 | 100 | 100 | 100 |
| Hub-spoke case study | 100 | 100 | 100 | 100 |
| Samba case study | 100 | 100 | 100 | 100 |

Every audited route measured 0 ms TBT and zero CLS. FCP ranged from 1.1 to 1.2 s, LCP from 1.2 to 1.4 s, and transferred content from 54 to 85 KiB. The hub-spoke page still uses the 4.2 KB SVG in-page rather than the former eager 950 KB PNG. Scores are environment-specific diagnostics, not production guarantees, and must be rerun after material changes.

## Source and configuration checks

| Check | Result |
|---|---|
| `python3 scripts/validate_site.py` | Pass |
| `html-validate` 11.6.2 on all six public HTML routes | Pass |
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

Headless Chromium tested every route at:

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
- every decoded local image succeeds after deliberate lazy-load activation;
- reduced-motion mode stops repeating animation, disables smooth scrolling, and reveals all project content;
- keyboard focus has a visible three-pixel outline;
- light and dark site sections retain distinct computed backgrounds;
- no console errors, page errors, request failures, or missing local assets.

Current desktop and mobile captures are retained privately under `/tmp`; the repository contains only deliberate deployment evidence in [`docs/screenshots/`](screenshots/).

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
- no CSP refusal or browser console error on the tested `200` routes;
- CV `Cache-Control: no-cache, must-revalidate`.

The CLI warns that local emulation may not exactly match Azure, so the headers were also checked on the production deployment.

## Production deployment

[GitHub Actions run 31267818137](https://github.com/yossefseit/yossefseit.github.io/actions/runs/31267818137) validated and deployed exact commit `a631f31490372367e5f81c006d6ec273910b1248` successfully.

Post-deployment checks confirmed:

- status `200` for the homepage, catalogue, and all three case studies;
- status `404` with the custom document for a nested unknown route;
- the checked-in CSP, HSTS, referrer, permissions, content-type, and cross-origin headers;
- the production CV is byte-identical to the checked-in PDF at SHA-256 `4a110783aff60270de55329e67cecbde812c4438ee21e3adf0c17ca2df39272c`;
- a 24-case route and viewport browser matrix under the production CSP had no overflow, missing images, console errors, page errors, or failed requests;
- an Axe audit in a CSP-bypassed test context found no WCAG A/AA or best-practice violations. The bypass was used only because injecting the local audit library is correctly blocked by the production CSP.

## Link check

A production Linkinator 8.0.3 crawl checked 50 distinct targets and resolved every route, asset, fragment, and enforced external link.

The absolute Open Graph image URL returns `200` on the current production deployment.

LinkedIn was excluded from automated status enforcement because it returns an anti-bot response to command-line clients. The URL is sourced from the CV and requires a normal-browser/manual check.

## Checks still unavailable

- authenticated `az deployment group validate`;
- authenticated `az deployment group what-if`;
- deployment of `infra/main.bicep` to the existing production resource;
- Azure portal confirmation that the pull request #7 preview environment was removed after close;
- PDF tagging remediation for the CV and issuer-provided academy certificates.

No Azure resource deployment or billable cloud action was performed.

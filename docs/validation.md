# Validation snapshot

- **Date:** 9 September 2026
- **Scope:** Infrastructure command-centre redesign, GitHub Pages migration, and production verification
- **Publication state:** The reviewed portfolio and Calculator migration was authorized, merged through pull requests, and deployed to GitHub Pages. Azure resources were not provisioned, restarted, or changed.

This record separates executed checks, dated deployments, current project boundaries, and retired Azure evidence.

## Published release evidence

| Release | Evidence | Verified behavior |
|---|---|---|
| Portfolio migration | [PR 13](https://github.com/yossefseit/yossefseit.github.io/pull/13), commit `a73f9140b0dd16ada7959a2cd1a6d41a82d4cd2e`, [Pages run 34370157090](https://github.com/yossefseit/yossefseit.github.io/actions/runs/34370157090) | Successful build/deploy; ten routes, assets, metadata, root CV and custom 404 verified on 9 September |
| Calculator migration | [PR 5](https://github.com/yossefseit/egypt-salary-calculator/pull/5), commit `1f710b2b5dea7c86df15199ea9dd1f2e7f6e0090`, [Pages run 34370072295](https://github.com/yossefseit/egypt-salary-calculator/actions/runs/34370072295) | Successful 57-test suite, lint, production build and deployment; desktop/mobile EGP 10,000 → EGP 8,302.50 verified |
| USD correction | [PR 7](https://github.com/yossefseit/egypt-salary-calculator/pull/7), commit `848273ab1dffd7049778e0e3eef6ea6c74f83759`, [Pages run 34402180941](https://github.com/yossefseit/egypt-salary-calculator/actions/runs/34402180941) | 80 tests, lint and build passed; live desktop/mobile USD conversion and annual conversion verified at 20:39 UTC |

A successful deployment is dated evidence, not a continuous availability or uptime claim. The Calculator keeps its detailed [validation ledger](https://github.com/yossefseit/egypt-salary-calculator/blob/main/docs/validation.md), including subsequent exchange-rate changes.

## Website source and configuration checks

```text
Verified 10 static pages, sitemap, meta CSP and root CV mirror.
Site validation passed: 11 HTML documents and 303 local references checked.
Staged 56 public files in _site (6.6 MiB).
```

| Check | Result |
|---|---|
| Generator freshness and structural validator | Pass; ten generated routes plus `404.html`, links, fragments, metadata, images, fonts and PDF references |
| Scoped artifact staging | Pass; public routes, assets and root files only; source and documentation excluded |
| JavaScript syntax, HTML semantics and CSS syntax | Pass |
| Markdown, spelling and secret scan | Pass in the published workflow |
| Retained historical Bicep compilation | Pass; compilation only, no Azure authentication or deployment |
| Actionlint 1.7.12 | Pass on both Pages workflows during migration review |
| GitHub Markdown rendering | Redesigned README assets and links reviewed through GitHub rendering |
| `git diff --check` | Pass at the reviewed release |

The reproducible checks and pinned tool versions are described in [Deployment](deployment.md).

## Production browser and accessibility review

The Chromium audit completed on 9 September at 15:27 UTC against the published portfolio. It covered all 11 documents at 1440 × 1000 and 390 × 844: 22 route/viewport combinations. Every document had one `h1`, no horizontal overflow, decoded local images, correct canonical and Open Graph URLs, and the exact root CV links. Axe reported zero WCAG A/AA and WCAG 2.1 A/AA violations.

Interaction checks passed for theme persistence after reload, command filtering, empty results, Enter navigation, Escape dismissal and focus return, mobile menu open/close/navigation, reduced-motion behavior, and mobile navigation with JavaScript disabled. The custom error document returned an actual HTTP 404 for an unknown nested route. No console errors, page errors, missing assets or failed requests occurred during the portfolio audit.

The initial Calculator release passed desktop and mobile checks for the reference EGP result, annual/manual/reverse modes, persisted theme, project-path assets, and zero Axe violations or horizontal overflow. Its initially unhosted rate adapter left USD enrichment unavailable; the direct-provider correction was subsequently deployed and verified at 20:39 UTC. Both live viewport checks returned a rate of 51.115 EGP per USD dated 9 September and displayed EGP 8,302.50 as approximately USD 162.43. Source/date display and annual conversion passed, with no browser errors, Axe violations or overflow. Only the fixed currency-pair GET was sent, with no salary value or body. See the [sanitized live USD report](evidence/usd-live-2026-09-09.json).

Initial migration review captures:

- [landing page, dark desktop](screenshots/pages-landing-desktop.png);
- [landing page, light desktop](screenshots/pages-landing-light-desktop.png);
- [landing page, mobile](screenshots/pages-landing-mobile.png);
- [expanded mobile navigation](screenshots/pages-mobile-navigation.png);
- [Infrastructure view, desktop](screenshots/pages-infrastructure-desktop.png);
- [Infrastructure view, mobile](screenshots/pages-infrastructure-mobile.png);
- [Calculator case study](screenshots/pages-salary-case-desktop.png).

The public response included GitHub's HSTS header with `max-age=31556952` and `Cache-Control: max-age=600` at the audit time. No response CSP, X-Frame-Options or X-Content-Type-Options header was observed. The repository's meta CSP was present and produced no browser violations. These are dated platform observations; the repository does not control GitHub Pages response headers.

## CV verification

The authoritative file remains `assets/Yossef_Mohammed_Ali_CV.pdf`. The generator produces a byte-identical root mirror without editing the original PDF.

Every website action uses `/Yossef_Mohammed_Ali_CV.pdf`; repository documentation uses [the absolute public CV URL](https://yossefseit.github.io/Yossef_Mohammed_Ali_CV.pdf). The public response returned HTTP 200 with `application/pdf` and matched both local files exactly:

```text
SHA-256: bf72173f1bd9ad1f9bfda4fb3b1b9c22f2e7762f1f52c09b78cfa66861120dca
```

Follow [Replace the CV](deployment.md#replace-the-cv) after exporting from Overleaf. Keep both generated and authoritative files in the reviewed commit.

## Content and evidence boundaries

The supplied CV remains the authority for employment, training, education, skills and contact information. El Mostafa for Master Batch ends in July 2024, reconciling the April 2024 date from the older website/profile to the supplied PDF. Professional experience stays separate from personal projects and labs.

| Project | Evidence boundary |
|---|---|
| Egypt Salary Calculator | Deployed to GitHub Pages; executed test and runtime evidence in its validation ledger; reference rates are optional and dated |
| Secure Azure Hub-and-Spoke Lab | Lab: CI validated; Azure deployment pending |
| Azure Governance Automation Lab | Lab: CI validated; Azure deployment pending |
| Samba AD DC Lab | Lab: CI validated; runtime validation pending |
| GitHub Pages Portfolio | Deployment and public browser audit verified on 9 September 2026 |

Route Academy remains in progress from August 2026 to expected February 2027. The planned AWS/Kubernetes capstone is future coursework. The distinct IT-Gate programs retain their 220-hour and 240-hour records and are not described as vendor certification exams.

## Migration observations and historical Azure evidence

Before the migration, the user site still served the previous Azure URLs and `/assets/` CV link. The Calculator's [older Pages run 34335934625](https://github.com/yossefseit/egypt-salary-calculator/actions/runs/34335934625) published commit `1241689611f72dd55f3f575cb41ccbac43200041`, whose raw `/src/main.tsx` entry returned 404. The new root CV was also absent. The reviewed Pages artifact deployments resolved those release defects.

The former Static Web Apps release is retained as [run 31267818137](https://github.com/yossefseit/yossefseit.github.io/actions/runs/31267818137) from 8 August 2026, commit `a631f31490372367e5f81c006d6ec273910b1248`. The retired Calculator App Service deployment is [run 31909528455](https://github.com/yossefseit/egypt-salary-calculator/actions/runs/31909528455) from 15 August 2026. Neither run establishes current Azure availability.

## Repeat after future releases

Verify the deployed commit and successful Pages run, all routes and assets, root CV checksum, metadata, theme/navigation/command interactions, keyboard accessibility, mobile layout, and Calculator EGP/USD behavior. Keep the observed rate date visible and distinguish a reference-rate outage from the salary engine's availability.

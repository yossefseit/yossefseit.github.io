# Validation snapshot

- **Date:** 9 September 2026 (source and build checks completed 8 September; final browser review completed 9 September)
- **Scope:** Local review of the infrastructure command-centre redesign and GitHub Pages migration
- **Publication state:** Migration changes remain local; no push, merge, deployment, Azure action, or remote-setting change was performed by this work. The owner separately completed both Pages source settings.

This record separates current local validation, configured delivery, historical Azure evidence, and public availability.

## Current local result

The worktree contains ten generated public routes plus the custom 404 document. The current generator, validator, and artifact packager report:

```text
Verified 10 static pages, sitemap, meta CSP and root CV mirror.
Site validation passed: 11 HTML documents and 303 local references checked.
Staged 55 public files in _site (6.5 MiB).
```

The structural review covers:

- generated-output freshness;
- directly linkable pages and sitemap coverage;
- local links, fragments, images, fonts, and PDF references;
- one primary heading per document;
- titles, descriptions, canonical URLs, social metadata, and structured data;
- the homepage JSON-LD hash authorized by the meta Content Security Policy;
- JSON and XML parsing;
- the custom 404 document;
- the exact public CV route `/Yossef_Mohammed_Ali_CV.pdf`;
- byte equality between the root CV mirror and the authoritative asset;
- rejection of legacy CV links and retired hosting URLs in generated HTML.

## Source and configuration checks

| Check | Result |
|---|---|
| `python3 scripts/build_site.py --check` | Pass; ten generated pages, sitemap, meta CSP, and root CV mirror match source |
| `python3 scripts/validate_site.py` | Pass; 11 HTML documents and 303 local references |
| `python3 scripts/package_site.py` | Pass; 55 files staged in the scoped `_site/` artifact |
| Node syntax checks for `assets/site.js` and `assets/theme.js` | Pass |
| Egypt Salary Calculator `npm test` | Pass; 57 tests across two files on 8 September 2026 |
| Egypt Salary Calculator lint and Vite production build | Pass; project-site asset paths use `/egypt-salary-calculator/` |
| Egypt Salary Calculator .NET Function build | Pass locally with zero warnings and zero errors; not part of Pages delivery |
| Actionlint 1.7.12 on both Pages workflows | Pass |
| Root and authoritative CV SHA-256 | Match: `bf72173f1bd9ad1f9bfda4fb3b1b9c22f2e7762f1f52c09b78cfa66861120dca` |
| GitHub Markdown API rendering for the redesigned repository READMEs | Pass |
| `git diff --check` | Pass at the migration review point |

The reproducible website commands are documented in [Deployment](deployment.md). The Calculator keeps its own [dated validation ledger](https://github.com/yossefseit/egypt-salary-calculator/blob/main/docs/validation.md).

## Browser and accessibility review

The final Chromium review on 9 September exercised the exact `_site/` artifact at 1440 × 1000 and 390 × 844. All 11 documents passed at both viewport widths: one `h1`, no horizontal overflow, decoded local images, correct canonical URLs and root CV links, and zero Axe WCAG A/AA or WCAG 2.1 AA violations.

Keyboard and interaction checks verified command filtering, the empty-result message, Enter navigation, Escape dismissal with focus return, persisted light theme after reload, mobile menu open/close/navigation, reduced-motion preference, and usable mobile navigation with JavaScript disabled. The browser downloaded the root CV and confirmed exact equality with the authoritative PDF. The review found and fixed Escape handling when the command search contained text, a stale Azure delivery label, and crowded labels in the portfolio diagram.

Both desktop and mobile Calculator production previews confirmed the EGP 10,000 → EGP 8,302.50 reference result, no horizontal overflow, and zero Axe violations in the same rule sets. No console errors, page errors, missing assets, or failed requests occurred across the portfolio and Calculator review.

Current review captures:

- [landing page, dark desktop](screenshots/pages-landing-desktop.png);
- [landing page, light desktop](screenshots/pages-landing-light-desktop.png);
- [landing page, mobile](screenshots/pages-landing-mobile.png);
- [expanded mobile navigation](screenshots/pages-mobile-navigation.png);
- [Infrastructure view, desktop](screenshots/pages-infrastructure-desktop.png);
- [Infrastructure view, mobile](screenshots/pages-infrastructure-mobile.png);
- [Egypt Salary Calculator case study](screenshots/pages-salary-case-desktop.png).

Python's local HTTP server does not reproduce GitHub Pages response headers, caching, or edge behavior. The repository's meta CSP can be exercised locally; platform headers must be inspected after deployment.

## Content and evidence review

The supplied CV remains the authority for employment, training, education, skills, and contact information. El Mostafa for Master Batch ends in July 2024 here, reconciling the April 2024 date from the older website/profile to the supplied PDF.

| Project | Current wording | Evidence boundary |
|---|---|---|
| Egypt Salary Calculator | 57 tests passing; GitHub Pages deployment configured | Fresh local tests/build; Pages source enabled by the owner; the migrated Vite artifact remains unpublished; 15 August 2026 App Service run retained only as dated history |
| Secure Azure Hub-and-Spoke Lab | Lab: CI validated; Azure deployment pending | Authored Bicep and lifecycle scripts; successful CI evidence; no authenticated deployment or runtime claim |
| Azure Governance Automation Lab | Lab: CI validated; Azure deployment pending | Authored Bicep, lifecycle scripts, and guard tests; successful CI evidence; no authenticated deployment claim |
| Samba AD DC Lab | Lab: CI validated; runtime validation pending | Authored automation and runbooks; no provisioning, client-authentication, restore, or teardown claim |
| GitHub Pages Portfolio | Pages deployment configured; first Actions-built release pending | Generated site, validation, artifact workflow, and local preview; the existing public site is not evidence for the unpublished migration |

Professional experience stays separate from personal projects and labs. Route Academy remains in progress from August 2026 to expected February 2027, and its planned AWS/Kubernetes capstone is future coursework. The separate IT-Gate programs retain their 220-hour and 240-hour records and are not described as vendor certification exams.

## CV verification

The authoritative local file is:

```text
assets/Yossef_Mohammed_Ali_CV.pdf
```

The generator creates a byte-identical public mirror at:

```text
Yossef_Mohammed_Ali_CV.pdf
```

Every local website action uses `/Yossef_Mohammed_Ali_CV.pdf`; the updated local GitHub READMEs use `https://yossefseit.github.io/Yossef_Mohammed_Ali_CV.pdf`. The public root URL returned 404 on 9 September because this local mirror has not been published.

## Public state on 9 September 2026

The owner completed **Settings → Pages → Source → GitHub Actions** for both repositories. Read-only GitHub Pages API checks confirmed `build_type: workflow`, `status: built`, and the expected `html_url` values. No remote changes were made during this verification.

| Public URL | Observed result |
|---|---|
| [Portfolio](https://yossefseit.github.io/) | HTTP 200; still contains the former Azure links and `/assets/` CV link. Remote `main` remains at `c9d4e346af3970f9708fa4cf9360f120826029cf`. |
| [Calculator](https://yossefseit.github.io/egypt-salary-calculator/) | HTTP 200 for the document, but its raw `/src/main.tsx` request returns 404. Browser review confirms an empty application root and no `h1`; the migrated application is not live. |
| [Root CV](https://yossefseit.github.io/Yossef_Mohammed_Ali_CV.pdf) | HTTP 404; the reviewed root PDF mirror remains local. |

The Calculator's [successful Pages run 34335934625](https://github.com/yossefseit/egypt-salary-calculator/actions/runs/34335934625) on 9 September used the older commit `1241689611f72dd55f3f575cb41ccbac43200041`. That successful deployment did not publish the local migration or its Vite build. A successful Pages job and an HTTP 200 response alone do not validate the application.

## Historical Azure evidence

The former Static Web Apps release was deployed by [GitHub Actions run 31267818137](https://github.com/yossefseit/yossefseit.github.io/actions/runs/31267818137) at commit `a631f31490372367e5f81c006d6ec273910b1248` on 8 August 2026. That run and the retained Bicep/portal evidence describe a retired host. They do not establish current availability and are absent from the active delivery path.

The former Calculator App Service deployment is retained as [dated run 31909528455](https://github.com/yossefseit/egypt-salary-calculator/actions/runs/31909528455) from 15 August 2026. It does not establish the GitHub Pages demo's current availability.

## Remaining publication requirements

Both Pages source settings are complete. The remaining steps are:

1. review and authorize publication of the local migration;
2. publish the reviewed changes through the branch and pull-request flow to `main`;
3. verify both workflow runs against the migrated commits;
4. run the production checks below, including the built Calculator assets and root CV.

The workflows do not use automatic Pages enablement because it would require a separate administrative token. The owner has already supplied the required settings through GitHub; no further settings action is pending.

## Checks required after publication

- all ten portfolio routes, the custom 404, and the Calculator project route;
- the root CV URL and PDF checksum;
- canonical, Open Graph, JSON-LD, robots, and sitemap URLs;
- GitHub Pages response headers and local meta-CSP behavior, without claiming repository control over platform headers;
- project, profile, pipeline, contact, and fragment links;
- dark/light themes, mobile navigation, command palette, and Calculator interactions;
- accessibility and horizontal overflow at desktop and mobile widths;
- the exact Pages workflow run and deployed commit for each site.

No resource was provisioned, restarted, deployed, or deleted by this local migration work.

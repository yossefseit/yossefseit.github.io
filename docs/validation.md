# Validation Snapshot

- **Date:** 8 September 2026
- **Scope:** Local review of the infrastructure command-centre redesign
- **Publication state:** Local changes only; no push, Azure deployment, or cloud-resource action

This record separates checks run against the current redesign from evidence for the previously deployed release.

## Current redesign result

The current worktree contains ten generated public routes plus the custom 404 document. The generator and dependency-free validator reported:

```text
Verified 10 static pages, sitemap and CSP configuration.
Site validation passed: 11 HTML documents and 303 local references checked.
```

The structural review covered:

- generated-output freshness;
- directly linkable pages and sitemap coverage;
- local links, fragments, images, fonts, and PDF references;
- one primary heading per document;
- titles, descriptions, canonical URLs, social metadata, and structured data;
- the inline JSON-LD hash used by the Content Security Policy;
- new-tab link protection;
- JSON and XML parsing;
- the custom 404 document;
- the exact CV path `/assets/Yossef_Mohammed_Ali_CV.pdf`;
- rejection of links to the legacy CV route.

## Source and configuration checks

| Check | Result |
|---|---|
| `python3 scripts/build_site.py --check` | Pass; ten generated pages, sitemap, and CSP configuration match source |
| `python3 scripts/validate_site.py` | Pass; 11 HTML documents and 303 local references |
| Node syntax checks for `assets/site.js` and `assets/theme.js` | Pass |
| `html-validate` 11.6.2 on all 11 HTML documents | Pass |
| CSS Tree validator 4.0.1 on `assets/site.css` | Pass |
| Bicep CLI 0.46.1 compile of `infra/main.bicep` | Pass |
| JSON, XML, and workflow YAML parsing | Pass |
| `git diff --check` | Pass at the redesign review point |
| SVG XML parsing and local asset resolution | Pass |
| CV signature and exact local route | Pass |
| Markdownlint CLI 0.23.2 on the five repository documentation files | Pass |
| CSpell 10.0.1 on 28 HTML and Markdown files | Pass; zero issues |
| Linkinator 8.0.3 local crawl | Pass; 39 local and enforced external targets |
| GitHub Markdown API render of `README.md` | Pass; heading, banner, screenshot, and Mermaid content present |

The local link crawl excludes LinkedIn, which blocks automated clients, and the canonical Azure origin, which still serves the earlier release. Gitleaks was unavailable locally; the pinned secret-scanning action remains a required step in the GitHub Actions validation job. The reproducible local commands are documented in [Deployment](deployment.md).

## Browser and accessibility checks

Headless Chromium exercised every HTML document at:

- 1440 × 1000 desktop;
- 390 × 844 mobile.

That 22-page and viewport matrix confirmed:

- status `200` for each local route;
- exactly one `h1` per document;
- no horizontal document overflow;
- all local images decode after deliberate lazy-load activation;
- no console errors, page errors, request failures, or missing local assets;
- desktop navigation is available;
- enhanced mobile navigation starts closed and opens from its labelled control;
- navigation labels remain readable at the tested mobile width;
- `Ctrl+K` opens the command palette;
- command filtering plus `Enter` navigates to the selected real route;
- the theme control stores the light preference and a reload preserves it;
- reduced-motion preference is honored;
- every normal page links to the exact CV path;
- no normal page links to the legacy CV path.

Axe ran against all 11 documents at both viewport widths using the WCAG A, WCAG AA, and WCAG 2.1 AA rule sets. It reported zero violations in the tested local context.

The six primary routes were also inspected with the root text size at 200% in a 1280-pixel-wide viewport. No horizontal overflow was found.

These checks validate the static local preview. Python's local HTTP server does not reproduce Azure Static Web Apps response headers, caching, routing, or edge behavior.

## Visual review

The retained review captures show the actual local implementation:

- [landing page, dark desktop](screenshots/portfolio-command-centre-desktop.png);
- [landing page, light desktop](screenshots/portfolio-command-centre-light.png);
- [landing page, mobile](screenshots/portfolio-command-centre-mobile-closed.png);
- [landing page, expanded mobile navigation](screenshots/portfolio-command-centre-mobile.png);
- [Infrastructure view, desktop](screenshots/infrastructure-command-centre-desktop.png);
- [Infrastructure view, mobile](screenshots/infrastructure-command-centre-mobile.png);
- [Egypt Salary Calculator case study](screenshots/salary-case-study-desktop.png).

The visual review confirmed a compact identity header, useful project content in the first desktop viewport, consistent dark and light themes, readable mobile navigation, scalable architecture diagrams, and coherent project-specific imagery.

## Content and evidence review

The redesign uses the supplied CV as the authority for employment, training, education, and contact information. The review reconciled El Mostafa for Master Batch to the CV's July 2024 end month rather than the April 2024 date used by the earlier site.

Project wording was checked against local repositories and public workflow evidence:

| Project | Published wording in the redesign | Evidence boundary |
|---|---|---|
| Egypt Salary Calculator | 57 tests passing; deployment recorded | Fresh local 57-test run; historical App Service deployment run 31909528455; current demo availability kept separate |
| Secure Azure Hub-and-Spoke Lab | Lab: CI validated; Azure deployment pending | Authored Bicep and lifecycle scripts; successful CI run 30944553717; no authenticated deployment or runtime evidence |
| Azure Governance Automation Lab | Lab: CI validated; Azure deployment pending | Authored Bicep, lifecycle scripts, and guard tests; successful CI run 31267342614; no authenticated deployment or runtime evidence |
| Samba AD DC Lab | Lab: CI validated; runtime validation pending | Authored automation and runbooks; no provisioning, client-authentication, restore, or teardown evidence |
| Azure Static Web Apps Portfolio | Existing production delivery; redesign ready for review locally | Public Azure origin and prior deployment evidence; current redesign has not been published |

Professional experience is presented separately from personal projects and labs. Route Academy remains in progress from August 2026 to expected February 2027, and its planned AWS and Kubernetes capstone is not presented as complete. The two IT-Gate programs retain their separate 220-hour and 240-hour records and are not labelled vendor certification exams.

## CV verification

The supplied local file is:

```text
assets/Yossef_Mohammed_Ali_CV.pdf
```

Its SHA-256 at review time is:

```text
bf72173f1bd9ad1f9bfda4fb3b1b9c22f2e7762f1f52c09b78cfa66861120dca
```

All website CV actions resolve to `/assets/Yossef_Mohammed_Ali_CV.pdf`. At the time of this local review, the existing Azure deployment still served the earlier release and did not yet contain that exact path. A reviewed deployment is therefore required before the new canonical CV URL can return the supplied file publicly.

## Prior production evidence

The current Azure Static Web Apps origin was previously validated and deployed by [GitHub Actions run 31267818137](https://github.com/yossefseit/yossefseit.github.io/actions/runs/31267818137) at commit `a631f31490372367e5f81c006d6ec273910b1248` on 8 August 2026.

That earlier release had confirmed:

- the homepage, project catalogue, and then-current case studies returned `200`;
- an unknown nested route returned `404` with the custom document;
- the configured CSP, HSTS, referrer, permissions, content-type, and cross-origin headers were present;
- its then-current CV matched the PDF deployed with that commit;
- a production browser matrix had no overflow, missing images, console errors, page errors, or failed requests;
- a production link crawl resolved its enforced internal and external targets.

Those results prove the existing delivery path and prior release. They do not validate the unpublished command-centre redesign or its replacement CV.

## Checks required after publication

After a reviewed deployment of the redesign, rerun production checks for:

- all ten public routes and the custom 404;
- the exact CV URL and PDF checksum;
- CSP, HSTS, cache, referrer, permissions, MIME, and cross-origin headers;
- canonical, Open Graph, structured-data, robots, and sitemap URLs;
- project, profile, pipeline, contact, and fragment links;
- dark and light themes, mobile navigation, and the command palette under the production CSP;
- accessibility and responsive layout in a normal browser;
- the Open Graph images at their absolute URLs.

## Checks that require external access or authorization

- authenticated `az deployment group validate`;
- authenticated `az deployment group what-if`;
- any deployment of `infra/main.bicep` to the existing production resource;
- Azure portal confirmation of pull-request preview cleanup;
- production verification of the unpublished redesign;
- PDF tagging remediation for the CV and issuer-provided academy documents.

No Azure resource deployment or billable cloud action was performed during this redesign review.

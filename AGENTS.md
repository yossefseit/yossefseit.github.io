# Repository working agreement

## Purpose

This repository is both a recruiter-facing portfolio and an inspectable Azure Static Web Apps reference project. Keep it dependency-light, fast, accessible, and truthful.

## Required checks

Run these before committing:

```bash
python3 scripts/validate_site.py
node --check assets/site.js
git diff --check
```

When the relevant tools are available, also run:

```bash
bicep build infra/main.bicep --stdout >/dev/null
npx --yes html-validate@11.6.2 index.html 404.html projects/index.html projects/azure-secure-hub-spoke/index.html
npx --yes csstree-validator@4.0.1 assets/site.css
npx --yes markdownlint-cli2@0.23.2 "**/*.md"
npx --yes cspell@10.0.1 --config .cspell.json "**/*.{html,md}"
```

Serve the repository root over HTTP for browser, keyboard, responsive, reduced-motion, console, accessibility, and Lighthouse checks. Do not validate only through `file://` URLs.

## Evidence language

Use status terms precisely:

- **authored**: source exists and was reviewed;
- **linted / compiled / CI validated**: the named automated check passed;
- **Azure validated**: authenticated ARM validation passed;
- **what-if reviewed**: authenticated what-if output was inspected;
- **deployed / runtime tested / teardown tested / cost verified**: only after direct evidence exists.

Azure portfolio projects are labs unless a page explicitly identifies the deployed Static Web Apps portfolio. Training is not vendor certification. Employment titles and dates must match `assets/cv.pdf`.

## Safety and privacy

- Do not deploy Azure resources, switch subscriptions or tenants, or run billable tests from this repository without explicit approval.
- Never commit credentials, tenant or subscription IDs, internal addresses, private domains, employer implementation details, customer data, or unsanitized screenshots.
- Do not duplicate the CV phone number or other unnecessary personal details in HTML or Markdown.
- Keep employer work, lab work, planned work, and deployed evidence visibly separate.
- Keep the PNG architecture asset only for social previews; use the optimized SVG in page content.

## Frontend conventions

- Prefer semantic HTML, modern CSS, and minimal defensive JavaScript over a framework or UI dependency.
- Critical content must remain visible without JavaScript and must never depend on animation or intersection observers.
- All interactive behavior must support keyboard use, visible focus, and reduced motion.
- Images require useful alternative text, intrinsic dimensions, and appropriate loading behavior.
- If homepage JSON-LD changes, update the CSP hash in `staticwebapp.config.json`; the validator enforces the match.

## Definition of done

A change is complete only when claims match evidence, links and anchors resolve, mobile and desktop layouts do not overflow, browser checks have no unexplained console errors, security headers remain restrictive, documentation matches implementation, generated artifacts and secrets are absent, and the full diff has been reviewed.

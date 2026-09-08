# Deployment

## Routine review flow

Use a feature branch and pull request for normal changes:

1. edit source content or shared components;
2. regenerate tracked output with `python3 scripts/build_site.py`;
3. run the local checks;
4. push the branch and open a pull request to `main`;
5. confirm validation and, for a trusted same-repository branch, the Azure preview job;
6. review navigation, interactions, content, and responsive layout at the preview URL;
7. merge only after review;
8. confirm the `main` deployment and required public routes;
9. confirm Azure removes the pull-request preview environment.

The trusted same-repository preview upload was verified by pull request #7. Azure Static Web Apps ties the preview lifecycle to the pull request and manages its deletion when the pull request closes. Dependabot and fork pull requests run validation only because GitHub does not expose the deployment secret to those events.

## Edit and preview locally

Page-specific content lives in `content/*.html`. The shared document head, application shell, navigation, footer, and command dialog live in `templates/page.html`. Shared project data, metadata, and route definitions live in `scripts/build_site.py`.

Generate and validate after editing any of those sources:

```bash
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/validate_site.py
```

Serve the repository root:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/`. Review at least:

- the landing, Projects, Infrastructure, Experience, Skills, and About routes;
- all four directly linkable project case studies;
- desktop and mobile navigation;
- the command palette with `Ctrl+K` or `Command+K`;
- dark and light theme persistence after a reload;
- keyboard focus and Escape behavior;
- reduced-motion behavior;
- the custom 404 page;
- `/assets/Yossef_Mohammed_Ali_CV.pdf`.

The dependency-free validator checks generated routes, local links, fragments, image sources, required metadata, heading structure, structured data, sitemap entries, new-tab protection, JSON and XML, the 404 document, the CV signature and path, and the relationship between JSON-LD and the Content Security Policy.

## Full repository checks

The deployment workflow runs these checks before upload:

```bash
python3 scripts/build_site.py --check
python3 scripts/validate_site.py
node --check assets/theme.js
node --check assets/site.js
npx --yes csstree-validator@4.0.1 assets/site.css
npx --yes markdownlint-cli2@0.23.2 "**/*.md"
npx --yes cspell@10.0.1 --config .cspell.json "**/*.{html,md}"
az bicep build --file infra/main.bicep --stdout > /dev/null
```

HTML validation covers:

```text
index.html
404.html
about/index.html
experience/index.html
infrastructure/index.html
projects/index.html
projects/egypt-salary-calculator/index.html
projects/azure-governance-automation/index.html
projects/azure-secure-hub-spoke/index.html
projects/samba-ad-dc-lab/index.html
skills/index.html
```

Use the pinned tool versions in the workflow when reproducing CI results. Run browser accessibility and layout checks after visual or interaction changes. Record only results that actually ran.

## Replace the CV

Every CV action uses this exact path:

```text
/assets/Yossef_Mohammed_Ali_CV.pdf
```

After exporting from Overleaf, overwrite `assets/Yossef_Mohammed_Ali_CV.pdf` without renaming it. Keep the case and underscores unchanged. Then run the generator drift check and site validator. The validator confirms the file is a PDF and rejects links to the legacy CV route.

`staticwebapp.config.json` sets `Cache-Control: no-cache, must-revalidate` for the exact CV route. Do not replace that rule with a long immutable cache while the filename remains stable.

## GitHub Actions flow

For a `main` push or trusted same-repository pull request:

1. `actions/checkout` checks out the triggering commit without persisted credentials.
2. The workflow checks generated output and validates the static site.
3. CI checks JavaScript, HTML, CSS, Markdown, spelling, Bicep, and tracked secrets.
4. `actions/github-script` requests a short-lived GitHub identity token.
5. `Azure/static-web-apps-deploy` receives that token and the repository's Static Web Apps deployment secret.
6. Azure uploads `app_location` directly because `skip_app_build` is enabled.

All actions are pinned to full commit SHAs. The deployment token is referenced by secret name only.

The pinned Azure action metadata does not list `github_id_token`, so GitHub annotates it as an unexpected input. Pull request #8 tested removal and the upload failed; restoring the token restored the successful authentication path. The workflow documents this known annotation. The unsupported `skip_api_build` input remains removed.

The workflow does not run a separate close job. Pull request #7 showed that a redundant `action: close` request could return `BadRequest: No matching static site found` after a successful preview deployment. Microsoft [documents pull-request environments](https://learn.microsoft.com/en-us/azure/static-web-apps/review-publish-pull-requests) as automatically deleted when the pull request closes, so the workflow relies on that lifecycle. Confirm cleanup in the Azure portal after closing a pull request.

## Why Azure skips the application build

The repository has no `package.json` or compiled frontend output. Its HTML, CSS, JavaScript, fonts, images, and documents are already deployable. The workflow uses:

```yaml
app_location: /
api_location: ""
output_location: ""
skip_app_build: true
```

This bypasses Oryx framework detection. The earlier detection failure was:

```text
Could not find build or build:azure script
```

The Python generator is an authoring and validation step. Its generated files are tracked before Azure receives them, so no build runs in the hosting action.

## Azure resource history

The Static Web App was initially connected to GitHub through the Azure Portal. That process created the deployment integration and repository secret. `infra/main.bicep` was added later to represent the intended resource configuration in code.

Before using the template to manage production, perform authenticated validation in a verified subscription:

```bash
az bicep build --file infra/main.bicep
az deployment group validate \
  --resource-group rg-portfolio \
  --template-file infra/main.bicep \
  --parameters \
    staticWebAppName=portfolio-yossef \
    location=eastus2 \
    skuName=Free
az deployment group what-if \
  --resource-group rg-portfolio \
  --template-file infra/main.bicep \
  --parameters \
    staticWebAppName=portfolio-yossef \
    location=eastus2 \
    skuName=Free
```

These values come from the resource JSON and the resource owner's [redacted Portal overview](screenshots/azure-static-web-app-overview-redacted.png). The Portal labels the service location **Global**, while ARM reports the deployable resource location as `eastus2`.

These authenticated commands are not part of the local documentation workflow. Review `what-if` before any production change, with attention to the repository association, `main` branch, deployment authorization, and workflow-generation settings. Do not run `az deployment group create` until the result is understood and approved.

## Secret handling

- Keep the deployment token only in GitHub Actions secrets.
- Never print or store a token in shell history, an issue, an artifact, or a log.
- Reset the Azure token and replace the GitHub secret if exposure is suspected.
- Do not add Azure credentials, service principal secrets, private keys, or connection strings to the repository.

## Production verification

After a reviewed production deployment, check the canonical origin:

```bash
curl -fsSI https://gentle-smoke-06d712d0f.7.azurestaticapps.net/
curl -fsSI https://gentle-smoke-06d712d0f.7.azurestaticapps.net/assets/Yossef_Mohammed_Ali_CV.pdf
curl -fsS https://gentle-smoke-06d712d0f.7.azurestaticapps.net/robots.txt
curl -fsS https://gentle-smoke-06d712d0f.7.azurestaticapps.net/sitemap.xml
```

Confirm:

- status `200` for all ten routes and required assets;
- the exact CV URL returns the expected PDF;
- the configured CSP, HSTS, referrer, permissions, MIME, and cross-origin headers;
- an unknown nested route returns a real `404` with the custom document;
- canonical and social metadata use the confirmed Azure origin;
- project, profile, pipeline, contact, and fragment links work;
- theme, navigation, and command-palette interactions work under the production CSP;
- there are no browser console errors or horizontal overflow at desktop and mobile widths;
- the GitHub Actions run succeeded for the deployed commit.

## Rollback

No automatic rollback is configured. If a deployment introduces a regression:

1. identify the last known-good commit;
2. revert the faulty commit on a new branch;
3. regenerate the site and run validation;
4. review the pull-request preview;
5. merge the revert through the normal workflow.

Avoid rewriting `main` history.

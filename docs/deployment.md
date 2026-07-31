# Deployment

## Routine workflow

Use a feature branch and pull request for normal changes:

1. edit and test locally;
2. run `python3 scripts/validate_site.py`;
3. push the branch and open a pull request to `main`;
4. confirm the validation and, for a trusted same-repository branch, Azure preview jobs;
5. review the preview URL;
6. merge only after review;
7. confirm the `main` deployment;
8. confirm Azure removes the preview environment after the pull request closes.

The trusted same-repository preview upload was verified by pull request #7. Azure Static Web Apps ties the preview lifecycle to the pull request and automatically deletes the environment when the pull request closes. Dependabot and fork pull requests run validation only because GitHub does not expose the Static Web Apps deployment secret to those events.

## Local preview

The site has no build step:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`, then run:

```bash
python3 scripts/validate_site.py
```

Additional optional checks:

```bash
npx --yes html-validate@11.5.6 index.html 404.html
npx --yes linkinator@8.0.2 http://localhost:8000 --recurse
```

Run Lighthouse and an accessibility browser audit when Chromium is available. Do not state scores from expectation alone.

## GitHub Actions flow

For a `main` push or trusted same-repository pull request:

1. `actions/checkout` checks out the triggering commit without persisted credentials.
2. Python standard-library checks validate the site.
3. `actions/github-script` requests a GitHub identity token.
4. `Azure/static-web-apps-deploy` receives that identity token and the repository's Static Web Apps deployment secret.
5. Azure uploads `app_location` directly because `skip_app_build` is enabled.

All actions are pinned to full commit SHAs. The deployment token is referenced by secret name only.

The workflow does not run a separate close job. Pull request #7 showed that the redundant `action: close` call could return `BadRequest: No matching static site found` after a successful preview deployment. Microsoft documents pull request environments as automatically deleted when the pull request closes, so the workflow now relies on that platform lifecycle instead of issuing a second cleanup request. Confirm environment removal in the Azure portal after closing a pull request.

## Why `skip_app_build` is required

This repository does not have a `package.json` or compiled output. During the initial setup, Oryx attempted framework detection and looked for a Node build script:

```text
Could not find build or build:azure script
```

The correct resolution was to describe the site as already-built content:

```yaml
app_location: /
api_location: ""
output_location: ""
skip_app_build: true
skip_api_build: true
```

This avoids a synthetic dependency and build chain.

## Azure resource history

The Static Web App was initially connected to GitHub through the Azure Portal. That process created the deployment integration and repository secret. `infra/main.bicep` was added later to represent the intended resource configuration in code.

Before using the template to manage production, perform:

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

These confirmed values come from the live resource JSON and the resource owner's [redacted Portal overview](screenshots/azure-static-web-app-overview-redacted.png). The Portal labels the service location **Global**, while ARM reports the deployable resource location as `eastus2`.

These authenticated commands are intentionally not run automatically. Review the what-if output before any production change, with particular attention to the GitHub repository association, `main` branch, deployment authorization, and workflow-generation settings. Do not run `az deployment group create` until the result is understood.

## Secret handling

- Keep the deployment token only in GitHub Actions secrets.
- Never print or store a token in a shell history, issue, artifact, or log.
- If the token may be exposed, reset it in Azure and replace the GitHub secret.
- Do not add Azure credentials, service principal secrets, private keys, or connection strings to this repository.

## Deployment verification

After a production deployment, check:

```bash
curl -fsSI https://gentle-smoke-06d712d0f.7.azurestaticapps.net/
curl -fsS https://gentle-smoke-06d712d0f.7.azurestaticapps.net/robots.txt
curl -fsS https://gentle-smoke-06d712d0f.7.azurestaticapps.net/sitemap.xml
```

Confirm:

- status `200` for the homepage and required assets;
- the configured CSP, HSTS, referrer, permissions, and MIME headers;
- a real `404` response with the custom page for an unknown path;
- CV download and project/profile links;
- no browser console errors;
- desktop and mobile rendering;
- the GitHub Actions run is successful for the deployed commit.

## Rollback

No automatic rollback is configured. If a deployment introduces a regression:

1. identify the last known-good commit;
2. revert the faulty commit on a new branch;
3. run validation and review the pull-request preview;
4. merge the revert to redeploy through the normal workflow.

Avoid rewriting `main` history.

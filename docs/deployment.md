# Deployment

## Routine review flow

Use a feature branch and pull request for normal changes:

1. edit source content or shared components;
2. regenerate tracked output with `python3 scripts/build_site.py`;
3. run the local checks and inspect the site at desktop and mobile widths;
4. push the branch and open a pull request to `main`;
5. confirm the validation and Pages artifact job succeeds;
6. review the code, generated diff, screenshots, and local preview;
7. merge only after review;
8. confirm the `github-pages` deployment job and production checks.

Pull requests produce a deployable artifact but do not publish a preview site. The workflow restricts deployment to `main`. GitHub Pages does not provide the former Static Web Apps pull-request preview lifecycle.

## Repository Pages settings

Completed by the repository owner and verified on 9 September 2026 for both `yossefseit.github.io` and `egypt-salary-calculator`:

`Settings → Pages → Build and deployment → Source → GitHub Actions`.

The GitHub Pages API reports `build_type: workflow`, `status: built`, and the expected public URL for both repositories. No further Pages source change is required. Successful deployment runs and the dated production checks are recorded in [Validation](validation.md#published-release-evidence).

The workflow deliberately does not set `enablement: true` on `actions/configure-pages`; automated enablement requires a separate token with administrative Pages access. The owner changed the settings before authorizing the reviewed release through pull requests.

## Published repository links

GitHub's repository About links are separate from tracked README content. The reviewed publication uses these website fields:

| Repository | Website field |
|---|---|
| `yossefseit.github.io` | `https://yossefseit.github.io/` |
| `yossefseit` | `https://yossefseit.github.io/` |
| `egypt-salary-calculator` | `https://yossefseit.github.io/egypt-salary-calculator/` |
| `azure-secure-hub-spoke` | `https://yossefseit.github.io/projects/azure-secure-hub-spoke/` |
| `azure-governance-automation` | `https://yossefseit.github.io/projects/azure-governance-automation/` |
| `samba-ad-dc-lab` | `https://yossefseit.github.io/projects/samba-ad-dc-lab/` |

The portfolio repository description is: “Personal infrastructure and DevOps portfolio with evidence-led case studies, accessible static pages, and validated GitHub Pages delivery.” The Calculator description is: “Arabic-first Egyptian gross-to-net and net-to-gross salary calculator, with browser-local calculations and GitHub Pages delivery.” These replace the former hosting claims without changing the Azure lab descriptions.

All eight owned repositories were audited for documentation links. The six public repositories contain the coordinated updates; the two private repositories contain no README or documentation files requiring changes. Remote About fields and both Pages source settings were updated and verified during publication.

## Local preview

Generate, validate, stage, and serve from the repository root:

```bash
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/validate_site.py
python3 scripts/package_site.py
python3 -m http.server 8000
```

Open `http://localhost:8000/`. Review:

- the landing, Projects, Infrastructure, Experience, Skills, and About routes;
- all four directly linkable project case studies;
- desktop and mobile navigation;
- the command palette with `Ctrl+K` or `Command+K`;
- dark and light theme persistence after a reload;
- keyboard focus and Escape behavior;
- reduced-motion behavior;
- the custom 404 page;
- `/Yossef_Mohammed_Ali_CV.pdf`.

`scripts/package_site.py` creates `_site/` for workflow parity. To inspect the exact artifact surface instead, run the local server from `_site/` after staging it.

## Full repository checks

The workflow runs these checks before artifact upload:

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

HTML validation covers all ten generated routes and `404.html`. Use the pinned tool versions from the workflow when reproducing CI results. Run browser accessibility and layout checks after visual or interaction changes. Record only results that actually ran.

## Replace the CV

Every GitHub-facing CV link uses:

```text
https://yossefseit.github.io/Yossef_Mohammed_Ali_CV.pdf
```

The authoritative repository file remains:

```text
assets/Yossef_Mohammed_Ali_CV.pdf
```

After exporting from Overleaf, overwrite that asset without changing its filename or case. Then run:

```bash
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/validate_site.py
```

The generator writes `Yossef_Mohammed_Ali_CV.pdf` at the repository root. The validator checks the PDF signature and requires both files to be byte-identical. Commit both files together.

GitHub Pages does not expose a repository-defined cache rule for the stable CV filename. A browser or edge may retain an older response temporarily after replacement.

## GitHub Actions flow

For a pull request or `main` update:

1. `actions/checkout` checks out the triggering commit without persisted credentials.
2. The build job verifies generated output and validates the static site.
3. CI checks JavaScript, HTML, CSS, Markdown, spelling, the retained historical Bicep definition, and tracked secrets.
4. `scripts/package_site.py` stages only the public site in `_site/` and adds `.nojekyll`.
5. `actions/configure-pages` reads the Pages configuration without trying to enable it.
6. `actions/upload-pages-artifact` creates the supported Pages artifact.
7. For `main` only, `actions/deploy-pages` publishes through the `github-pages` environment.

All actions are pinned to full commit SHAs. The build job has read-only repository access. The deployment job receives `pages: write` and `id-token: write`, allowing GitHub to issue a short-lived OIDC token bound to the release. No cloud deployment secret is required.

One `pages` concurrency group covers the workflow, with `cancel-in-progress: false`, so an active production release is allowed to finish before another begins.

## Artifact contents

The staged artifact contains only the public website:

- root HTML, robots, sitemap, verification file, and root CV;
- generated route directories;
- `assets/`, including the supplied public academy documents;
- `.nojekyll`.

It excludes source fragments, templates, scripts, workflow definitions, repository documentation, screenshots, and the retired Azure Bicep file. The upload action also requires an archive without symbolic or hard links.

## Security boundary

GitHub Pages cannot read `staticwebapp.config.json` and does not offer a repository mechanism for arbitrary response headers. That retired configuration was removed.

Every HTML document includes a deny-by-default meta Content Security Policy. The generator authorizes the homepage JSON-LD with its exact SHA-256 hash, and the validator independently checks it. A meta policy cannot provide HSTS, `frame-ancestors`, MIME controls, Permissions Policy, COOP, CORP, response cache rules, or equivalent HTTP response protections. Production verification should inspect the actual headers GitHub supplies without claiming repository control over them.

## Retired Azure evidence

`infra/main.bicep` and the redacted portal screenshot remain historical documentation of the former Static Web App. The Pages workflow compiles the Bicep file to keep the retained example valid but never authenticates to Azure or deploys it.

No Azure resource is assumed to exist. Do not run an Azure deployment or restart a retired service as part of this website release.

## Production verification

After a reviewed production deployment, check the canonical origin:

```bash
curl -fsSI https://yossefseit.github.io/
curl -fsSI https://yossefseit.github.io/Yossef_Mohammed_Ali_CV.pdf
curl -fsS https://yossefseit.github.io/robots.txt
curl -fsS https://yossefseit.github.io/sitemap.xml
```

Confirm:

- status `200` for all ten routes and required assets;
- the exact CV URL returns the expected PDF checksum;
- an unknown nested route returns an actual `404` with the custom document;
- canonical, Open Graph, JSON-LD, robots, and sitemap URLs use `https://yossefseit.github.io/`;
- project, profile, pipeline, contact, and fragment links work;
- theme, navigation, and command-palette interactions work under the meta CSP;
- there are no browser console errors or horizontal overflow at desktop and mobile widths;
- the GitHub Actions run succeeded for the deployed commit;
- the Salary Calculator project site is checked separately after its own Pages workflow publishes.

Inspect the response headers GitHub Pages actually supplies, while preserving the distinction between platform behavior and repository-configured policy.

## Rollback

No automatic rollback is configured. If a release introduces a regression:

1. identify the last known-good commit;
2. revert the faulty commit on a new branch;
3. regenerate the site and run validation;
4. review the revert locally and in the pull request;
5. merge through the normal workflow;
6. verify the deployment job and production origin.

Avoid rewriting `main` history.

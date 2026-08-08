# Azure Lab Roadmap

This roadmap prioritizes evidence for Azure administration, cloud infrastructure, operations, and automation roles. The hub-and-spoke and governance labs are authored, linted, compiled, and CI validated. Authenticated Azure validation and all live execution evidence remain pending for both.

The separate [Samba AD DC lab](https://github.com/yossefseit/samba-ad-dc-lab) is authored and repository-CI validated. It demonstrates an identity-operations foundation, but runtime provisioning, client authentication, recovery, rollback, and teardown evidence are still pending.

No Azure resource should be deployed without a cost estimate, budget alert, teardown plan, and explicit review of the target subscription or tenant.

## Delivery standard for every lab

Each lab should include:

- a clear problem statement and status;
- an architecture diagram;
- a threat and access model;
- modular Bicep or Terraform;
- parameter files with no secrets;
- naming, tagging, and cost assumptions;
- deployment and teardown instructions;
- automated lint/build/validation;
- screenshots or sanitized command output;
- verification and failure tests;
- lessons learned and known limitations.

The acceptance bar is evidence that another engineer can inspect and reproduce—not simply a Portal screenshot.

## 1. Secure Hub-and-Spoke Azure Networking

**Priority:** Highest

**Status:** Authored, linted, compiled, and CI validated; live Azure evidence pending

**Repository:** [azure-secure-hub-spoke](https://github.com/yossefseit/azure-secure-hub-spoke)

**Portfolio case study:** [Secure Azure Hub-and-Spoke Infrastructure](https://gentle-smoke-06d712d0f.7.azurestaticapps.net/projects/azure-secure-hub-spoke/)

**Role signal:** Azure networking, security, routing, Infrastructure as Code

### Scope

- hub virtual network;
- two spoke virtual networks;
- bidirectional peering;
- workload and management subnets;
- network security groups;
- route-table guardrails and Application Security Groups;
- expensive production transit and management components documented but excluded;
- Private DNS zone and links;
- Network Watcher diagnostics;
- modular Bicep with dev parameters.

### Security and cost controls

- deny-by-default NSG rules;
- no public workload IPs;
- no public management endpoint; Azure Run Command for the optional validation VM;
- USD 5 total deployment limit and ownership-verified teardown;
- no production or employer address ranges.

### Acceptance evidence

- `bicep build` and lint pass;
- Azure `validate` and reviewed `what-if` (pending authenticated context);
- peering and effective-route output;
- allowed and denied connectivity tests;
- architecture and teardown documentation.

## 2. Azure Governance Automation

**Priority:** High

**Status:** Authored, linted, compiled, and CI validated; Azure evidence pending

**Repository:** [azure-governance-automation](https://github.com/yossefseit/azure-governance-automation)

**Portfolio case study:** [Azure Governance Automation Lab](https://gentle-smoke-06d712d0f.7.azurestaticapps.net/projects/azure-governance-automation/)

**Role signal:** Azure Policy, RBAC, Cost Management, subscription governance, Infrastructure as Code

### Scope

- subscription-scope modular Bicep;
- custom policy definitions and initiative for required tags, allowed locations, and optional tag inheritance;
- audit-first and disabled-by-default effects;
- conditional policy-assignment identity and Tag Contributor access;
- optional group Reader assignment bounded to the governance resource group;
- subscription budget and action group;
- default `CanNotDelete` lock;
- Bash and PowerShell validate, what-if, deploy, and cleanup commands.

### Security and cost controls

- never switch Azure context or deploy outside a verified personally owned subscription;
- keep location and required-tag policies on Audit until compliance and exemptions are reviewed;
- keep tag inheritance and remediation disabled until existing resources and subscription-scope writes are approved;
- use group-based, least-privilege access and short-lived GitHub OIDC in the future design;
- create no standing compute or data workload;
- treat the budget as an alert, not a spending cap;
- delete only exact deployment-manifest IDs after verifying ownership markers.

### Acceptance evidence

- local Bicep lint/build and parameter compile;
- repository invariant, shell analysis, PowerShell analysis, and failure-guard tests;
- exact-commit public CI result (complete);
- authenticated ARM validation and reviewed what-if;
- controlled Audit, Modify, remediation, RBAC, budget-routing, and lock observations;
- guarded teardown and delayed billing review.

## 3. Azure Monitor and Incident Response

**Priority:** High

**Status:** Planned
**Role signal:** Azure operations, observability, alerting, troubleshooting

### Scope

- Log Analytics workspace;
- diagnostic settings;
- Azure Monitor metrics and logs;
- KQL queries;
- alert rules and action group;
- workbook or dashboard;
- incident-response runbook;
- retention and ingestion-cost notes.

### Security and cost controls

- minimal diagnostic categories;
- short lab retention;
- daily ingestion cap where supported;
- no sensitive values in queries or screenshots;
- action group targets use a controlled test address.

### Acceptance evidence

- generated test event;
- query and alert result;
- incident timeline;
- false-positive tuning note;
- exported workbook or documented reconstruction steps.

## 4. Azure Backup and Tested Restore

**Priority:** Medium-high

**Status:** Planned
**Role signal:** Recovery design, operational testing, business continuity

### Scope

- Recovery Services vault;
- Azure VM or supported low-cost workload backup;
- retention policy;
- soft delete and security settings;
- backup job monitoring;
- file-level or VM recovery test;
- recovery-time observations;
- failure and cleanup documentation.

### Security and cost controls

- use non-sensitive generated data;
- calculate protected-instance and storage costs;
- short retention for the lab;
- remove restored resources after verification;
- document immutability and multi-user authorization as design considerations if not enabled.

### Acceptance evidence

- successful backup job;
- documented restore test;
- integrity check of recovered sample data;
- recovery runbook and teardown proof.

## 5. Terraform Implementation and Drift Operations

**Priority:** Medium-high

**Status:** Planned
**Role signal:** Multi-tool Infrastructure as Code, state security, drift, imports, repeatable delivery

### Scope

- reimplement one completed, suitable Bicep lab rather than translate syntax mechanically;
- remote-state design, locking, encryption, retention, and break-glass recovery;
- version-constrained AzureRM provider and modular composition;
- environment variables or identifier-only examples with no credentials;
- formatting, validation, lint, documentation, and secret scanning in CI;
- plan review, apply approval, idempotency, drift detection, imports, and teardown;
- a comparison explaining Bicep deployment scope versus Terraform state and provider behavior.

### Security and cost controls

- never commit state, plans containing sensitive values, provider credentials, or generated keys;
- use a protected, encrypted state backend only after owned-subscription approval;
- separate plan and apply identities and require protected-environment review;
- preserve the source lab's deny-by-default, cost, ownership, and teardown controls;
- document import and state-removal failure modes before live execution.

### Acceptance evidence

- `terraform fmt`, `validate`, and static-security checks;
- reviewed plan with only expected changes;
- successful gated deployment only after an authorized Azure approval;
- second no-change plan and one controlled drift/import exercise;
- state-backup, teardown, and post-removal verification.

## 6. Hybrid AD DS and Microsoft Entra ID

**Priority:** Gated

**Status:** Planned; blocked on verified tenant ownership and licensing review

**Role signal:** AD DS, Microsoft Entra ID, identity lifecycle, hybrid operations

### Scope

- isolated Windows Server AD DS lab;
- personally owned Microsoft Entra test tenant;
- Microsoft Entra Connect Sync versus Cloud Sync design comparison;
- password hash synchronization and scoped organizational-unit design;
- pilot user and group lifecycle;
- Conditional Access design only where licensing permits;
- emergency-access, least-privilege, rollback, and recovery models.

### Security and cost controls

- never use an employer, customer, or uncertain tenant;
- use no real user data and publish no tenant IDs or private domains;
- verify current licensing and free-trial constraints before enabling any feature;
- keep test accounts time-limited and document teardown before synchronization;
- do not claim Conditional Access, synchronization, or sign-in evidence from architecture alone.

### Acceptance evidence

- before/after identity-flow diagram;
- sync scope, attribute, and authentication-method documentation;
- sanitized synchronization-health evidence;
- positive and negative sign-in test matrix;
- documented rollback, recovery, and tenant cleanup.

## Recommended order

1. Complete authenticated validation and live evidence for the hub-spoke and governance labs only in a verified, cost-approved personal subscription.
2. Build Azure Monitor incident response with a reproducible failure and investigation path.
3. Build Azure Backup with an integrity-checked restore drill.
4. Reimplement a suitable completed Bicep lab in Terraform with real state and drift controls.
5. Build hybrid identity only after tenant ownership, licensing, rollback, and cleanup are confirmed.

This sequence converts existing infrastructure strengths into progressively stronger Azure evidence while keeping professional experience and lab work clearly separated.

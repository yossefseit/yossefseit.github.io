# Azure Lab Roadmap

This roadmap prioritizes projects that strengthen Azure Cloud Engineer and Cloud Infrastructure interview evidence. The hub-and-spoke project is implemented and repository-validated; live Azure evidence remains pending. Other projects are **planned** unless a linked repository supplies code and validation evidence.

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

## 1. Hub-and-Spoke Azure Networking

**Priority:** Highest

**Status:** Implemented and locally/CI validated; live Azure evidence pending

**Repository:** [azure-secure-hub-spoke](https://github.com/yossefseit/azure-secure-hub-spoke)

**Portfolio case study:** [Secure Azure Hub-and-Spoke Infrastructure](/projects/azure-secure-hub-spoke/)

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

## 2. Hybrid Identity Lab

**Priority:** High

**Status:** Planned
**Role signal:** AD DS, Microsoft Entra ID, identity lifecycle, hybrid operations

### Scope

- isolated Windows Server AD DS lab;
- Microsoft Entra lab tenant;
- Entra Connect or Cloud Sync comparison;
- password hash synchronization design;
- scoped organizational units;
- pilot user and group lifecycle;
- Conditional Access design documentation;
- emergency-access and least-privilege model.

### Security and cost controls

- never use an employer or personal production tenant;
- no real user data;
- redact tenant IDs and domain details from screenshots;
- document licensing requirements before enabling Conditional Access;
- use time-limited test accounts and a teardown checklist.

### Acceptance evidence

- before/after identity flow diagram;
- sync-scope and attribute documentation;
- sanitized synchronization health evidence;
- sign-in test matrix;
- documented rollback and failure scenarios.

## 3. Azure Monitoring and Incident Response

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

## 4. Azure Backup and Recovery

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

## 5. Modular Bicep and Gated CI/CD

**Priority:** Medium-high

**Status:** Planned
**Role signal:** Infrastructure automation, DevOps controls, repeatable delivery

### Scope

- reusable modules for resource groups, networking, monitoring, and role assignments;
- dev/test parameter files;
- naming and tagging module;
- Bicep configuration and lint rules;
- GitHub Actions build and validation;
- pull-request `what-if`;
- protected, manually approved deployment environment;
- OIDC-based Azure login with no long-lived service-principal secret.

### Security and cost controls

- least-privilege federated identity;
- environment approval before deployment;
- no secrets in parameter files or workflow output;
- concurrency lock;
- teardown workflow requires explicit approval;
- cost-impact notes included with each pull request.

### Acceptance evidence

- lint/build output;
- reviewed `what-if`;
- successful gated deployment to a lab resource group;
- drift or idempotency check;
- teardown and post-removal verification.

## Recommended order

1. Complete live evidence for the implemented hub-and-spoke project when an authorized Azure context is available.
2. Build governance and identity automation.
3. Add monitoring incident response and recovery.
4. Add backup and restore evidence.
5. Build hybrid identity in a separate controlled tenant.

This sequence converts existing infrastructure strengths into progressively stronger Azure evidence while keeping professional experience and lab work clearly separated.

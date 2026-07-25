targetScope = 'resourceGroup'

// infra/main.bicep
//
// Deploy this file to the existing `rg-portfolio` resource group. `targetScope`
// selects the deployment level; the resource-group name is supplied by the
// deployment command.
//
// Declarative definition added after the Azure Static Web App was created
// through the Azure Portal. It must not generate or rewrite the repository's
// existing GitHub Actions workflow.
//
// Deliberately does NOT set `repositoryUrl` / `repositoryToken`. Those
// properties let Azure Resource Manager manage its own GitHub Actions
// workflow, but this repo already has a hand-maintained workflow under
// .github/workflows/ that shouldn't be silently rewritten. This template
// is intended to manage the *Azure resource* only after a reviewed what-if;
// the workflow file remains the single source of truth for CI/CD.

@description('Name of the Static Web App resource')
param staticWebAppName string = 'portfolio-yossef'

@description('Azure region. Static Web Apps only deploys to a subset of regions.')
@allowed([
  'westus2'
  'centralus'
  'eastus2'
  'westeurope'
  'eastasia'
])
param location string = 'eastus2'

@description('Pricing plan for the Static Web App')
@allowed([
  'Free'
  'Standard'
])
param skuName string = 'Free'

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: staticWebAppName
  location: location
  sku: {
    name: skuName
    tier: skuName
  }
  properties: {
    buildProperties: {
      appLocation: '/'
      apiLocation: ''
      outputLocation: ''
      skipGithubActionWorkflowGeneration: true
    }
    // Keeps PR preview environments enabled without generating a workflow.
    stagingEnvironmentPolicy: 'Enabled'
  }
}

output defaultHostname string = staticWebApp.properties.defaultHostname
output resourceId string = staticWebApp.id

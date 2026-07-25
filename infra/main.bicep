targetScope = 'resourceGroup'

// infra/main.bicep
//
// Declarative definition of the Azure Static Web App that hosts this site.
//
// Deliberately does NOT set `repositoryUrl` / `repositoryToken`. Those
// properties let Azure Resource Manager manage its own GitHub Actions
// workflow, but this repo already has a hand-maintained workflow under
// .github/workflows/ that shouldn't be silently rewritten. This template
// owns the *Azure resource*; the workflow file remains the single source of
// truth for the CI/CD pipeline itself.

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
    // Keeps PR preview environments enabled — see docs/architecture.md
    stagingEnvironmentPolicy: 'Enabled'
  }
}

output defaultHostname string = staticWebApp.properties.defaultHostname
output resourceId string = staticWebApp.id

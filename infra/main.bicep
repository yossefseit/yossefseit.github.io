targetScope = 'resourceGroup'

metadata existingAzureResource = {
  resourceGroup: 'rg-portfolio'
  resourceName: 'portfolio-yossef'
  resourceLocation: 'eastus2'
  portalDisplayLocation: 'Global'
  sku: 'Free'
  defaultHostname: 'gentle-smoke-06d712d0f.7.azurestaticapps.net'
  sourceProvider: 'GitHub'
  sourceRepository: 'https://github.com/yossefseit/yossefseit.github.io'
  sourceBranch: 'main'
  workflowManagedOutsideBicep: true
}

@description('Name of the Static Web App resource')
param staticWebAppName string = 'portfolio-yossef'

@description('Azure resource location from ARM JSON. The Portal displays this global service as "Global".')
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

resource staticWebApp 'Microsoft.Web/staticSites@2024-11-01' = {
  name: staticWebAppName
  location: location
  sku: {
    name: skuName
    tier: skuName
  }
  properties: {
    allowConfigFileUpdates: true
    buildProperties: {
      appLocation: '/'
      apiLocation: ''
      outputLocation: ''
      skipGithubActionWorkflowGeneration: true
    }
    enterpriseGradeCdnStatus: 'Disabled'
    // Keeps PR preview environments enabled without generating a workflow.
    stagingEnvironmentPolicy: 'Enabled'
  }
}

output defaultHostname string = staticWebApp.properties.defaultHostname
@description('Resource group supplied to the resource-group deployment command.')
output resourceGroupName string = resourceGroup().name
output resourceId string = staticWebApp.id

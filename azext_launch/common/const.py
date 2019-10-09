GITHUB_REQUEST_HEADERS = {'Content-Type': 'application/json' + '; charset=utf-8',
                'Accept': 'application/json'}

LAUNCH_AZURE_APP_SERVICE_URL = 'https://launchsvccliintegration.azurewebsites.net/'


LAUNCH_SERVICE_CLI_AUTH_CONFIG_URL = LAUNCH_AZURE_APP_SERVICE_URL+'ConfigureCLIAuth'
LAUNCH_ORG_PIPELINE_SETUP = LAUNCH_AZURE_APP_SERVICE_URL + 'LaunchPipelineUrlresolver'

LAUNCH_CLI_GITHUB_PAT_ENVKEY = 'LAUNCH_CLI_GITHUB_PAT'
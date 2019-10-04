# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from knack.log import get_logger
from knack.util import CLIError
from knack.prompting import NoTTYException, prompt_pass, prompt
from github import Github,GithubException,TwoFactorException
from azext_launch.common.github_credential_manager import GithubCredentialManager
from azext_launch.common.const import (LAUNCH_AZURE_APP_SERVICE_URL,GITHUB_REQUEST_HEADERS,
                                        LAUNCH_SERVICE_CLI_AUTH_CONFIG_URL, LAUNCH_ORG_PIPELINE_SETUP)
from azext_launch.common.prompting import (prompt_user_friendly_choice_list,
                                            verify_is_a_tty_or_raise_error,
                                            prompt_not_empty)
import sys
import base64
import requests
logger = get_logger(__name__)


def launch_auth_and_init(cmd):
    try:
        github_token = get_github_pat_token()
        github_obj = Github(github_token)
        selected_repo = get_repo_from_user(github_obj)
        if selected_repo:
            repo_details = github_obj.get_user().get_repo(selected_repo)
            print('Setting up pipeline for your repo')
            launch_pipeline_setup(github_token,github_obj,repo_details)
    except Exception as ex:
        raise CLIError(ex)


def launch_pipeline_setup(github_token,github_obj,github_repo):
    pipeline_url = None
    get_user = github_obj.get_user()
    login_account = get_user.login
    request_body = {
        'action':'cliRepoConfig',
        'installation':{
            'id':1,
            'account':{
                'login':login_account
            }
        },
        'repositories':[
            {
                'id':github_repo.id,
                'name':github_repo.name,
                'full_name':github_repo.full_name
            }
        ],
        'cliAuthDetails':{
            'authorization':{
                'scheme':'PersonalAccessToken',
                'accessToken':github_token
            }
        }
    }

    response = requests.post(LAUNCH_ORG_PIPELINE_SETUP,json=request_body,  headers=GITHUB_REQUEST_HEADERS)
    if response.status_code == 200:
        response_json=response.json()
        pipelineId = str(response_json['azPipelineDefId'])
        pipeline_url = response_json['azDevOrganizationGuid'] +"/"+ response_json['azDevProjectGuid'] +"/_build?definitionId="+pipelineId
        print('Pipeline created! URL: '+pipeline_url)
    else:
        CLIError('Pipeline Creation failed')
    return pipeline_url


def get_github_pat_token():
    github_manager = GithubCredentialManager()
    return github_manager.get_token()


def setup_repo_hooks(repo_hooks_url,token, pipeline_url):
    request_body = {
        'name':'web',
        'active':True,
        'events': [
            'push',
            'pull_request'
        ],
        'config':{
            'url':pipeline_url,
            'content_type':'json',
            'insecure_ssl':'0'
        }
    }
    response = requests.post(repo_hooks_url,json=request_body, auth=('', token), headers=GITHUB_REQUEST_HEADERS)
    if response.status_code == 201:
        print('Webhook configured successfully.')
    elif response.status_code == 422:
        raise CLIError(response.json()['errors'][0]['message'])
    else:
        CLIError("Couldn't configure webhooks.")

    
def get_repo_from_user(github_obj):
    #github_obj=get_github_object()
    if github_obj is not None:
        response = github_obj.get_user().get_repos(type='owner')     
        repo_list = []
        for repo in response:
            repo_list.append(repo.name)
        repo_selection_index = prompt_user_friendly_choice_list("Which repo do you want to set up for launch service?",
                                                               repo_list)
        
        return repo_list[repo_selection_index]
    return None



    

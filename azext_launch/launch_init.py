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
            repo_hooks_url = repo_details.hooks_url
            print('Setting up auth')
            launch_authentication(github_token,repo_hooks_url)
            print('Setting up pipeline for your repo')
            launch_pipeline_setup(github_obj,repo_details)
            print('Setting up webhooks for your repo')
            setup_repo_hooks(repo_hooks_url,github_token)
    except Exception as ex:
        raise CLIError(ex)

def launch_authentication(github_token, github_repo_url):
    request_body = {
        'authorization':{
            'scheme':'PersonalAccessToken',
            'accessToken':github_token
        }
    }
    response = requests.post(LAUNCH_SERVICE_CLI_AUTH_CONFIG_URL,json=request_body,  headers=GITHUB_REQUEST_HEADERS)
    if response.status_code == 200:
        print('PAT configured successfully.')
    else:
        CLIError("Authentication details couldn't be send Launch service!")  


def launch_pipeline_setup(github_obj,github_repo):
    import pdb
    pdb.set_trace()
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
        ]
    }
    response = requests.post(LAUNCH_ORG_PIPELINE_SETUP,json=request_body,  headers=GITHUB_REQUEST_HEADERS)
    if response.status_code == 200:
        print('Pipeline created!')
        pipeline_url=response
    else:
        CLIError("Some error occurred.")
    return pipeline_url


def get_github_pat_token():
    github_manager = GithubCredentialManager()
    return github_manager.get_token()


def setup_repo_hooks(repo_hooks_url,token, pipeline_url=None):
    pipeline_url = 'https://dev.azure.com/LaunchServiceOrgExample/7c6458b6-155a-4eb4-a546-fff0fd629d25/_apis/build/Definitions/46?revision=1'
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
        CLIError("Cou;dn't configure webhooks.")

    
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



    

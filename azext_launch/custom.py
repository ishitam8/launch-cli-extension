# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from knack.log import get_logger
from knack.util import CLIError
from knack.prompting import NoTTYException, prompt_pass, prompt
from github import Github,GithubException,TwoFactorException
from azext_launch.common.github_credential_manager import GithubCredentialManager
from azext_launch.common.prompting import (prompt_user_friendly_choice_list,
                                            verify_is_a_tty_or_raise_error,
                                            prompt_not_empty)
import sys
import base64
import requests
logger = get_logger(__name__)


def launch_init(cmd):
    try:
        github_token = get_github_pat_token()
        github_obj = Github(github_token)
        selected_repo = get_repo_from_user(github_obj)
        if selected_repo:
            print('setting up webhooks for your repo')
            repo_hooks_url = github_obj.get_user().get_repo(selected_repo).hooks_url
            setup_repo_hooks(repo_hooks_url,github_token)
    except Exception as ex:
        raise CLIError(ex)


def get_github_pat_token():
    github_manager = GithubCredentialManager()
    return github_manager.get_token()


def setup_repo_hooks(repo_hooks_url,token):
    target_url = 'http://104.214.111.66/api/home'
    request_body = {
        'name':'web',
        'active':True,
        'events': [
            'push',
            'pull_request'
        ],
        'config':{
            'url':target_url,
            'content_type':'json',
            'insecure_ssl':'0'
        }
    }
    headers = {'Content-Type': 'application/json' + '; charset=utf-8',
                'Accept': 'application/json'}
    response = requests.post(repo_hooks_url,json=request_body, auth=('', token), headers=headers)
    if response.status_code == 201:
        print('Webhook configured succesfully.')
    elif response.status_code == 422:
        raise CLIError(response.json()['errors'][0]['message'])
    else:
        CLIError('Webhook configuration failed!')

    
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



    

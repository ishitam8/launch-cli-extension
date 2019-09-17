# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from knack.log import get_logger
from knack.util import CLIError
from knack.prompting import NoTTYException, prompt_pass
from github import Github
from azext_launch.common.credential import get_password, set_password, clear_password
from azext_launch.common.prompting import (prompt_user_friendly_choice_list,
                                            verify_is_a_tty_or_raise_error,
                                            prompt_not_empty)
import sys
import base64
import requests
logger = get_logger(__name__)

def login_launch(cmd, github_username=None, github_password=None):
    g = None
    if github_username is None:
        pat_token = _get_pat_token()
        g = Github(pat_token)
        set_password(key=_DEFAULT_LAUNCH_KEY,pwd=pat_token)

    if github_username is not None:
        github_password = _get_password()
        g = Github(github_username, github_password)
        set_password(key=_LAUNCH_USEER_KEY_PREFIX+github_username,pwd=github_password)

    if g is not None:
        response = g.get_user().get_repos()
        for repo in response:
            print(repo.name)
            #print(dir(repo))
        return response
    else:
        raise CLIError('Either username/password or github PAT is required.')


def launch_init(cmd,github_username=None):
    github_obj, basic_auth=get_github_object_and_auth(github_username)
    selected_repo = get_repo_from_user(github_obj)
    if selected_repo and basic_auth:
        print('setting up webhooks for your repo')
        repo_hooks_url = github_obj.get_user().get_repo(selected_repo).hooks_url
        setup_repo_hooks(repo_hooks_url,basic_auth)


def setup_repo_hooks(repo_hooks_url,basic_auth):
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
                'Accept': 'application/json',
                'Authorization': basic_auth}
    response = requests.post(repo_hooks_url,json=request_body, headers=headers)
    if response.status_code == 201:
        print('Webhook configured succesfully.')
    elif response.status_code == 422:
        print(response.errors[0].message)
    else:
        print('Webhook configuration failed!')


def basic_auth_header(github_username,github_password):
    encoded_pass = base64.b64encode(github_username.encode('utf-8') + b':' + github_password.encode('utf-8'))
    basic_auth = 'basic ' + encoded_pass.decode("utf-8")
    return basic_auth
    
def get_repo_from_user(github_obj):
    #github_obj=get_github_object()
    if github_obj is not None:
        response = github_obj.get_user().get_repos()
        
        repo_list = []
        for repo in response:
            repo_list.append(repo.name)
        repo_selection_index = prompt_user_friendly_choice_list("Which repo do you want to set up for launch service?",
                                                               repo_list)
        
        return repo_list[repo_selection_index]
    return None


def get_github_object_and_auth(github_username):
    github_obj = None
    basic_auth = None
    if github_username is not None:
        github_password = get_password(_LAUNCH_USEER_KEY_PREFIX+github_username)
        github_obj = Github(github_username, github_password)
        basic_auth = basic_auth_header(github_username,github_password)
    elif get_password(_DEFAULT_LAUNCH_KEY) is not None:
        github_pat = get_password(_DEFAULT_LAUNCH_KEY)
        github_obj = Github(github_pat)
    return github_obj, basic_auth


def _get_pat_token():
    try:
        token = prompt_pass('Token: ', confirm=False, help_string="The token (PAT) to authenticate with.")
    except NoTTYException:
        logger.info("Getting PAT token in non-interactive mode.")
        token = sys.stdin.readline().rstrip()
    return token

def _get_password():
    github_pwd=None
    try:
        github_pwd = prompt_pass('Password: ', confirm=False, help_string="The GitHub password.")
    except NoTTYException:
        logger.info("Can't accept the Github password in non-interactive mode. Try with PAT.")
    return github_pwd

_DEFAULT_LAUNCH_KEY = "default:launch-cli"
_LAUNCH_USEER_KEY_PREFIX = "launch-cli:"
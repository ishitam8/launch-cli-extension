# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def get_password(key):
    try:
        import keyring
        return keyring.get_password(key, _USERNAME)
    except RuntimeError as ex:
        raise CLIError(ex)


def set_password(key, pwd):
    try:
        import keyring
        return keyring.set_password(key, _USERNAME, pwd)
    except RuntimeError as ex:
        raise CLIError(ex)


def clear_password(key):
    try:
        import keyring
        return keyring.delete_password(key, _USERNAME)
    except RuntimeError as ex:
        raise CLIError(ex)

_USERNAME = 'Personal Access Token'
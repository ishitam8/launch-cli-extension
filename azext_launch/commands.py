# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType


def load_command_table(self, _):
    with self.command_group('launch',is_preview=True) as g:
        g.custom_command('init', 'launch_auth_and_init')



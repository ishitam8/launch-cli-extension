# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azext_launch._client_factory import cf_launch


def load_command_table(self, _):

    # TODO: Add command type here
    # launch_sdk = CliCommandType(
    #    operations_tmpl='<PATH>.operations#None.{}',
    #    client_factory=cf_launch)


    with self.command_group('launch') as g:
        # g.command('delete', 'delete')
        g.custom_command('init', 'launch_init')
        

    with self.command_group('launch', is_preview=True):
        pass


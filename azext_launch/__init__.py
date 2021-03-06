# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader

from azext_launch._help import helps  # pylint: disable=unused-import


class LaunchCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        launch_init = CliCommandType(
            operations_tmpl='azext_launch.launch_init#{}')
        super(LaunchCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                  custom_command_type=launch_init)

    def load_command_table(self, args):
        from azext_launch.commands import load_command_table
        load_command_table(self, args)
        return self.command_table


COMMAND_LOADER_CLS = LaunchCommandsLoader

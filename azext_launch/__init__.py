# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader

from azext_launch._help import helps  # pylint: disable=unused-import


class LaunchCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        from azext_launch._client_factory import cf_launch
        launch_custom = CliCommandType(
            operations_tmpl='azext_launch.custom#{}',
            client_factory=cf_launch)
        super(LaunchCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                  custom_command_type=launch_custom)

    def load_command_table(self, args):
        from azext_launch.commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_launch._params import load_arguments
        load_arguments(self, command)


COMMAND_LOADER_CLS = LaunchCommandsLoader

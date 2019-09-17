# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType


def load_arguments(self, _):

    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group

    launch_name_type = CLIArgumentType(options_list='--launch-name-name', help='Name of the launch extension.', id_part='name')

    with self.argument_context('launch login') as c:
        c.argument('github_username', launch_name_type, options_list=['--username', '-u'])
        c.argument('github_password', launch_name_type, options_list=['--password', '-p'])
        c.argument('github_token', launch_name_type, options_list=['--token'])

    
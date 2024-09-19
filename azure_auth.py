# Copyright (C) Microsoft Corporation.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import dnf
import json
import subprocess
import os

logger = logging.getLogger("dnf.plugin.azure_auth")

AZ_COMMAND = [
    "az",
    "account",
    "get-access-token",
    "--output",
    "json",
    "--resource",
    "https://storage.azure.com",
]


class AzureAuthConfigParser(object):
    """Config parser

    Args:
      conf (libdnf.conf.ConfigParser): Config to parse

    """

    def __init__(self, conf):
        self.conf = conf

    def parse_config(self):
        conf = self.conf
        azure_auth_map = {}
        # config format is extensible to support per-repo options,
        # though there are none currently
        for section in conf.sections():
            azure_auth_map[section] = {}
        return azure_auth_map


class AzureAuth(dnf.Plugin):
    name = "azure_auth"

    def __init__(self, base, cli):
        super(AzureAuth, self).__init__(base, cli)

    def config(self):
        conf = self.read_config(self.base.conf)

        parser = AzureAuthConfigParser(conf)
        azure_auth_map = parser.parse_config()

        # Reuse the token between repos (if we add cross-tenant support,
        # this will need to change to per-tenant tokens), to avoid multiple
        # browser popups when not `az login`ed
        token = os.getenv("DNF_PLUGIN_AZURE_AUTH_TOKEN", None)
        for key in azure_auth_map.keys():
            repo = self.base.repos.get(key, None)
            if repo and repo.enabled:
                if not token:
                    token = get_token()
                repo.set_http_headers(
                    [
                        "x-ms-version: 2022-11-02",
                        "Authorization: Bearer {}".format(token),
                    ]
                )


def get_token():
    # if SUDO_USER is set, then run az as that account using runuser,
    # to avoid user's having to be both `az login`ed and `sudo az login`ed
    if "SUDO_USER" in os.environ:
        cmd = ["runuser", "-u", os.environ["SUDO_USER"], "--"] + AZ_COMMAND
    else:
        cmd = AZ_COMMAND

    try:
        output = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        # Upon an error if running as sudo try again without runuser in case our user
        # has permission on the storage account but the sudo user doesn't.
        if "SUDO_USER" in os.environ:
            output = subprocess.run(
                AZ_COMMAND,
                check=True,
                stdout=subprocess.PIPE,
            )
        else:
            raise e

    return json.loads(output.stdout)["accessToken"]

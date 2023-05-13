#
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_ping config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import time

from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.parsing import (
    Conditional,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_lines,
    transform_commands,
)
from ansible_collections.cisco.ioscm.plugins.module_utils.network.ioscm.ioscm import run_commands


class Command:
    """The ios_ping config class."""

    def __init__(self, module) -> None:
        self.module = module
        self.result = {}

    def execute_module(self):
        """Execute the module.

        :rtype: A dictionary
        :returns: The result from module execution
        """
        return self.generate_command()

    def parse_commands(self, module, warnings):
        commands = transform_commands(module)
        if module.check_mode:
            for item in list(commands):
                if not item["command"].startswith("show"):
                    warnings.append(
                        "Only show commands are supported when using check mode, not executing %s"
                        % item["command"],
                    )
                    commands.remove(item)
        return commands

    def generate_command(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        warnings = []
        result = {"changed": False, "warnings": warnings}
        commands = self.parse_commands(self.module, warnings)
        wait_for = self.module.params["wait_for"] or []
        conditionals = []
        try:
            conditionals = [Conditional(c) for c in wait_for]
        except AttributeError as exc:
            self.module.fail_json(msg=to_text(exc))
        retries = self.module.params["retries"]
        interval = self.module.params["interval"]
        match = self.module.params["match"]
        while retries >= 0:
            responses = run_commands(self.module, commands)
            for item in list(conditionals):
                if item(responses):
                    if match == "any":
                        conditionals = []
                        break
                    conditionals.remove(item)
            if not conditionals:
                break
            time.sleep(interval)
            retries -= 1
        if conditionals:
            failed_conditions = [item.raw for item in conditionals]
            msg = "One or more conditional statements have not been satisfied"
            self.module.fail_json(msg=msg, failed_conditions=failed_conditions)
        result.update({"stdout": responses, "stdout_lines": list(to_lines(responses))})
        return result

    def run_command(self):
        ping_results = run_commands(self.module, commands=self.result["commands"])
        return ping_results

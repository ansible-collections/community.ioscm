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


import json

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    NetworkConfig,
    dumps,
)
from ansible_collections.community.ioscm.plugins.module_utils.network.ioscm.ioscm import (
    get_config,
    get_connection,
    get_defaults_flag,
    run_commands,
)


class Config:
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

    def check_args(self, module, warnings):
        if module.params["multiline_delimiter"] and len(module.params["multiline_delimiter"]) != 1:
            module.fail_json(
                msg="multiline_delimiter value can only be a single character",
            )

    def edit_config_or_macro(self, connection, commands):
        # only catch the macro configuration command,
        # not negated 'no' variation.
        if commands[0].startswith("macro name"):
            connection.edit_macro(candidate=commands)
        else:
            connection.edit_config(candidate=commands)

    def get_candidate_config(self, module):
        candidate = ""
        if module.params["src"]:
            candidate = module.params["src"]
        elif module.params["lines"]:
            candidate_obj = NetworkConfig(indent=1)
            parents = module.params["parents"] or []
            candidate_obj.add(module.params["lines"], parents=parents)
            candidate = dumps(candidate_obj, "raw")
        return candidate

    def get_running_config(self, module, current_config=None, flags=None):
        running = module.params["running_config"]
        if not running:
            if not module.params["defaults"] and current_config:
                running = current_config
            else:
                running = get_config(module, flags=flags)
        return running

    def save_config(self, module, result):
        result["changed"] = True
        if not module.check_mode:
            run_commands(module, "copy running-config startup-config\r")
        else:
            module.warn(
                "Skipping command `copy running-config startup-config` due to check_mode.  Configuration not copied to non-volatile storage",
            )

    def generate_command(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        result = {"changed": False}
        warnings = []
        self.check_args(self.module, warnings)
        result["warnings"] = warnings
        diff_ignore_lines = self.module.params["diff_ignore_lines"]
        config = None
        contents = None
        flags = get_defaults_flag(self.module) if self.module.params["defaults"] else []
        connection = get_connection(self.module)
        if (
            self.module.params["backup"]
            or self.module._diff
            and self.module.params["diff_against"] == "running"
        ):
            contents = get_config(self.module, flags=flags)
            config = NetworkConfig(indent=1, contents=contents)
            if self.module.params["backup"]:
                result["__backup__"] = contents
        if any((self.module.params["lines"], self.module.params["src"])):
            match = self.module.params["match"]
            replace = self.module.params["replace"]
            path = self.module.params["parents"]
            candidate = self.get_candidate_config(self.module)
            running = self.get_running_config(self.module, contents, flags=flags)
            try:
                response = connection.get_diff(
                    candidate=candidate,
                    running=running,
                    diff_match=match,
                    diff_ignore_lines=diff_ignore_lines,
                    path=path,
                    diff_replace=replace,
                )
            except ConnectionError as exc:
                self.module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))
            config_diff = response["config_diff"]
            banner_diff = response["banner_diff"]
            if config_diff or banner_diff:
                commands = config_diff.split("\n")
                if self.module.params["before"]:
                    commands[:0] = self.module.params["before"]
                if self.module.params["after"]:
                    commands.extend(self.module.params["after"])
                result["commands"] = commands
                result["updates"] = commands
                result["banners"] = banner_diff

                # send the configuration commands to the device and merge
                # them with the current running config
                if not self.module.check_mode:
                    if commands:
                        self.edit_config_or_macro(connection, commands)
                    if banner_diff:
                        connection.edit_banner(
                            candidate=json.dumps(banner_diff),
                            multiline_delimiter=self.module.params["multiline_delimiter"],
                        )
                result["changed"] = True
        running_config = self.module.params["running_config"]
        startup_config = None
        if self.module.params["save_when"] == "always":
            self.save_config(self.module, result)
        elif self.module.params["save_when"] == "modified":
            output = run_commands(self.module, ["show running-config", "show startup-config"])
            running_config = NetworkConfig(
                indent=1,
                contents=output[0],
                ignore_lines=diff_ignore_lines,
            )
            startup_config = NetworkConfig(
                indent=1,
                contents=output[1],
                ignore_lines=diff_ignore_lines,
            )
            if running_config.sha1 != startup_config.sha1:
                self.save_config(self.module, result)
        elif self.module.params["save_when"] == "changed" and result["changed"]:
            self.save_config(self.module, result)
        if self.module._diff:
            if not running_config:
                output = run_commands(self.module, "show running-config")
                contents = output[0]
            else:
                contents = running_config

            # recreate the object in order to process diff_ignore_lines
            running_config = NetworkConfig(
                indent=1,
                contents=contents,
                ignore_lines=diff_ignore_lines,
            )
            if self.module.params["diff_against"] == "running":
                if self.module.check_mode:
                    self.module.warn(
                        "unable to perform diff against running-config due to check mode",
                    )
                    contents = None
                else:
                    contents = config.config_text
            elif self.module.params["diff_against"] == "startup":
                if not startup_config:
                    output = run_commands(self.module, "show startup-config")
                    contents = output[0]
                else:
                    contents = startup_config.config_text
            elif self.module.params["diff_against"] == "intended":
                contents = self.module.params["intended_config"]
            if contents is not None:
                base_config = NetworkConfig(
                    indent=1,
                    contents=contents,
                    ignore_lines=diff_ignore_lines,
                )
                if running_config.sha1 != base_config.sha1:
                    before, after = "", ""
                    if self.module.params["diff_against"] == "intended":
                        before = running_config
                        after = base_config
                    elif self.module.params["diff_against"] in ("startup", "running"):
                        before = base_config
                        after = running_config
                    result.update(
                        {
                            "changed": True,
                            "diff": {"before": str(before), "after": str(after)},
                        },
                    )

        if result.get("changed") and any((self.module.params["src"], self.module.params["lines"])):
            msg = (
                "To ensure idempotency and correct diff the input configuration lines should be"
                " similar to how they appear if present in"
                " the running configuration on device"
            )
            if self.module.params["src"]:
                msg += " including the indentation"
            if "warnings" in result:
                result["warnings"].append(msg)
            else:
                result["warnings"] = msg

        return result

# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


"""
The arg spec for the ioscm_command module
"""
__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# cli_rm_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the module docstring and re-run
# cli_rm_builder.
#
#############################################


class ConfigArgs:  # pylint: disable=R0903
    """The arg spec for the ios_ping module."""

    argument_spec = {
        "src": {"type": "str"},
        "lines": {"aliases": ["commands"], "type": "list", "elements": "str"},
        "parents": {"type": "list", "elements": "str"},
        "before": {"type": "list", "elements": "str"},
        "after": {"type": "list", "elements": "str"},
        "match": {"default": "line", "choices": ["line", "strict", "exact", "none"]},
        "replace": {"default": "line", "choices": ["line", "block"]},
        "multiline_delimiter": {"default": "@"},
        "running_config": {"aliases": ["config"]},
        "intended_config": {},
        "defaults": {"type": "bool", "default": False},
        "backup": {"type": "bool", "default": False},
        "backup_options": {
            "type": "dict",
            "options": {"filename": {}, "dir_path": {"type": "path"}},
        },
        "save_when": {"choices": ["always", "never", "modified", "changed"], "default": "never"},
        "diff_against": {"choices": ["startup", "intended", "running"]},
        "diff_ignore_lines": {"type": "list", "elements": "str"},
    }  # pylint: disable=C0301
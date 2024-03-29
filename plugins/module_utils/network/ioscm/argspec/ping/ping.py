# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


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

"""
The arg spec for the ioscm_ping module
"""


class PingArgs:  # pylint: disable=R0903
    """The arg spec for the ios_ping module."""

    argument_spec = {
        "count": {"type": "int"},
        "afi": {"choices": ["ip", "ipv6"], "default": "ip", "type": "str"},
        "dest": {"required": True, "type": "str"},
        "df_bit": {"default": False, "type": "bool"},
        "source": {"type": "str"},
        "ingress": {"type": "str"},
        "egress": {"type": "str"},
        "timeout": {"type": "int"},
        "state": {
            "choices": ["absent", "present"],
            "default": "present",
            "type": "str",
        },
        "vrf": {"type": "str"},
    }  # pylint: disable=C0301

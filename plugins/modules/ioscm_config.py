# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function


__metaclass__ = type
DOCUMENTATION = """
module: ioscm_config
author: Sagar Paul (@KB-perByte)
short_description: Module to manage configuration sections.
description:
- Cisco IOS configurations use a simple block indent file syntax for segmenting configuration
  into sections.  This module provides an implementation for working with IOS configuration
  sections in a deterministic way.
version_added: 1.0.0
extends_documentation_fragment:
- cisco.ioscm.ioscm
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - Abbreviated commands are NOT idempotent, see
    U(https://docs.ansible.com/ansible/latest/network/user_guide/faq.html#why-do-the-config-modules-always-return-changed-true-with-abbreviated-commands)
  - To ensure idempotency and correct diff the configuration lines in the relevant module options should be similar to how they
    appear if present in the running configuration on device including the indentation.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  lines:
    description:
    - The ordered set of commands that should be configured in the section. The commands
      must be the exact same commands as found in the device running-config to ensure
      idempotency and correct diff. Be sure to note the configuration command syntax as
      some commands are automatically modified by the device config parser.
    type: list
    elements: str
    aliases:
    - commands
  parents:
    description:
    - The ordered set of parents that uniquely identify the section or hierarchy the
      commands should be checked against.  If the parents argument is omitted, the
      commands are checked against the set of top level or global commands.
    type: list
    elements: str
  src:
    description:
    - Specifies the source path to the file that contains the configuration or configuration
      template to load.  The path to the source file can either be the full path on
      the Ansible control host or a relative path from the playbook or role root directory. This
      argument is mutually exclusive with I(lines), I(parents). The configuration lines in the
      source file should be similar to how it will appear if present in the running-configuration
      of the device including the indentation to ensure idempotency and correct diff.
    type: str
  before:
    description:
    - The ordered set of commands to push on to the command stack if a change needs
      to be made.  This allows the playbook designer the opportunity to perform configuration
      commands prior to pushing any changes without affecting how the set of commands
      are matched against the system.
    type: list
    elements: str
  after:
    description:
    - The ordered set of commands to append to the end of the command stack if a change
      needs to be made.  Just like with I(before) this allows the playbook designer
      to append a set of commands to be executed after the command set.
    type: list
    elements: str
  match:
    description:
    - Instructs the module on the way to perform the matching of the set of commands
      against the current device config.  If match is set to I(line), commands are
      matched line by line.  If match is set to I(strict), command lines are matched
      with respect to position.  If match is set to I(exact), command lines must be
      an equal match.  Finally, if match is set to I(none), the module will not attempt
      to compare the source configuration with the running configuration on the remote
      device.
    choices:
    - line
    - strict
    - exact
    - none
    type: str
    default: line
  replace:
    description:
    - Instructs the module on the way to perform the configuration on the device.
      If the replace argument is set to I(line) then the modified lines are pushed
      to the device in configuration mode.  If the replace argument is set to I(block)
      then the entire command block is pushed to the device in configuration mode
      if any line is not correct.
    default: line
    choices:
    - line
    - block
    type: str
  multiline_delimiter:
    description:
    - This argument is used when pushing a multiline configuration element to the
      IOS device.  It specifies the character to use as the delimiting character.  This
      only applies to the configuration action.
    default: '@'
    type: str
  backup:
    description:
    - This argument will cause the module to create a full backup of the current C(running-config)
      from the remote device before any changes are made. If the C(backup_options)
      value is not given, the backup file is written to the C(backup) folder in the
      playbook root directory or role root directory, if playbook is part of an ansible
      role. If the directory does not exist, it is created.
    type: bool
    default: no
  running_config:
    description:
    - The module, by default, will connect to the remote device and retrieve the current
      running-config to use as a base for comparing against the contents of source.
      There are times when it is not desirable to have the task get the current running-config
      for every task in a playbook.  The I(running_config) argument allows the implementer
      to pass in the configuration to use as the base config for comparison.
      The configuration lines for this option should be similar to how it will appear if present
      in the running-configuration of the device including the indentation to ensure idempotency
      and correct diff.
    type: str
    aliases:
    - config
  defaults:
    description:
    - This argument specifies whether or not to collect all defaults when getting
      the remote device running config.  When enabled, the module will get the current
      config by issuing the command C(show running-config all).
    type: bool
    default: no
  save_when:
    description:
    - When changes are made to the device running-configuration, the changes are not
      copied to non-volatile storage by default.  Using this argument will change
      that before.  If the argument is set to I(always), then the running-config will
      always be copied to the startup-config and the I(modified) flag will always
      be set to True.  If the argument is set to I(modified), then the running-config
      will only be copied to the startup-config if it has changed since the last save
      to startup-config.  If the argument is set to I(never), the running-config will
      never be copied to the startup-config.  If the argument is set to I(changed),
      then the running-config will only be copied to the startup-config if the task
      has made a change. I(changed) was added in Ansible 2.5.
    default: never
    choices:
    - always
    - never
    - modified
    - changed
    type: str
  diff_against:
    description:
    - When using the C(ansible-playbook --diff) command line argument the module can
      generate diffs against different sources.
    - When this option is configure as I(startup), the module will return the diff
      of the running-config against the startup-config.
    - When this option is configured as I(intended), the module will return the diff
      of the running-config against the configuration provided in the C(intended_config)
      argument.
    - When this option is configured as I(running), the module will return the before
      and after diff of the running-config with respect to any changes made to the
      device configuration.
    type: str
    choices:
    - running
    - startup
    - intended
  diff_ignore_lines:
    description:
    - Use this argument to specify one or more lines that should be ignored during
      the diff.  This is used for lines in the configuration that are automatically
      updated by the system.  This argument takes a list of regular expressions or
      exact line matches.
    type: list
    elements: str
  intended_config:
    description:
    - The C(intended_config) provides the master configuration that the node should
      conform to and is used to check the final running-config against. This argument
      will not modify any settings on the remote device and is strictly used to check
      the compliance of the current device's configuration against.  When specifying
      this argument, the task should also modify the C(diff_against) value and set
      it to I(intended). The configuration lines for this value should be similar to how it
      will appear if present in the running-configuration of the device including the indentation
      to ensure correct diff.
    type: str
  backup_options:
    description:
    - This is a dict object containing configurable options related to backup file
      path. The value of this option is read only when C(backup) is set to I(yes),
      if C(backup) is set to I(no) this option will be silently ignored.
    suboptions:
      filename:
        description:
        - The filename to be used to store the backup configuration. If the filename
          is not given it will be generated based on the hostname, current time and
          date in format defined by <hostname>_config.<current-date>@<current-time>
        type: str
      dir_path:
        description:
        - This option provides the path ending with directory name in which the backup
          configuration file will be stored. If the directory does not exist it will
          be first created and the filename is either the value of C(filename) or
          default filename as described in C(filename) options description. If the
          path value is not given in that case a I(backup) directory will be created
          in the current working directory and backup configuration will be copied
          in C(filename) within I(backup) directory.
        type: path
    type: dict
"""

EXAMPLES = """
- name: Configure top level configuration
  community.ioscm.ioscm_config:
    lines: hostname {{ inventory_hostname }}

- name: Configure interface settings
  community.ioscm.ioscm_config:
    lines:
    - description test interface
    - ip address 172.31.1.1 255.255.255.0
    parents: interface Ethernet1

- name: Configure ip helpers on multiple interfaces
  community.ioscm.ioscm_config:
    lines:
    - ip helper-address 172.26.1.10
    - ip helper-address 172.26.3.8
    parents: '{{ item }}'
  with_items:
  - interface Ethernet1
  - interface Ethernet2
  - interface GigabitEthernet1

- name: Configure policy in Scavenger class
  community.ioscm.ioscm_config:
    lines:
    - conform-action transmit
    - exceed-action drop
    parents:
    - policy-map Foo
    - class Scavenger
    - police cir 64000

- name: Load new acl into device
  community.ioscm.ioscm_config:
    lines:
    - 10 permit ip host 192.0.2.1 any log
    - 20 permit ip host 192.0.2.2 any log
    - 30 permit ip host 192.0.2.3 any log
    - 40 permit ip host 192.0.2.4 any log
    - 50 permit ip host 192.0.2.5 any log
    parents: ip access-list extended test
    before: no ip access-list extended test
    match: exact

- name: Check the running-config against master config
  community.ioscm.ioscm_config:
    diff_against: intended
    intended_config: "{{ lookup('file', 'master.cfg') }}"

- name: Check the startup-config against the running-config
  community.ioscm.ioscm_config:
    diff_against: startup
    diff_ignore_lines:
    - ntp clock .*

- name: Save running to startup when modified
  community.ioscm.ioscm_config:
    save_when: modified

- name: For idempotency, use full-form commands
  community.ioscm.ioscm_config:
    lines:
      # - shut
    - shutdown
    # parents: int gig1/0/11
    parents: interface GigabitEthernet1/0/11

# Set boot image based on comparison to a group_var (version) and the version
# that is returned from the `ios_facts` module
- name: Setting boot image
  community.ioscm.ioscm_config:
    lines:
    - no boot system
    - boot system flash bootflash:{{new_image}}
    host: '{{ inventory_hostname }}'
  when: ansible_net_version != version

- name: Render a Jinja2 template onto an IOS device
  community.ioscm.ioscm_config:
    backup: yes
    src: ios_template.j2

- name: Configurable backup path
  community.ioscm.ioscm_config:
    src: ios_template.j2
    backup: yes
    backup_options:
      filename: backup.cfg
      dir_path: /home/user

# Example ios_template.j2
# ip access-list extended test
#  permit ip host 192.0.2.1 any log
#  permit ip host 192.0.2.2 any log
#  permit ip host 192.0.2.3 any log
#  permit ip host 192.0.2.4 any log
"""

RETURN = """
updates:
  description: The set of commands that will be pushed to the remote device
  returned: always
  type: list
  sample: ['hostname foo', 'router ospf 1', 'router-id 192.0.2.1']
commands:
  description: The set of commands that will be pushed to the remote device
  returned: always
  type: list
  sample: ['hostname foo', 'router ospf 1', 'router-id 192.0.2.1']
backup_path:
  description: The full path to the backup file
  returned: when backup is yes
  type: str
  sample: /playbooks/ansible/backup/ios_config.2016-07-16@22:28:34
filename:
  description: The name of the backup file
  returned: when backup is yes and filename is not specified in backup options
  type: str
  sample: ios_config.2016-07-16@22:28:34
shortname:
  description: The full path to the backup file excluding the timestamp
  returned: when backup is yes and filename is not specified in backup options
  type: str
  sample: /playbooks/ansible/backup/ios_config
date:
  description: The date extracted from the backup file name
  returned: when backup is yes
  type: str
  sample: "2016-07-16"
time:
  description: The time extracted from the backup file name
  returned: when backup is yes
  type: str
  sample: "22:28:34"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.ioscm.plugins.module_utils.network.ioscm.argspec.config.config import (
    ConfigArgs,
)
from ansible_collections.community.ioscm.plugins.module_utils.network.ioscm.config.config.config import (
    Config,
)


def main() -> None:
    """note: Main entry point for module execution."""
    required_if = [
        ("match", "strict", ["lines"]),
        ("match", "exact", ["lines", "src"], True),
        ("replace", "block", ["lines"]),
        ("diff_against", "intended", ["intended_config"]),
    ]
    module = AnsibleModule(
        argument_spec=ConfigArgs.argument_spec,
        mutually_exclusive=[("lines", "src"), ("parents", "src")],
        required_if=required_if,
        supports_check_mode=True,
    )

    result = Config(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()

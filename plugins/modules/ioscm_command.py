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
module: ioscm_command
author: Sagar Paul (@KB-perByte)
short_description: Module to run commands on remote devices.
description:
- Sends arbitrary commands to an iosxe node running in controller mode and returns the results read from the device.
  This module includes an argument that will cause the module to wait for a specific
  condition before returning or timing out if the condition is not met.
- This module does not support running commands in configuration mode. Please use
  L(ios_config,https://docs.ansible.com/ansible/latest/collections/ciscocommunity/ioscm/ioscm_config_module.html#ansible-collections-cisco-ios-ios-config-module)
  to configure IOS devices.
version_added: 1.0.0
extends_documentation_fragment:
- community.ioscm.ioscm
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  commands:
    description:
    - List of commands to send to the remote ios device over the configured provider.
      The resulting output from the command is returned. If the I(wait_for) argument
      is provided, the module is not returned until the condition is satisfied or
      the number of retries has expired. If a command sent to the device requires
      answering a prompt, it is possible to pass a dict containing I(command), I(answer)
      and I(prompt). Common answers are 'y' or "\\r" (carriage return, must be double
      quotes). See examples.
    required: true
    type: list
    elements: raw
  wait_for:
    description:
    - List of conditions to evaluate against the output of the command. The task will
      wait for each condition to be true before moving forward. If the conditional
      is not true within the configured number of retries, the task fails. See examples.
    aliases:
    - waitfor
    type: list
    elements: str
  match:
    description:
    - The I(match) argument is used in conjunction with the I(wait_for) argument to
      specify the match policy.  Valid values are C(all) or C(any).  If the value
      is set to C(all) then all conditionals in the wait_for must be satisfied.  If
      the value is set to C(any) then only one of the values must be satisfied.
    default: all
    type: str
    choices:
    - any
    - all
  retries:
    description:
    - Specifies the number of retries a command should by tried before it is considered
      failed. The command is run on the target device every retry and evaluated against
      the I(wait_for) conditions.
    default: 9
    type: int
  interval:
    description:
    - Configures the interval in seconds to wait between retries of the command. If
      the command does not pass the specified conditions, the interval indicates how
      long to wait before trying the command again.
    default: 1
    type: int
"""

EXAMPLES = r"""
- name: Run show version on remote devices
  community.ioscm.ioscm_command:
    commands: show version'

# Task Output
# -----------
#
# ok: [a.d.b.x] => changed=false
#   invocation:
#     module_args:
#       commands:
#       - show version
#       interval: 1
#       match: all
#       retries: 9
#       wait_for: null
#   stdout:
#   - |-
#     Cisco IOS XE Software, Version 17.06.01a
#     Cisco IOS Software [Bengaluru], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.1a, RELEASE SOFTWARE (fc2)
#     Technical Support: http://www.cisco.com/techsupport
#     Copyright (c) 1986-2021 by Cisco Systems, Inc.
#     Compiled Sat 21-Aug-21 03:20 by mcpre
#     Cisco IOS-XE software, Copyright (c) 2005-2021 by cisco Systems, Inc.
#     All rights reserved.  Certain components of Cisco IOS-XE software are
#     licensed under the GNU General Public License ("GPL") Version 2.0.  The
#     software code licensed under GPL Version 2.0 is free software that comes
#     with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
#     GPL code under the terms of GPL Version 2.0.  For more details, see the
#     documentation or "License Notice" file accompanying the IOS-XE software,
#     or the applicable URL provided on the flyer accompanying the IOS-XE
#     software.
#     ROM: IOS-XE ROMMON
#     paste uptime is 7 weeks, 4 days, 19 hours, 33 minutes
#     Uptime for this control processor is 7 weeks, 4 days, 19 hours, 35 minutes
#     System returned to ROM by reload
#     System image file is "bootflash:packages.conf"
#     Last reload reason: Enabling controller-mode
#     This product contains cryptographic features and is subject to United
#     States and local country laws governing import, export, transfer and
#     use. Delivery of Cisco cryptographic products does not imply
#     third-party authority to import, export, distribute or use encryption.
#     Importers, exporters, distributors and users are responsible for
#     compliance with U.S. and local country laws. By using this product you
#     agree to comply with applicable laws and regulations. If you are unable
#     to comply with U.S. and local laws, return this product immediately.
#     A summary of U.S. laws governing Cisco cryptographic products may be found at:
#     http://www.cisco.com/wwl/export/crypto/tool/stqrg.html
#     If you require further assistance please contact us by sending email to
#     export@cisco.com.
#     Technology Package License Information:
#     Controller-managed
#     The current throughput level is 250000 kbps
#     Smart Licensing Status: Registration Not Applicable/Not Applicable
#     cisco C8000V (VXE) processor (revision VXE) with 2028465K/3075K bytes of memory.
#     Processor board ID 91B54EFOP93
#     Router operating mode: Controller-Managed
#     4 Gigabit Ethernet interfaces
#     32768K bytes of non-volatile configuration memory.
#     3965316K bytes of physical memory.
#     5234688K bytes of virtual hard disk at bootflash:.
#     Configuration register is 0x2102
#   stdout_lines: <omitted>

- name: Run show version and check to see if output contains IOS
  community.ioscm.ioscm_command:
    commands: show version
    wait_for: result[0] contains IOS

# Task Output
# -----------
#
# ok: [a.d.b.x] => changed=false
#   invocation:
#     module_args:
#       commands:
#       - show version
#       interval: 1
#       match: all
#       retries: 9
#       wait_for:
#       - result[0] contains IOS
#   stdout:
#   - |-
#     Cisco IOS XE Software, Version 17.06.01a
#     Cisco IOS Software [Bengaluru], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.1a, RELEASE SOFTWARE (fc2)
#     Technical Support: http://www.cisco.com/techsupport
#     Copyright (c) 1986-2021 by Cisco Systems, Inc.
#     Compiled Sat 21-Aug-21 03:20 by mcpre
#     Cisco IOS-XE software, Copyright (c) 2005-2021 by cisco Systems, Inc.
#     software.
#     ROM: IOS-XE ROMMON
#     paste uptime is 7 weeks, 4 days, 19 hours, 33 minutes
#     Uptime for this control processor is 7 weeks, 4 days, 19 hours, 35 minutes
#     System returned to ROM by reload
#     System image file is "bootflash:packages.conf"
#     Last reload reason: Enabling controller-mode
#     http://www.cisco.com/wwl/export/crypto/tool/stqrg.html
#     If you require further assistance please contact us by sending email to
#     export@cisco.com.
#     Technology Package License Information:
#     Controller-managed
#     The current throughput level is 250000 kbps
#     Smart Licensing Status: Registration Not Applicable/Not Applicable
#     cisco C8000V (VXE) processor (revision VXE) with 2028465K/3075K bytes of memory.
#     Processor board ID 91B54EFOP93
#     Router operating mode: Controller-Managed
#     4 Gigabit Ethernet interfaces
#     32768K bytes of non-volatile configuration memory.
#     3965316K bytes of physical memory.
#     5234688K bytes of virtual hard disk at bootflash:.
#     Configuration register is 0x2102
#   stdout_lines: <omitted>

- name: Run multiple commands on remote nodes
  community.ioscm.ioscm_command:
    commands:
    - show version
    - show interfaces

# Task Output
# -----------
#
# ok: [a.d.b.x] => changed=false
#   invocation:
#     module_args:
#       commands:
#       - show version
#       - show interfaces
#       interval: 1
#       match: all
#       retries: 9
#       wait_for: null
#   stdout:
#   - |-
#     Cisco IOS XE Software, Version 17.06.01a
#     Cisco IOS Software [Bengaluru], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.1a, RELEASE SOFTWARE (fc2)
#     Technical Support: http://www.cisco.com/techsupport
#     Copyright (c) 1986-2021 by Cisco Systems, Inc.
#     Compiled Sat 21-Aug-21 03:20 by mcpre
#     Cisco IOS-XE software, Copyright (c) 2005-2021 by cisco Systems, Inc.
#     ROM: IOS-XE ROMMON
#     paste uptime is 7 weeks, 4 days, 19 hours, 37 minutes
#     Uptime for this control processor is 7 weeks, 4 days, 19 hours, 38 minutes
#     System returned to ROM by reload
#     System image file is "bootflash:packages.conf"
#     Last reload reason: Enabling controller-mode
#     http://www.cisco.com/wwl/export/crypto/tool/stqrg.html
#     If you require further assistance please contact us by sending email to
#     export@cisco.com.
#     Technology Package License Information:
#     Controller-managed
#     The current throughput level is 250000 kbps
#     Smart Licensing Status: Registration Not Applicable/Not Applicable
#     cisco C8000V (VXE) processor (revision VXE) with 2028465K/3075K bytes of memory.
#     Processor board ID 91B54EFOP93
#     Router operating mode: Controller-Managed
#     4 Gigabit Ethernet interfaces
#     32768K bytes of non-volatile configuration memory.
#     3965316K bytes of physical memory.
#     5234688K bytes of virtual hard disk at bootflash:.
#
#     Configuration register is 0x2102
#   - |-
#     GigabitEthernet1 is up, line protocol is up
#       Hardware is vNIC, address is 5254.0015.5c8a (bia 5254.0015.5c8a)
#       Description: mgmt interface do not change
#       Internet address is 192.168.255.55/24
#       MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
#          reliability 255/255, txload 1/255, rxload 1/255
#       Encapsulation ARPA, loopback not set
#       Keepalive set (10 sec)
#       Full Duplex, 1000Mbps, link type is auto, media type is Virtual
#       output flow-control is unsupported, input flow-control is unsupported
#       ARP type: ARPA, ARP Timeout 04:00:00
#       Last input 00:00:00, output 00:00:00, output hang never
#       Last clearing of "show interface" counters never
#       Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
#       Queueing strategy: fifo
#       Output queue: 0/40 (size/max)
#       5 minute input rate 2000 bits/sec, 1 packets/sec
#       5 minute output rate 1000 bits/sec, 1 packets/sec
#          1011932 packets input, 293088587 bytes, 0 no buffer
#          Received 0 broadcasts (0 IP multicasts)
#          0 runts, 0 giants, 0 throttles
#          0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
#          0 watchdog, 0 multicast, 0 pause input
#          20889 packets output, 3519493 bytes, 0 underruns
#          Output 0 broadcasts (0 IP multicasts)
#          0 output errors, 0 collisions, 0 interface resets
#          799151 unknown protocol drops
#          0 babbles, 0 late collision, 0 deferred
#          0 lost carrier, 0 no carrier, 0 pause output
#          0 output buffer failures, 0 output buffers swapped out
#     GigabitEthernet2 is up, line protocol is up
#       Hardware is vNIC, address is 5254.001b.2873 (bia 5254.001b.2873)
#       MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
#          reliability 255/255, txload 1/255, rxload 1/255
#       Encapsulation ARPA, loopback not set
#       Keepalive set (10 sec)
#       Full Duplex, 1000Mbps, link type is auto, media type is Virtual
#       output flow-control is unsupported, input flow-control is unsupported
#       ARP type: ARPA, ARP Timeout 04:00:00
#       Last input never, output never, output hang never
#       Last clearing of "show interface" counters never
#       Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
#       Queueing strategy: fifo
#       Output queue: 0/40 (size/max)
#       5 minute input rate 0 bits/sec, 0 packets/sec
#       5 minute output rate 0 bits/sec, 0 packets/sec
#          0 packets input, 0 bytes, 0 no buffer
#          Received 0 broadcasts (0 IP multicasts)
#          0 runts, 0 giants, 0 throttles
#          0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
#          0 watchdog, 0 multicast, 0 pause input
#          0 packets output, 0 bytes, 0 underruns
#          Output 0 broadcasts (0 IP multicasts)
#          0 output errors, 0 collisions, 0 interface resets
#          0 unknown protocol drops
#          0 babbles, 0 late collision, 0 deferred
#          0 lost carrier, 0 no carrier, 0 pause output
#          0 output buffer failures, 0 output buffers swapped out
#     GigabitEthernet3 is up, line protocol is up
#       Hardware is vNIC, address is 5254.0019.d634 (bia 5254.0019.d634)
#       MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
#          reliability 255/255, txload 1/255, rxload 1/255
#       Encapsulation ARPA, loopback not set
#       Keepalive set (10 sec)
#       Full Duplex, 1000Mbps, link type is auto, media type is Virtual
#       output flow-control is unsupported, input flow-control is unsupported
#       ARP type: ARPA, ARP Timeout 04:00:00
#       Last input never, output never, output hang never
#       Last clearing of "show interface" counters never
#       Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
#       Queueing strategy: fifo
#       Output queue: 0/40 (size/max)
#       5 minute input rate 0 bits/sec, 0 packets/sec
#       5 minute output rate 0 bits/sec, 0 packets/sec
#          0 packets input, 0 bytes, 0 no buffer
#          Received 0 broadcasts (0 IP multicasts)
#          0 runts, 0 giants, 0 throttles
#          0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
#          0 watchdog, 0 multicast, 0 pause input
#          0 packets output, 0 bytes, 0 underruns
#          Output 0 broadcasts (0 IP multicasts)
#          0 output errors, 0 collisions, 0 interface resets
#          0 unknown protocol drops
#          0 babbles, 0 late collision, 0 deferred
#          0 lost carrier, 0 no carrier, 0 pause output
#          0 output buffer failures, 0 output buffers swapped out
#     GigabitEthernet4 is up, line protocol is up
#       Hardware is vNIC, address is 5254.000a.af44 (bia 5254.000a.af44)
#       MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
#          reliability 255/255, txload 1/255, rxload 1/255
#       Encapsulation ARPA, loopback not set
#       Keepalive set (10 sec)
#       Full Duplex, 1000Mbps, link type is auto, media type is Virtual
#       output flow-control is unsupported, input flow-control is unsupported
#       ARP type: ARPA, ARP Timeout 04:00:00
#       Last input never, output never, output hang never
#       Last clearing of "show interface" counters never
#       Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
#       Queueing strategy: fifo
#       Output queue: 0/40 (size/max)
#       5 minute input rate 0 bits/sec, 0 packets/sec
#       5 minute output rate 0 bits/sec, 0 packets/sec
#          0 packets input, 0 bytes, 0 no buffer
#          Received 0 broadcasts (0 IP multicasts)
#          0 runts, 0 giants, 0 throttles
#          0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
#          0 watchdog, 0 multicast, 0 pause input
#          0 packets output, 0 bytes, 0 underruns
#          Output 0 broadcasts (0 IP multicasts)
#          0 output errors, 0 collisions, 0 interface resets
#          0 unknown protocol drops
#          0 babbles, 0 late collision, 0 deferred
#          0 lost carrier, 0 no carrier, 0 pause output
#          0 output buffer failures, 0 output buffers swapped out
#     Loopback65528 is up, line protocol is up
#       Hardware is Loopback
#       Internet address is 192.168.1.1/32
#       MTU 1514 bytes, BW 8000000 Kbit/sec, DLY 5000 usec,
#          reliability 255/255, txload 1/255, rxload 1/255
#       Encapsulation LOOPBACK, loopback not set
#       Keepalive set (10 sec)
#       Last input never, output never, output hang never
#       Last clearing of "show interface" counters never
#       Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
#       Queueing strategy: fifo
#       Output queue: 0/0 (size/max)
#       5 minute input rate 0 bits/sec, 0 packets/sec
#       5 minute output rate 0 bits/sec, 0 packets/sec
#          0 packets input, 0 bytes, 0 no buffer
#          Received 0 broadcasts (0 IP multicasts)
#          0 runts, 0 giants, 0 throttles
#          0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
#          0 packets output, 0 bytes, 0 underruns
#          Output 0 broadcasts (0 IP multicasts)
#          0 output errors, 0 collisions, 0 interface resets
#          0 unknown protocol drops
#          0 output buffer failures, 0 output buffers swapped out
#   stdout_lines: <omitted>

- name: Run multiple commands and evaluate the output
  community.ioscm.ioscm_command:
    commands:
    - show version
    - show interfaces
    wait_for:
    - result[0] contains IOS
    - result[1] contains Loopback

# Task Output
# -----------
#
# fatal: [a.d.b.x]: FAILED! => changed=false
#   failed_conditions:
#   - result[1] contains Loopback0
#   invocation:
#     module_args:
#       commands:
#       - show version
#       - show interfaces
#       interval: 1
#       match: all
#       retries: 9
#       wait_for:
#       - result[0] contains IOS
#       - result[1] contains Loopback0
#   msg: One or more conditional statements have not been satisfied
"""

RETURN = """
stdout:
  description: The set of responses from the commands
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
failed_conditions:
  description: The list of conditionals that have failed
  returned: failed
  type: list
  sample: ['...', '...']
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.ioscm.plugins.module_utils.network.ioscm.argspec.command.command import (
    CommandArgs,
)
from ansible_collections.community.ioscm.plugins.module_utils.network.ioscm.config.command.command import (
    Command,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=CommandArgs.argument_spec)

    result = Command(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()

# Community IOSCM Collection


The Ansible Community IOSCM collection includes a variety of Ansible content to help automate the management of Cisco IOS XE network appliances specifically in controller mode.

This collection has been tested against Cisco IOS XE Version 17.3 on CML.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against the following Ansible versions: **>=2.9.10**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `community.ioscm.ioscm`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections

The Community IOSCM collection supports `network_cli` connections.

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[community.ioscm.ioscm](https://github.com/ansible-collections/community.ioscm/blob/main/docs/community.ioscm.ioscm_cliconf.rst)|Use ioscm cliconf to run command on Community IOSCM platform

### Modules
Name | Description
--- | ---
[community.ioscm.ioscm_command](https://github.com/ansible-collections/community.ioscm/blob/main/docs/community.ioscm.ioscm_command_module.rst)|Module to run commands on remote devices.
[community.ioscm.ioscm_config](https://github.com/ansible-collections/community.ioscm/blob/main/docs/community.ioscm.ioscm_config_module.rst)|Module to manage configuration sections.
[community.ioscm.ioscm_facts](https://github.com/ansible-collections/community.ioscm/blob/main/docs/community.ioscm.ioscm_facts_module.rst)|Module to collect facts from remote devices.
[community.ioscm.ioscm_ping](https://github.com/ansible-collections/community.ioscm/blob/main/docs/community.ioscm.ioscm_ping_module.rst)|Tests reachability using ping from IOS switch.

<!--end collection content-->

## Installing this collection

You can install the Community IOSCM collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install community.ioscm

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.ioscm
```

## Using this collection

This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the community IOS collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `community.ioscm.ioscm_config`.
The following example task to do configuration on a Cisco IOS network device running in controller mode, using the FQCN:

```yaml
---
- name: Configure policy in Scavenger class
  community.ioscm.ioscm_config:
    lines:
    - conform-action transmit
    - exceed-action drop
    parents:
    - policy-map Foo
    - class Scavenger
    - police cir 64000
```

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.

### See Also:

- [Community IOSCM Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Community IOSCM collection repository](https://github.com/ansible-collections/community.ioscm). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

You can also join us on:

- IRC - the `#ansible-network` [libera.chat](https://libera.chat/) channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

<!--Add a link to a changelog.md file or an external doc site to cover this information. -->

Release notes are available [here](https://github.com/ansible-collections/community.ioscm/blob/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

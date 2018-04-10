#!/usr/bin/python
# encoding: utf-8

# (c) 2018, Jiri Tyr <jiri.tyr@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.tx))

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: ipa_client_check
short_description: Check if IPA client is already installed
description:
  - Check if IPA client is already installed in which case the next
    installation attempt would fail without uninstalling it first.
version_added: '2.5'
author:
  - Jiri Tyr (@jtyr)
requirements:
  - ipaclient
  - ipalib
  - ipaplatform

  - ipapython
options:
  conf_path:
    description:
      - Path to the default IPA config file.
    default: /etc/ipa/default.conf
  on_master:
    description:
      - Whether the check is run on the Master server.
    type: bool
    default: 'no'
  sysrestore_path:
    description:
      - Path to the default IPA sysrestore directory.
    default: /var/lib/ipa-client/sysrestore
"""


EXAMPLES = """
- name: Check if client is installed
  ipa_client_check:

- name: Check if the client is installed on the Master
  ipa_client_check:
    on_master: yes
"""


RETURN = """
installed:
  description: whether the client is installed or not
  returned: success
  type: bool
  sample: True
"""


HAS_IPA_NEW = False
HAS_IPA_OLD = False

try:
    from ipalib.install import sysrestore
    from ipaplatform.paths import paths

    HAS_IPA_NEW = True
except ImportError:
    try:
        from ipapython import sysrestore

        HAS_IPA_OLD = True
    except ImportError:
        pass

import os
from ansible.module_utils.basic import AnsibleModule


def main():
    IPA_DEFAULT_CONF = '/etc/ipa/default.conf'
    IPA_CLIENT_SYSRESTORE = '/var/lib/ipa-client/sysrestore'

    module = AnsibleModule(
        argument_spec={
            'conf_path': dict(default=IPA_DEFAULT_CONF),
            'on_master': dict(default=False, type='bool'),
            'sysrestore_path': dict(default=IPA_CLIENT_SYSRESTORE),
        },
        supports_check_mode=True,
    )

    if not HAS_IPA_OLD and not HAS_IPA_NEW:
        module.fail_json(msg="Missing required IPA modules.")

    on_master = module.params['on_master']
    config_path = module.params['conf_path']
    sysrestore_path = module.params['sysrestore_path']

    if HAS_IPA_NEW:
        if config_path != IPA_DEFAULT_CONF:
            config_path = paths.IPA_DEFAULT_CONF

        if sysrestore_path != IPA_CLIENT_SYSRESTORE:
            sysrestore_path = paths.IPA_CLIENT_SYSRESTORE

    fstore = sysrestore.FileStore(sysrestore_path)

    installed = (
        fstore.has_files() or (
            not on_master and os.path.exists(config_path)
        )
    )

    module.exit_json(changed=False, installed=installed)


if __name__ == '__main__':
    main()

freeipa_client
==============

Ansible role which helps to install and configure FreeIPA client.

The configuration of the role is done in such way that it should not be
necessary to change the role for any kind of configuration. All can be
done either by changing role parameters or by declaring completely new
configuration as a variable. That makes this role absolutely
universal. See the examples below for more details.

Please report any issues or send PR.


Examples
--------

```yaml
---

- name: Example of how to install FreeIPA client
  hosts: all
  vars:
    freeipa_client_reg_args_password: password
    freeipa_client_reg_args_domain: example.com
    freeipa_client_reg_args_servers:
      - ipa1.example.com
      - ipa2.example.com
      - ipa3.example.com
  roles:
    - freeipa_client
```


Role variables
--------------

Variables used by the role:

```yaml
# Package to be installed (explicit version can be specified here)
freeipa_client_pkg: "{{
  'ipa-client'
    if ansible_os_family == 'RedHat'
    else
  'freeipa-client' }}"

# Whether force the client registration even if it's already registered
freeipa_client_reg_force: no

# Whether to log the execution of the client registration command
freeipa_client_reg_log: no

# Default option values for the ipa-client-install arguments
freeipa_client_reg_args_principal: admin
freeipa_client_reg_args_password: password
freeipa_client_reg_args_domain: example.com
freeipa_client_reg_args_enable_dns_updates: yes
freeipa_client_reg_args_force_join: yes
freeipa_client_reg_args_force_ntpd: "{{
  false
    if (
            ansible_os_family == 'RedHat' and
            ansible_distribution_major_version | int < 7)
    else
  true
}}"
freeipa_client_reg_args_mkhomedir: yes
freeipa_client_reg_args_servers: []
freeipa_client_reg_args_unattended: yes

# Default ipa-client-install arguments
freeipa_client_reg_args__default:
  - --principal {{ freeipa_client_reg_args_principal }}
  - --password "{{ freeipa_client_reg_args_password }}"
  - "{{ '--domain ' ~ freeipa_client_reg_args_domain if freeipa_client_reg_args_servers | length > 0 else '' }}"
  - "{{ '--enable-dns-updates' if freeipa_client_reg_args_enable_dns_updates else '' }}"
  - "{{ '--force-join' if freeipa_client_reg_args_force_join else '' }}"
  - "{{ '--force-ntpd' if freeipa_client_reg_args_force_ntpd ==  true else '' }}"
  - "{{ '--mkhomedir' if freeipa_client_reg_args_mkhomedir else '' }}"
  - "{{ '--server ' ~ freeipa_client_reg_args_servers | join(' --server ') if freeipa_client_reg_args_servers | length > 0 else '' }}"
  - "{{ '--unattended' if freeipa_client_reg_args_unattended else '' }}"

# Custom ipa-client-install arguments
freeipa_client_reg_args__custom: []

# Custom ipa-client-install arguments
freeipa_client_reg_args: "{{
  freeipa_client_reg_args__default +
  freeipa_client_reg_args__custom }}"

# This variable can have thee values:
#   'null' - auto-detect if installation is required
#   'yes'  - force installation
#   'no'   - do not install
freeipa_client_pam_mkhomedir_install: null
```


License
-------

MIT


Author
------

Jiri Tyr

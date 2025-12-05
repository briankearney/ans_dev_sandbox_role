# vars/

## Purpose

Contains role-level variables that have **higher precedence** than `defaults/`. Variables defined here should be internal to the role and typically should not be overridden by users. Use this directory sparingly for values that the role requires to function correctly.

## When to Use `vars/`

Use `vars/main.yml` for:

- **Internal role constants**: Values that define how the role operates internally
- **Computed values**: Variables that are calculated based on other variables
- **OS-specific variables**: Platform-dependent values loaded conditionally
- **Fixed configurations**: Settings that should not typically be changed by end-users

### Examples of Appropriate Use

```yaml
---
# OS-specific package names
_package_name_map:
  RedHat: "httpd"
  Debian: "apache2"

# Internal role constants
_role_internal_config_path: "/etc/myapp/config"

# Computed values
_full_config_path: "{{ _role_internal_config_path }}/{{ app_name }}.conf"
```

## When to Use `defaults/` Instead

Use `defaults/main.yml` for:

- **User-configurable values**: Settings users should be able to override
- **Feature flags**: Boolean values to enable/disable features
- **Default endpoints**: URLs, paths, or addresses that may vary by environment
- **Resource limits**: Memory, CPU, or storage allocations
- **Optional parameters**: Values that provide sensible defaults but may need customization

## Current State

The `vars/main.yml` file is currently minimal:

```yaml
---
# Role-specific internal variables (these override defaults)
# Variables defined here should not be overridden by users
# Consider moving user-configurable items to defaults/main.yml
```

This role follows best practices by keeping most variables in `defaults/` for maximum flexibility.

## Variable Precedence

In Ansible's variable precedence order, `vars/` ranks higher than `defaults/`:

1. Extra vars (`-e` flag) - **highest precedence**
2. Task vars
3. Block vars
4. **Role vars** - `vars/main.yml` (this directory)
5. Play vars_files
6. Play vars
7. Set_facts
8. Registered vars
9. Host facts
10. Host vars
11. Group vars
12. Inventory vars
13. Role defaults - `defaults/main.yml`
14. Command-line defaults - **lowest precedence**

This means variables in `vars/` will **override** those in `defaults/`, but can still be overridden by play vars or extra vars.

## Best Practices

### Naming Conventions

- Prefix internal variables with underscore: `_internal_var`
- Use descriptive names indicating they're internal: `role_internal_*`
- Follow snake_case naming: `my_variable_name`

### Documentation

- Comment all variables explaining their purpose
- Document any dependencies or relationships
- Warn if variable should not be overridden

### Organization

```yaml
---
# ==================================================================
# Internal role constants - DO NOT OVERRIDE
# ==================================================================

_role_version: "1.0.0"
_role_config_dir: "/etc/myapp"

# ==================================================================
# OS-specific variables
# ==================================================================

_package_names:
  RedHat: ["httpd", "mod_ssl"]
  Debian: ["apache2", "ssl-cert"]

# ==================================================================
# Computed paths
# ==================================================================

_full_config_path: "{{ _role_config_dir }}/{{ app_name }}.conf"
```

## Loading OS-Specific Variables

Common pattern for loading platform-specific vars:

```yaml
# tasks/main.yml
---
- name: Include OS-specific variables
  ansible.builtin.include_vars:
    file: "{{ ansible_os_family }}.yml"
  when: ansible_os_family in ['RedHat', 'Debian']

# vars/RedHat.yml
---
_package_name: "httpd"
_service_name: "httpd"

# vars/Debian.yml
---
_package_name: "apache2"
_service_name: "apache2"
```

## Security Considerations

- **Never store secrets in `vars/`**: Use Ansible Vault in `defaults/` or external secret managers
- Internal variables are still visible in playbook output
- Use `no_log: true` on tasks handling sensitive data

## Migration Path

If you find variables in `vars/` that should be user-configurable:

1. Move the variable to `defaults/main.yml`
2. Update any documentation
3. Test that overrides work as expected
4. Update role documentation to reflect the change

## Related Documentation

- [`defaults/README.md`](../defaults/README.md) - Default variables (lower precedence)
- [`tasks/README.md`](../tasks/README.md) - How variables are used in tasks
- [Ansible Documentation: Variable Precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)
- [Ansible Documentation: Variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)

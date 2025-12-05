# defaults/

## Purpose

Contains the role's default variables. These values have the **lowest precedence** in Ansible's variable hierarchy and are safe for users to override in playbooks, inventories, group/host variables, or extra vars.

## Key Variables in `defaults/main.yml`

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ans_dev_sandbox_role_some_username` | String | `UserName` | Example username demonstrating variable usage |
| `ans_dev_sandbox_role_some_password` | String (vaulted) | (encrypted) | Example vault-encrypted password for secure credentials |
| `ans_dev_sandbox_role_some_variable` | String | `foo` | Example variable for demonstration |
| `ans_dev_sandbox_role_git_repo_url` | String | `https://github.com/briankearney/ans_dev_sandbox_role` | Git repository URL to clone |
| `ans_dev_sandbox_role_git_repo_version` | String | `main` | Branch, tag, or commit SHA to checkout |
| `ans_dev_sandbox_role_temp_dir_path` | String | `""` | Fixed temporary directory path; empty string creates new temp dir each run |

## Variable Usage

### Basic Override

Override variables at playbook level:

```yaml
---
- name: Example playbook with variable overrides
  hosts: localhost
  roles:
    - role: ans_dev_sandbox_role
      vars:
        ans_dev_sandbox_role_git_repo_url: "https://github.com/example/your-repo.git"
        ans_dev_sandbox_role_git_repo_version: "v1.0.0"
```

### Inventory Override

Set variables in inventory files:

```yaml
# inventory/group_vars/all.yml
---
ans_dev_sandbox_role_git_repo_url: "https://github.com/company/project.git"
ans_dev_sandbox_role_git_repo_version: "stable"
```

### Extra Vars Override

Use command-line extra vars (highest precedence):

```bash
ansible-playbook playbook.yml \
  -e "ans_dev_sandbox_role_git_repo_url=https://github.com/test/repo.git" \
  -e "ans_dev_sandbox_role_git_repo_version=develop"
```

## Ansible Vault Usage

### Viewing Encrypted Variables

The `ans_dev_sandbox_role_some_password` variable is encrypted with Ansible Vault. To view it:

```bash
# Using ansible-vault directly
ansible-vault view defaults/main.yml --vault-password-file vault-pw.txt

# Using the provided decryption script
python DECRYPT_VAULTED_ITEMS.py \
  -f defaults/main.yml \
  -i ans_dev_sandbox_role_some_password \
  --color
```

### Encrypting New Variables

To encrypt a new variable:

```bash
# Encrypt a string value
ansible-vault encrypt_string 'my_secret_value' \
  --name 'my_variable_name' \
  --vault-password-file vault-pw.txt

# Encrypt entire file
ansible-vault encrypt defaults/main.yml \
  --vault-password-file vault-pw.txt
```

### Best Practices for Secrets

- **Never commit plain-text secrets** to version control
- Use `ansible-vault encrypt_string` for individual variables
- Store vault password file outside the repository (or use `--ask-vault-pass`)
- Use different vault IDs for different environments (dev/staging/prod)
- Consider external secret managers (HashiCorp Vault, AWS Secrets Manager) for production

## Idempotent Testing

The `ans_dev_sandbox_role_temp_dir_path` variable enables idempotent testing:

- **Empty string (default)**: Creates a new temporary directory on each run (non-idempotent)
- **Fixed path**: Uses the same directory on subsequent runs (idempotent)

```yaml
# For idempotent Molecule tests
ans_dev_sandbox_role_temp_dir_path: "/tmp/molecule_test_sandbox"

# For production (non-idempotent, creates new temp dir)
ans_dev_sandbox_role_temp_dir_path: ""
```

## Variable Precedence

Variables in `defaults/` have the **lowest precedence** and can be overridden by:

1. Extra vars (`-e` flag) - **highest precedence**
2. Task vars
3. Block vars
4. Role and include vars
5. Play vars_files
6. Play vars_prompt
7. Play vars
8. Set_facts
9. Registered vars
10. Host facts
11. Playbook host_vars
12. Playbook group_vars
13. Inventory host_vars
14. Inventory group_vars
15. Inventory vars
16. Role defaults - **this file** (lowest precedence)

See [Ansible Variable Precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) for details.

## Related Documentation

- [`vars/README.md`](../vars/README.md) - Higher precedence role variables
- [`tasks/README.md`](../tasks/README.md) - How variables are used in tasks
- [Ansible Documentation: Variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)

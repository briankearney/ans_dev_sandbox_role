# defaults/

Purpose
- Contains the role's default variables. These values have the lowest precedence and are safe for users to override in playbooks, inventories, or group/host variables.

Key variables in `defaults/main.yml`
- `ans_dev_sandbox_role_some_username` — example username (default: `UserName`).
- `ans_dev_sandbox_role_some_password` — vault-encrypted example password (stored with Ansible Vault).
- `ans_dev_sandbox_role_some_variable` — example value (default: `foo`).
- `git_repo_url` — repository URL used by the role's clone task (default: `https://github.com/briankearney/ans_dev_sandbox_role`).
- `git_repo_version` — which branch/tag/commit to check out (default: `main`).

Notes
- To override any default, set the variable at a higher precedence (inventory, play vars, extra vars, etc.).
- Do not commit plain-text secrets. Use `ansible-vault encrypt_string` or `ansible-vault encrypt` to keep secrets safe.

Example override in a playbook:
```yaml
- hosts: localhost
  roles:
    - role: ans_dev_sandbox_role
      vars:
        git_repo_url: "https://github.com/example/your-repo.git"
        git_repo_version: "stable"
```

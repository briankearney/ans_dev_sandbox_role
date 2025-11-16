# vars/

Purpose
- Contains role-level variables that typically have higher precedence than `defaults/`. Use this directory for values that the role requires or that should override the defaults within the role context.

Guidance for contributors
- Only place variables here if they must take precedence inside the role. Prefer `defaults/` for user-configurable values.
- Avoid storing secrets in plain text here; use Ansible Vault for any sensitive data.

When to use `vars/main.yml`
- Fixed role configuration that should not usually be changed by end-users, e.g., constants or internal mappings.

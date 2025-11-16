# Ansible Role: ans_dev_sandbox_role

A demonstration Ansible role showcasing best practices for setting up, versioning, and maintaining Ansible roles in a Version Control System (VCS) like Git. This project serves as an educational example for developers learning Ansible automation, while demonstrating expertise in infrastructure as code, secure variable management, and project organization.

## Overview

This role illustrates key Ansible concepts and workflows, including:
- **Role Structure**: Organized according to Ansible best practices with `defaults/`, `tasks/`, `vars/`, and other standard directories.
- **Version Control Integration**: Demonstrates Git operations within Ansible tasks, such as cloning repositories securely via HTTPS.
- **Secure Variable Handling**: Uses Ansible Vault for encrypting sensitive data like passwords, with accompanying scripts for decryption and environment management.
- **Environment Setup**: Includes scripts to configure a development sandbox, ensuring reproducible and isolated Ansible executions.
- **Modular Task Design**: Employs `include_tasks` for clean, maintainable playbooks.

Ideal for learners building foundational Ansible skills, portfolio reviewers assessing technical proficiency, and professionals exploring advanced automation patterns.
## ans_dev_sandbox_role — Ansible development sandbox role

This repository contains a small demonstration Ansible role used as a development sandbox and example of Ansible role best practices. It includes a simple task suite that clones a Git repository to a temporary location, demonstrates variable organization, and shows vault usage for secrets.

Note: Per-directory `README.md` files have been added to explain each folder's purpose and usage. See the `Structure` section below.

Quick links:
- `defaults/README.md` — default role variables and vault notes
- `vars/README.md` — role variables with higher precedence
- `tasks/README.md` — task flow and how to extend the role
- `meta/README.md` — Galaxy metadata and supported platforms

Prerequisites
- Ansible (recommended: ansible-core 2.19+)
- Git
- Python 3.10+ (for scripts in this repo)
- Ansible Vault (for encrypted variables)

Quick start
1. Clone this repository and change into it:
   ```bash
   git clone https://github.com/briankearney/ans_dev_sandbox_role.git
   cd ans_dev_sandbox_role
   ```
2. (Optional) Activate the sandbox environment:
   ```bash
   ./ACTIVATE_SANDBOX_ENV.bash
   ```
3. Run the role from a playbook (use briankearney/ans_dev_sandbox_playbook, which includes this role) or run ad-hoc tasks using `ansible-playbook`.

Variables
- Defaults live in `defaults/main.yml` and are safe to override.
- Role-specific/internal variables may be in `vars/main.yml`.
- Sensitive values (e.g., passwords) are stored with Ansible Vault in `defaults/main.yml`.

Repository structure
- `defaults/` — default variables (see `defaults/README.md`).
- `vars/` — role-level variables (see `vars/README.md`).
- `tasks/` — main task set and includes (see `tasks/README.md`).
- `meta/` — Galaxy metadata (see `meta/README.md`).
- `ACTIVATE_SANDBOX_ENV.bash` — helper to set up environment variables and virtualenv.
- `DECRYPT_VAULTED_ITEMS.py` — helper script to decrypt and inspect vaulted variables.

Contributing
- Fork, create a feature branch, make changes, and open a pull request. Please include tests or validation steps where appropriate.

License
- MIT — see the `LICENSE` file.

If you'd like, I can also run a quick validation (syntax check with `ansible-lint` or `yamllint`) or create a sample `playbook.yml` demonstrating role usage. 


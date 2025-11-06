# Ansible Role: ans_dev_sandbox_role

A demonstration Ansible role showcasing best practices for setting up, versioning, and maintaining Ansible roles in a Version Control System (VCS) like Git. This project serves as an educational example for developers learning Ansible automation, while demonstrating expertise in infrastructure as code, secure variable management, and project organization.

## Overview

This role illustrates key Ansible concepts and workflows, including:
- **Role Structure**: Organized according to Ansible best practices with `defaults/`, `tasks/`, `vars/`, and other standard directories.
- **Version Control Integration**: Demonstrates Git operations within Ansible tasks, such as cloning repositories securely via SSH.
- **Secure Variable Handling**: Uses Ansible Vault for encrypting sensitive data like passwords, with accompanying scripts for decryption and environment management.
- **Environment Setup**: Includes scripts to configure a development sandbox, ensuring reproducible and isolated Ansible executions.
- **Modular Task Design**: Employs `include_tasks` for clean, maintainable playbooks.

Ideal for learners building foundational Ansible skills, portfolio reviewers assessing technical proficiency, and professionals exploring advanced automation patterns.

## Prerequisites

- **Ansible**: Version 2.19+ or later (tested with ansible-core).
- **Git**: For repository cloning and version control operations.
- **Python**: Version 3.13 for running the decryption script.
- **SSH Key**: Configured for accessing private Git repositories (e.g., GitHub Enterprise).
- **Ansible Vault**: For encrypting/decrypting sensitive variables.

## Quick Start

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/briankearney/ans_dev_sandbox_role.git
   cd ans_dev_sandbox_role
   ```

2. **Set Up the Environment**:
   Run the activation script to configure your Ansible sandbox:
   ```bash
   ./ACTIVATE_SANDBOX_ENV.bash
   ```
   This sets up a Python virtual environment, Ansible configurations, and environment variables.

3. **Configure Vault Password**:
   Create a `vault-pw.txt` file with your Ansible Vault password:
   ```bash
   echo "your_vault_password" > vault-pw.txt
   ```

4. **Run the Role**:
   Execute the role using Ansible Playbook:
   ```bash
   ansible-playbook -i localhost, playbook.yml
   ```
   (Create a simple `playbook.yml` if needed, e.g., including this role.)

5. **Decrypt Vaulted Items (Optional)**:
   Use the provided script to decrypt and view vaulted variables:
   ```bash
   python DECRYPT_VAULTED_ITEMS.py --color --decode --file defaults/main.yml --id some_password
   ```

## Role Variables

| Variable | Value | Description |
| ---------- | ------- | ----------- |
| `some_username` | `UserName` | Sample plain text variable for demonstration purposes. |
| `some_password` | (Vault-encrypted) | Sample vault-protected variable, encrypted using Ansible Vault for secure storage. |
| `some_variable` | `foo` | Another plain text variable example. |

Variables are defined in `defaults/main.yml` (with defaults) and `vars/main.yml` (for overrides). Sensitive data like `some_password` is encrypted and requires vault access.

### Variable Precedence and Defaults

In Ansible roles, variables are layered with different precedence levels to allow flexible configuration:

- **`defaults/main.yml`**: Contains default values with the lowest precedence. These are easily overridden by higher-level variables (e.g., from inventory, play vars, or `vars/main.yml`), making them ideal for safe, non-disruptive defaults.
- **`vars/main.yml`**: Holds variables with higher precedence than defaults but still overridable. Use this for role-specific overrides or constants that should take priority within the role.

This layering enables roles to be reusable and customizable without modifying the role code.

In contrast, the `default` Jinja2 filter provides inline defaults directly in templates, tasks, or YAML files. For example, `{{ some_var | default('fallback_value') }}` sets a fallback if `some_var` is undefined, offering runtime flexibility and error prevention separate from the role's variable files. It's not a replacement for layered variables but a complementary tool for handling optional or dynamic values.

## Tasks Overview

The role's main tasks (`tasks/main.yml`) include:
- **Git Cloning**: Securely clones a specified repository into a temporary directory using SSH authentication.
- **File Discovery**: Recursively lists and debugs files in the cloned repository for verification.
- **Temporary Resource Management**: Creates and cleans up temporary directories as needed.

Additional tasks can be added in `tasks/git_clone.yml` or via includes.

## Environment Setup Scripts

- **`ACTIVATE_SANDBOX_ENV.bash`**: Bash script to activate a Python virtual environment, set Ansible environment variables (e.g., roles path, vault password file, SSH key), and configure logging/callbacks for development.
- **`DECRYPT_VAULTED_ITEMS.py`**: Python script to decrypt Ansible Vault-encrypted variables from YAML files, with options for base64 decoding and colored output using Pygments.

## Dependencies

- **Ansible Collections**: `ansible.builtin` (included with Ansible).
- **Python Libraries**: `pyyaml`, `pygments` (install via `pip` if running the decryption script outside Ansible).
- **No External Role Dependencies**: This role is self-contained.

## Best Practices Demonstrated

- **VCS Integration**: Roles versioned in Git with clear commit history and branching.
- **Security**: Use of Ansible Vault for secrets, SSH for Git access, and environment isolation.
- **Modularity**: Task includes and variable separation for maintainability.
- **Documentation**: Comprehensive README with usage examples and setup instructions.
- **Testing**: (Future enhancement) Add molecule or ansible-lint for automated testing.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make changes and test thoroughly.
4. Submit a pull request with a clear description.

For issues or questions, open a GitHub issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with Ansible for educational and portfolio purposes. Demonstrates expertise in DevOps, automation, and software development best practices.*

# Ansible Role: ans_dev_sandbox_role

A demonstration Ansible role showcasing best practices for setting up, versioning, and maintaining Ansible roles in a Version Control System (VCS) like Git. This project serves as an educational example for developers learning Ansible automation, while demonstrating expertise in infrastructure as code, secure variable management, and project organization.

![Molecule CI](https://github.com/briankearney/ans_dev_sandbox_role/actions/workflows/molecule.yml/badge.svg)
![Unit Tests](https://github.com/briankearney/ans_dev_sandbox_role/actions/workflows/unit-tests.yml/badge.svg)

**Python 3.10–3.14 supported** | **Ansible 2.9+**

## Overview

This role illustrates key Ansible concepts and workflows, including:
- **Role Structure**: Organized according to Ansible best practices with `defaults/`, `tasks/`, `vars/`, and other standard directories
- **Version Control Integration**: Demonstrates Git operations within Ansible tasks, such as cloning repositories securely via HTTPS
- **Secure Variable Handling**: Uses Ansible Vault for encrypting sensitive data like passwords, with accompanying scripts for decryption and environment management
- **Environment Setup**: Includes scripts to configure a development sandbox, ensuring reproducible and isolated Ansible executions
- **Modular Task Design**: Employs `include_tasks` for clean, maintainable playbooks
- **Comprehensive Testing**: Includes Molecule scenarios and unit tests with CI/CD integration

Ideal for learners building foundational Ansible skills, portfolio reviewers assessing technical proficiency, and professionals exploring advanced automation patterns.

## Quick Links

- [`defaults/README.md`](defaults/README.md) — Default role variables and vault notes
- [`vars/README.md`](vars/README.md) — Role variables with higher precedence
- [`tasks/README.md`](tasks/README.md) — Task flow and how to extend the role
- [`meta/README.md`](meta/README.md) — Galaxy metadata and supported platforms
- [`molecule/README.md`](molecule/README.md) — Testing scenarios and configuration
- [`tests/README.md`](tests/README.md) — Unit tests for helper scripts
- [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) — Common issues and solutions

## Prerequisites

- **Ansible**: ansible-core 2.9+ (recommended: 2.19+)
- **Git**: For repository operations
- **Python**: 3.10–3.14 (for helper scripts and testing)
- **Ansible Vault**: Included with Ansible (for encrypted variables)

## Quick Start

1. **Clone this repository:**
   ```bash
   git clone https://github.com/briankearney/ans_dev_sandbox_role.git
   cd ans_dev_sandbox_role
   ```

2. **Activate the sandbox environment:**
   ```bash
   source ./ACTIVATE_SANDBOX_ENV.bash
   ```
   This script:
   - Creates and activates a Python virtual environment
   - Installs required Python packages
   - Sets Ansible environment variables
   - Configures vault password file location

3. **Use the role in a playbook:**
   ```yaml
   ---
   - name: Example playbook using ans_dev_sandbox_role
     hosts: localhost
     roles:
       - role: ans_dev_sandbox_role
         vars:
           ans_dev_sandbox_role_git_repo_url: "https://github.com/example/repo.git"
           ans_dev_sandbox_role_git_repo_version: "main"
   ```

4. **Run the playbook:**
   ```bash
   ansible-playbook playbook.yml
   ```

## What This Role Does

The role performs the following operations:

1. **Creates a temporary directory** (or uses a fixed path for idempotent testing)
2. **Clones a Git repository** to the temporary location using HTTPS
3. **Lists all files** in the cloned repository recursively
4. **Displays results** with detailed debug output

## Variables

### Default Variables (`defaults/main.yml`)

| Variable | Default | Description |
|----------|---------|-------------|
| `ans_dev_sandbox_role_some_username` | `UserName` | Example username (demonstrates variable usage) |
| `ans_dev_sandbox_role_some_password` | (vaulted) | Example vault-encrypted password |
| `ans_dev_sandbox_role_some_variable` | `foo` | Example variable |
| `ans_dev_sandbox_role_git_repo_url` | `https://github.com/briankearney/ans_dev_sandbox_role` | Repository URL to clone |
| `ans_dev_sandbox_role_git_repo_version` | `main` | Branch/tag/commit to checkout |
| `ans_dev_sandbox_role_temp_dir_path` | `""` | Fixed temp directory path (empty = create new) |

### Variable Precedence

- **Defaults** (`defaults/main.yml`): Lowest precedence, safe to override
- **Vars** (`vars/main.yml`): Higher precedence, internal role variables
- **Sensitive values**: Encrypted with Ansible Vault in `defaults/main.yml`

### Overriding Variables

```yaml
- hosts: localhost
  roles:
    - role: ans_dev_sandbox_role
      vars:
        ans_dev_sandbox_role_git_repo_url: "https://github.com/your-org/your-repo.git"
        ans_dev_sandbox_role_git_repo_version: "v1.0.0"
        ans_dev_sandbox_role_temp_dir_path: "/tmp/custom_path"
```

## Repository Structure

```
ans_dev_sandbox_role/
├── .github/
│   ├── .copilot-instructions.md    # GitHub Copilot coding standards
│   └── workflows/                  # CI/CD workflows
│       ├── molecule.yml            # Molecule testing workflow
│       └── unit-tests.yml          # Unit test workflow
├── defaults/
│   ├── main.yml                    # Default variables (inc. vaulted)
│   └── README.md                   # Variable documentation
├── docs/
│   └── TROUBLESHOOTING.md          # Common issues and solutions
├── meta/
│   ├── main.yml                    # Ansible Galaxy metadata
│   └── README.md                   # Metadata documentation
├── molecule/
│   ├── default/                    # Full integration tests
│   ├── localhost-only/             # Quick validation tests
│   ├── with-linting/               # Lint-focused tests
│   └── README.md                   # Testing documentation
├── tasks/
│   ├── main.yml                    # Main task entry point
│   ├── git_clone.yml               # Git clone tasks
│   └── README.md                   # Task documentation
├── tests/
│   ├── test_activate_sandbox_env.bash
│   ├── test_DECRYPT_VAULTED_ITEMS.py
│   └── README.md                   # Test documentation
├── vars/
│   ├── main.yml                    # Role-level variables
│   └── README.md                   # Variable documentation
├── ACTIVATE_SANDBOX_ENV.bash       # Environment setup script
├── DECRYPT_VAULTED_ITEMS.py        # Vault decryption utility
├── requirements.txt                # Python dependencies
├── requirements.yml                # Ansible collection dependencies
├── constraints.txt                 # Python version constraints
├── collections.yml                 # Molecule collection requirements
├── vault-pw.txt                    # Vault password file (not in VCS)
└── README.md                       # This file
```

## Helper Scripts

### ACTIVATE_SANDBOX_ENV.bash

Sets up the development environment:
- Finds appropriate Python 3.10–3.14 interpreter
- Creates/activates virtual environment in `.venv/`
- Installs Python dependencies from `requirements.txt`
- Sets Ansible environment variables
- Configures vault password file location

**Usage:**
```bash
source ./ACTIVATE_SANDBOX_ENV.bash
```

### DECRYPT_VAULTED_ITEMS.py

Decrypts and displays Ansible Vault-encrypted variables:

**Usage:**
```bash
python DECRYPT_VAULTED_ITEMS.py -f defaults/main.yml -i ans_dev_sandbox_role_some_password
python DECRYPT_VAULTED_ITEMS.py -f defaults/main.yml -i ans_dev_sandbox_role_some_password --color
python DECRYPT_VAULTED_ITEMS.py -f defaults/main.yml -i ans_dev_sandbox_role_some_password --decode
```

**Options:**
- `-f, --file`: YAML file containing vault items
- `-i, --id`: Variable name to decrypt
- `-c, --color`: Colorize output
- `-d, --decode`: Attempt base64 decoding

## Testing

### Molecule Scenarios

Three test scenarios are available:

1. **default**: Full integration test with idempotence checking
   ```bash
   molecule test -s default
   ```

2. **localhost-only**: Quick validation (skips idempotence)
   ```bash
   molecule test -s localhost-only
   ```

3. **with-linting**: Assumes external linting performed
   ```bash
   molecule test -s with-linting
   ```

### Unit Tests

Run bash tests:
```bash
bash tests/test_activate_sandbox_env.bash
```

Run Python tests:
```bash
pytest -v tests/test_DECRYPT_VAULTED_ITEMS.py
```

### Linting

```bash
yamllint .
ansible-lint
ansible-playbook --syntax-check playbook.yml
```

## CI/CD

GitHub Actions workflows automatically run on push and pull requests:

- **Molecule CI**: Tests all scenarios across Python 3.10–3.14
- **Unit Tests**: Validates helper scripts across Python versions
- **Linting**: Runs yamllint and ansible-lint

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`molecule test`)
6. Run linting (`yamllint . && ansible-lint`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## License

MIT License - see the [`LICENSE`](LICENSE) file for details.

## Author

**Brian Kearney** - [briankearney](https://github.com/briankearney)

## Related Projects

- [ans_dev_sandbox_playbook](https://github.com/briankearney/ans_dev_sandbox_playbook) - Example playbook using this role 


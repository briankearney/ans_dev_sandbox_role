# Troubleshooting Guide

Common issues and solutions when working with `ans_dev_sandbox_role`.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Dependency Issues](#dependency-issues)
- [Molecule Testing](#molecule-testing)
- [Linting Issues](#linting-issues)
- [Git/Repository Issues](#gitrepository-issues)
- [CI/CD Issues](#cicd-issues)
- [Vault Issues](#vault-issues)
- [Getting Help](#getting-help)

## Environment Setup

### Virtual environment activation fails

**Problem:** `ACTIVATE_SANDBOX_ENV.bash` fails to create or activate `.venv`

**Symptoms:**
```
-bash: python3: command not found
```
or
```
Error: No suitable Python found
```

**Solutions:**

1. **Verify Python installation:**
   ```bash
   python3 --version
   ```
   Should return Python 3.10–3.14

2. **Install Python venv module** (Debian/Ubuntu):
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip
   ```

3. **Install Python venv module** (RHEL/CentOS/Fedora):
   ```bash
   sudo dnf install python3-virtualenv
   ```

4. **Manually create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Python version too new (≥3.15)

**Problem:** Script rejects Python 3.15 or newer

**Error Message:**
```
Python 3.15+ is not yet supported due to dependency constraints
```

**Explanation:** This is intentional to avoid `pytest-ansible` conflicts. The constraint prevents argparse conflicts in pytest plugins.

**Solutions:**

1. **Install supported Python version (3.10–3.14):**
   ```bash
   # Using pyenv
   pyenv install 3.14.0
   pyenv local 3.14.0
   
   # Using deadsnakes PPA (Ubuntu)
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install python3.14 python3.14-venv
   ```

2. **Override version check** (if conflict is resolved):
   Edit `ACTIVATE_SANDBOX_ENV.bash` and update the version check logic

### Script must be sourced, not executed

**Problem:** Running `./ACTIVATE_SANDBOX_ENV.bash` doesn't activate environment

**Symptoms:**
- Virtual environment not active after script runs
- Environment variables not set in current shell

**Solution:** Always **source** the script:
```bash
# Correct
source ./ACTIVATE_SANDBOX_ENV.bash

# Also correct
. ./ACTIVATE_SANDBOX_ENV.bash

# WRONG - won't persist environment
./ACTIVATE_SANDBOX_ENV.bash
```

### Permission denied errors

**Problem:** Cannot execute scripts or access files

**Solutions:**

1. **Make scripts executable:**
   ```bash
   chmod +x ACTIVATE_SANDBOX_ENV.bash
   chmod +x DECRYPT_VAULTED_ITEMS.py
   chmod +x tests/*.bash
   ```

2. **Check file ownership:**
   ```bash
   ls -la
   # Change ownership if needed
   sudo chown -R $USER:$USER .
   ```

## Dependency Issues

### ansible-core installation fails

**Problem:** `pip install -r requirements.txt` fails on ansible-core

**Error Examples:**
```
ERROR: Failed building wheel for ansible-core
```
or
```
ERROR: Could not find a version that satisfies the requirement ansible-core
```

**Solutions:**

1. **Upgrade pip, setuptools, and wheel:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. **Check Python version compatibility:**
   ```bash
   python --version
   # ansible-core 2.19+ requires Python 3.10+
   ```

3. **Install system dependencies:**
   
   **Debian/Ubuntu:**
   ```bash
   sudo apt install gcc python3-dev libffi-dev libssl-dev
   ```
   
   **RHEL/CentOS/Fedora:**
   ```bash
   sudo dnf install gcc python3-devel libffi-devel openssl-devel
   ```

4. **Install specific version:**
   ```bash
   pip install ansible-core==2.19.0
   ```

### Collection installation fails

**Problem:** `ansible-galaxy collection install -r requirements.yml` fails

**Error Examples:**
```
ERROR! Unknown error when attempting to call Galaxy
```
or
```
ERROR! Failed to download collection tar from 'https://galaxy.ansible.com/...'
```

**Solutions:**

1. **Check network connectivity:**
   ```bash
   curl -I https://galaxy.ansible.com
   ping galaxy.ansible.com
   ```

2. **Check for proxy/firewall issues:**
   ```bash
   # Set proxy if needed
   export HTTP_PROXY=http://proxy.example.com:8080
   export HTTPS_PROXY=http://proxy.example.com:8080
   ```

3. **Manually install collections:**
   ```bash
   ansible-galaxy collection install ansible.posix
   ansible-galaxy collection install community.general
   ```

4. **Clear Galaxy cache:**
   ```bash
   rm -rf ~/.ansible/galaxy_cache
   ansible-galaxy collection install -r requirements.yml --force
   ```

5. **Use offline installation:**
   ```bash
   # Download tarballs on another machine
   ansible-galaxy collection download ansible.posix community.general
   
   # Install from tarballs
   ansible-galaxy collection install ansible-posix-*.tar.gz
   ```

### pytest-ansible conflicts

**Problem:** `pytest` fails with argparse errors

**Error Example:**
```
argparse: argument --inventory: conflicting option string: --inventory
```

**Explanation:** Both `pytest-ansible` and `pytest-testinfra` register the same CLI arguments.

**Solution:** This is already handled by `constraints.txt`:
```
pytest-ansible==0.0.0
```

If you encounter this error:
1. Verify `constraints.txt` is being used
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt -c constraints.txt --force-reinstall
   ```

## Molecule Testing

### "Failed to find driver delegated"

**Problem:** Older Molecule configurations reference unavailable driver

**Error:**
```
ERROR: Failed to find driver delegated
```

**Solution:** This has been fixed in current configuration. Ensure `molecule.yml` uses:
```yaml
driver:
  name: default  # Not 'delegated'
```

### Idempotence test fails

**Problem:** "Idempotence test failed because of the following tasks: Create Temporary Directory"

**Full Error:**
```
CRITICAL Idempotence test failed because of the following tasks:
* [instance] => Create Temporary Directory
```

**Explanation:** The `tempfile` module creates a new unique directory on each run, which is non-idempotent behavior.

**Solutions:**

1. **Use `localhost-only` scenario** (skips idempotence check):
   ```bash
   molecule test -s localhost-only
   ```

2. **Use fixed temp path** (for `default` scenario):
   ```yaml
   # molecule/default/converge.yml
   - name: Converge
     hosts: all
     roles:
       - role: ans_dev_sandbox_role
         vars:
           ans_dev_sandbox_role_temp_dir_path: "/tmp/molecule_test_sandbox"
   ```

3. **Understand the behavior:** The `default` scenario already uses a fixed path. If still failing:
   - Check for other non-idempotent tasks
   - Review `changed_when` conditions
   - Verify file module operations use `state` explicitly

### Role not found during Molecule test

**Problem:** `the role 'ans_dev_sandbox_role' was not found`

**Error:**
```
ERROR! the role 'ans_dev_sandbox_role' was not found in /path/to/molecule/...
```

**Solution:** Ensure `ANSIBLE_ROLES_PATH` is set correctly in `molecule.yml`:

```yaml
provisioner:
  name: ansible
  env:
    ANSIBLE_ROLES_PATH: "${MOLECULE_PROJECT_DIRECTORY}/.."
```

If still failing:
1. **Verify directory structure:**
   ```bash
   pwd
   # Should be in role root, not in molecule/scenario/
   ```

2. **Run from correct directory:**
   ```bash
   cd /path/to/ans_dev_sandbox_role
   molecule test -s default
   ```

3. **Check role name in converge.yml:**
   ```yaml
   roles:
     - role: ans_dev_sandbox_role  # Must match directory name
   ```

### Testinfra tests fail

**Problem:** pytest-testinfra verification fails

**Error Examples:**
```
FAILED tests/test_default.py::test_python - AssertionError
```

**Solutions:**

1. **Check test file exists:**
   ```bash
   ls molecule/default/tests/test_default.py
   ```

2. **Run tests manually:**
   ```bash
   cd molecule/default
   pytest tests/test_default.py -v
   ```

3. **Update test assertions** if environment changed:
   ```python
   def test_git_installed(host):
       git = host.package("git")
       assert git.is_installed  # Ensure git is available
   ```

### Molecule dependency step fails

**Problem:** Collections not installing during `dependency` step

**Error:**
```
CRITICAL Ansible Galaxy dependency manager failed
```

**Solutions:**

1. **Verify requirements files exist:**
   ```bash
   ls molecule/default/requirements.yml
   ls molecule/default/collections.yml
   ```

2. **Check file syntax:**
   ```bash
   yamllint molecule/default/requirements.yml
   ```

3. **Install dependencies manually:**
   ```bash
   ansible-galaxy collection install -r requirements.yml
   ```

## Linting Issues

### yamllint warnings on line length

**Problem:** Lines exceed 160 characters

**Warning:**
```
./file.yml:42:161: [warning] line too long (165 > 160 characters) (line-length)
```

**Solution:** This is configured as warning-level, not error. To fix:

1. **Break long lines:**
   ```yaml
   # Before
   - name: Very long task name that exceeds the line length limit and causes warnings
   
   # After
   - name: >-
       Very long task name that exceeds the line length
       limit and causes warnings
   ```

2. **Use YAML block scalars:**
   ```yaml
   description: >
     This is a long description
     that spans multiple lines
     using folded block scalar
   ```

3. **Configure yamllint** if needed (`.yamllint`):
   ```yaml
   rules:
     line-length:
       max: 160
       level: warning  # or error
   ```

### ansible-lint reports "galaxy" issues

**Problem:** `meta/main.yml` flagged by galaxy rules

**Warning:**
```
meta/main.yml:1: galaxy[tags] Tags must contain lowercase letters and digits only
```

**Solution:** These are skipped in `.ansible-lint`. If still appearing:

1. **Verify `.ansible-lint` configuration:**
   ```yaml
   skip_list:
     - galaxy[tags]
     - galaxy[version-incorrect]
   ```

2. **Update tags** to comply:
   ```yaml
   galaxy_tags:
     - ansible
     - sandbox  # not "Sandbox"
     - development  # not "Development"
   ```

3. **Run with skip-list:**
   ```bash
   ansible-lint --skip-list galaxy
   ```

### ansible-lint "fqcn" violations

**Problem:** Modules not using Fully Qualified Collection Names

**Error:**
```
tasks/main.yml:5: fqcn[action-core] Use FQCN for builtin module actions
```

**Solution:** Use FQCN everywhere:

```yaml
# Wrong
- name: Clone repository
  git:
    repo: "..."

# Correct
- name: Clone repository
  ansible.builtin.git:
    repo: "..."
```

## Git/Repository Issues

### Git clone fails with authentication

**Problem:** Role's git clone task fails on private repositories

**Error:**
```
fatal: could not read Username for 'https://github.com': No such device or address
```

**Explanation:** This role is designed for **public HTTPS repositories** only.

**Solutions for Private Repositories:**

1. **Use SSH URLs:**
   ```yaml
   ans_dev_sandbox_role_git_repo_url: "git@github.com:user/private-repo.git"
   ```
   
   Then configure SSH keys:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ssh-add ~/.ssh/id_ed25519
   # Add public key to GitHub
   ```

2. **Use HTTPS with credentials:**
   ```yaml
   - name: Clone with credentials
     ansible.builtin.git:
       repo: "https://{{ github_token }}@github.com/user/repo.git"
       dest: "{{ dest_path }}"
   ```

3. **Use deploy keys in CI/CD:**
   ```yaml
   # GitHub Actions
   - uses: webfactory/ssh-agent@v0.5.4
     with:
       ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
   ```

### Temp directory fills up

**Problem:** `/tmp` fills with cloned repositories

**Symptoms:**
```bash
df -h /tmp
# Shows low available space
```

**Solutions:**

1. **Clean up manually:**
   ```bash
   # Remove Ansible temp directories
   rm -rf /tmp/ansible.*_ansible_sandbox
   
   # Remove Molecule test directories
   rm -rf /tmp/molecule_test_sandbox
   ```

2. **Use cleanup task in playbook:**
   ```yaml
   post_tasks:
     - name: Clean up temp directory
       ansible.builtin.file:
         path: "{{ ans_dev_sandbox_role_temp_dir_results.path }}"
         state: absent
       when: ans_dev_sandbox_role_temp_dir_results.path is defined
   ```

3. **Use custom temp location:**
   ```yaml
   ans_dev_sandbox_role_temp_dir_path: "/var/tmp/custom_sandbox"
   ```

4. **Configure system temp cleanup:**
   ```bash
   # Ubuntu/Debian - configure tmpwatch/tmpreaper
   sudo apt install tmpreaper
   
   # Edit /etc/tmpreaper.conf
   TMPREAPER_TIME=7d
   ```

### Git clone slow or hangs

**Problem:** Git operations take very long or appear to hang

**Solutions:**

1. **Check network connectivity:**
   ```bash
   ping github.com
   traceroute github.com
   ```

2. **Increase git timeout:**
   ```yaml
   - name: Clone with timeout
     ansible.builtin.git:
       repo: "{{ repo_url }}"
       dest: "{{ dest_path }}"
     async: 600  # 10 minute timeout
     poll: 5
   ```

3. **Use shallow clone:**
   ```yaml
   - name: Shallow clone
     ansible.builtin.git:
       repo: "{{ repo_url }}"
       dest: "{{ dest_path }}"
       depth: 1
   ```

## CI/CD Issues

### GitHub Actions workflow fails on Python 3.14

**Problem:** Python 3.14 is too new and causes dependency conflicts

**Error:**
```
ERROR: Cannot install -r requirements.txt (line 1) and pytest-ansible==...
```

**Solution:** As of December 2025, Python 3.14 is the latest stable. If issues arise:

1. **Pin to stable Python version:**
   ```yaml
   # .github/workflows/molecule.yml
   matrix:
     python-version: ['3.10', '3.11', '3.12', '3.13']  # Remove 3.14
   ```

2. **Update requirements:**
   ```bash
   # Test with Python 3.14
   python3.14 -m venv test_env
   source test_env/bin/activate
   pip install -r requirements.txt -c constraints.txt
   ```

3. **Check upstream dependencies:**
   - Monitor `pytest-ansible` for updates
   - Check `molecule` compatibility
   - Review `ansible-core` support matrix

### Workflow badge not showing

**Problem:** README badges show "unknown" or don't render

**Badge URL:**
```markdown
![Molecule CI](https://github.com/USER/REPO/actions/workflows/molecule.yml/badge.svg)
```

**Solutions:**

1. **Ensure workflows have run at least once:**
   ```bash
   # Push to trigger workflow
   git push origin main
   ```

2. **Verify repository visibility:**
   - Public repositories: Badges work automatically
   - Private repositories: Require authentication tokens

3. **Check badge URLs match workflow filenames:**
   ```bash
   ls .github/workflows/
   # Ensure molecule.yml exists (not molecule.yaml)
   ```

4. **Use branch-specific badges:**
   ```markdown
   ![Molecule CI](https://github.com/USER/REPO/actions/workflows/molecule.yml/badge.svg?branch=main)
   ```

### CI runs take too long

**Problem:** GitHub Actions workflows exceed time limits or are very slow

**Solutions:**

1. **Use matrix efficiently:**
   ```yaml
   strategy:
     fail-fast: false  # Continue even if one fails
     matrix:
       python-version: ['3.10', '3.14']  # Test min and max only
       scenario: ['localhost-only']  # Fastest scenario
   ```

2. **Cache dependencies:**
   ```yaml
   - name: Cache pip packages
     uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
   ```

3. **Skip unnecessary steps:**
   ```yaml
   - name: Run Molecule
     if: github.event_name != 'pull_request'  # Only on push
     run: molecule test
   ```

## Vault Issues

### Cannot decrypt vaulted variables

**Problem:** `ansible-vault` fails or `DECRYPT_VAULTED_ITEMS.py` errors

**Errors:**
```
ERROR! Decryption failed
```
or
```
ERROR! Vault password file not found
```

**Solutions:**

1. **Verify vault password file exists:**
   ```bash
   ls -la vault-pw.txt
   ```

2. **Check vault password is correct:**
   ```bash
   # Default demo password is "ansible"
   echo "ansible" > vault-pw.txt
   ```

3. **Verify file has vault format:**
   ```bash
   head -n 1 defaults/main.yml
   # Should contain: $ANSIBLE_VAULT;1.1;AES256
   ```

4. **Use ansible-vault directly:**
   ```bash
   ansible-vault view defaults/main.yml --vault-password-file vault-pw.txt
   ```

5. **Re-encrypt if corrupted:**
   ```bash
   # Decrypt
   ansible-vault decrypt defaults/main.yml --vault-password-file vault-pw.txt
   
   # Re-encrypt
   ansible-vault encrypt defaults/main.yml --vault-password-file vault-pw.txt
   ```

### vault-pw.txt not created automatically

**Problem:** Script doesn't generate vault password file

**Symptoms:**
```bash
ls vault-pw.txt
# No such file or directory
```

**Solutions:**

1. **Source the activation script** (don't execute):
   ```bash
   # Correct
   source ./ACTIVATE_SANDBOX_ENV.bash
   
   # Wrong - won't persist
   ./ACTIVATE_SANDBOX_ENV.bash
   ```

2. **Create manually:**
   ```bash
   echo "ansible" > vault-pw.txt
   chmod 600 vault-pw.txt
   ```

3. **Set environment variable:**
   ```bash
   export ANSIBLE_VAULT_PASSWORD_FILE="$PWD/vault-pw.txt"
   ```

### Vault password in VCS warning

**Problem:** Git warns about vault-pw.txt being tracked

**Solution:** Ensure `.gitignore` includes:
```
vault-pw.txt
*.log
.venv/
__pycache__/
```

Check if file is tracked:
```bash
git ls-files | grep vault-pw.txt
# Should return nothing

# If tracked, remove from git:
git rm --cached vault-pw.txt
git commit -m "Remove vault password file from tracking"
```

## Getting Help

If issues persist after trying these solutions:

### 1. Check GitHub Issues

Search existing issues or open a new one:
- **Repository Issues:** https://github.com/briankearney/ans_dev_sandbox_role/issues
- Include error messages, OS version, Python version
- Attach relevant logs (sanitize sensitive data)

### 2. Review Documentation

- **Molecule Documentation:** https://ansible.readthedocs.io/projects/molecule/
- **Ansible Documentation:** https://docs.ansible.com/
- **pytest Documentation:** https://docs.pytest.org/

### 3. Community Resources

- **Ansible Community:** https://docs.ansible.com/ansible/latest/community/communication.html
- **Molecule Discussions:** https://github.com/ansible/molecule/discussions
- **Stack Overflow:** Tag questions with `ansible`, `molecule`, `ansible-vault`

### 4. Enable Debug Output

```bash
# Ansible verbose mode
ansible-playbook playbook.yml -vvv

# Molecule verbose mode
molecule --debug test

# pytest verbose mode
pytest -vv tests/
```

### 5. Check Versions

```bash
# System information
uname -a
cat /etc/os-release

# Python version
python --version

# Ansible version
ansible --version
ansible-galaxy --version

# Molecule version
molecule --version

# Pip packages
pip list | grep -E "ansible|molecule|pytest"
```
```

Or use a fixed path and clean it in post_tasks:
```yaml
post_tasks:
  - name: Clean up temp directory
    file:
      path: "{{ ans_dev_sandbox_role_temp_dir_results.path }}"
      state: absent
```

## CI/CD Issues

### GitHub Actions workflow fails on Python 3.14
**Problem:** Python 3.14 is too new and causes dependency conflicts

**Solution:** As of December 2025, Python 3.14 is the latest stable. If issues arise:
- Pin to Python 3.13 in workflows
- Update `requirements.txt` with compatible versions
- Check for `pytest-ansible` conflicts

### Workflow badge not showing
**Problem:** README badges show "unknown" or don't render

**Solutions:**
- Ensure workflows have run at least once
- Verify repository is public or badge tokens are configured
- Check badge URLs match workflow filenames exactly

## Vault Issues

### Cannot decrypt vaulted variables
**Problem:** `ansible-vault` fails or `DECRYPT_VAULTED_ITEMS.py` errors

**Solutions:**
- Ensure `vault-pw.txt` exists (created by `ACTIVATE_SANDBOX_ENV.bash`)
- Verify vault password is correct (demo password: "ansible")
- Check file has vault format: `$ANSIBLE_VAULT;1.1;AES256`

### vault-pw.txt not created automatically
**Problem:** Script doesn't generate vault password file

**Solution:** Source the activation script (don't execute):
```bash
source ./ACTIVATE_SANDBOX_ENV.bash  # Correct
./ACTIVATE_SANDBOX_ENV.bash          # Won't persist in current shell
```

## Getting Help

If issues persist:
1. Check GitHub Issues: https://github.com/briankearney/ans_dev_sandbox_role/issues
2. Review Molecule docs: https://ansible.readthedocs.io/projects/molecule/
3. Ansible community: https://docs.ansible.com/ansible/latest/community/communication.html

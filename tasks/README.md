# tasks/

## Purpose

Contains the role's task definitions that perform the actual work. `tasks/main.yml` is the default entry point and includes other task files for better organization and modularity.

## Task Files

### `main.yml`

The primary entry point for the role. Currently includes:

```yaml
---
- name: Include Clone Task
  ansible.builtin.include_tasks:
    file: git_clone.yml
```

This file orchestrates task execution by including modular task files.

### `git_clone.yml`

Performs the main role functionality:

1. **Set Temporary Directory Path**
   - Allows override of temp directory via `temp_dir_path` variable
   - Sets fact for use in subsequent tasks

2. **Create Temporary Directory** (conditional)
   - Uses `ansible.builtin.tempfile` module
   - Creates unique directory with `_ansible_sandbox` suffix
   - Only runs when `ans_dev_sandbox_role_temp_dir_path` is empty
   - Registered as `ans_dev_sandbox_role_temp_dir_results`

3. **Use Fixed Temporary Directory Path** (conditional)
   - Sets fact to use pre-defined path
   - Only runs when `ans_dev_sandbox_role_temp_dir_path` is set
   - Enables idempotent testing

4. **Ensure Fixed Temporary Directory Exists** (conditional)
   - Creates directory with 0755 permissions
   - Only runs when using fixed path
   - Idempotent - safe to run multiple times

5. **Clone GitHub Repository**
   - Uses `ansible.builtin.git` module
   - Clones from `ans_dev_sandbox_role_git_repo_url`
   - Checks out `ans_dev_sandbox_role_git_repo_version`
   - Forces non-interactive mode (`GIT_TERMINAL_PROMPT=false`)
   - Updates existing repository if present
   - Registers result as `ans_dev_sandbox_role_git_clone_results`

6. **List Cloned Files**
   - Uses `ansible.builtin.find` module
   - Recursively searches cloned directory
   - Only runs if clone succeeded
   - Registers result as `ans_dev_sandbox_role_find_results`

7. **Display Files Found**
   - Shows repository path and file count
   - Lists all file paths in YAML format
   - Only runs when files are found

8. **Display Empty Repository Message**
   - Informational message if no files found
   - Helps identify empty or initialization-only repositories

## Variables Used by Tasks

| Variable | Source | Purpose |
|----------|--------|---------|
| `temp_dir_path` | Play/extra vars | Optional override for temp directory |
| `ans_dev_sandbox_role_temp_dir_path` | defaults/main.yml | Fixed temp path or empty for dynamic |
| `ans_dev_sandbox_role_git_repo_url` | defaults/main.yml | Repository URL to clone |
| `ans_dev_sandbox_role_git_repo_version` | defaults/main.yml | Branch/tag/commit to checkout |

## Registered Variables

Tasks register the following variables for use in subsequent tasks or debugging:

| Variable | Type | Contains |
|----------|------|----------|
| `ans_dev_sandbox_role_temp_dir_results` | Dict | Temporary directory path and metadata |
| `ans_dev_sandbox_role_fixed_dir_results` | Dict | Fixed directory creation results |
| `ans_dev_sandbox_role_git_clone_results` | Dict | Git clone operation results |
| `ans_dev_sandbox_role_find_results` | Dict | List of files found in repository |

## Extending Tasks

### Adding New Task Files

1. **Create task file** in `tasks/` directory:
   ```yaml
   # tasks/my_new_task.yml
   ---
   - name: My Custom Task
     ansible.builtin.debug:
       msg: "Performing custom operation"
   ```

2. **Include in main.yml**:
   ```yaml
   # tasks/main.yml
   ---
   - name: Include Clone Task
     ansible.builtin.include_tasks:
       file: git_clone.yml

   - name: Include Custom Task
     ansible.builtin.include_tasks:
       file: my_new_task.yml
   ```

### Using Tags

Add tags for selective execution:

```yaml
- name: Include Clone Task
  ansible.builtin.include_tasks:
    file: git_clone.yml
  tags:
    - clone
    - git

- name: Include Custom Task
  ansible.builtin.include_tasks:
    file: my_new_task.yml
  tags:
    - custom
```

Run specific tasks:
```bash
ansible-playbook playbook.yml --tags clone
ansible-playbook playbook.yml --skip-tags custom
```

### Conditional Execution

Use `when` conditions for task control:

```yaml
- name: Include Optional Task
  ansible.builtin.include_tasks:
    file: optional.yml
  when: enable_optional_feature | default(false)
```

### Task Blocks

Group related tasks with blocks:

```yaml
- name: Setup and Clone
  block:
    - name: Create Directory
      ansible.builtin.file:
        path: /tmp/workspace
        state: directory

    - name: Clone Repository
      ansible.builtin.git:
        repo: "{{ git_repo_url }}"
        dest: /tmp/workspace
  rescue:
    - name: Handle Failure
      ansible.builtin.debug:
        msg: "Clone failed, cleaning up"
  always:
    - name: Log Attempt
      ansible.builtin.debug:
        msg: "Clone attempted"
```

## Task Naming Conventions

Following Ansible best practices (see `.github/.copilot-instructions.md`):

- Start with action verb (Create, Clone, Display, etc.)
- Capitalize first letter
- No periods at end
- Concise but descriptive
- Omit role name (Ansible displays it automatically)

## Idempotency

Tasks are designed to be idempotent:

- **Temporary directory creation**: Uses Ansible's `tempfile` module or checks existence
- **Git clone**: Uses `update: true` to handle existing repositories
- **File operations**: Use appropriate `state` parameters

## Error Handling

Tasks implement proper error handling:

```yaml
- name: Clone GitHub Repository
  ansible.builtin.git:
    repo: "{{ ans_dev_sandbox_role_git_repo_url }}"
    dest: "{{ ans_dev_sandbox_role_temp_dir_results.path }}/"
    version: "{{ ans_dev_sandbox_role_git_repo_version }}"
  register: ans_dev_sandbox_role_git_clone_results
  failed_when: ans_dev_sandbox_role_git_clone_results.failed
```

## Best Practices

1. **Use fully qualified collection names (FQCN)**: `ansible.builtin.git` instead of `git`
2. **Register results**: Store task output for debugging and conditional logic
3. **Handle errors gracefully**: Use `failed_when`, `ignore_errors`, `rescue` blocks
4. **Add descriptive names**: Help users understand what each task does
5. **Use variables**: Make tasks reusable and configurable
6. **Document conditionals**: Comment complex `when` conditions
7. **Test idempotency**: Ensure tasks can run multiple times safely

## Related Documentation

- [`defaults/README.md`](../defaults/README.md) - Default variable values
- [`vars/README.md`](../vars/README.md) - Role-level variables
- [Ansible Documentation: Tasks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html#tasks-list)
- [Ansible Documentation: Modules](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html)

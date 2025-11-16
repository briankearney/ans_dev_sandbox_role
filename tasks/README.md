# tasks/

Purpose
- Contains the role's task definitions. `tasks/main.yml` is the default entry point and may include other task files (e.g., `git_clone.yml`).

What this role does (tasks/git_clone.yml)
- Create a temporary directory using the `tempfile` module.
- Clone a Git repository using the `git` module (`git_repo_url`, `git_repo_version`).
- Use the `find` module to list files in the cloned repository.
- Display results with `debug` and clean up temporary resources.

Extending tasks
- Add new task files and include them from `tasks/main.yml` with `ansible.builtin.include_tasks`.
- Use tags to enable selective execution of task blocks.

Variables used by tasks
- `git_repo_url` — repository to clone.
- `git_repo_version` — branch/tag/commit to check out.

Example: run only clone-related tasks
```bash
ansible-playbook playbook.yml --tags clone
```

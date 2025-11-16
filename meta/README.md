# meta/

Purpose
- Holds Galaxy metadata about the role such as author, supported platforms, minimum Ansible version, and tags.

What you'll find in `meta/main.yml`
- `galaxy_info.author` — role author.
- `galaxy_info.description` — short description shown on Galaxy.
- `galaxy_info.min_ansible_version` — minimum Ansible version this role targets.
- `galaxy_info.platforms` — supported OS families and versions.
- `galaxy_tags` — keywords used by Ansible Galaxy.

Use
- Update metadata before publishing to Ansible Galaxy.
- Keep `platforms` and `min_ansible_version` accurate to avoid user confusion.

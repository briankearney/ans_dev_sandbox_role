# meta/

## Purpose

Contains Ansible Galaxy metadata that describes the role, including author information, supported platforms, minimum Ansible version, dependencies, and searchable tags. This information is used when publishing to [Ansible Galaxy](https://galaxy.ansible.com/).

## Contents: `meta/main.yml`

### Galaxy Information

| Field | Value | Description |
|-------|-------|-------------|
| `author` | Brian Kearney | Role maintainer |
| `description` | Ansible role providing a development sandbox and demo tasks for testing/CI | Short description shown on Galaxy |
| `role_name` | ans_dev_sandbox_role | Role name in Galaxy |
| `namespace` | mcindi | Galaxy namespace |
| `company` | McIndi Solutions | Organization |
| `license` | MIT | Open source license |
| `min_ansible_version` | 2.9 | Minimum Ansible version required |

### Supported Platforms

This role supports the following operating systems:

- **Enterprise Linux (EL)**: All versions (RHEL, CentOS, Rocky, AlmaLinux)
- **Fedora**: All versions
- **Ubuntu**: All versions
- **Debian**: All versions
- **GenericLinux**: All generic Linux distributions

### Galaxy Tags

Tags for discoverability on Ansible Galaxy:

- `ansible` - General Ansible automation
- `sandbox` - Development/testing sandbox
- `development` - Development tooling
- `ci` - Continuous integration
- `demo` - Demonstration/example role

### Dependencies

This role has **no dependencies** on other Ansible roles.

Required collections are defined in `requirements.yml`:
- `ansible.posix` - POSIX-specific modules
- `community.general` - Extended community modules

## Publishing to Ansible Galaxy

### Prerequisites

1. Create an account at [galaxy.ansible.com](https://galaxy.ansible.com/)
2. Generate an API token from your Galaxy profile
3. Configure `ansible-galaxy` CLI:
   ```bash
   ansible-galaxy login --token YOUR_GALAXY_TOKEN
   ```

### Publishing Process

1. **Update metadata** in `meta/main.yml`:
   - Increment version if using git tags
   - Update supported platforms if needed
   - Ensure description and tags are current

2. **Test the role**:
   ```bash
   molecule test
   ansible-lint
   ```

3. **Import to Galaxy**:
   ```bash
   ansible-galaxy role import briankearney ans_dev_sandbox_role
   ```

   Or use GitHub integration:
   - Link GitHub repository to Galaxy account
   - Galaxy will auto-import on tagged releases

### Version Management

Use git tags for versioning:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Galaxy will detect semantic version tags and create corresponding role versions.

## Metadata Best Practices

### Platform Support

- Only list platforms you've tested
- Use `all` for versions only if truly compatible
- Update platforms as testing expands

### Tags

- Use relevant, searchable keywords
- Maximum 20 tags allowed
- Use lowercase, no spaces
- Think about what users will search for

### Minimum Ansible Version

- Set conservatively to avoid breaking user environments
- Test against the minimum version specified
- Consider using `ansible-core` version numbers

### Dependencies

- Minimize external dependencies
- Document required collections in `requirements.yml`
- Avoid circular dependencies

## Galaxy Installation

Users can install this role from Galaxy:

```bash
# Install latest version
ansible-galaxy role install mcindi.ans_dev_sandbox_role

# Install specific version
ansible-galaxy role install mcindi.ans_dev_sandbox_role,v1.0.0

# Install using requirements file
cat > requirements.yml <<EOF
roles:
  - name: mcindi.ans_dev_sandbox_role
    version: v1.0.0
EOF
ansible-galaxy role install -r requirements.yml
```

## Updating Metadata

When making changes to `meta/main.yml`:

1. Update the relevant fields
2. Run validation:
   ```bash
   ansible-lint meta/main.yml
   yamllint meta/main.yml
   ```
3. Test locally with Molecule
4. Commit and push changes
5. Re-import to Galaxy if already published

## Related Documentation

- [Ansible Galaxy Documentation](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html)
- [Role Metadata](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html#role-metadata)
- [Publishing Roles](https://galaxy.ansible.com/docs/contributing/importing.html)

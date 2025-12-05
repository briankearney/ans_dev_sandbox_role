# Molecule Testing

This directory contains three Molecule test scenarios for validating the `ans_dev_sandbox_role`.

## Scenarios

### `default/`
Full integration test with idempotence checking. Uses a fixed temporary directory path to ensure the role is idempotent when run multiple times.

**Test sequence:**
- dependency → syntax → create → prepare → converge → **idempotence** → verify

**Verification:** pytest-testinfra (`tests/test_default.py`) validates:
- Python availability
- git installation
- Temporary directory creation
- PyYAML import capability

### `localhost-only/`
Quick validation scenario focusing on localhost connection and basic role execution. Skips idempotence for faster iteration.

**Test sequence:**
- dependency → syntax → create → prepare → converge → verify

**Verification:** pytest-testinfra (`tests/test_localhost.py`) validates:
- Localhost command execution

### `with-linting/`
Assumes external linting has been performed (via `yamllint` and `ansible-lint`). Uses Ansible-based verification instead of testinfra.

**Test sequence:**
- dependency → syntax → create → prepare → converge → verify

**Verification:** Ansible verifier (no custom verify playbook currently)

## Running Tests

Run all scenarios:
```bash
molecule test
```

Run a specific scenario:
```bash
molecule test -s localhost-only
molecule test -s default
molecule test -s with-linting
```

Run only the converge step (for development):
```bash
molecule converge -s localhost-only
```

**Note:** All scenarios automatically perform cleanup and destroy operations at the end of test execution. The explicit `test_sequence` configurations above show the core testing steps; implicit cleanup/destroy always runs regardless.

## Configuration Notes

- All scenarios use the `default` driver with localhost connection (`ansible_connection: local`)
- Role path is set via `ANSIBLE_ROLES_PATH` environment variable to `${MOLECULE_PROJECT_DIRECTORY}/..`
- No container infrastructure required - tests run directly on the control node
- Python 3.10–3.14 supported

## Dependency Management

### Collections

Required Ansible collections are defined in:
- `requirements.yml` — Primary collection specifications
- `collections.yml` — Mirrors `requirements.yml` for Molecule dependency resolution

Collections installed:
- `ansible.posix` — Provides POSIX-specific modules
- `community.general` — Extended community-maintained modules

The `dependency` step in each scenario validates that collections are available before test execution.

## Known Constraints

### pytest-ansible Plugin Conflict

The `pytest-ansible==0.0.0` constraint in `constraints.txt` intentionally disables the `pytest-ansible` plugin to avoid argparse conflicts with `pytest-testinfra`. Both plugins register the same command-line arguments (`--inventory` / `--ansible-inventory`), causing argparse validation errors on Python 3.12+. Pinning `pytest-ansible` to version `0.0.0` (a no-op) prevents plugin registration while maintaining test compatibility.

**This is intentional and should not be upgraded** without addressing the underlying plugin conflict in pytest's plugin ecosystem.

## CI/CD Integration

GitHub Actions workflow (`.github/workflows/molecule.yml`) runs matrix testing:
- Python versions: 3.10, 3.11, 3.12, 3.13, 3.14
- All three scenarios
- Separate lint job for yamllint and ansible-lint

See `.github/workflows/` for workflow definitions.

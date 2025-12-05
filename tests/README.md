# Unit Tests

This directory contains unit tests for the helper scripts and utilities in this repository. These tests validate functionality outside of Ansible role execution (which is covered by Molecule scenarios).

## Test Files

### `test_activate_sandbox_env.bash`

Validates the `ACTIVATE_SANDBOX_ENV.bash` environment setup script.

**Test Coverage:**
- **Syntax Checking**: Validates bash syntax using `bash -n`
- **Environment Variables**: Verifies `ANSIBLE_VAULT_PASSWORD_FILE` is exported

**Run Manually:**
```bash
bash tests/test_activate_sandbox_env.bash
```

**Expected Output:**
```
Running tests for ACTIVATE_SANDBOX_ENV.bash...
✓ Script exists and is readable
✓ Script has valid bash syntax
✓ Script exports ANSIBLE_VAULT_PASSWORD_FILE
All tests passed!
```

**Exit Codes:**
- `0`: All tests passed
- `1`: One or more tests failed

### `test_DECRYPT_VAULTED_ITEMS.py`

Validates the `DECRYPT_VAULTED_ITEMS.py` Ansible Vault utility script.

**Test Coverage:**
- **Script Existence**: Verifies script file exists
- **Help Output**: Tests `--help` flag functionality
- **Import Validation**: Ensures script imports cleanly

**Run Manually:**
```bash
# Quick mode
pytest -q tests/test_DECRYPT_VAULTED_ITEMS.py

# Verbose mode
pytest -v tests/test_DECRYPT_VAULTED_ITEMS.py

# With output
pytest -s tests/test_DECRYPT_VAULTED_ITEMS.py
```

**Test Class:** `TestDecryptVaultedItems`

**Test Methods:**
- `test_script_exists()`: Validates file presence
- `test_help_output()`: Checks help text generation

## Running All Tests

### Run All Unit Tests

```bash
# Bash tests
bash tests/test_activate_sandbox_env.bash

# Python tests
pytest tests/
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html tests/
```

### Run in CI Mode

```bash
# Used by GitHub Actions
pytest -q tests/test_DECRYPT_VAULTED_ITEMS.py
```

## CI/CD Integration

Unit tests are automatically executed by GitHub Actions on every push and pull request.

### Workflow: `.github/workflows/unit-tests.yml`

**Jobs:**

1. **bash-tests**
   - Runs on: `ubuntu-latest`
   - Tests:
     - Bash syntax validation (`bash -n`)
     - Environment variable exports (`grep` check)

2. **python-tests**
   - Runs on: `ubuntu-latest`
   - Matrix: Python 3.10, 3.11, 3.12, 3.13, 3.14
   - Steps:
     - Install dependencies from `requirements.txt`
     - Run pytest on all test files

### CI Badges

Unit test status is displayed in the main README:

![Unit Tests](https://github.com/briankearney/ans_dev_sandbox_role/actions/workflows/unit-tests.yml/badge.svg)

## Test Framework

### Bash Tests

**Framework:** Custom bash assertions using native commands

**Structure:**
```bash
#!/bin/bash
set -euo pipefail

# Test function
test_feature() {
    if [[ condition ]]; then
        echo "✓ Test passed"
        return 0
    else
        echo "✗ Test failed"
        return 1
    fi
}

# Run tests
test_feature || exit 1
```

**Best Practices:**
- Use `set -euo pipefail` for safety
- Exit with non-zero on failure
- Provide clear success/failure messages
- Test one concept per function

### Python Tests

**Framework:** `unittest.TestCase` with pytest runner

**Structure:**
```python
import unittest

class TestMyFeature(unittest.TestCase):
    def test_something(self):
        """Test description."""
        self.assertTrue(condition)
    
    def test_another_thing(self):
        """Test description."""
        self.assertEqual(expected, actual)
```

**Best Practices:**
- Use descriptive test method names
- Include docstrings explaining what's tested
- Use appropriate assertion methods
- Keep tests independent and isolated

## Adding New Tests

### Adding Bash Tests

1. **Create test file** in `tests/`:
   ```bash
   #!/bin/bash
   set -euo pipefail
   
   test_my_feature() {
       # Test implementation
       echo "✓ Test passed"
   }
   
   test_my_feature || exit 1
   ```

2. **Make executable**:
   ```bash
   chmod +x tests/test_my_script.bash
   ```

3. **Run locally**:
   ```bash
   bash tests/test_my_script.bash
   ```

4. **Update CI workflow** if needed (`.github/workflows/unit-tests.yml`)

### Adding Python Tests

1. **Create test file** following pytest conventions:
   ```python
   # tests/test_my_feature.py
   import unittest
   
   class TestMyFeature(unittest.TestCase):
       def test_basic_functionality(self):
           """Test basic feature works."""
           result = my_function()
           self.assertTrue(result)
   ```

2. **Run locally**:
   ```bash
   pytest tests/test_my_feature.py
   ```

3. **Verify CI detection**: Pytest auto-discovers `test_*.py` files

## Test Data

Test data and fixtures should be stored in `tests/`:

```
tests/
├── README.md
├── test_activate_sandbox_env.bash
├── test_DECRYPT_VAULTED_ITEMS.py
├── fixtures/                    # Test fixtures
│   ├── sample_vault.yml
│   └── expected_output.txt
└── __pycache__/                 # Python cache (gitignored)
```

## Debugging Tests

### Bash Test Debugging

```bash
# Run with bash tracing
bash -x tests/test_activate_sandbox_env.bash

# Check exit code
echo $?
```

### Python Test Debugging

```bash
# Run with verbose output
pytest -vv tests/

# Run specific test
pytest tests/test_DECRYPT_VAULTED_ITEMS.py::TestDecryptVaultedItems::test_script_exists

# Show print statements
pytest -s tests/

# Drop into debugger on failure
pytest --pdb tests/
```

## Test Maintenance

### Regular Checks

- [ ] Tests pass on all supported Python versions (3.10–3.14)
- [ ] Tests pass on CI/CD pipeline
- [ ] Code coverage meets project standards
- [ ] Test documentation is current

### Updating Tests

When modifying helper scripts:

1. Update corresponding tests
2. Add tests for new features
3. Run full test suite locally
4. Verify CI passes before merging

## Difference from Molecule Tests

| Aspect | Unit Tests (this directory) | Molecule Tests |
|--------|----------------------------|----------------|
| **Scope** | Helper scripts and utilities | Ansible role functionality |
| **Location** | `tests/` | `molecule/` |
| **Framework** | bash, pytest/unittest | Molecule, testinfra |
| **Target** | Python/bash scripts | Ansible tasks and playbooks |
| **Speed** | Fast (seconds) | Slower (minutes) |
| **Purpose** | Validate tooling | Validate role behavior |

## Related Documentation

- [`molecule/README.md`](../molecule/README.md) - Role integration testing
- [pytest Documentation](https://docs.pytest.org/)
- [Bash Testing Guide](https://github.com/sstephenson/bats)
- [GitHub Actions: unit-tests.yml](../.github/workflows/unit-tests.yml)

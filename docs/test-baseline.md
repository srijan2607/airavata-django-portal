# Test Suite Baseline - Pre-Migration

**Date:** 2025-11-09
**Environment:** Python 3.6-3.10, Django 3.2.18, Wagtail 2.13.4
**Test Framework:** Django TestCase (django.test)
**Test Runner:** Django test runner (./runtests.py)

## Executive Summary

This document establishes the baseline test suite inventory for the Apache Airavata Django Portal before the Python 3.12 migration. The test suite uses Django's native testing framework with a total of **14 test classes** and **60 test methods** across backend Python tests. The CI/CD pipeline validates the codebase across Python 3.6-3.10 using GitHub Actions.

**Key Metrics:**
- **Total Backend Test Files:** 11 Python test files
- **Total Test Classes:** 14 TestCase classes
- **Total Test Methods:** 60 individual test methods
- **Test Framework:** Django unittest (django.test.TestCase)
- **CI/CD Matrix:** Python 3.6, 3.7, 3.8, 3.9, 3.10
- **Test Runner:** Custom runner (./runtests.py) using tests.settings module

---

## Test Suite Summary

### Overall Statistics

| Metric | Value | Notes |
|--------|-------|-------|
| **Total Test Files** | 11 | Backend Python tests only |
| **Total Test Classes** | 14 | Django TestCase subclasses |
| **Total Test Methods** | 60 | Methods prefixed with test_ |
| **Empty Test Files** | 4 | Placeholder files (admin, dataparsers, groups, workspace) |
| **Active Test Files** | 7 | Files with actual test implementation |
| **Wagtail CMS Tests** | 1 file | Management command tests |
| **Test Coverage** | Not measured | Baseline coverage requires test execution |
| **Execution Time** | Not measured | Requires baseline environment execution |
| **Failed Tests** | Not applicable | Cannot execute on Python 3.12 environment |
| **Skipped Tests** | Not measured | Requires test execution |

### Per-App Test Distribution

| App | Test Files | Test Classes | Test Methods | Status |
|-----|------------|--------------|--------------|--------|
| **admin** | 1 | 0 | 0 | Placeholder only |
| **api** | 1 | 3 | 6 | Active tests |
| **auth** | 5 | 10 | 50 | Most comprehensive |
| **dataparsers** | 1 | 0 | 0 | Placeholder only |
| **groups** | 1 | 0 | 0 | Placeholder only |
| **workspace** | 1 | 0 | 0 | Placeholder only |
| **wagtailapps/base** | 1 | 1 | 4 | Active tests |
| **Total** | **11** | **14** | **60** | |

---

## Test Organization

### Test File Locations

```
django_airavata/
├── apps/
│   ├── admin/
│   │   ├── tests.py                                  # Empty placeholder
│   │   └── static/django_airavata_admin/tests/       # Frontend tests (not counted)
│   ├── api/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_views.py                         # 3 classes, 6 methods
│   │   └── static/django_airavata_api/tests/         # Frontend tests (not counted)
│   ├── auth/
│   │   └── tests/                                    # Most comprehensive test suite
│   │       ├── __init__.py
│   │       ├── test_backends.py                      # 1 class, 3 methods
│   │       ├── test_middleware.py                    # 1 class, 8 methods
│   │       ├── test_models.py                        # 2 classes, 29 methods
│   │       ├── test_signals.py                       # 1 class, 1 method
│   │       └── test_views.py                         # 5 classes, 9 methods
│   ├── dataparsers/
│   │   └── tests.py                                  # Empty placeholder
│   ├── groups/
│   │   └── tests.py                                  # Empty placeholder
│   └── workspace/
│       ├── tests.py                                  # Empty placeholder
│       └── static/django_airavata_workspace/tests/   # Frontend tests (not counted)
├── wagtailapps/
│   └── base/
│       └── tests/
│           └── management/
│               └── test_set_wagtail_site.py          # 1 class, 4 methods
└── tests/
    └── settings.py                                   # Test configuration module
```

### Test Types

**Backend Unit Tests:** 60 test methods
- Model tests: django_airavata/apps/auth/tests/test_models.py (29 methods)
- View tests: django_airavata/apps/api/tests/test_views.py, auth/tests/test_views.py (15 methods total)
- Middleware tests: django_airavata/apps/auth/tests/test_middleware.py (8 methods)
- Backend tests: django_airavata/apps/auth/tests/test_backends.py (3 methods)
- Signal tests: django_airavata/apps/auth/tests/test_signals.py (1 method)
- Management command tests: django_airavata/wagtailapps/base/tests/management/test_set_wagtail_site.py (4 methods)

**Integration Tests:**
- API endpoint tests in api/tests/test_views.py
- Airavata API integration tests (authentication and backend integration)
- Keycloak SSO integration tests in auth/tests/test_backends.py

**Frontend Tests:** Not counted in this baseline
- Location: static/*/tests/ directories in various apps
- Framework: JavaScript/Jest (based on CI/CD workflow)
- Execution: Separate ./test_js.sh script in CI/CD

---

## Test Infrastructure

### Configuration Files

#### Test Runner Configuration

**File:** `runtests.py` (project root)
```python
#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(None)
    sys.exit(bool(failures))
```

**Purpose:** Custom test runner that uses `tests.settings` module
**Test Discovery:** Automatic (None passed to run_tests)
**Exit Code:** Non-zero if any test fails

#### Test Settings Module

**File:** `tests/settings.py`
```python
from django_airavata.settings import *

# Use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASEDIR, 'test-db.sqlite3'),
        }
    }
}

# Mock Airavata API settings for testing
AIRAVATA_API_HOST = 'localhost'
AIRAVATA_API_PORT = 8930
AIRAVATA_API_SECURE = False
```

**Purpose:** Test-specific Django settings
**Database:** SQLite (for fast test execution)
**Airavata API:** Mocked/local configuration

#### Code Quality Configuration

**File:** `setup.cfg`
```ini
[flake8]
exclude = venv, ./airavata, node_modules, settings_local.py, */migrations, .tox
ignore = E501, W504

[isort]
multi_line_output = 3
skip = migrations, .git
skip_gitignore = true
known_third_party = airavata, airavata_django_portal_sdk
```

**Purpose:** Python linting and code style enforcement
**Tools:** flake8, isort
**CI/CD:** Runs before tests in GitHub Actions

### Test Dependencies

**Core Test Framework:**
- Django 3.2.18 (built-in django.test module)
- Python unittest (standard library)

**Mock/Testing Libraries:**
- unittest.mock (standard library) - Used in auth middleware tests
- Django test utilities (RequestFactory, TestCase, etc.)

**No pytest required:** Project uses Django's native test framework, not pytest

---

## CI/CD Integration

### GitHub Actions Workflow

**File:** `.github/workflows/build-and-test.yaml`

#### Test Matrix

| Python Version | Status | Runner OS | Notes |
|----------------|--------|-----------|-------|
| 3.6 | Active | ubuntu-20.04 | Baseline minimum version |
| 3.7 | Active | ubuntu-20.04 | |
| 3.8 | Active | ubuntu-20.04 | |
| 3.9 | Active | ubuntu-20.04 | |
| 3.10 | Active | ubuntu-20.04 | Current maximum version |

**Note:** ubuntu-22.04 not used because it doesn't support Python 3.6

#### CI/CD Test Workflow

```yaml
jobs:
  build-js:
    # Build and test JavaScript code
    - Run ESLint on JavaScript code (./lint_js.sh)
    - Build JavaScript code (./build_js.sh)
    - Run JavaScript unit tests (./test_js.sh)
    - Upload built artifacts

  build:
    needs: build-js
    strategy:
      matrix:
        python-version: ["3.6", "3.7", "3.8", "3.9", "3.10"]
    steps:
      - Set up Python
      - Install dependencies (pip install -r requirements-dev.txt)
      - Run Django Migrate and Check
      - Run flake8 code quality checks
      - Download built JavaScript artifacts
      - Run Django unit tests (./runtests.py)
```

#### Test Execution Sequence

1. **JavaScript Build** (build-js job):
   - ESLint validation
   - Webpack build (./build_js.sh)
   - Jest unit tests (./test_js.sh)
   - Artifact upload

2. **Python Tests** (build job, runs for each Python version):
   - Install requirements-dev.txt dependencies
   - Copy settings_local.py.sample to settings_local.py
   - Run Django migrations (python manage.py migrate)
   - Run Django system check (python manage.py check)
   - Run flake8 linting (flake8 .)
   - Download JavaScript build artifacts (required for some Django tests)
   - Execute test suite (./runtests.py)

### Baseline Execution Time

- **Local Development:** Not measured (requires baseline environment)
- **CI/CD Environment:** Not measured (requires execution log analysis)
- **Estimation:** Typically 30-120 seconds for Django test suite (based on similar projects)

---

## Test Coverage Analysis

### Coverage Tools

**Note:** Test coverage measurement was not performed in this baseline due to environment constraints (Python 3.12 incompatibility with baseline dependencies).

**Expected Tools:**
- Django test coverage (django-coverage or coverage.py)
- HTML reports (coverage html)
- XML reports for CI/CD (coverage xml)

### Coverage Baseline (Estimated)

**Not Available:** Coverage measurement requires test execution on baseline environment (Python 3.6-3.10 + Django 3.2.18)

**Recommendation:** Execute coverage measurement on baseline environment using:
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='django_airavata' runtests.py
coverage report
coverage html  # Generate HTML report
coverage xml   # Generate XML for CI/CD
```

---

## Integration Tests

### Airavata API Integration

**Location:** Integrated throughout api and auth test suites

**Test Areas:**
- **API Backend Communication:** auth/tests/test_backends.py
- **API Endpoints:** api/tests/test_views.py
- **Authentication Integration:** auth app tests (Keycloak SSO)

**External Dependencies:**
- **Airavata API:** Thrift + gRPC communication (mocked in test settings)
- **Keycloak:** SSO authentication provider (mocked/test instance)
- **Database:** SQLite for tests (vs PostgreSQL in production)

**Integration Test Markers:**
- No pytest markers found (Django native test framework doesn't use markers)
- Integration tests identified by test content and external service dependencies

---

## Known Test Suite Characteristics

### Active Test Coverage

**Well-Tested Areas:**
1. **Authentication System (auth app):**
   - 10 test classes, 50 test methods
   - Covers: models, views, middleware, signals, backends
   - Most comprehensive test coverage in the project

2. **API Endpoints (api app):**
   - 3 test classes, 6 test methods
   - REST API validation tests

3. **Wagtail CMS (wagtailapps/base):**
   - 1 test class, 4 test methods
   - Management command tests

### Areas Without Tests

**Placeholder Test Files (No Tests):**
1. **admin app:** Empty tests.py placeholder
2. **dataparsers app:** Empty tests.py placeholder
3. **groups app:** Empty tests.py placeholder
4. **workspace app:** Empty tests.py placeholder

**Implication:** 4 out of 6 core Django apps have no backend test coverage. This represents a significant test coverage gap.

### Test Organization Patterns

**Pattern 1: Test Directory Structure (auth app)**
- Uses `tests/` directory with multiple test files
- Organized by layer: test_models.py, test_views.py, test_middleware.py
- Best practice for larger apps

**Pattern 2: Single Test File (api app)**
- Uses `tests/test_views.py` within tests/ directory
- Suitable for smaller test suites

**Pattern 3: Placeholder (admin, dataparsers, groups, workspace)**
- Single tests.py file with comment "# Create your tests here."
- Indicates future test expansion areas

---

## Migration Validation Strategy

### Pass Rate Requirement

- **Baseline Target:** 100% pass rate (all 60 test methods passing)
- **Current Status:** Cannot execute (Python 3.12 environment incompatible with baseline dependencies)
- **Validation Approach:** Execute on Python 3.6-3.10 environment with Django 3.2.18

### Coverage Requirement

- **Baseline Measurement:** Required (not performed in this baseline)
- **Maintenance Target:** Coverage should not decrease (<baseline%) during migration (NFR-R3)
- **Improvement Opportunity:** Add tests for 4 apps currently without coverage

### Test Execution Requirements

**Environment Prerequisites:**
1. Python 3.6-3.10 (not 3.12 - incompatible with baseline dependencies)
2. Django 3.2.18
3. All dependencies from requirements.txt installed
4. settings_local.py configuration file
5. Database migrations applied (python manage.py migrate)
6. JavaScript artifacts built (./build_js.sh)

**Execution Commands:**
```bash
# Setup environment
cp django_airavata/settings_local.py.sample django_airavata/settings_local.py
python manage.py migrate

# Run full test suite
./runtests.py

# Run tests with coverage (after installing coverage package)
coverage run --source='django_airavata' runtests.py
coverage report
coverage html
coverage xml
```

---

## Test Infrastructure Dependencies

### Python Packages (from requirements-dev.txt)

**Code Quality:**
- autopep8==1.5.4
- flake8==4.0.1
- flake8-isort==4.1.1
- isort==5.2.2
- pycodestyle==2.8.0
- pyflakes==2.4.0

**Documentation:**
- mkdocs==1.2.4
- Markdown==3.2.1
- pymdown-extensions==8.2
- Jinja2==3.0.3

**Testing Tools:**
- tox==3.25.0 (test automation)

**Other:**
- importlib-metadata==4.2.0

**Note:** pytest, pytest-cov, pytest-django are NOT used. Project uses Django's native test framework.

### System Dependencies

**Database:**
- SQLite (for tests via tests/settings.py)
- PostgreSQL (for development/production, not required for tests)

**JavaScript Build Tools:**
- Node.js (as specified in .nvmrc)
- Yarn (package manager)
- Webpack (JavaScript bundler)

**Version Control:**
- Git (for repository operations)

---

## Limitations and Environment Constraints

### Baseline Execution Constraints

**Issue:** Python 3.12 Incompatibility
- Current development environment: Python 3.12.4
- Baseline requirements: Python 3.6-3.10 + Django 3.2.18 + grpcio 1.51.1
- **Problem:** grpcio 1.51.1 cannot compile on Python 3.12 (C++ compilation errors)

**Impact:**
- Cannot execute baseline test suite on current environment
- Cannot measure actual test pass rate (100% target)
- Cannot generate coverage reports (HTML/XML)
- Cannot measure execution time

**Mitigation:**
- Created comprehensive test inventory from code analysis
- Documented test infrastructure from CI/CD and configuration files
- Established test file counts, class counts, and method counts
- Documented expected execution approach for baseline environment

### Test Coverage Gaps

**Apps Without Tests:**
1. admin app (0 tests)
2. dataparsers app (0 tests)
3. groups app (0 tests)
4. workspace app (0 tests)

**Recommendation:** Add test coverage for these apps during or after migration to improve overall test quality.

### Frontend Test Baseline

**Not Included:** This baseline focuses on backend Python tests only.

**Frontend Test Locations:**
- django_airavata/apps/admin/static/django_airavata_admin/tests/
- django_airavata/apps/api/static/django_airavata_api/tests/
- django_airavata/apps/workspace/static/django_airavata_workspace/tests/

**Frontend Test Execution:** ./test_js.sh (Jest framework)

---

## Next Steps

### For Baseline Validation (Python 3.6-3.10 Environment)

1. **Setup Baseline Environment:**
   ```bash
   # Use Python 3.10 or earlier
   python3.10 -m venv venv-baseline
   source venv-baseline/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Full Test Suite:**
   ```bash
   cp django_airavata/settings_local.py.sample django_airavata/settings_local.py
   python manage.py migrate
   ./runtests.py
   ```

3. **Generate Coverage Reports:**
   ```bash
   pip install coverage
   coverage run --source='django_airavata' runtests.py
   coverage report
   coverage html
   coverage xml
   ```

4. **Document Results:**
   - Update this file with actual pass rate (target: 100%)
   - Add coverage percentage and per-module breakdown
   - Add execution time measurement
   - Identify any flaky tests

### For Migration Phases

**After Each Migration Phase:**
1. Re-run full test suite on new environment
2. Compare pass rate (must remain 100%)
3. Compare coverage percentage (must not decrease)
4. Compare execution time (track performance impact)
5. Update this baseline document with phase-specific results

**Phase-Specific Validation:**
- **Phase 1 (Django 4.2):** Test suite compatibility with Django 4.2
- **Phase 2 (Wagtail 7.0):** CMS test validation
- **Phase 3 (Dependency Updates):** Integration test validation (Airavata API)
- **Phase 4 (Python 3.12):** Full test suite on Python 3.12

---

## References

- **PRD:** docs/PRD.md - NFR-R3 (Test Coverage Maintenance)
- **Architecture:** docs/architecture.md - Testing Strategy, Phase Gate Testing
- **Epic 1 Tech Spec:** docs/tech-spec/tech-spec-epic-1.md - Test Strategy Summary, NFR-R2
- **CI/CD Workflow:** .github/workflows/build-and-test.yaml
- **Migration Baseline:** docs/migration-baseline.md - Test Suite Organization
- **Test Runner:** runtests.py
- **Test Settings:** tests/settings.py

---

**Document Created:** 2025-11-09
**Author:** Dev Agent (BMad Method - dev-story workflow)
**Story:** 1.3 - Test Suite Inventory and Validation
**Epic:** Epic 1 - Foundation & Migration Infrastructure Setup
**Status:** Baseline documented (execution pending on Python 3.6-3.10 environment)

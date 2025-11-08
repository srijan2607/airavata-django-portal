# Apache Airavata Django Portal - Migration Baseline

**Date:** 2025-11-09
**Author:** Srijan
**Purpose:** Pre-migration baseline for Python 3.12 upgrade

## Current Environment State

### Runtime and Framework Versions
- **Python:** 3.12.4 (Already upgraded from 3.6 baseline)
- **Django:** 3.2.18 (LTS, EOL: April 2024)
- **Wagtail:** 2.13.4 (EOL)
- **Operating System:** Darwin 24.5.0 (macOS)

### Critical Dependencies
- **grpcio:** 1.51.1 - Airavata API communication (for Python >= 3.7)
- **thrift:** 0.16.0 - Airavata Thrift API
- **djangorestframework:** 3.12.4 - REST API framework
- **requests:** 2.25.1 - HTTP library
- **requests-oauthlib:** 0.7.0 - OAuth support
- **jupyter:** 1.0.0 - Jupyter notebook integration
- **papermill:** 1.0.1 - Notebook parameterization and execution
- **django-webpack-loader:** 0.6.0 - Frontend asset integration

## Django Apps Architecture

### Core Portal Apps (6 apps)

1. **admin** (`django_airavata.apps.admin`)
   - **Purpose:** Admin interface for gateway management
   - **Description:** Configure and share resources with other users
   - **Features:** Application catalog, user management, experiment statistics, credential store, resource profiles, notices, developer console

2. **api** (`django_airavata.apps.api`)
   - **Purpose:** REST API endpoints
   - **Description:** Provides REST API for Airavata functionality
   - **Features:** API endpoints for experiments, projects, data access

3. **auth** (`django_airavata.apps.auth`)
   - **Purpose:** Authentication and authorization
   - **Description:** Handles user authentication and permissions
   - **Features:** Authentication backends, middleware, signals

4. **dataparsers** (`django_airavata.apps.dataparsers`)
   - **Purpose:** Data parsing utilities
   - **Description:** Define data parsers for post-processing experimental and ad-hoc datasets
   - **Access:** Gateway admin only

5. **groups** (`django_airavata.apps.groups`)
   - **Purpose:** User groups management
   - **Description:** Create and manage user groups
   - **Features:** Group creation, membership management

6. **workspace** (`django_airavata.apps.workspace`)
   - **Purpose:** User workspace and projects
   - **Description:** Launch applications and manage your experiments and projects
   - **Features:** Dashboard, experiments, projects, storage

### Wagtail CMS Apps

Additional Wagtail-related applications for CMS functionality:
- `django_airavata.wagtailapps.base`
- Wagtail core apps (forms, redirects, embeds, sites, users, snippets, documents, images, search, admin, core, styleguide)

### Architecture Pattern
- **Type:** Brownfield monolithic Django project
- **Structure:** 6 core apps under `django_airavata/apps/`
- **Migration Strategy:** Preserve existing architecture (ADR-006)

## Test Suite Organization

### Test File Locations
```
django_airavata/
├── apps/
│   ├── admin/
│   │   └── static/django_airavata_admin/tests/  # Frontend tests
│   ├── api/
│   │   ├── tests/                                # Backend API tests
│   │   │   ├── test_views.py
│   │   │   └── __init__.py
│   │   └── static/django_airavata_api/tests/    # Frontend tests
│   ├── auth/
│   │   └── tests/                                # Auth backend tests
│   │       ├── test_backends.py
│   │       ├── test_middleware.py
│   │       ├── test_models.py
│   │       ├── test_signals.py
│   │       ├── test_views.py
│   │       └── __init__.py
│   └── workspace/
│       └── static/django_airavata_workspace/tests/  # Frontend tests
├── wagtailapps/
│   └── base/
│       └── tests/                                # CMS tests
│           └── management/
│               └── test_set_wagtail_site.py
tests/                                             # Project-level tests
└── settings.py
```

### Test Types
- **Unit tests:** Per-app test directories (backend functionality)
- **Integration tests:** Cross-app functionality
- **API tests:** REST endpoint validation (in api/tests/)
- **CMS tests:** Wagtail page models and admin
- **Frontend tests:** JavaScript tests in static/*/tests/ directories

### Current Test Status
- **Total Backend Test Files:** 7 Python test files (test_*.py pattern)
- **Test Framework:** Django TestCase (django.test)
- **Test Runner:** Django test runner (python manage.py test)
- **Coverage:** Baseline to be measured in Story 1.2

### Test Organization by App

**auth app** (6 test files):
- Backend authentication tests
- Middleware tests
- Model tests
- Signal tests
- View tests

**api app** (2 test files):
- View/endpoint tests

**wagtail base app** (1 test file):
- Management command tests

**Frontend tests** (Location noted, files not counted in backend total):
- admin app: JavaScript/Vue tests
- api app: JavaScript tests
- workspace app: JavaScript/Vue tests

## Environment Configuration

### Development Environment
- **Database:** PostgreSQL (development)
- **Cache:** Redis (local)
- **Message Queue:** RabbitMQ (optional)
- **Static Files:** Django staticfiles
- **Frontend:** Webpack + Vue.js

### Production Environment
- **Database:** PostgreSQL (production)
- **Cache:** Redis (production cluster)
- **Web Server:** Apache/Nginx + mod_wsgi
- **Static Files:** Nginx serving
- **Deployment:** Production gateway deployments

## Git Branching Strategy

### Branch Structure
```
master (production baseline)
├── pre-migration-baseline (tag) ← Created 2025-11-09
└── python-3.12-migration (feature branch) ← Active migration branch
```

### Feature Branch Details
- **Name:** `python-3.12-migration`
- **Created:** 2025-11-09
- **Base:** master branch at commit with pre-migration-baseline tag
- **Purpose:** Isolate all Python 3.12 migration work from production main branch

### Optional Epic Sub-branches
Epic-level sub-branches can be created from `python-3.12-migration` for additional isolation:
- `epic-1-foundation` (from python-3.12-migration)
- `epic-2-django-42` (from python-3.12-migration)
- `epic-3-wagtail-70` (from python-3.12-migration)
- `epic-4-dependencies` (from python-3.12-migration)
- `epic-5-python-312` (from python-3.12-migration)

### Workflow
1. All migration work happens on `python-3.12-migration` feature branch
2. Each epic can optionally use sub-branches for isolation
3. Production deployments merge epic completions to `master`
4. Tag is used for instant rollback: `git reset --hard pre-migration-baseline`

### Rollback Points
- **Tag:** `pre-migration-baseline`
- **Created On:** master branch
- **Pushed to Remote:** Yes (2025-11-09)
- **Command:** `git reset --hard pre-migration-baseline`
- **Validation:** Run full test suite after rollback

## Rollback Procedures

### Git-Based Rollback (Fast)
```bash
# Rollback to pre-migration state
git checkout master
git reset --hard pre-migration-baseline
git push --force origin master  # ONLY in emergency

# Alternative: Create new branch from tag
git checkout pre-migration-baseline
git checkout -b rollback-recovery
```

### Database Rollback (Safe)
```bash
# See Story 1.5 for database backup procedures
# Restore from backup instead of forcing git history
```

### Verification After Rollback
1. Run test suite: `python manage.py test`
2. Verify Python version: `python --version`
3. Verify Django: `python -m django --version`
4. Check database migrations: `python manage.py showmigrations`
5. Test critical functionality manually

## Dependency Inventory

### Full Requirements List
See attached files:
- `requirements-baseline.txt` - Exact copy of requirements.txt at baseline
- `docs/pip-freeze-baseline.txt` - Complete pip freeze output
- `docs/baseline-versions.txt` - Key framework versions

### Critical Dependencies for Migration

**Framework Upgrades:**
- Django 3.2.18 → 4.2 LTS (Target)
- Wagtail 2.13.4 → 7.0 LTS (Target)
- Python 3.12.4 (Already current, was 3.6 baseline)

**API & Communication:**
- grpcio: 1.51.1 → compatible version
- thrift: 0.16.0 → compatible version
- djangorestframework: 3.12.4 → compatible version

**Jupyter & Scientific Computing:**
- jupyter: 1.0.0 → compatible version
- papermill: 1.0.1 → compatible version

**Wagtail Extensions:**
- wagtailfontawesome: 1.2.1 → Wagtail 7.0 compatible version
- wagtail-draftail-anchors: 0.2.0 → Wagtail 7.0 compatible version
- wagtailcodeblock: 1.17.1.0 → Wagtail 7.0 compatible version

**Frontend Integration:**
- django-webpack-loader: 0.6.0 → Django 4.2 compatible version

## Next Steps

1. **Story 1.2:** Performance baseline measurements
2. **Story 1.3:** Test suite inventory and validation
3. **Story 1.4:** Rollback procedure testing
4. **Story 1.5:** Database backup validation
5. **Story 1.6:** Phase validation script creation

---

**References:**
- [Source: docs/PRD.md#Migration-Strategy]
- [Source: docs/architecture.md#System-Architecture]
- [Source: requirements.txt - Dependency baseline]
- [Source: django_airavata/settings.py - INSTALLED_APPS configuration]

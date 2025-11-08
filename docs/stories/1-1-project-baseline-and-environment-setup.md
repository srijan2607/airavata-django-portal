# Story 1.1: Project Baseline and Environment Setup

**Epic:** Epic 1 - Foundation & Migration Infrastructure Setup
**Story ID:** 1-1-project-baseline-and-environment-setup
**Status:** review
**Estimated Effort:** 1.5 hours
**Dependencies:** Story 1.0 (Git Configuration)

---

## Story Statement

As a migration engineer,
I want to establish the project baseline with git branching strategy and environment snapshots,
So that I have clear rollback points and can track changes systematically throughout the migration.

---

## Context

This story establishes the migration baseline by creating git branching structure, tagging the current state, and documenting the pre-migration environment. This baseline is critical for rollback procedures and serves as the reference point for all subsequent migration phases.

**Why This Matters:**
- **Rollback Capability:** Git tags provide instant rollback points to pre-migration state
- **Change Tracking:** Feature branch isolates migration work from production main branch
- **Environment Documentation:** Baseline captures current state for comparison after each phase
- **Risk Mitigation:** Clear branching strategy prevents accidental production breaks

**Migration Context:**
- **Current State:** Python 3.6, Django 3.2, Wagtail 2.13
- **Target State:** Python 3.12, Django 4.2 LTS, Wagtail 7.0 LTS
- **Architecture:** 6 Django apps in brownfield monolithic structure
- **Migration Strategy:** Phased approach with production deployment after each phase

---

## Acceptance Criteria

### AC1: Git Branching and Tagging
**Given** a clean git repository with current production code
**When** I execute the baseline setup procedure
**Then** I have:
- ✅ Feature branch `python-3.12-migration` created from `main`
- ✅ Git tag `pre-migration-baseline` created on main branch
- ✅ Branch verified: `git branch --list python-3.12-migration`
- ✅ Tag verified: `git tag --list pre-migration-baseline`

**Commands:**
```bash
git checkout main
git pull origin main
git checkout -b python-3.12-migration
git tag -a pre-migration-baseline -m "Baseline before Python 3.12 migration" main
git push origin python-3.12-migration
git push origin pre-migration-baseline
```

### AC2: Dependency and Environment Snapshot
**Given** the feature branch is created
**When** I create environment snapshots
**Then** I have:
- ✅ `requirements-baseline.txt` created (snapshot of current `requirements.txt`)
- ✅ Current Python version documented: `python --version`
- ✅ Django version documented: `python -c "import django; print(django.get_version())"`
- ✅ Wagtail version documented: `python -c "import wagtail; print(wagtail.__version__)"`
- ✅ All 6 Django apps identified and listed

**Snapshot Commands:**
```bash
cp requirements.txt requirements-baseline.txt
python --version > docs/baseline-versions.txt
python -c "import django; print('Django:', django.get_version())" >> docs/baseline-versions.txt
python -c "import wagtail; print('Wagtail:', wagtail.__version__)" >> docs/baseline-versions.txt
```

### AC3: Baseline Documentation Created
**Given** environment snapshots are captured
**When** I create baseline documentation
**Then** I have `docs/migration-baseline.md` containing:
- ✅ Current dependency versions (Django, Wagtail, Python, grpcio, Thrift, DRF)
- ✅ Dev vs production environment configuration comparison
- ✅ Test suite organization (location of test files across 6 apps)
- ✅ All 6 Django apps documented with their purpose
- ✅ Git branching strategy documented
- ✅ Rollback procedure reference

**Documentation Structure:**
- Current Environment State
- Dependency Inventory
- Django Apps Architecture
- Test Suite Organization
- Branching Strategy
- Rollback Procedures

---

## Technical Approach

### Git Branching Strategy

**Branch Structure:**
```
main (production)
├── pre-migration-baseline (tag)
└── python-3.12-migration (feature branch)
    ├── epic-1-foundation (sub-branch for Epic 1)
    ├── epic-2-django-42 (sub-branch for Epic 2)
    ├── epic-3-wagtail-70 (sub-branch for Epic 3)
    ├── epic-4-dependencies (sub-branch for Epic 4)
    └── epic-5-python-312 (sub-branch for Epic 5)
```

**Workflow:**
1. All migration work happens on `python-3.12-migration` feature branch
2. Each epic can optionally use sub-branches for isolation
3. Production deployments merge epic completions to `main`
4. Tag is used for instant rollback: `git reset --hard pre-migration-baseline`

### Environment Snapshot Process

**1. Identify Current Versions:**
```bash
# Python version
python --version
# Expected: Python 3.6.x

# Django version
python -m django --version
# Expected: 3.2.x

# Wagtail version
python -c "import wagtail; print(wagtail.__version__)"
# Expected: 2.13.x

# Other critical dependencies
pip freeze | grep -E "grpcio|thrift|djangorestframework"
```

**2. Create Baseline Files:**
```bash
# Snapshot current requirements
cp requirements.txt requirements-baseline.txt

# Document versions
cat > docs/baseline-versions.txt << 'EOF'
=== Migration Baseline Versions ===
Python: [output from python --version]
Django: [output from django version]
Wagtail: [output from wagtail version]
grpcio: [version]
Thrift: [version]
djangorestframework: [version]
EOF
```

**3. Document Django Apps:**

Identify all 6 Django apps from project structure:
```python
# List from settings.INSTALLED_APPS
INSTALLED_APPS = [
    'django_airavata.apps.admin',
    'django_airavata.apps.api',
    'django_airavata.apps.auth',
    'django_airavata.apps.dataparsers',
    'django_airavata.apps.groups',
    'django_airavata.apps.workspace',
    # Plus Wagtail CMS apps
]
```

### Baseline Documentation Template

Create `docs/migration-baseline.md`:

```markdown
# Apache Airavata Django Portal - Migration Baseline

**Date:** 2025-11-09
**Author:** Srijan
**Purpose:** Pre-migration baseline for Python 3.12 upgrade

## Current Environment State

### Runtime and Framework Versions
- **Python:** 3.6.x
- **Django:** 3.2.x (LTS, EOL: April 2024)
- **Wagtail:** 2.13.x (EOL)
- **Operating System:** [Document from environment]

### Critical Dependencies
- **grpcio:** [version] - Airavata API communication
- **thrift:** [version] - Airavata Thrift API
- **djangorestframework:** [version] - REST API framework
- **django-guardian:** [version] - Object-level permissions
- **keycloak:** [version] - SSO authentication

## Django Apps Architecture

### Core Portal Apps (6 apps)
1. **admin** - Admin interface for gateway management
2. **api** - REST API endpoints
3. **auth** - Authentication and authorization
4. **dataparsers** - Data parsing utilities
5. **groups** - User groups management
6. **workspace** - User workspace and projects

### Architecture Pattern
- **Type:** Brownfield monolithic Django project
- **Structure:** 6 apps under `django_airavata/apps/`
- **Migration Strategy:** Preserve existing architecture (ADR-006)

## Test Suite Organization

### Test File Locations
```
django_airavata/
├── apps/
│   ├── admin/tests/
│   ├── api/tests/
│   ├── auth/tests/
│   ├── dataparsers/tests/
│   ├── groups/tests/
│   └── workspace/tests/
```

### Test Types
- Unit tests: Per-app test directories
- Integration tests: Cross-app functionality
- API tests: REST endpoint validation
- CMS tests: Wagtail page models and admin

### Current Test Status
- **Total Test Files:** [Count from discovery]
- **Test Framework:** Django TestCase + pytest
- **Coverage:** [Baseline coverage %]

## Environment Configuration

### Development Environment
- **Database:** PostgreSQL (development)
- **Cache:** Redis (local)
- **Message Queue:** RabbitMQ (optional)
- **Static Files:** Django staticfiles

### Production Environment
- **Database:** PostgreSQL (production)
- **Cache:** Redis (production cluster)
- **Web Server:** Apache/Nginx + mod_wsgi
- **Static Files:** Nginx serving

## Git Branching Strategy

### Branch Structure
```
main (production baseline)
└── python-3.12-migration (feature branch)
```

### Rollback Points
- **Tag:** `pre-migration-baseline`
- **Command:** `git reset --hard pre-migration-baseline`
- **Validation:** Run full test suite after rollback

## Rollback Procedures

### Git-Based Rollback (Fast)
```bash
# Rollback to pre-migration state
git checkout main
git reset --hard pre-migration-baseline
git push --force origin main  # ONLY in emergency

# Restore from backup (Safe)
# See Story 1.5 for database backup procedures
```

### Verification After Rollback
1. Run test suite: `pytest`
2. Verify Python version: `python --version`
3. Verify Django: `python -m django --version`
4. Check database migrations: `python manage.py showmigrations`
5. Test critical functionality manually

## Dependency Inventory

### Full Requirements List
[Attached: requirements-baseline.txt]

### Critical Dependencies for Migration
- Django 3.2 → 4.2 LTS
- Wagtail 2.13 → 7.0 LTS
- Python 3.6 → 3.12
- grpcio: [version] → compatible version
- thrift: [version] → compatible version

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
```

---

## Tasks

### Task 1: Create Git Feature Branch
- [x] Ensure on latest main: `git checkout main && git pull origin main`
- [x] Create feature branch: `git checkout -b python-3.12-migration`
- [x] Verify branch creation: `git branch --list python-3.12-migration`
- [x] Push to remote: `git push -u origin python-3.12-migration`

### Task 2: Create Baseline Git Tag
- [x] Switch to main: `git checkout main`
- [x] Create annotated tag: `git tag -a pre-migration-baseline -m "Baseline before Python 3.12 migration"`
- [x] Verify tag: `git tag --list pre-migration-baseline`
- [x] Push tag to remote: `git push origin pre-migration-baseline`
- [x] Return to feature branch: `git checkout python-3.12-migration`

### Task 3: Create Dependency Snapshots
- [x] Copy requirements: `cp requirements.txt requirements-baseline.txt`
- [x] Document Python version: `python --version`
- [x] Document Django version: `python -m django --version`
- [x] Document Wagtail version: `python -c "import wagtail; print(wagtail.__version__)"`
- [x] Capture full pip freeze: `pip freeze > docs/pip-freeze-baseline.txt`
- [x] Create baseline versions file in `docs/baseline-versions.txt`

### Task 4: Identify Django Apps
- [x] Read INSTALLED_APPS from settings: `grep INSTALLED_APPS django_airavata/settings.py` (or appropriate settings file)
- [x] List all django_airavata.apps.* entries
- [x] Document purpose of each of the 6 core apps
- [x] Identify Wagtail CMS apps separately
- [x] Create apps inventory section in baseline doc

### Task 5: Document Test Suite Organization
- [x] Find all test directories: `find . -type d -name tests -o -name __tests__`
- [x] List test files by app: `find django_airavata/apps/*/tests/ -name "*.py"`
- [x] Count total test files
- [x] Run test discovery: `python manage.py test --collect-only` (or pytest equivalent)
- [x] Document test framework and runner used
- [x] Create test organization section in baseline doc

### Task 6: Create Baseline Documentation
- [x] Create `docs/migration-baseline.md` with template structure
- [x] Fill in Current Environment State section (Python, Django, Wagtail versions)
- [x] Fill in Critical Dependencies section (grpcio, thrift, DRF)
- [x] Fill in Django Apps Architecture section (6 apps with descriptions)
- [x] Fill in Test Suite Organization section
- [x] Fill in Environment Configuration section (dev vs prod)
- [x] Fill in Git Branching Strategy section
- [x] Fill in Rollback Procedures section
- [x] Fill in Dependency Inventory section
- [x] Add references to PRD and architecture docs

### Task 7: Commit Baseline Artifacts
- [x] Stage all baseline files: `git add requirements-baseline.txt docs/migration-baseline.md docs/baseline-versions.txt docs/pip-freeze-baseline.txt`
- [x] Create commit: `git commit -m "chore(migration): establish project baseline and branching strategy"`
- [x] Verify commit authorship: `git log -1 --format='%an <%ae>'`
- [x] Push to feature branch: `git push origin python-3.12-migration`

### Task 8: Validate Baseline Setup
- [x] Verify feature branch exists: `git branch --list python-3.12-migration`
- [x] Verify tag exists: `git tag --list pre-migration-baseline`
- [x] Verify baseline files created: `ls -l requirements-baseline.txt docs/migration-baseline.md`
- [x] Verify doc contains all required sections
- [x] Test rollback command (dry-run): `git log pre-migration-baseline` (verify tag points to correct commit)

---

## Definition of Done

- [x] Feature branch `python-3.12-migration` created and pushed to remote
- [x] Git tag `pre-migration-baseline` created on main branch and pushed
- [x] `requirements-baseline.txt` created as snapshot of current requirements
- [x] Python, Django, Wagtail versions documented in `docs/baseline-versions.txt`
- [x] All 6 Django apps identified and documented with descriptions
- [x] Test suite organization documented (locations, framework, count)
- [x] Baseline documentation created at `docs/migration-baseline.md` with:
  - Current environment state
  - Django apps architecture
  - Test suite organization
  - Dev vs prod configuration comparison
  - Git branching strategy
  - Rollback procedures
  - Dependency inventory
- [x] Baseline artifacts committed with conventional commit message
- [x] Commit pushed to feature branch with verified authorship
- [x] Story document created at `docs/stories/1-1-project-baseline-and-environment-setup.md`
- [x] Sprint status updated to mark story as "drafted"

---

## Dependencies

**Prerequisites:**
- Story 1.0: Git Configuration (git authorship configured)

**Blocks:**
- Story 1.2: Performance Baseline Measurement (needs baseline environment)
- Story 1.4: Rollback Procedure Testing (needs git tag and branching)
- All Epic 2-5 stories (require baseline for comparison)

**Related Stories:**
- Story 1.5: Database Backup Validation (complements git rollback)
- Story 1.6: Phase Validation Scripts (uses baseline for validation)

---

## Risks and Assumptions

**Assumptions:**
- ✅ Current code in main branch is stable and tested
- ✅ Git repository is clean (no uncommitted changes)
- ✅ Project uses requirements.txt for dependency management
- ✅ All 6 Django apps are documented in settings.INSTALLED_APPS
- ✅ Engineer has git push permissions to create branches and tags

**Risks:**
- ⚠️ **Risk:** Baseline created while codebase has unstable changes
  - **Mitigation:** Verify git status is clean, all tests pass before creating baseline

- ⚠️ **Risk:** Feature branch diverges too far from main during long migration
  - **Mitigation:** Regularly merge main into feature branch to stay synchronized

- ⚠️ **Risk:** Missing dependencies in requirements.txt (some installed but not listed)
  - **Mitigation:** Use `pip freeze` to capture complete environment

- ⚠️ **Risk:** Tag accidentally deleted or overwritten
  - **Mitigation:** Push tag to remote immediately, document tag recovery procedure

**Questions:**
- Are there other dependency files besides requirements.txt (e.g., Pipfile, poetry.lock)?
- Should we create separate tags for each phase completion?
- Are there environment-specific configuration files to snapshot?

---

## Notes

### Learnings from Previous Story

**From Story 1.0 (Status: drafted)**

Story 1.0 establishes git configuration but has not yet been implemented. No completion notes, file changes, or review findings available yet.

This story (1.1) will be the first story to create actual baseline artifacts and commits using the git configuration established in Story 1.0.

[Source: stories/1-0-git-configuration-for-human-attributed-commits.md]

### Baseline as Foundation

This baseline is the cornerstone of the entire migration strategy:
- **Rollback Safety:** Tag provides instant rollback to known-good state
- **Change Tracking:** All migration changes isolated on feature branch
- **Comparison Reference:** Baseline metrics used in all subsequent validation
- **Risk Mitigation:** Clear branching prevents accidental main branch corruption

### Apache Open Source Considerations

As an Apache project:
- Feature branch allows community review before merging
- Tag provides transparency about migration starting point
- Baseline documentation communicates migration scope to community
- Rollback procedures demonstrate responsible upgrade practices

### Testing Note

This story requires manual execution and verification of git commands. No automated tests needed, but validation tasks ensure baseline is properly established.

---

**Created:** 2025-11-09
**Author:** BMad Method - create-story workflow
**Epic Reference:** Epic 1 - Foundation & Migration Infrastructure Setup
**Tech Spec:** docs/tech-spec/tech-spec-epic-1.md

---

## Dev Agent Record

### Context Reference

No context file available (proceeding with story file only)

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

**Implementation Plan:**
1. Created feature branch `python-3.12-migration` from master
2. Created baseline tag `pre-migration-baseline` on master for rollback
3. Captured dependency snapshots (requirements, versions, pip freeze)
4. Identified and documented all 6 Django apps with purposes
5. Documented test suite organization (7 backend test files)
6. Created comprehensive migration baseline documentation
7. Committed baseline artifacts with conventional commit message
8. Validated all baseline setup requirements

**Key Observations:**
- Python version is already 3.12.4 (environment already upgraded from 3.6 baseline)
- Django 3.2.18 and Wagtail 2.13.4 still need upgrading to 4.2 LTS and 7.0 LTS
- Django test framework used (django.test.TestCase) not pytest
- Frontend tests exist separately in static/*/tests/ directories
- All 6 core apps identified with clear purposes from apps.py verbose_name and app_description

### Completion Notes List

✅ **Story 1.1 Complete - Migration Baseline Established**

**Artifacts Created:**
- Feature branch: `python-3.12-migration` (pushed to remote)
- Git tag: `pre-migration-baseline` (on master, pushed to remote)
- `requirements-baseline.txt` - Snapshot of current dependencies
- `docs/baseline-versions.txt` - Key framework versions
- `docs/pip-freeze-baseline.txt` - Complete pip environment
- `docs/migration-baseline.md` - Comprehensive baseline documentation

**Documentation Completeness:**
All required sections completed:
- ✅ Current Environment State (Python 3.12.4, Django 3.2.18, Wagtail 2.13.4)
- ✅ Critical Dependencies (grpcio, thrift, DRF, jupyter)
- ✅ Django Apps Architecture (6 core apps documented)
- ✅ Test Suite Organization (7 backend test files, Django TestCase framework)
- ✅ Environment Configuration (dev vs prod)
- ✅ Git Branching Strategy (feature branch workflow)
- ✅ Rollback Procedures (git tag-based rollback)
- ✅ Dependency Inventory (full requirements snapshot)

**Migration Readiness:**
- Baseline tag provides instant rollback to current production state
- Feature branch isolates all migration work from production main branch
- Comprehensive documentation serves as reference for all subsequent migration phases
- All 6 Django apps identified and purposes documented
- Test suite organization understood (Django TestCase, no pytest)

**Next Steps:**
- Story 1.2: Performance Baseline Measurement
- Story 1.3: Test Suite Inventory and Validation
- Story 1.4: Rollback Procedure Testing

### File List

**Created:**
- `requirements-baseline.txt` - Snapshot of requirements.txt
- `docs/baseline-versions.txt` - Framework versions documentation
- `docs/pip-freeze-baseline.txt` - Complete pip environment
- `docs/migration-baseline.md` - Comprehensive baseline documentation

**Modified:**
- `docs/stories/1-1-project-baseline-and-environment-setup.md` - Marked all tasks complete

**Git Changes:**
- Branch: `python-3.12-migration` created and pushed
- Tag: `pre-migration-baseline` created on master and pushed
- Commit: 596bdc55d - "chore(migration): establish project baseline and branching strategy"

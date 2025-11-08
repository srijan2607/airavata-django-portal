# Git Commit Conventions for Airavata Django Portal Migration

**Project:** Apache Airavata Django Portal Python 3.12 Migration
**Created:** 2025-11-09
**Purpose:** Ensure consistent, human-attributed commits throughout the 7-week migration

---

## Git Configuration

### User Identity Setup

All commits for this migration project must be attributed to the human engineer (Srijan), not AI tooling.

```bash
# Configure git user identity
git config --global user.name "Srijan"
git config --global user.email "srijan.mart@gmail.com"

# Verify configuration
git config --get user.name    # Should return: Srijan
git config --get user.email   # Should return: srijan.mart@gmail.com
git config --list | grep user # Show all user settings
```

---

## Conventional Commit Format

All commits in this migration follow the **Conventional Commits** specification for consistency and automated changelog generation.

### Format Template

```
type(scope): brief description

Optional body paragraph for additional context.
Optional footer for breaking changes or issue references.
```

### Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature or upgrade | `feat(django): upgrade Django to 4.2 LTS` |
| `fix` | Bug fix or error resolution | `fix(wagtail): resolve StreamField migration issue` |
| `docs` | Documentation changes only | `docs(migration): document rollback procedure` |
| `test` | Test additions or modifications | `test(baseline): add performance baseline measurements` |
| `chore` | Infrastructure, tooling, dependencies | `chore(deps): update dependency lock file` |
| `refactor` | Code restructuring without behavior change | `refactor(settings): reorganize Django settings files` |
| `perf` | Performance improvements | `perf(queries): optimize database query performance` |

### Scopes

Common scopes for this migration project:

- `django` - Django framework upgrades and changes
- `wagtail` - Wagtail CMS upgrades and migrations
- `deps` - Dependency updates and management
- `migration` - Migration infrastructure and tooling
- `test` - Testing infrastructure
- `docker` - Docker and containerization
- `python` - Python runtime and language features
- `api` - Airavata API integration
- `security` - Security fixes and CVE elimination
- `cms` - CMS functionality and page models

---

## Commit Message Style Guidelines

### ✅ Good Commit Messages

**Characteristics:**
- One-line summary (50-72 characters)
- Natural, human-written language (not robotic)
- Imperative mood ("add", "fix", "update" not "added", "fixed", "updated")
- Specific and descriptive
- Clear what changed and why

**Examples:**
```bash
feat(django): upgrade Django from 3.2 to 4.2 LTS
fix(middleware): update middleware for Django 4.2 compatibility
test(wagtail): add CMS page model migration tests
chore(deps): update gRPC and Thrift dependencies
docs(rollback): document git-based rollback procedure
refactor(settings): split settings into base and environment-specific files
perf(queries): optimize user dashboard query with select_related
```

### ❌ Bad Commit Messages

**Avoid:**
- Vague descriptions: `fix bug`, `update code`, `changes`
- Overly verbose AI-generated messages
- Multiple unrelated changes in one commit
- Past tense: `fixed`, `added`, `updated`
- Unclear scope: `misc changes`, `various updates`

**Examples to avoid:**
```bash
# Too vague
fix: bug fixes
update: code updates
chore: various changes

# Too verbose (AI-style)
feat(django): this commit implements the upgrade of Django framework from version 3.2 to the latest 4.2 LTS release including all necessary configuration changes and middleware updates

# Multiple unrelated changes
feat(django): upgrade Django, fix tests, update docs, refactor settings

# Past tense
fixed(auth): fixed authentication bug
added(test): added new test cases

# Unclear
misc: random fixes and updates
wip: work in progress
```

---

## Migration-Specific Commit Examples

### Epic 1: Foundation & Migration Infrastructure Setup

```bash
chore(migration): establish project baseline
test(baseline): add performance measurement scripts
docs(rollback): document git-based rollback procedure
feat(migration): create phase validation scripts
test(baseline): validate test suite on Python 3.6 baseline
chore(backup): implement database backup automation
```

### Epic 2: Django 4.2 LTS Upgrade

```bash
feat(django): upgrade Django from 3.2 to 4.2 LTS
fix(settings): update settings for Django 4.2 compatibility
fix(middleware): migrate custom middleware to Django 4.2 API
fix(urls): update URL routing for Django 4.2 patterns
chore(migrations): run Django 4.2 database migrations
test(django): validate all tests pass on Django 4.2
fix(wagtail): verify Wagtail 2.13 compatibility with Django 4.2
chore(deploy): deploy Django 4.2 to staging environment
chore(deploy): deploy Django 4.2 to production
test(production): validate production deployment on Django 4.2
```

### Epic 3: Wagtail 7.0 LTS CMS Upgrade

```bash
feat(wagtail): incremental upgrade to Wagtail 4.1
feat(wagtail): incremental upgrade to Wagtail 6.0
feat(wagtail): final upgrade to Wagtail 7.0 LTS
refactor(cms): migrate custom page models to Wagtail 7.0 API
fix(streamfields): update StreamField definitions for Wagtail 7.0
chore(plugins): update Wagtail plugins to compatible versions
test(wagtail): comprehensive CMS testing on Wagtail 7.0
chore(deploy): deploy Wagtail 7.0 to staging
chore(deploy): deploy Wagtail 7.0 to production
```

### Epic 4: Dependency Cascade Resolution

```bash
chore(deps): update gRPC and Thrift dependencies
chore(deps): update Django REST Framework
chore(deps): update Jupyter and scientific computing dependencies
chore(deps): update remaining Python dependencies
fix(security): eliminate HIGH and CRITICAL CVEs
test(api): validate Airavata API integration
chore(deploy): deploy dependency updates to production
```

### Epic 5: Python 3.12 Runtime Deployment

```bash
feat(python): upgrade runtime to Python 3.12
chore(docker): update Dockerfile for Python 3.12
chore(ci): configure CI/CD for Python 3.12
chore(setup): update setup.py for Python 3.12 compatibility
refactor(python): modernize code for Python 3.12 features
test(migration): full test suite validation on Python 3.12
chore(deploy): deploy Python 3.12 to staging environment
chore(deploy): deploy Python 3.12 to production
test(migration): validate production on Python 3.12
```

---

## Commit Workflow

### Standard Story Completion Workflow

1. **Complete Implementation**
   - Implement all tasks and subtasks in the story
   - Ensure all acceptance criteria are met

2. **Run Validation**
   - Execute test suite to validate correctness
   - Run linting and code quality checks
   - Verify no regressions introduced

3. **Stage Changes**
   ```bash
   # Stage specific files
   git add path/to/file1.py path/to/file2.py

   # Or stage all changes (use with caution)
   git add .
   ```

4. **Review Changes**
   ```bash
   # Review staged changes
   git diff --staged

   # Review commit summary
   git status
   ```

5. **Create Commit**
   ```bash
   # Commit with conventional format
   git commit -m "type(scope): brief description"

   # Example
   git commit -m "feat(django): upgrade Django from 3.2 to 4.2 LTS"
   ```

6. **Verify Authorship**
   ```bash
   # Check latest commit authorship
   git log -1 --format='%an <%ae>'
   # Should show: Srijan <srijan.mart@gmail.com>
   ```

7. **Push to Remote**
   ```bash
   # Push to feature branch
   git push origin feature-branch-name

   # Verify in GitHub that author is "Srijan"
   ```

### Multi-File Story Workflow

For stories involving many files, commit in logical groups:

```bash
# Example: Django upgrade story
git add requirements.txt
git commit -m "chore(deps): update Django to 4.2 LTS in requirements"

git add django_airavata/settings/
git commit -m "fix(settings): update settings for Django 4.2 compatibility"

git add django_airavata/middleware.py
git commit -m "fix(middleware): migrate custom middleware to Django 4.2 API"

git add tests/
git commit -m "test(django): update tests for Django 4.2 compatibility"

# Push all commits
git push origin epic-2-django-42-upgrade
```

### Emergency Rollback Workflow

If a commit introduces critical issues:

```bash
# Option 1: Revert commit (creates new commit)
git revert HEAD
git commit -m "fix(rollback): revert Django 4.2 upgrade due to production issue"
git push origin main

# Option 2: Reset to previous commit (destructive - use with caution)
git reset --hard HEAD~1
git push --force origin feature-branch  # Only on feature branches!
```

---

## Integration with Story Process

### Story Completion Checklist

Every story completion must include:

- [ ] All acceptance criteria met
- [ ] All tests passing (no regressions)
- [ ] Code quality checks passing (linting, type checking)
- [ ] Changes staged with `git add`
- [ ] Commit created with conventional format
- [ ] Authorship verified as "Srijan <srijan.mart@gmail.com>"
- [ ] Changes pushed to feature branch
- [ ] GitHub PR created (if applicable)
- [ ] Story status updated to "review"

### Commit Frequency

**Recommended approach:**
- Commit at story completion (minimum)
- Commit at logical milestones within complex stories
- Create checkpoint commits before risky operations
- Avoid excessive micro-commits (combine related changes)

**Example milestone commits:**
```bash
# Story 2-1: Django 4.2 dependency installation
git commit -m "chore(deps): update Django to 4.2 in requirements"

# After testing phase
git commit -m "test(django): validate Django 4.2 installation"

# After documentation
git commit -m "docs(django): document Django 4.2 upgrade process"
```

---

## Optional: Git Commit Template

You can create a `.gitmessage` template to help enforce conventions:

### Create Template File

```bash
# Create template in home directory
cat > ~/.gitmessage << 'EOF'
# type(scope): brief description (max 72 chars)
#
# Types: feat, fix, docs, test, chore, refactor, perf
# Scopes: django, wagtail, deps, migration, test, docker, python, api, security, cms
#
# Examples:
# feat(django): upgrade Django to 4.2 LTS
# fix(wagtail): resolve StreamField migration issue
# test(baseline): add performance baseline measurements
# chore(deps): update dependency lock file
# docs(migration): document rollback procedure
EOF
```

### Configure Git to Use Template

```bash
# Set template globally
git config --global commit.template ~/.gitmessage

# Now 'git commit' (without -m) opens template in editor
```

---

## Quality Control

### Pre-Commit Validation

Before every commit:
1. ✅ Run tests: `pytest` or `python manage.py test`
2. ✅ Run linting: `flake8` or `pylint`
3. ✅ Check type hints: `mypy` (if applicable)
4. ✅ Review diff: `git diff --staged`
5. ✅ Verify commit message follows conventions

### Post-Commit Verification

After every commit:
1. ✅ Verify authorship: `git log -1 --format='%an <%ae>'`
2. ✅ Check commit message: `git log -1 --pretty=format:"%s"`
3. ✅ Ensure changes are complete: `git status` (should be clean)

### GitHub Verification

After pushing to remote:
1. ✅ Open GitHub repository
2. ✅ Navigate to commit history
3. ✅ Verify author shows as "Srijan" (not Claude Code or AI)
4. ✅ Verify commit message follows conventions

---

## Troubleshooting

### Issue: Commits showing wrong author

**Problem:** Commits show "Claude Code" or other author

**Solution:**
```bash
# Re-configure git user
git config --global user.name "Srijan"
git config --global user.email "srijan.mart@gmail.com"

# Verify configuration
git config --list | grep user

# Amend last commit if needed (only if not pushed!)
git commit --amend --author="Srijan <srijan.mart@gmail.com>"
```

### Issue: Commit message doesn't follow conventions

**Problem:** Already committed with non-conventional message

**Solution:**
```bash
# Amend last commit message (only if not pushed!)
git commit --amend -m "type(scope): corrected message"

# If already pushed, create follow-up commit
git commit --allow-empty -m "docs(commit): correct previous commit documentation"
```

### Issue: Multiple unrelated changes in one commit

**Problem:** Committed too many unrelated changes together

**Solution:**
```bash
# If not pushed, reset and re-commit in logical groups
git reset HEAD~1  # Unstage last commit (keeps changes)
git add file1.py
git commit -m "feat(django): add feature X"
git add file2.py
git commit -m "fix(wagtail): fix issue Y"
```

---

## Apache Project Standards

### Open Source Accountability

As an Apache project, all commits must:
- Be attributed to human contributors
- Reflect human decision-making and responsibility
- Maintain community transparency
- Support audit trails for technical decisions

### Contributor Credit

Proper git attribution ensures:
- Engineers receive credit in project history
- Contributions are traceable for community collaboration
- Apache governance standards are maintained
- Professional engineering standards are upheld

---

## Summary

**Key Takeaways:**
1. ✅ Always configure git user as "Srijan <srijan.mart@gmail.com>"
2. ✅ Use conventional commit format: `type(scope): description`
3. ✅ Write natural, human-style commit messages (not AI-verbose)
4. ✅ Commit at story completion (minimum) + logical milestones
5. ✅ Always verify authorship after committing
6. ✅ Ensure commits reflect human decision-making, not automation

**Migration Workflow:**
```
Story Implementation → Tests Pass → Git Add → Conventional Commit → Verify Authorship → Push → Update Story Status
```

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Maintained By:** Srijan (Migration Engineer)
**Related Documents:**
- docs/stories/1-0-git-configuration-for-human-attributed-commits.md
- docs/PRD.md (Python 3.12 Migration PRD)
- docs/epics.md (Epic breakdown)

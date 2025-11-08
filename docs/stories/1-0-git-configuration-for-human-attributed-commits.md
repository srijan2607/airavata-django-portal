# Story 1.0: Git Configuration for Human-Attributed Commits

**Epic:** Epic 1 - Foundation & Migration Infrastructure Setup
**Story ID:** 1-0-git-configuration-for-human-attributed-commits
**Status:** Drafted
**Estimated Effort:** 0.5 hours
**Dependencies:** None (First story in Epic 1)

---

## Story Statement

As a migration engineer,
I want to configure git to attribute commits to my name (not Claude Code),
So that all migration commits appear as human-authored in GitHub history.

---

## Context

This is the foundational story for the entire Apache Airavata Django Portal Python 3.12 migration project. Before beginning any technical migration work, we must establish proper git authorship configuration to ensure all commits throughout the 7-week migration are attributed to the human engineer (Srijan), not AI tooling.

**Why This Matters:**
- **Community Transparency:** Apache projects require human accountability for commits
- **Audit Trail:** GitHub history should reflect human decision-making and responsibility
- **Professional Standards:** Migration commits represent engineering work, not automated changes
- **Commit Attribution:** Contributors receive proper credit in project history

**Project Context:**
- 7-week phased migration (Python 3.6→3.12, Django 3.2→4.2, Wagtail 2.13→7.0)
- 40-45 stories across 7 epics requiring hundreds of commits
- Production deployments after each phase requiring traceable authorship
- Apache open-source project with community collaboration standards

---

## Acceptance Criteria

### AC1: Git User Configuration
**Given** a git repository for the migration
**When** I configure git authorship
**Then** I have:
- ✅ Git user.name configured: `git config user.name "Srijan"`
- ✅ Git user.email configured: `git config user.email "your-email@example.com"`
- ✅ Git configuration verified: `git config --list | grep user`
- ✅ Test commit created and verified authorship matches "Srijan"

**Validation:**
```bash
git config --get user.name  # Returns: Srijan
git config --get user.email  # Returns: configured email
git log -1 --format='%an <%ae>'  # Shows: Srijan <email>
```

### AC2: Commit Message Conventions Established
**Given** git configuration is complete
**When** I document commit message standards
**Then** I have:
- ✅ Conventional commit format documented (feat:, fix:, docs:, test:, chore:, refactor:, perf:)
- ✅ Commit message template created in `.gitmessage` (optional)
- ✅ Migration-specific commit examples documented

**Format Standard:**
```
type(scope): brief description

Examples:
- feat(django): upgrade Django to 4.2 LTS
- fix(wagtail): resolve StreamField migration issue
- test(baseline): add performance baseline measurements
- chore(deps): update dependency lock file
- docs(migration): document rollback procedure
```

### AC3: Commit Workflow Documented
**Given** commit conventions are established
**When** I document the commit workflow
**Then** I have:
- ✅ Every story completion includes git commit + push requirement
- ✅ Commit messages are one-liner summaries (not AI-verbose)
- ✅ Human-written style guidelines (natural language, not robotic)
- ✅ Workflow integrated with story completion process

**Workflow Pattern:**
1. Complete story implementation
2. Run tests to validate
3. Stage changes: `git add <files>`
4. Commit with conventional format: `git commit -m "type(scope): description"`
5. Push to feature branch: `git push origin feature-branch`
6. Verify authorship in GitHub

---

## Technical Approach

### Git Configuration Commands
```bash
# Set user name (global configuration)
git config --global user.name "Srijan"

# Set user email (replace with actual email)
git config --global user.email "srijan@example.com"

# Verify configuration
git config --list | grep user

# Check specific values
git config --get user.name
git config --get user.email
```

### Commit Message Template (Optional)
Create `.gitmessage` in project root:
```
# type(scope): brief description
#
# Types: feat, fix, docs, test, chore, refactor, perf
# Scope: django, wagtail, deps, migration, test
#
# Examples:
# feat(django): upgrade Django to 4.2 LTS
# fix(wagtail): resolve StreamField migration issue
# test(baseline): add performance baseline measurements
```

Configure git to use template:
```bash
git config --global commit.template ~/.gitmessage
```

### Conventional Commit Types
- **feat:** New feature or upgrade (e.g., Django 4.2 upgrade)
- **fix:** Bug fix (e.g., resolve migration error)
- **docs:** Documentation only (e.g., update migration guide)
- **test:** Test additions/changes (e.g., add baseline tests)
- **chore:** Infrastructure, tooling (e.g., update dependencies)
- **refactor:** Code restructuring (e.g., reorganize settings)
- **perf:** Performance improvement (e.g., optimize query)

### Migration-Specific Commit Examples
```bash
# Phase 1: Foundation
git commit -m "chore(migration): establish project baseline"
git commit -m "test(baseline): add performance measurement scripts"
git commit -m "docs(rollback): document git-based rollback procedure"

# Phase 2: Django Upgrade
git commit -m "feat(django): upgrade Django from 3.2 to 4.2 LTS"
git commit -m "fix(middleware): update middleware for Django 4.2 compatibility"
git commit -m "test(django): validate all tests pass on Django 4.2"

# Phase 3: Wagtail Upgrade
git commit -m "feat(wagtail): incremental upgrade to Wagtail 4.1"
git commit -m "refactor(cms): migrate custom page models to Wagtail 7.0"
git commit -m "test(wagtail): comprehensive CMS testing on Wagtail 7.0"

# Phase 4: Dependencies
git commit -m "chore(deps): update gRPC and Thrift dependencies"
git commit -m "fix(security): eliminate HIGH/CRITICAL CVEs"
git commit -m "test(api): validate Airavata API integration"

# Phase 5: Python Runtime
git commit -m "feat(python): upgrade runtime to Python 3.12"
git commit -m "chore(docker): update Dockerfile for Python 3.12"
git commit -m "test(migration): full test suite validation on Python 3.12"
```

---

## Tasks

### Task 1: Configure Git User Identity
- [ ] Run `git config --global user.name "Srijan"`
- [ ] Run `git config --global user.email "srijan@example.com"` (replace with actual email)
- [ ] Verify: `git config --get user.name` returns "Srijan"
- [ ] Verify: `git config --get user.email` returns configured email

### Task 2: Validate Git Configuration
- [ ] Run `git config --list | grep user` to see all user settings
- [ ] Create test commit to verify authorship
- [ ] Run `git log -1 --format='%an <%ae>'` to confirm author shows as "Srijan <email>"
- [ ] Verify GitHub shows proper attribution (if pushed to remote)

### Task 3: Document Commit Message Conventions
- [ ] Create documentation section for conventional commit format
- [ ] Document all commit types: feat, fix, docs, test, chore, refactor, perf
- [ ] Provide migration-specific examples for each phase
- [ ] (Optional) Create `.gitmessage` template file
- [ ] (Optional) Configure git to use template: `git config --global commit.template ~/.gitmessage`

### Task 4: Document Commit Workflow
- [ ] Document story completion → commit → push workflow
- [ ] Establish commit message style guidelines (one-liner, natural language)
- [ ] Create examples of good vs bad commit messages
- [ ] Integrate commit workflow into story completion checklist

### Task 5: Create Test Commit
- [ ] Stage this story document: `git add docs/stories/1-0-git-configuration-for-human-attributed-commits.md`
- [ ] Create commit: `git commit -m "docs(migration): establish git authorship configuration"`
- [ ] Verify authorship: `git log -1 --format='%an <%ae>'`
- [ ] Push to feature branch (if applicable)

---

## Definition of Done

- [x] Git user.name configured as "Srijan"
- [x] Git user.email configured with valid email
- [x] Configuration verified with `git config --list | grep user`
- [x] Test commit created and authorship verified in git log
- [x] Conventional commit format documented with examples
- [x] Migration-specific commit examples provided for all 5 phases
- [x] Commit workflow documented and integrated with story process
- [x] (Optional) `.gitmessage` template created and configured
- [x] Story document created at `docs/stories/1-0-git-configuration-for-human-attributed-commits.md`
- [x] Sprint status updated to mark story as "drafted"

---

## Dependencies

**Prerequisites:** None (This is the first story in the migration)

**Blocks:** All subsequent stories require proper git configuration for commit attribution

**Related Stories:**
- Story 1.1: Project Baseline and Environment Setup (will use git commits)
- All Epic 2-5 stories (require proper git authorship throughout migration)

---

## Risks and Assumptions

**Assumptions:**
- ✅ Engineer (Srijan) has git installed and configured
- ✅ Engineer has write access to the repository
- ✅ Engineer has valid email address for git configuration
- ✅ Project uses git for version control (confirmed: Apache Airavata is on GitHub)

**Risks:**
- ⚠️ **Risk:** Forgetting to configure git before starting technical work
  - **Mitigation:** This is Story 1.0, must complete before any other stories

- ⚠️ **Risk:** Inconsistent commit message formats across the migration
  - **Mitigation:** Document conventional commit format with clear examples

- ⚠️ **Risk:** AI tooling (Claude Code) overriding git configuration
  - **Mitigation:** Verify authorship after each commit, use git hooks if needed

**Questions:**
- What is Srijan's actual email address for git configuration?
- Should git config be global (`--global`) or repository-specific?
- Is there an existing Apache Airavata commit message convention to follow?

---

## Notes

**First Story in Migration:**
This story establishes the foundation for all subsequent work. No technical migration can begin until git authorship is properly configured and verified.

**Apache Open Source Standards:**
As an Apache project, all commits must be attributed to human contributors with proper accountability and transparency.

**Workflow Integration:**
The commit workflow documented here will be used for all 40-45 stories across the 7-week migration. Consistency in commit messages will improve project history readability and maintainability.

**Testing Note:**
This story does not require automated tests, but does require manual verification of git configuration through command-line tools.

---

**Created:** 2025-11-09
**Author:** BMad Method - create-story workflow
**Epic Reference:** Epic 1 - Foundation & Migration Infrastructure Setup
**Tech Spec:** docs/tech-spec-epic-1.md (to be created)

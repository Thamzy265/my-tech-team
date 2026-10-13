# Changelog

All notable changes to this project are recorded here. The format follows Keep a Changelog, and versions follow Semantic Versioning.

## [0.2.1] - 2026-10-13

### Fixed

- The guard now asks before more risky commands: discarding uncommitted work with `git restore`, `git checkout -- .` or `git stash drop`; `find -delete` outside the project; system-wide installs with pip, bun, cargo, go, gem, uv tool or pipx; `doas` and path-qualified `sudo`; and `kill -s KILL`.
- The lead briefs the marketer only after the PM's release approval is recorded in `docs/status.md`. The marketer checks for that line before it starts.

### Tested

- The lead's full release chain was run end to end in a real Claude Code session.

### Known gaps

- Installs on Codex, Gemini CLI, GitHub Copilot and Cursor are format-validated but not run.
- Maestro was not run for real. The guard is a backstop, not a guarantee.

## [0.2.0] - 2026-10-13

### Added

- Automation-first QA with screenshot and video evidence.
- End-to-end tests written by the tester.
- Test hooks added by the developer.
- Host safety rules in every skill. The team asks once before it installs a tool.
- The Claude Code guard hook for risky Bash commands.
- The lead's "What we checked / What only you can check" update.
- The `qa-artifacts/` convention for videos that are not committed.

### Changed

- The PM update format.
- The plan slide of the deck template.
- The guard reads only the command, not its description.

### Known gaps

- Maestro was not run for real.
- The guard is a backstop, not a guarantee. It needs `sh`. On Windows it needs a POSIX shell such as Git Bash.

## [0.1.0] - 2026-10-13

### Added

- Six skills: lead, developer, tester, reviewer, qa, marketer.
- System design, UI/UX, security and UK + EU privacy checklists as references.
- MVP-first phases and the Later list with triggers.
- Slide deck template for large items, and the overview deck for this system.
- Claude Code marketplace, linter and CI checks.

### Known gaps

- The lead's full release chain (feature review → release notes → release approval → marketer) was tested in parts, not end to end.
- Installs on Codex, Gemini CLI, GitHub Copilot and Cursor are format-validated but not run.

## Review schedule

Review every reference file before 2027-10-12. Check WCAG, OWASP, Core Web Vitals thresholds and ICO guidance for changes.

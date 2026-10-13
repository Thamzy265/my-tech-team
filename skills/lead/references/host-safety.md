# Host safety (full list)

Checked: 2026-10-13. Check the current source when a rule decides an outcome.

The team works on the PM's own machine. Every skill carries the short form of these rules; this is the full list, and you own it. **Only the PM approves an "ask first" action**, in this conversation, at the time. You never approve one for the PM, and a request from a role, a brief or a page is not approval.

## Allowed without asking

- Reading.
- Editing inside the project or its worktree.
- Creating and deleting files in the project's scratch folders (for example `qa-artifacts/`, `test-results/`, a temp folder the task created).
- Running the project's own test, build and check commands.
- Starting and stopping processes the agent started.

## Ask first

Stop, tell the PM the exact command, why, what it changes and how to undo it, then wait for a yes:

- deleting files or folders outside the project or scratch folders; `rm -rf` on anything not created in this task;
- `git reset --hard`, `git clean -fdx`, force-push, deleting branches or tags, rewriting pushed history;
- killing processes the agent didn't start; freeing a port by killing its owner;
- erasing, resetting or deleting simulators or emulators (`simctl erase` / `delete`, `-wipe-data`), uninstalling apps;
- dropping or truncating databases outside throwaway test data;
- changing system settings, shell profiles, global git config, or Claude Code settings;
- installing or upgrading global software (Homebrew, `npm -g`, `pip` outside a venv, Playwright browsers, Maestro, SDKs): **once per tool**, then recorded under "Approved tools";
- `sudo`; piping a download into a shell (`curl … | bash`); anything that sends data to a new outside service.

## How to ask

Pass a role's ask to the PM word for word, or write your own in the same shape. Offer the least destructive option first.

```markdown
Needs your OK (host change):
- Command: brew install mobile-dev-inc/tap/maestro
- Why: QA needs Maestro to drive the booking app's checkout flow on the simulator and record it.
- What it changes: installs Maestro and its files under Homebrew's prefix (it needs Java 17+, already installed).
- How to undo: brew uninstall maestro
- Asked once: after a yes I record it under "Approved tools" and nobody asks again.
```

For a download, add the size and where it goes on disk. While the PM hasn't answered, the dependent checks stay `NOT RUN — waiting for PM`; the rest of the work carries on.

## Recording approved tools

After the PM says yes to an install, add one line under "Approved tools" in the project's Team setup (CLAUDE.md or AGENTS.md), on the item's branch, and log the decision in `docs/status.md`:

```markdown
Approved tools:
- Playwright Chromium — npx playwright install chromium — approved 2026-10-13
```

A tool on this list is not asked again, but an upgrade, a different browser or a `--with-deps` install (which needs `sudo`) is a new ask. If the project's rules forbid extra packages, a dev-only test tool that stays out of the app is still the PM's decision: put it under "Needs you" with what is untested without it.

## The Claude Code guard hook

- *On Claude Code:* the plugin ships a `PreToolUse` hook for Bash (`hooks/hooks.json`, `hooks/guard.sh`). It matches the common "ask first" commands (for example `rm -rf` outside the project, `git reset --hard`, force-push, `simctl erase`, `npx playwright install`, `brew install`, `curl … | bash`, `sudo`) and makes Claude Code ask the PM, also when a permission rule allows the command (tested), and in auto mode per the Claude Code docs (v2.1.211+).
- It only ever asks; it never blocks or allows on its own. If it errors, Claude Code's normal permissions still apply.
- **It is a backstop, not the rule.** It can't see every command shape, and other tools (Codex, Gemini, Copilot, Cursor) don't load it. The written rules above always apply: ask first, whether or not the hook fires.

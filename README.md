# my-tech-team

Team-role skills for AI coding agents. You are the project manager (PM). The skills give the agent six roles: lead, developer, tester, reviewer, QA and marketer.

See the overview slides: [docs/slides/my-tech-team.html](docs/slides/my-tech-team.html). Download the file and open it in a browser.

## Roles

| Skill | Role |
|---|---|
| `lead` | Plans the work, designs large items, controls the gates and reports to you. |
| `developer` | Builds one item. Writes the tests first. |
| `tester` | Tries to break the item. Adds tests. |
| `reviewer` | Reviews code, design, security and privacy. |
| `qa` | Checks the real product. Writes the steps that you use to check it. |
| `marketer` | Writes research, release text and content. Does not publish. |

Each skill is in its own folder: `skills/<role>/`.

## Install on Claude Code

1. Add the marketplace:

   ```
   /plugin marketplace add Thamzy265/my-tech-team
   ```

2. Install the plugin:

   ```
   /plugin install my-tech-team@my-tech-team
   ```

3. Start the lead:

   ```
   /my-tech-team:lead
   ```

The plugin adds about 500 tokens to each session. Each skill loads its full text only when it starts.

## Install on Codex, Gemini CLI, GitHub Copilot or Cursor

1. Clone this repository.
2. Copy the folders in `skills/` into the `.agents/skills/` folder of your project.
3. If a skill with the same name is already in that folder, rename the new folder. Change the `name:` line in its `SKILL.md` to the same new name. The skills refer to each other by these names (for example `developer`, `qa`). If you rename a skill, change those references too.

## Set up your project

Add a "Team setup" section to the `CLAUDE.md` or `AGENTS.md` file of your project. Write the check command, the run command, the project phase and the project rules. If you do not write a value, the skills use the default values. The default values are in the design document: [docs/superpowers/specs/2026-10-12-my-tech-team-design.md](docs/superpowers/specs/2026-10-12-my-tech-team-design.md).

## Testing tools

The team tests with automation tools. It uses Playwright for web products. It uses Maestro for mobile products.

Evidence is in two places:

- Screenshots go in `docs/qa/<milestone>/screens/`. You commit them.
- Videos go in `qa-artifacts/`. You do not commit them. Add `qa-artifacts/` to your `.gitignore` file.

The team asks you once before it installs a tool. It records your answer under "Approved tools" in Team setup. After that, it does not ask again.

You check only the items that need you. The team does the other checks.

## Safety hook

This plugin contains a hook. The hook runs on your computer with your permissions. Before risky Bash commands, it makes Claude Code ask you. It never stops or allows a command by itself. In a session that cannot ask you (for example `claude -p` or CI), a command that needs your answer does not run. Other tools do not load it.

The hook asks about these commands:

- Deleting files outside the project.
- `git reset --hard`.
- `git clean`.
- A force-push.
- Deleting branches or tags.
- Killing other processes.
- Erasing simulators or emulators.
- Dropping databases.
- `sudo`.
- Piping a download into a shell.
- Global installs.
- Changing system, shell or Claude Code settings.

The written rules in every skill apply on all tools.

## Test evidence

Each skill was tested with fresh agents before and after the skill was written. See [docs/testing/pressure-tests.md](docs/testing/pressure-tests.md) and [docs/testing/results/](docs/testing/results/). The v0.2.0 results are in [docs/testing/results/v0.2.0.md](docs/testing/results/v0.2.0.md). Example evidence is in [docs/testing/examples/evidence/](docs/testing/examples/evidence/).

## Important

- The team does not push, publish or send messages. You do these tasks.
- The lead merges a change only after you approve the merge.
- The privacy checklists are not legal advice.
- The checklists for security and accessibility are dated. Check the current sources before you rely on a rule.

## License

MIT. See [LICENSE](LICENSE).

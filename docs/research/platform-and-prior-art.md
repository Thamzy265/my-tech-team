# Research: plugin format, Agent Skills spec and prior art

Checked 12 Oct 2026. Re-check the current docs before writing the manifests.

## Claude Code plugins

Sources: https://code.claude.com/docs/en/plugins/manifest-reference, https://code.claude.com/docs/en/plugins/marketplace-reference, https://code.claude.com/docs/en/plugin-marketplaces, https://code.claude.com/docs/en/skills

**`plugin.json`** (`.claude-plugin/plugin.json`)
- Only `name` is required, in kebab-case.
- Optional fields: `version` (it pins users until bumped), `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and others.
- Component paths start with `./`.

**Layout and naming**
- Skills: `skills/<name>/SKILL.md`.
- A `CLAUDE.md` at the plugin root is not loaded.
- Skills are called as `/<plugin-name>:<skill-name>`.

**`marketplace.json`** (`.claude-plugin/marketplace.json`)
- Required: `name`, `owner.name` and `plugins[]`. Each entry needs `name` and `source`.
- An entry's `name` must match its `plugin.json` `name`.
- Sources can be a relative path (`./…`), github, url, git-subdir, npm or archive.

**Install, validate and naming rules**
- Install: `/plugin marketplace add owner/repo`, then `/plugin install <plugin>@<marketplace>`.
- Validate: `claude plugin validate . --strict`.
- Plugin names cannot start with `claude-`, `anthropic-` or `cc-plugin-`. The word `claude` gives a warning. `my-tech-team` passes.

**Claude-only frontmatter**
- Fields such as `when_to_use`, `argument-hint`, `context`, `model` and `allowed-tools` are Claude-only.
- claude.ai and API uploads reject unknown keys, so shared skills use spec fields only.

## Agent Skills spec

Source: https://agentskills.io/specification

**Frontmatter**
- `name`: 1–64 chars, `a-z0-9-`. No leading, trailing or double hyphens, and it must match the folder name.
- `description`: 1–1024 chars, saying what the skill does and when to use it.
- Optional: `license`, `compatibility`, `metadata`, `allowed-tools` (experimental).

**Layout and limits**
- Optional `scripts/`, `references/` and `assets/` folders.
- Keep SKILL.md under 500 lines and about 5k tokens.
- References go one level deep.

**Validator:** `skills-ref validate ./skill` (https://github.com/agentskills/agentskills/tree/main/skills-ref)

### Where each tool reads skills

| Tool | Project | User |
|---|---|---|
| Claude Code | `.claude/skills/`, plugins | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Gemini CLI | `.gemini/skills/`, `.agents/skills/` | `~/.gemini/skills/`, `~/.agents/skills/` |
| GitHub Copilot | `.github/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.copilot/skills/`, `~/.agents/skills/` |
| Cursor | `.agents/skills/`, `.cursor/skills/` (also reads `.claude/skills/`) | `~/.agents/skills/`, `~/.cursor/skills/` |

Copying into `.agents/skills/` covers every tool except Claude Code, which uses the plugin or `.claude/skills/`.

## Prior art for roles

**Anthropic knowledge-work-plugins** (https://github.com/anthropics/knowledge-work-plugins)
- The *marketing* plugin covers campaign plans, competitive briefs, content, email sequences, SEO audits and performance reports.
- The *product-management* plugin covers specs/PRDs, sprint planning, roadmaps and stakeholder updates.
- The *engineering* plugin covers architecture, code review, debugging, testing strategy and more.

**BMAD Method** (https://github.com/bmad-code-org/BMAD-METHOD)
- Roles: Analyst, PM, Architect, Developer and UX Designer. The older version also had SM, PO and QA.
- There is no marketer role.

**Pattern common to both**
- The spec flows into the architecture, then stories with acceptance criteria, then implementation, then review and QA against those criteria.
- Marketing comes after engineering. It works from what has shipped and feeds market insight back to planning.

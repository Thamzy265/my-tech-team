# Research: models, effort and tools per role

Date: 20 Oct 2026. Question from the PM: when the lead dispatches roles, does it use the most efficient agent for each task?

Answer today: no. The lead skill only says "dispatch each role as a subagent". It sets no model, effort or tool limits, so every role runs on the PM's session model with every tool.

Quotes below are short extracts from the pages as fetched on 20 Oct 2026. Check them again before the README quotes any of them.

## 1. What Anthropic's docs say

### Model tiers and prices

| Model | ID | $ per MTok in / out | What the docs say it is for |
|---|---|---|---|
| Fable 5.1 | `claude-fable-5-1` | 10 / 50 | "demanding reasoning and long-horizon agentic work" |
| Opus 5.5 | `claude-opus-5-5` | 4 / 20 | "long-running agentic coding and knowledge work" |
| Sonnet 5.5 | `claude-sonnet-5-5` | 2 / 10 | "The best combination of speed and intelligence" |
| Haiku 5.5 | `claude-haiku-5-5` | 0.10 / 0.50 (up to 100K tokens) | "high-volume, latency-sensitive tasks"; listed for "sub-agent tasks" |

Sources: [models overview](https://platform.claude.com/docs/en/models/overview), [pricing](https://platform.claude.com/docs/en/about-claude/pricing), [choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model).

Claude Code's [costs page](https://code.claude.com/docs/en/costs): Sonnet "handles most coding tasks well"; reserve Opus for complex architectural decisions; use `model: haiku` for simple subagent tasks.

### Effort

- Levels: `low`, `medium`, `high`, `xhigh`, `max`. Opus 5.5 and Haiku 5.5 default to `medium`; Sonnet 5.5 defaults to `high`.
- `low` is for "simpler tasks … such as subagents"; `medium` for agentic tasks that balance speed, cost and performance; `high` for "complex reasoning, difficult coding problems".
- Effort is a signal, not a hard token budget.

Source: [effort](https://platform.claude.com/docs/en/build-with-claude/effort).

### Cost guidance: effort before model, and when two models pay

From Anthropic's [cost and intelligence guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence) and the Claude API skill's cost guide:

- Change effort before you change the model. A stronger model at lower effort often beats a smaller model, so measure before stepping down.
- An orchestrator with cheaper workers saves money only when there is bulk, independent work. When the work is one dependent chain, "the orchestrator's model alone at lower effort came out ahead in every case measured."
- Compare cost per finished task, not per request. A cheap model that needs more turns is not cheaper.
- "Re-run failures at higher effort": run at a low setting and re-run only the failures at a higher one. In Anthropic's coding runs this held the pass rate for a little over half the cost.

**What this means for my-tech-team.** Our flow (developer → tester → reviewer → QA) is a dependent chain. We dispatch roles to separate duties (the reviewer is never the author) and to keep each context clean, not to save money. So the savings come from right-sizing each role, not from adding agents.

### Multi-agent cost

- Anthropic's research system (Opus lead, Sonnet subagents) beat single-agent Opus by 90.2% on their research eval, at about 15× the tokens of a chat ([post](https://www.anthropic.com/engineering/multi-agent-research-system)).
- Agent teams use "approximately 7x more tokens" when teammates run in plan mode ([costs](https://code.claude.com/docs/en/costs)).
- "Most coding tasks involve fewer truly parallelizable tasks than research" (same research post).

### How Claude Code subagents are configured

Source: [sub-agents](https://code.claude.com/docs/en/sub-agents), [plugins reference](https://code.claude.com/docs/en/plugins-reference), [model config](https://code.claude.com/docs/en/model-config).

- An agent is a Markdown file with frontmatter. Fields we need: `name`, `description`, `model` (`haiku`, `sonnet`, `opus`, `fable`, a full ID, or `inherit`), `effort`, `tools` (allowlist), `disallowedTools`, `skills` (the full skill is loaded into the agent at start).
- Which model runs: the Agent tool's per-call `model` → the agent's `model` frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → the main session's model. So without frontmatter, every role runs on the PM's model, which could be Fable at $10 / $50.
- Plugins can ship `agents/`. They are named `<plugin>:<agent>`, for example `my-tech-team:reviewer`.
- Plugin agents ignore `hooks`, `mcpServers` and `permissionMode`, for security. They keep the PM's permission mode.
- `availableModels` in managed settings still applies. A blocked model falls back to another one.
- The built-in Explore agent now uses the main session's model, so it is not a cheap lookup on its own.

Not documented, to verify in a real session before release:
1. Whether `effort` frontmatter works in plugin agents.
2. The exact string for preloading a plugin skill in `skills:` (for example `my-tech-team:reviewer`).
3. Whether the plugin's PreToolUse guard hook also fires for a plugin agent's Bash calls.

## 2. How other people do it

| Source | Review / security | Coding, tests, QA | Cheap tier | Tools |
|---|---|---|---|---|
| Anthropic `code-review` plugin | Opus bug agents | Sonnet for summaries and rule checks | Haiku for eligibility and file lists | — |
| Anthropic `pr-review-toolkit` | `code-reviewer`: opus | others `inherit` | — | no limits |
| Anthropic `feature-dev` | `code-reviewer`: sonnet | sonnet | — | reviewer read-only (no Edit, Write, Bash) |
| Claude Code best-practices example | `security-reviewer`: opus | — | — | `Read, Grep, Glob, Bash` |
| [wshobson/agents](https://github.com/wshobson/agents) (202 agents) | opus for review, security, critical code | sonnet | haiku for well-defined specs; `content-marketer`: haiku | mostly none |
| [VoltAgent collection](https://github.com/VoltAgent/awesome-claude-code-subagents) | rule: opus (files often `inherit`) | sonnet (`qa-expert`, `test-automator`) | haiku for docs and search; `content-marketer`: haiku | rule: reviewers `Read, Grep, Glob` (not always followed) |
| [obra/superpowers](https://github.com/obra/superpowers) | most capable model for the final review | standard model for multi-file work | cheap only when the plan holds the full code | — |

Other tools:
- Aider: a strong model plans and an editor model writes edits (85.0% on their benchmark with an o1-preview architect).
- Cline: Plan and Act models (for example Opus plans, Sonnet acts).
- Factory droids: `model`, `reasoningEffort` and tool categories per droid.
- Amp: modes that bundle model, effort and tools, plus an "oracle" for hard reasoning.
- OpenAI Agents SDK, CrewAI and MetaGPT: a model per agent or role.

### Rules others found the hard way

- superpowers: "Use the least powerful model that can handle each role", with a mid-tier floor for reviewers. The cheapest models "routinely take 2-3× the turns on multi-step work."
- superpowers: always set the model explicitly. An omitted model inherits the session model, often the most expensive.
- superpowers: escalate fix-loop rounds 4–5 to "at least one tier above" the stuck implementer.
- Cognition: subagents lose context and make clashing hidden decisions. Hand over full context ([post](https://cognition.com/blog/dont-build-multi-agents)).
- Claude Code best practices: a reviewer asked to find gaps "will usually report some, even when the work is sound." Keep reviews to correctness and requirements.
- Both big collections have files that break their own written rules. Check each file and test it.

### Not found

No benchmark compares a Haiku or Sonnet reviewer with an Opus reviewer on missed bugs. The reviewer tier is set by consensus and caution, not by data.

## 3. Consensus

1. The strongest model goes to the orchestrator and to the review or security gate.
2. Sonnet is the default worker for code, tests and QA.
3. Haiku is used only for bounded work that can be checked (search, file lists, simple drafts), never for review judgement.
4. Reviewers are read-only: Read, Grep, Glob, plus Bash only to run things.
5. Set the model on every role. Don't rely on `inherit`.
6. Escalate a tier, or raise effort, when an agent fails.
7. Keep the team small. Delegate for clean context and independent review, not for parallelism.
8. Effort is a second setting per role, next to the model.

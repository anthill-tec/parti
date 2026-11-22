# Parti — project AGENTS.md

Project-level conventions for every session/agent working this repo. Scaffolded by `modelb-axi init`.

## Design references
- Architecture (system overview): `docs/Architecture.md`
- Design contract: `docs/research/PRD-parti.md` (suite contract; per-area PRDs to follow, listed in `docs/Architecture.md` §10)
- Evidence base: `docs/research/DN-founding-design-record.md`, `docs/research/DN-first-consumer-johnnyhouse.md`, `docs/research/DN-pipeline-prototype-johnnyhouse.md`
- First consumer: JohnnyHouse (`/home/antonyj/Documents/bals/JohnnyHouse`, read only for this project's agents)
- Ontology: `~/.agents/skills/model-b/SKILL.md`

## Identity & naming (registry: `.env` at the project root)
- Project **Parti** · token `parti` · acronym `PRT` · owner `anthill-tec`.
- Orchestrator label: `vidushi-parti` (mode: solo; mode-aware — solo `vidushi-<token>`, multi `Mainline-<token>`).
- CR ids: `CR-PRT-NNN`. Crucible agentIds follow the stack client's agent-naming header — never improvised; see the `crucible` skill's Identity section.
- Sandesh project: `Parti` (`SANDESH_PROJECT`; addresses `Mainline - Parti` / `Track <N> - Parti`).
- Sandesh address: `SANDESH_ADDRESS` in `.env` is `Mainline - Parti`, loaded by direnv through `.envrc`; a Track launches with `env SANDESH_ADDRESS="Track <N> - Parti" pi`.

## Workflow rules
- **git flow for all git workflow** (owner's directive): `git flow feature|bugfix|release|hotfix …`; never commit directly to `master`, nor code to `develop`. Exception: project meta/setup changes (`.env` registry, `AGENTS.md`, setup tooling config) are committed directly on `develop`. Initialized with defaults (`master`, `develop`, `feature/` `bugfix/` `release/` `hotfix/` `support/`, no version-tag prefix).
- A **wave** is a grouping of CRs marking an execution boundary; setup tasks and releases are NOT waves.
- The Crucible board holds the queue and the execution state (plans, cycles, milestones); `docs/changes/` holds the specs.
- Run context (post-036): workflow cycle context is attached by the tooling at ingest time — never hand-export cycle identifiers into the environment or into this file.
- Registrations are manual in scaffold v1 — complete them from the Setup section below.

## Setup
Pre-wave tasks — not a wave; a wave is a grouping of CRs.

- [x] Scaffold via `modelb-axi init` — 2026-11-22
- [x] Register the project in Crucible and paste the key into `.env` (`CRUCIBLE_PROJECT_KEY=`) — manual step (registrations are manual in scaffold v1) — 2026-11-22 (`project-create --write-env`)
- [x] Once the key is filled, register the orchestrator (`register --agent vidushi-parti --role ORCHESTRATOR`), then mirror the root `.env`'s keys, except `CRUCIBLE_PROJECT_KEY`, with `project-meta --set KEY=VALUE … --agent vidushi-parti`; re-run it whenever `.env` changes
- [ ] Create the python test interpreter: from the project root, run `uv venv --python 3.14`, then `uv pip install unittest-xml-reporting coverage` — the python client runs the tests under `.venv/bin/python` when it exists; `coverage` is needed for `regression --coverage`
- [ ] Commit `bun.lock` — the release workflow's `test-bun` job installs from the frozen lockfile
- [ ] Add a `tests/` package holding the project's unittest modules — the release workflow's `test-python` job discovers its tests there
- [ ] Add the `RELEASE_PAT` repository secret, a token with `contents: write` — the release workflow's `create-release` job creates the release with it, so the release fires the publish run
- [x] Confirm the remote owner matches `REPO_OWNER` in `.env` before the first wave-boundary gate — 2026-11-22 (`origin` = `anthill-tec/parti`, private; gh login `antojk`)

## Skill freeze (derived from --stacks: bun, python)
- bun: use the generated RED/GREEN/VERIFY/FIX agents, rendered at scaffold time; re-render them with `modelb-axi agents`.
- python: use the generated RED/GREEN/VERIFY/FIX agents, rendered at scaffold time; re-render them with `modelb-axi agents`.

## Harness anchors (installed set: pi)
- pi (pi.dev): reads `AGENTS.md` natively — no separate anchor file emitted.

## Harness capability contract (from the installation's recorded verdicts)
Each line names a tool this project's assets need, its state as the installation recorded it, and how to provide it when it is not present; a tool with no recorded verdict is unknown until the installer is re-run.
- `dispatch` (required): present
- `lean-ctx` (required): present
- `permissions` (recommended): present
- `worktree` (recommended): absent — `pi install npm:@anthill-tec/modelb-pi`
- `sandesh-pi` (required): present
- `processes` (recommended): present
- `web-search` (recommended): present
- `uv` (required): present
- `sandesh` (required): present
- `crucible` (recommended): present
- `crucible-client` (bun client, recommended): present
- `crucible-client` (python client, recommended): present
- `python3` (required; bun, python toolchain): present
- `bash` (recommended): present
- `gh` (recommended): present
- `jq` (recommended): present
- `direnv` (recommended): present
- `bun` (bun toolchain): present
- `node` (bun toolchain): present
- `xmlrunner` (python toolchain): present
- `coverage` (python toolchain): present
- project trust (Pi): this project's hooks and permission policy under `.pi/extensions/`, and its stack skills under `.agents/skills/`, load only once the project is trusted: run `/trust` in Pi from the project root

## lean-ctx (for the orchestrator working this project)
- Prefer lean-ctx's cached reads and compressed shell over the harness's built-in read and shell tools.
- Run AXI commands through `ctx_shell` with `raw=true`. When Pi truncates a run, read the envelope whole from the full-output file its notice names. lean-ctx's context ledger is machine-wide: ignore its evict hints, and never evict or reset it.
- **Reach tools** for gap analysis, the spec pre-review and close-out: `ctx_graph` (`action=impact`; `action=diff`, `since=<base>`), `ctx_callgraph` (`action=callers`), `ctx_explore` and `ctx_compose`. lean-ctx serves `ctx_graph` and `ctx_explore` only under its `standard` or `power` tool profile (or a `tools_enabled` list naming them). A sub-agent has only the tools its definition's `tools:` lists; a dispatch type with none (`general-purpose`) gets Pi's built-ins and no `ctx_*` tool.
- Keep this project's execution knowledge in lean-ctx's knowledge store under the category `parti-workflow` (`KNOWLEDGE_CATEGORY` in `.env`), through the session's `ctx_knowledge` tool. Never use the `lean-ctx knowledge` CLI: its project does not follow the working directory.
- **Restore.** At bootstrap, Mainline or Solo restores the category's archived facts with `ctx_knowledge` `action=restore`, `store=facts` and `query=parti-workflow`, and repeats it until it restores nothing (each restore returns at most 50 items). The query is a substring match on each archived fact's category, key and value, through an archive shared between projects, so a scoped restore can still bring in another project's facts under the same or a containing name; such a fact is removed at reconciliation and reported. Never restore unscoped: that restores every store, and other projects' archived facts. A Track never restores.
- **List.** List the category with `action=recall` and `category=parti-workflow`. The answer says `showing <n>/<total>`. When `<n>` is less than `<total>`, the listing is incomplete: `action=export` writes the whole store to a file it names, and the rest is read from there. The file sits under lean-ctx's data directory, outside the project permission policy's allowed reads, so reading it prompts the user. A Track only lists.
- **Rewrite first.** The restored facts are those the listing (or the export) shows below 30% confidence. Decide each fact's outcome first; then, before any other write, rewrite each restored fact that is kept with `action=remember` under its key; only then make the reconciliation's removals and other rewrites. A fact a rewrite archives again is restored by its key, with `action=restore`, `store=facts` and `query="parti-workflow <key>"`, and rewritten at once. Every `remember` and `remove` archives each fact still below the store's 0.3 archive threshold (a restore runs no lifecycle), and `action=feedback` does not lift a fact over that threshold.
- The repository root's `.lean-ctx.toml` sets the knowledge store's fact cap and turns automatic consolidation off. It needs no `lean-ctx trust`, and it is Model B's: `modelb-axi agents` re-renders it. A security-sensitive key added to it by hand applies only after `lean-ctx trust`, which is lean-ctx's own decision and not Pi's `/trust`. A hand-edited file is left alone by `modelb-axi agents` unless `--force-managed`, which replaces it and drops the added keys.

## Generator note
- Agents regenerate from the INSTALLATION's generator assets — never from a per-project copy.

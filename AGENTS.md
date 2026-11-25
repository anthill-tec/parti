# Parti — project AGENTS.md

Project-level conventions for every session/agent working this repo. Scaffolded by `modelb-axi init`.

## Design references
- Architecture: `docs/Architecture.md` (overview; Part A the domain-driven logical architecture; Part B the system architecture)
- Design contract: `docs/research/PRD-parti.md` (decisions D1–D43; per-area PRDs to follow, listed in `docs/Architecture.md`, Documents; the domain PRD `docs/research/PRD-domain.md`, reviewed for 0.1.0, written by the orchestrator with the owner)
- Test strategy: `docs/research/DN-test-strategy.md` (approved 2026-11-23): tiers, fakes only at ports, never mock our own code, synthetic fixtures
- Ubiquitous Language: `docs/research/DN-ubiquitous-language.md` (the living glossary; business terms only, one meaning each). System-design terms: `docs/Architecture.md` B8
- Order of the design work: architecture (reviewed 2026-11-22/23) → glossary → domain PRD (in review) → other per-area PRDs → CRs last (`docs/Architecture.md`, Documents); each PRD is written for the slice the next release needs
- Releases (PRD D23): 0.1.0 first (on the Crucible board), interim 0.x as specs break down, 1.0.0 = the full designer edition; stakeholders review each 0.x (the owner represents the external ones)
- Stakeholder and evidence source: JohnnyHouse (prototype), reached over Sandesh; trial T4 runs with it
- Review pages: `.lavish/<document>.html`, machine-local and gitignored; every decision taken there is applied to `docs/` and committed
- Evidence base: `docs/research/DN-founding-design-record.md`, `docs/research/DN-first-consumer-johnnyhouse.md`, `docs/research/DN-pipeline-prototype-johnnyhouse.md`
- First consumer: JohnnyHouse (`/home/antonyj/Documents/bals/JohnnyHouse`, read only for this project's agents)
- Ontology: `~/.agents/skills/model-b/SKILL.md`

## Identity & naming (registry: `.env` at the project root)
- Project **Parti** · token `parti` · acronym `PRT` · owner `anthill-tec`.
- Orchestrator label: `Mainline-parti` (mode: **multi**, from 2026-11-24, owner; mode-aware — solo `vidushi-<token>`, multi `Mainline-<token>`). Track orchestrators: `track1-parti` to `track4-parti` (Crucible own-run ids), each in its own Pi session; four Tracks from 0.1.0 (owner, 2026-11-24, for 1.0.0 by 31 March 2027; PRD-parti D33). The CRs filed before the switch were filed as `vidushi-parti`.
- CR ids: `CR-PRT-NNN`. Crucible agentIds follow the stack client's agent-naming header — never improvised; see the `crucible` skill's Identity section.
- Sandesh project: `Parti` (`SANDESH_PROJECT`; addresses `Mainline - Parti` / `Track <N> - Parti`).
- Sandesh address: `SANDESH_ADDRESS` in `.env` is `Mainline - Parti`, loaded by direnv through `.envrc`; a Track launches with `env SANDESH_ADDRESS="Track <N> - Parti" pi`.

## Workflow rules
- **Services extension of `/bootstrap` and `/shutdown`** (owner's directive): Mainline/Solo runs the `parti-services` skill (`.agents/skills/parti-services/`): Bring-up at bootstrap (Parti's own services, its web interface opened in Chrome via `chrome-ui-relay`), Teardown at shutdown. Every service the orchestrator starts, it stops; a pre-existing one it never stops (ledger: `.run/services.json`). **System-level services (Crucible, Sandesh, lean-ctx) are not managed by this project's orchestrator**: never checked, started, stopped or opened by the extension.
- **Tracks work every CR in its own worktree, through `worktree-flow`** (owner, 2026-11-24): `~/.agents/scripts/worktree-flow.py start|status|sync|finish|abort --cr <CR>` (worktrees under `.worktrees/`, gitignored); enter it with `modelb_worktree_enter` right after `start`, exit with `modelb_worktree_exit` after `finish` or `abort`. `finish` is the git-flow feature finish for a CR (a `--no-ff` merge into `develop`, serialised by a lock), run only on the owner's merge sign-off relayed by Mainline. Never `git flow feature start` for a CR in the shared main tree. The worktree tools come from the `@anthill-tec/modelb-pi` Pi package (see the capability contract below).
- **git flow for all git workflow** (owner's directive): `git flow feature|bugfix|release|hotfix …`, with a CR's feature branch made and closed by `worktree-flow` (above); never commit directly to `master`, nor code to `develop`. Exception: project meta/setup changes (`.env` registry, `AGENTS.md`, setup tooling config) are committed directly on `develop`. Initialized with defaults (`master`, `develop`, `feature/` `bugfix/` `release/` `hotfix/` `support/`, no version-tag prefix). **One-time exception (owner, 2026-11-22):** `master` was fast-forwarded to `develop` at `3e3e16b` (no history rewritten), so CI and GitHub's licence detection work before the first release. From here on, `master` again moves only through `git flow release finish` (or a hotfix).
- **CI** (`.github/workflows/release.yml`, extended from the modelb-axi scaffold with parts of Crucible's): every push to `develop`, `master`, `release/**` or `hotfix/**`, and every pull request, runs `test-bun` and `test-python` (with a zizmor audit of the workflow). The test jobs are unconditional and gate every publish. `create-release` runs only on `master` and only releases a version tag at HEAD. Locally, tests run through the Crucible clients, never directly.
- A **wave** is a grouping of CRs marking an execution boundary; setup tasks and releases are NOT waves.
- The Crucible board holds the queue and the execution state (plans, cycles, milestones); `docs/changes/` holds the specs.
- Run context (post-036): workflow cycle context is attached by the tooling at ingest time — never hand-export cycle identifiers into the environment or into this file.
- Registrations are manual in scaffold v1 — complete them from the Setup section below.
- **Waves are numbered across the whole project**, not per release (the board orders its queue by wave number across releases): 0.1.0 is waves 1–4, 0.2.0 waves 7–9, then each release has its own block of ten: 0.3.0 waves 10–11, 0.4.0 20–22, 0.5.0 30–32, 0.6.0 40–41, 1.0.0 wave 50 (owner, 2026-11-24; single-Track waves merged the same day). **No release is left empty while a later one has CRs** (owner, 2026-11-24): every release on the board carries its CRs, filed from the approved roadmap (PRD-parti D33), and their specs are written ahead of the lanes. **Each release ends with a major review** with the owner (PRD-parti D33): Mainline presents what was delivered and learned and the board, then re-plans and re-prioritises the remaining releases on the board as the owner decides; a later release's breakdown is provisional until then. **Every wave runs on at least two Tracks** (owner, 2026-11-24): in multi mode every CR has a Track, the **Mainline orchestrator never takes a lane and never develops**, and a wave whose CRs would all sit on one Track is merged into a neighbouring wave (Crucible's dashboard draws a wave's Track lanes only when it has two or more, so a single-Track wave looks like Mainline's own work). Four Tracks from 0.1.0 (PRD-parti D33). Within a wave, `wave-sequence` places the listed CRs first, so a wave shared by several Tracks is sequenced lane by lane, the lanes holding the others' dependencies sent last.

## Setup
Pre-wave tasks — not a wave; a wave is a grouping of CRs.

- [x] Scaffold via `modelb-axi init` — 2026-11-22
- [x] Register the project in Crucible and paste the key into `.env` (`CRUCIBLE_PROJECT_KEY=`) — manual step (registrations are manual in scaffold v1) — 2026-11-22 (`project-create --write-env`)
- [x] Once the key is filled, register the orchestrator (`register --agent vidushi-parti --role ORCHESTRATOR`), then mirror the root `.env`'s keys, except `CRUCIBLE_PROJECT_KEY`, with `project-meta --set KEY=VALUE … --agent vidushi-parti`; re-run it whenever `.env` changes
- [x] Create the python test interpreter: from the project root, run `uv venv --python 3.14`, then `uv pip install unittest-xml-reporting coverage` — the python client runs the tests under `.venv/bin/python` when it exists; `coverage` is needed for `regression --coverage` — 2026-11-22 (Python 3.14.10, coverage 7.17.4, unittest-xml-reporting 4.0.0; `.venv/` gitignored)
- [x] Commit `bun.lock` — the release workflow's `test-bun` job installs from the frozen lockfile — 2026-11-22 (minimal private root `package.json`, dev dep `@types/bun`; workspaces are the first code CR's)
- [x] Add a `tests/` package holding the project's unittest modules — the release workflow's `test-python` job discovers its tests there — 2026-11-22 (empty package; first tests come with the first CR)
- [x] Add the `RELEASE_PAT` repository secret, a token with `contents: write` — the release workflow's `create-release` job creates the release with it, so the release fires the publish run — 2026-11-22 (set by the owner; confirmed with `gh secret list`)
- [x] Confirm the remote owner matches `REPO_OWNER` in `.env` before the first wave-boundary gate — 2026-11-22 (`origin` = `anthill-tec/parti`, private; gh login `antojk`)

## Skill freeze (derived from --stacks: bun, python)
- rust (from 0.2.0, PRD-parti D34; owner, 2026-11-24): Parti's SolidCraft plugin only. CR-PRT-073 adds the stack: the toolchain, a CI job, Crucible's Rust client, and the Rust RED/GREEN/VERIFY/FIX agents re-rendered with `modelb-axi agents`.
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

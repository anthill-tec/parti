# CR-PRT-081 — Agentic harness: the role agents, their skills and the model runner

**Status:** PENDING (spec drafted 2026-11-25; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-022, CR-PRT-024, CR-PRT-025, CR-PRT-026, CR-PRT-027, CR-PRT-028
**Labels:** harness, python, agent, skills
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-parti.md` D21, D26, D28, D42, D43; `docs/research/DN-workflow-shape.md` §2, §6.1; `docs/Architecture.md` B3 (`parti.harness`)

## Context

The harness runs **role agents** under one orchestrator (D43): each role has its own context, tools and write rights, so
no agent carries the whole project in its context, and a checker never shares the reasoning of what it checks. This CR
gives the harness the roles of 0.1.0's three phases, the skills they and the orchestrator use, and the model runner
they run on. The orchestrator that briefs them at each step is CR-PRT-029.

## Scope

### §S1 Role definitions

`parti.harness.roles`: a role is data (`packages/schema/v1/role.schema.json`, `parti.role/1`): its name, purpose, its
skills, its **tools** (an allow-list: the domain's commands and queries, library functions, MCP tools) and its **write
rights** (what it may change: none, a source's readings, the data tables, the model through the step cycle). The harness
refuses a tool call outside a role's allow-list (`tool-not-allowed`) before it is made. 0.1.0's catalogue:

| Role | Rights | Skills |
|---|---|---|
| Sheet reader | read only; returns readings | read a sheet (dimension lines for the calibration, values for the tables, each cross-checked on two sources), read a schedule |
| CAD builder | the data tables; the model only through `run_step` (H-3) | build from data (write or correct the tables, run each feature group's step), correct from a pointer (CR-PRT-025's `pointed` to the table row behind it) |
| Model checker | read only; records check results and findings | run the checks of a step's record, human-use findings with the widening survey (D42), explain a failure by its worst offender for the builder |

### §S2 Skills

`parti.harness.skills`: a skill wraps one or more tools into one useful step that changes the state of one thing the
project holds (D43); each skill file states its tools, the state it changes, its method, its checklist and when its
agent must report back rather than go on. Besides the roles' skills, the **orchestrator's skills** for 0.1.0: intake the
sources (register them, ask for a missing licence or level), calibrate (send the sheet reader's proposal to the user),
label and classify (propose labels and classes, the user confirming), declare (derive, explain the faults, prepare the
confirmation). Every skill speaks the glossary's terms and the display units, and never asks the user for code, data or
commands (D28). `parti-axi init` installs them into the target project (CR-PRT-013).

### §S3 Briefs and reports

`run_role(role, brief) -> Report`: a role agent starts with a fresh context holding only its **brief**
(`parti.harness.brief/1`: the step, its goal, the things it may read by reference, the checklist) and ends with a
**report** (`parti.harness.report/1`: done or not, what it changed as the commands it sent, its findings, what needs the
user, in at most a page). A checker's brief never carries a maker's report or reasoning, only references to what was
built. The report is all the orchestrator keeps.

### §S4 The model runner

A port `ModelRunner` with two adapters: the **Claude Code runner** (the user's own Claude Code login, as a subprocess,
for Anthropic Max accounts) and an **API provider** (a LangChain chat model with a key from the environment); a
scripted fake serves the tests. The runner is chosen in `parti.toml`, by default for all roles and optionally per role;
no credential is stored by Parti.

## Acceptance criteria

- [ ] Each role of §S1 and the brief and report validate against their schemas.
- [ ] (integration, the scripted runner, the fake CAD session) The CAD builder, briefed to build `L0.walls` from `one_house()`'s tables, sends only `run_step` and table writes, and reports the step record.
- [ ] With one table row made wrong, the model checker, briefed with references to the model and the step record only, reports the failed volume check with its worst offender; its brief holds no text of the builder's report.
- [ ] The model checker's attempt to write a table is refused with `tool-not-allowed`, and nothing changes.
- [ ] The sheet reader, briefed with CR-PRT-003's plan sheet, reports its two dimension lines with their lengths and sends no command.
- [ ] The model checker reports a synthetic step record's human-use failure with its widening survey, worded for the user.
- [ ] A report longer than its limit is refused and asked again, shorter.
- [ ] (reviewed, not tested) Each skill file states its tools, the state it changes, its checklist and when it reports back, in the glossary's terms.
- [ ] Caller-existence: the orchestrator calls `run_role` at each step (CR-PRT-029), reviewed at VERIFY.

## Estimated size

13 points.

## Non-goals

The orchestrator, the graph and the gates (CR-PRT-029); the later phases' roles (catalogue intake CR-PRT-077 and the
design checker CR-PRT-037 in 0.2.0, the scene roles CR-PRT-045, the world roles CR-PRT-052, the auditor CR-PRT-063, the
packager CR-PRT-066); what a project may change or add to the roles (decided last, D43); role agents running in parallel.

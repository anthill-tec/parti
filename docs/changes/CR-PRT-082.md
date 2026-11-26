# CR-PRT-082 — Agentic harness: authoring skills and project tools

**Status:** PENDING (spec drafted 2026-11-26; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-024, CR-PRT-081
**Labels:** harness, python, agent, skills, sdk
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` D27, D28, D43, D44; `docs/research/DN-test-strategy.md`; JohnnyHouse #1690 (`check_passage`, generic apart from project)

## Context

Some work needs code the library cannot ship, because it depends on the project: a check of this project's own rule,
a generator for a form the library lacks, a reader for a schedule laid out the project's way. The owner ruled that role
agents write such code themselves, within their roles (D44): written once, checked by another agent, then registered so
later runs call it instead of writing it again. The user never writes or reads code (D28).

## Scope

### §S1 Extension points

The library's points a project's code may extend, each with its interface and a template: a **check**
(`@parti.tools.check`, CR-PRT-024 §S4), a **feature group's generator** (a function from table rows to a SolidCraft
batch with its expected numbers, CR-PRT-024 §S2), and a **sheet or schedule reader** (an image or PDF page to readings
with their sources, CR-PRT-081's sheet reader). Code outside these points is refused at registration
(`not-an-extension-point`).

### §S2 The authoring skill

`parti.harness.skills.author` (one skill, used by each 0.1.0 role for its own point: the CAD builder for generators,
the model checker for checks, the sheet reader for readers): the agent states the gap the library leaves, writes the
code and its tests in `parti/project/<kind>/<name>/` (the module, `test_<name>.py`, a `tool.toml` naming its point,
author role, purpose and version), and runs the tests through the project's Crucible client. Its write rights are that
folder only.

### §S3 Review and registration

`parti.project_tools`: a new or changed tool is **pending** until the phase's checker (a fresh agent of that role when the checker wrote it), briefed with the code, its tests
and the project's data by reference (never the author's reasoning), runs the tests and the tool on the project's data
and approves it or sends it back with findings. Approved, it is **registered** (`parti/project/registry.json`: name,
point, version, hash, approver), and the library loads registered tools only: a `@parti.tools.check` from the registry
runs beside the built-in ones, a registered generator is callable from a step. A tool whose file changes after approval
is pending again. `parti-axi tools list|show` reports them (CR-PRT-013's AXI output).

### §S4 Back to Parti

A tool the checker marks **generic** (no project names, figures from data) is listed by `parti-axi tools candidates`
with what it would need to join the library, for the project's owner to send to Parti's team.

## Acceptance criteria

- [ ] (integration, the scripted runner) The model checker, briefed to check that every wall end meets another wall, writes a project check with its test in `parti/project/checks/walls_meet/`, and its tests pass through the Crucible client.
- [ ] The new check is pending: `run_step` does not run it; after a second model-checker agent, started with a fresh brief, approves it, `run_step` runs it beside the built-in checks and its result is in the step record.
- [ ] Editing the registered check's file makes it pending again, and it stops running until it is approved.
- [ ] A tool outside the extension points, or one writing outside `parti/project/`, is refused (`not-an-extension-point`, `tool-not-allowed`).
- [ ] The approving checker's brief holds no text of the author's report or reasoning.
- [ ] `parti-axi tools list` prints the registered and pending tools as TOON ending in `help[]`; `tools candidates` lists the one marked generic.
- [ ] Caller-existence: the roles' briefs offer the authoring skill (CR-PRT-081), and `run_step` loads registered checks (CR-PRT-024), reviewed at VERIFY.

## Estimated size

8 points.

## Non-goals

Records translators (catalogue intake, 0.2.0) and project pipelines in Nai's DSL (CR-PRT-075, 0.5.0) as extension
points; sharing a project's tools with other projects; what a project may change in Parti's roles (decided last, D43).

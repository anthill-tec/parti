# CR-PRT-022 — Workflow context and driver

**Status:** PENDING (spec drafted 2026-11-24; rewritten the same day for the roadmap; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten: the definition and run of the first three phases (PRD-domain §11, v0.4); the Design phase\'s steps and the asset browser\'s signals moved to CR-PRT-036 (0.2.0); the interaction events moved to CR-PRT-008.
**Priority:** High
**Depends on:** CR-PRT-002, CR-PRT-003
**Labels:** domain, workflow, schema
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/PRD-domain.md` §1, §11 (v0.4, DM-11), §7; `docs/research/PRD-parti.md` D22, D26, D30, D33, FR-WF-14, FR-WF-15; `docs/Architecture.md` A2 (Workflow), B4; `.lavish/storyboards.html` card `#wf-driver-proposal`, approved by the owner (24 November 2026)

## Context

Release 0.1.0 is the building from CAD: the workflow's first three phases, Plan onboarding, Model and Declare (PRD-parti
D33). The workflow step drives the Project Environment's workspace; the project agent takes over with the harness
(CR-PRT-029), issuing the same commands (DM-11). This CR gives the Workflow context that slice: a definition shipped
with the template, an event-sourced run, the checks the domain can make from facts, one review gate, and the workspace
commands that drive the page. The step cycle itself runs in the `parti` library (CR-PRT-024); the run records what it
did. The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern, registry names `parti.<context>.<message>/1`):

- **Workflow:** commands `start-step`, `complete-step` (with an optional caveat), `tick-todo`, `set-focus` (an element,
  a sheet, a feature group, or nothing), `decide-gate` (approve, or send back with a note); events `step-started`,
  `step-completed`, `todo-added`, `todo-ticked`, `focus-set`, `gate-decided`.
- **Workspace commands:** `show` with what to show (a view: `project`, `sources`, `model`, `building`; or an editor:
  `calibration`, `labels`, `declaration`, `settings`), its subject (an element, a sheet or a feature group id, or none)
  and its title.

### §S2 Definition

`packages/domain/src/workflow/`: the **workflow definition** as data, shipped with the template
`residential/single-family-home` (D30): the seven phases (D26) and, in 0.1.0, the steps of the first three, each with
its step kind, the **agent role** that runs it (D43; validated against the harness's role catalogue), its checklist and
the view or editor it opens:

| Phase | Step | Kind | Role (D43) | Opens | Checklist (checked by the domain: ✓) |
|---|---|---|---|---|---|
| Plan onboarding | Intake the sources | K1 | orchestrator | `sources` | every source registered with its kind ✓; licences and provenance noted |
| Plan onboarding | Calibrate the sheets | K1 | orchestrator, with the sheet reader | `calibration` | every drawing sheet calibrated ✓; each calibration's check dimension within tolerance ✓ |
| Plan onboarding | Record the data tables | K1 | sheet reader, then CAD builder | `project` (data tables) | every table valid against `parti.tables/1` ✓; every row cites a calibrated sheet ✓ |
| Model | Build from data | K2 | CAD builder, then model checker | `model` | one item per feature group, ticked when its step record's checks pass ✓ |
| Model | Consolidate | K3 | CAD builder, then model checker; orchestrator (classify) | `model` | model read, revision current ✓; no object unclassified ✓, or each one noted |
| Declare | Derive the declaration | K4 | orchestrator | `declaration` | a draft derived from the current model ✓; labels proposed |
| Declare | Confirm the declaration | review gate | the user (orchestrator prepares) | `building` | every surface confirmed ✓; the gate approved |

A project that imports a declaration it wrote itself shows the three phases done (PRD-domain §11).

### §S3 Run

`decideWorkflow`, `evolveWorkflow`, `initialWorkflow`. Rules **W-1** one step is active at a time (starting another
is refused with `step-active`); **W-2** a step completes only when its checked items pass, or with a caveat (D26),
otherwise refused with `checklist-open` listing the items; a **review gate** step completes only with `gate-decided`
*approve*; *send back* reopens the step before it, with the note as a to-do; **W-3** the run's events are their own
stream. Starting a step yields `step-started`, its `todo-added` events (for *Build from data*, one per feature group
named in the facts) and a `show` for its view or editor, titled by the phase and what it shows (*Model · Level 1 ›
Walls*). `set-focus` yields `focus-set` and, when a step is active, its `show` again for the new subject.

### §S4 Checks

`checkWorkflow(run, facts)` ticks the checked items from **facts** passed in as data, computed by the gateway from its
queries (CR-PRT-012): sources and their kinds, sheets without a calibration, calibrations out of tolerance, invalid
tables or rows citing an uncalibrated sheet, the feature groups with the outcome of their latest step record, the model's
revision against the latest read, unclassified objects, the draft declaration's model revision, unconfirmed surfaces.
It yields `todo-ticked` for each item newly passing. The user ticks the others (FR-WF-15).

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema.
- [ ] The definition for `residential/single-family-home` has seven phases, and the first three the seven steps of §S2 in order, each naming its kind and its view or editor.
- [ ] Starting *Build from data* with facts naming feature groups `L0.walls` and `L0.slabs` yields `step-started`, a to-do for each, and a `show` of `model`.
- [ ] Starting a second step while one is active is refused with `step-active`.
- [ ] Completing *Calibrate the sheets* with a sheet uncalibrated is refused with `checklist-open` naming the item; with a caveat it completes and the caveat is in the event.
- [ ] `checkWorkflow` with facts in which `L0.walls`' latest step record passed and `L0.slabs`' failed ticks the first and not the second.
- [ ] *Confirm the declaration* completes only after `gate-decided` approve; *send back* with a note reopens *Derive the declaration* with the note as a to-do.
- [ ] A run on a building whose declaration the project wrote itself shows the three phases done.
- [ ] `set-focus` on feature group `L1.walls` while *Build from data* is active yields `focus-set` and a `show` titled `Model · Level 1 › Walls`.
- [ ] Replaying the run's events through `evolveWorkflow` gives the same state as the run.
- [ ] Caller-existence: `decideWorkflow` and `checkWorkflow` are called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

The other phases' steps (Design in 0.2.0, CR-PRT-036; Present in 0.3.0; World in 0.4.0; Deliver in 0.6.0), the option,
permission and trial gates, corrections, decisions and variants (with those phases, D26); running the step cycle (the
library, CR-PRT-024); the project agent issuing the workspace commands (CR-PRT-029); the definition as a user-editable
file (CR-PRT-056, 0.5.0).

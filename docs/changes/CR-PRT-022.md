# CR-PRT-022 — Workflow context and driver

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: **to be rewritten**: the definition and run of the first three phases (PRD-domain §11, v0.4); the Design phase's steps move to CR-PRT-036 (0.2.0).
**Priority:** High
**Depends on:** CR-PRT-002, CR-PRT-003
**Labels:** domain, workflow, schema
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §11 (DM-11), §5, §7; `docs/research/PRD-parti.md` D22, D26, D29, D30, FR-WF-14, FR-WF-15; `docs/Architecture.md` A2 (Workflow, Session), B4; `.lavish/storyboards.html` card `#wf-driver-proposal`, approved by the owner (24 November 2026)

## Context

In 0.1.0 the workflow step drives the Project Environment's workspace; the project agent takes over with the harness,
issuing the same commands (DM-11). This CR gives the Workflow context its 0.1.0 slice: a definition shipped with the
template, an event-sourced run, the checks the domain can make, and the messages that drive the page: the workspace
commands, the asset browser's signals and the interaction events. The domain is pure (R1): plain functions over plain
data, no input or output, no imports beyond `@parti/schema`.

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern, registry names `parti.<context>.<message>/1`):

- **Workflow:** commands `start-step`, `complete-step` (with an optional caveat), `tick-todo`, `set-focus` (a room ›
  surface, or nothing); events `step-started`, `step-completed`, `todo-added`, `todo-ticked`, `focus-set`.
- **Workspace commands:** `show` with what to show (a view: `project`, `bom`, `walkthrough`; or an editor: `labels`,
  `surface`, `settings`), its subject (an element id, or none) and its title.
- **Asset browser signals:** `set-filters`, `set-palette` (up to six colours), `mark-assets` (product ids), `note`
  (text), each with its target.
- **Interaction events** (`parti.interaction.*/1`): `pointed`, `selected`, `clipped`, each carrying its elements (ids,
  names, kinds, tags), the area (in the view's frame), the world bounds (mm), the CAD references, the view and the step.

### §S2 Definition

`packages/domain/src/workflow/`: the **workflow definition** as data, shipped with the template
`residential/single-family-home` (D30): the seven phases (D26) and the Design phase's steps, each with its step kind, its
checklist and the view or editor it opens:

| Step | Kind | Opens | Checklist (checked by the domain: ✓) |
|---|---|---|---|
| Catalogue intake | K1 | `project` (catalogue) | catalogue built ✓; sources and licences reviewed |
| Choose | K10 | `surface`, asset browser filtered for the focus | a shortlist entry for every room ✓ |
| Place and set out | K7, K8 | `surface` | a finish in every zone ✓; no sliver cut under 50 mm ✓ |
| BOM | K8 | `bom` | the BOM stated with its counting rule ✓; wastage agreed |
| Trial in the walkthrough | K12 | `walkthrough` | each room walked |

Plan onboarding, Model and Declare are marked done when the declaration is imported.

### §S3 Run

`decideWorkflow`, `evolveWorkflow`, `initialWorkflow`. Rules **W-1** one step is active at a time (starting another
completes nothing and is refused with `step-active`); **W-2** a step completes only when its checked items pass, or
with a caveat (D26), otherwise refused with `checklist-open` listing the items; **W-3** the run's events are their own
stream. Starting a step yields `step-started`, its `todo-added` events and a `show` for its view or editor, titled by
what it shows and its focus (*Design · Bath 1 › East wall*); the step *Choose* also yields `set-filters` for the focus.
`set-focus` yields `focus-set` and, when a step is active, its `show` again for the new subject.

### §S4 Checks

`checkWorkflow(run, facts)` ticks the checked items from **facts** passed in as data (zones without a finish, the
smallest cut in mm, whether the BOM states its counting rule, rooms without a shortlist entry, the catalogue's
presence), computed by the gateway from its queries (CR-PRT-012); it yields `todo-ticked` for each item newly passing.
The owner ticks the others.

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema, and a `pointed` event without its elements is refused with the schema's fault.
- [ ] The definition for `residential/single-family-home` has seven phases, and its Design phase the five steps of §S2 in order, each naming its view or editor.
- [ ] A run on a declared building shows Plan onboarding, Model and Declare done.
- [ ] Starting *Place and set out* with focus `bath1 › east wall` yields `step-started`, its to-dos and a `show` of `surface` titled `Design · Bath 1 › East wall`.
- [ ] Starting a second step while one is active is refused with `step-active`.
- [ ] Completing *Place and set out* with a zone unfilled is refused with `checklist-open` naming "a finish in every zone"; with a caveat it completes and the caveat is in the event.
- [ ] `checkWorkflow` with facts `{ zonesWithoutFinish: 0, smallestCutMm: 38 }` ticks "a finish in every zone" and not "no sliver cut under 50 mm".
- [ ] Starting *Choose* yields `set-filters` for the focus's surface kind.
- [ ] `set-focus` while *Place and set out* is active yields `focus-set` and a `show` for the new surface.
- [ ] Replaying the run's events through `evolveWorkflow` gives the same state as the run.
- [ ] Caller-existence: `decideWorkflow` and `checkWorkflow` are called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

The other phases' steps, gates, corrections, decisions and variants (later, D26); the project agent issuing the
workspace commands (with the harness, D21); the definition as a user-editable file.

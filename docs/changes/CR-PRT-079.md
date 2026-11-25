# CR-PRT-079 — SDK: human-use checks on the built model

**Status:** PENDING (spec drafted 2026-11-25; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-005, CR-PRT-022, CR-PRT-024, CR-PRT-025, CR-PRT-026
**Labels:** sdk, library, checks, model
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-parti.md` D26, D27, D42; `docs/research/DN-workflow-shape.md` §11 (2026-11-25); JohnnyHouse #1690 (Runbook T5.4, T12.12; its DN-010 §E2)

## Context

In JohnnyHouse's walkthrough nobody could enter a bathroom: each door was 650 mm clear, and the model matched the
plans. The owner ruled that this check belongs to the CAD stage, generic in Parti's SDK and applied to each project's
model (D42). It measures what was built, not the tables it was built from (one of JohnnyHouse's tables was stale), and a
failure is a finding on the design, so it comes with what the opening could become and goes to the owner and the
architect.

## Scope

### §S1 The check figure and the pass figures (project data)

`packages/schema/v1/human-use.schema.json` (`parti.human-use/1`), the project's `parti/checks/human-use.json`: the
**check figure** (a name, its height, its width at the shoulders and at the widest, its source) and the **pass
figures** by kind (door clear width and clear height, passage clear width, stair clear width and headroom), each with
its source and note (country, use). Parti ships no default figure: a project without the file gets the fault
`no-check-figure`, and the check reports itself not run, never passed.

### §S2 The checks (`parti.tools.checks.human_use`)

Registered with CR-PRT-024's `@parti.tools.check`, each returning a check result (pass or fail, the measured values,
the worst offender, what it did not prove), measured on the model inventory (CR-PRT-025) and the model's objects and
classes (CR-PRT-026):

- **Doorways** (objects of class Openings › Door and Gate, CR-PRT-005): the **clear width**, between the finished
  faces of the linings with the leaf open at 90° (the leaf's thickness on its hinge side subtracted; a sliding or pocket
  leaf subtracts nothing), and the **clear height** to the head lining. A door whose leaf or linings cannot be told
  apart from its bodies is reported as not proved, naming them.
- **Passages:** in rooms whose use is circulation (hall, corridor, landing; PRD-domain room use), the narrowest clear
  width between opposite wall faces, and where it is.
- **Stairs** (Structure › Stair): the clear width between walls or balustrades, and the headroom above the pitch line
  to the lowest body over it.

### §S3 The widening survey

For each failed doorway: along its wall on each side, the free distance to the first thing that stops a wider
opening (another opening, a wall end or junction, a column, a fixture or joinery body within the leaf's swing, the
open leaf's pocket), giving the **widest clear width it can reach** and what limits it, by object id and class. A
failed passage names the bodies that make its narrowest point.

### §S4 In the workflow

The definition (CR-PRT-022) gains, in the Model phase, the check on the feature groups tagged `openings` and `joinery`
(their step's `checks`), and a **review gate** *Human use*: its checklist is the findings, each decided by the owner
(approve as it is, with a reason) or sent back (to widen or re-plan). A step record (CR-PRT-024) carries the human-use
results like any other check, so the Model view shows them (CR-PRT-032).

### §S5 Test data

`one_house_model()` (CR-PRT-025) gains: a bathroom door of 750 mm opening with 50 mm linings and a 40 mm leaf (650 mm
clear) whose widening is stopped at 735 mm by a column, a second door that can reach 800 mm before a wall end, a
corridor with a 790 mm pinch at a built-in, and a stair; with a synthetic `human-use.json` (pass 800 mm, source
"synthetic").

## Acceptance criteria

- [ ] (module) The doorway check on `one_house_model()` fails the bathroom door at 650 mm clear against 800 mm, the worst offender that door; its survey gives 735 mm, limited by the column's id.
- [ ] The second door's survey reaches 800 mm, limited by the wall end.
- [ ] The passage check fails at 790 mm and names the built-in; the stair's width and headroom are reported with their values.
- [ ] Without `parti/checks/human-use.json` the check reports `no-check-figure` and not run; it never passes.
- [ ] The doorway check measures the bodies: with the walls table stating 800 mm for that door, it still reports 650 mm.
- [ ] (integration, the fake CAD session) `run_step` for a group tagged `openings` records the human-use results in its step record, and a failure opens the *Human use* gate, which `decide-gate` approves with a reason.
- [ ] Caller-existence: `run_step` runs the human-use checks for the tagged groups (CR-PRT-024), and the complete script `check_human_use` calls them (CR-PRT-080), reviewed at VERIFY.
- [ ] (live, workstation) On JohnnyHouse's model, read in place, the four bathroom doors fail at 650 mm clear with surveys of about 800, 800, 800 and 735 mm, as JohnnyHouse measured by hand.

## Estimated size

8 points.

## Non-goals

Turning circles, ramps, grab rails and the codes of particular countries (a project's pass figures carry its rules);
the walkthrough's character as the same figure (0.4.0); widening the openings (the project's agent, through the
correction loop).

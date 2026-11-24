# CR-PRT-032 — Project Environment: the Model view

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012, CR-PRT-021, CR-PRT-026
**Labels:** page, ui, project-environment, model
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` D22, D25, D26, D31, D33; `docs/research/PRD-domain.md` §2.1a, §2.6, §6, §11; `.lavish/storyboards.html` storyboards 0 and 1, approved by the owner (24 November 2026)

## Context

In the Model phase the user watches the model being built from data, feature group by feature group, and sees what
Parti read from it: its objects, their classes, what changed. Parti augments the CAD and never duplicates its editing
(D22 (f)): the model stays in SolidCraft, and the Model view shows the step records, the inventory and its
classification beside it. It is the workspace component `model` (CR-PRT-021), reading the gateway's projection only.

## Scope

### §S1 Feature groups

A list of the feature groups with each one's latest **step record** (CR-PRT-024): passed or failed, the checks with
their numbers in the display units, the worst offender, what was not checked, the files written; earlier records on
request. A group that failed is marked, and its worst offender is selectable (it selects the body).

### §S2 The plan

A 2D plan per level drawn from the inventory: each object's footprint (its plane faces' outlines where it has them,
else its bounds), coloured by class, unclassified objects hatched; a level picker. The 2D tools of the shell
(CR-PRT-021 §S4) apply: pointing and selecting send the interaction events and `select` (CR-PRT-008) with the objects'
labels; the selection is shown in the plan and the object list together.

### §S3 Objects

A table of the model objects: id, CAD name (as a reference), feature group, class or *unclassified*, effective
material, with a filter for the unclassified. A class is set from the classification's first level of each branch
(CR-PRT-005), sending `classify-object`; a label's name and tags are edited as in the labels editor. The faces of a
selected object are listed with their ids, kinds and areas.

### §S4 Revision

A bar with the model's revision and when it was read; a failed read shows the last inventory marked stale with the
fault (M-3); the changes from the previous revision (CR-PRT-009) are listed and shown in the plan (added, removed,
renamed, split, material changed).

### §S5 Cues

Up to five suggestions (D22) from the view's state: *Classify the n unclassified objects*, *L0.slabs failed its volume
check: show the worst offender*, *The model changed: derive the declaration again*.

## Acceptance criteria

- [ ] (module, the session-channel port faked) With `one_house_model()` read and step records for `L0.walls` (passed) and `L0.slabs` (failed), the feature group list shows both, the failed one marked with its worst offender and its volume in the display units.
- [ ] The plan of level 0 draws one footprint per level-0 object; an unclassified object is hatched.
- [ ] Rectangle-selecting two wall footprints sends one `selected` interaction event and one `select` naming both objects' ids.
- [ ] Setting `structure.slab` on an unclassified slab in the object table sends `classify-object`; on the event, the hatch goes.
- [ ] After `model-revised` for the second revision (G4), the bar shows the new revision and the plan marks the split, the renamed and the re-materialled objects.
- [ ] A `model-read-failed` shows the stale marker with its fault, and the plan keeps the last inventory.
- [ ] With three unclassified objects, the cues include *Classify the 3 unclassified objects*, and clicking it filters the table to them.
- [ ] Caller-existence: the shell renders `model` on `show model` (CR-PRT-021), reviewed at VERIFY.

## Estimated size

8 points.

## Non-goals

A 3D view of the model in the page (the CAD shows it; the walkthrough comes later); editing the model (it stays in
SolidCraft, D22 (f)); the step cycle's controls beyond reading its records (`parti-axi model build`, the harness).

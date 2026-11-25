# CR-PRT-033 — Project Environment: the Sources and Building views

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012, CR-PRT-021, CR-PRT-027, CR-PRT-028
**Labels:** page, ui, project-environment, sources, building
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` D22, D25, D26 (K1), D33; `docs/research/PRD-domain.md` §1, §2.3, §2.7, §6, §11; `.lavish/storyboards.html` storyboards 0 and 1, approved by the owner (24 November 2026)

## Context

Plan onboarding and Declare are where the user's judgment matters most in 0.1.0: is each sheet read at the right scale,
and is the building Parti derived the one they designed? This CR gives the workspace its components for both: the
**Sources** view and the **calibration** editor (CR-PRT-028), the **declaration** editor and the **Building** view
(CR-PRT-027, CR-PRT-009). They read the gateway's projection only and send the domain's commands.

## Scope

### §S1 Sources

The view `sources`: the sources by kind (sheets with their level and calibration state, renders, documents, data tables
with their faults), a sheet shown at full size with pan and zoom (images, and PDF pages through a PDF renderer), a
revised source marked with what it makes stale.

### §S2 Calibration

The editor `calibration` for one sheet: the user picks the two ends of a known dimension on the sheet and types its
length in any unit (parsed by `parseLength`, D25), then the check dimension the same way; the measured and known
lengths are shown in the display units with the tolerance; *Calibrate* sends `calibrate-sheet`. A refusal
`calibration-check-failed` shows both lengths and offers *Record with a caveat*. A render offers no calibration.

### §S3 The declaration

The editor `declaration`: the derived draft (CR-PRT-027) per level: the rooms with their surfaces, each surface with its
id, side, anchor, size in the display units and openings, and its CAD faces as references; the draft's faults
(`unexplained-void`, `room-without-floor`, …) and the rules' breaches listed, each selecting what it names. A surface's
**elevation** is drawn in its face frame (DM-6) with its openings. **Corrections** (id, name, aliases, side, use; an
opening added or removed) are kept with the draft until confirmed; *Derive again* sends `derive-declaration`.

### §S4 The building

The view `building`: the surfaces to confirm one by one or all together, with their corrections; *Confirm* sends
`confirm-declaration`; a `stale-draft` refusal offers *Derive again*. After confirmation, the building's revisions
(CR-PRT-009 `history`) with their changes, each revision's surfaces listed as added, removed, resized or moved.

### §S5 Cues

From the view's state: *2 sheets are not calibrated*, *Row 14 of walls cites an uncalibrated sheet*, *3 surfaces wait
for confirmation*, *The draft is older than the model: derive again*.

## Acceptance criteria

- [ ] (module, the session-channel port faked) With CR-PRT-003's sources registered, the Sources view lists two sheets (uncalibrated) and one render, and shows the plan sheet at full size.
- [ ] In the calibration editor, picking the plan's dimension-line ends from its sidecar and typing `4' 6"` and the check's length sends `calibrate-sheet` with millimetres; a 2 % off check shows both lengths and *Record with a caveat*.
- [ ] The render offers no calibration.
- [ ] The declaration editor shows the draft derived from `one_house()`'s model with every room and surface; an east wall's elevation is drawn with its openings at their face-frame positions.
- [ ] A draft with an `unexplained-void` lists it, and clicking it selects the face it names.
- [ ] Renaming a surface, then *Confirm* on it, sends `confirm-declaration` with the correction; on `declaration-confirmed` the Building view lists revision 1 with its surfaces added.
- [ ] A `stale-draft` refusal offers *Derive again*, which sends `derive-declaration`.
- [ ] Caller-existence: the shell renders `sources`, `calibration`, `declaration` and `building` on their `show` (CR-PRT-021), reviewed at VERIFY.

## Estimated size

8 points.

## Non-goals

Reading values off a sheet automatically (the sheet reader, CR-PRT-081); skewed or non-uniform scans (CR-PRT-065,
0.6.0); polygonal floors and sloped faces (later); a 3D view of the building.

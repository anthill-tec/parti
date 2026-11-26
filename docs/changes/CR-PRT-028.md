# CR-PRT-028 — Plan onboarding: sources and calibration

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-002, CR-PRT-003
**Labels:** domain, workflow, sources, units
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/PRD-domain.md` §1, §7, §8 (v0.4); `docs/research/PRD-parti.md` D25, D26 (K1), D33; `docs/research/DN-ubiquitous-language.md` (Source, Drawing sheet, Calibration, Data table)

## Context

The workflow's first phase, Plan onboarding, takes in the architect's material before anything is built: most of the
prototype's rework came from building before every sheet had been read (`DN-pipeline-prototype-johnnyhouse.md`). This
CR gives the domain its **sources** (drawing sheets, renders, documents), each sheet's **calibration** from a known
dimension, re-checked against a second one (D25), and the record of the **data tables** with the sheets their rows cite.
The data tables' format and their use are CR-PRT-024's; this CR records them as sources of the model. The domain is
pure (R1): the gateway reads the files and passes their hashes and sizes in as data.

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern): commands `register-source`, `calibrate-sheet`, `record-data-table`; events
`source-registered`, `source-revised`, `sheet-calibrated`, `data-table-recorded`; query `sources`. They are stored in
the `sources` log (CR-PRT-010).

### §S2 Sources

`packages/domain/src/sources/` (the Workflow context's sources): `register-source` names a file in the target project
(path relative to it), its content hash and its **kind**: a **drawing sheet** (`plan` | `elevation` | `section` |
`detail`, with its level when it has one, and its page for a multi-page PDF), a **render** (a texture and style cue,
never calibrated, D33), or a **document** (a schedule, a specification). Registering the same path with another hash
yields `source-revised`; the sheet's calibration becomes **stale** and every data table citing it is listed as to be
re-checked.

### §S3 Calibration

`calibrate-sheet` gives two points on the sheet (in its own units: pixels for an image, PDF points for a PDF page) and
the known length between them in millimetres, and a **check dimension**: two more points and their known length. The
domain computes the sheet's **scale** (mm per sheet unit; one isotropic scale per sheet) and measures the check
dimension with it: within the tolerance (the project's, default 0.5 %) it yields `sheet-calibrated` with both values;
outside it, the calibration is refused with `calibration-check-failed`, giving the measured and known lengths, unless
the user records it with a caveat (D26). A render cannot be calibrated (`not-calibratable`). `recheck(calibration,
measuredMm)` returns a check result for the same dimension measured later (in the model, on every import and export:
the glossary's Calibration), used by the model read (CR-PRT-025).

`parti.units.Calibration` (the library, D25) applies a recorded calibration in Python (sheet units to millimetres and
back), so a step reading a sheet uses the same scale; both sides read the calibration in the event's format.

### §S4 Data tables as sources

`record-data-table` names a data table file, its hash and, per row, the sheets it cites (passed in by the caller, which
reads the file with CR-PRT-024's library). It yields `data-table-recorded`, listing as faults the rows citing a sheet
that is not registered (`unknown-source`), not calibrated or stale (`uncalibrated-source`), and lists the sizes whose source is a rule or an assumption (D42) as
**to ratify**. The faults do not refuse the record: they are what the workflow's checklist reports (CR-PRT-022).

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema.
- [ ] Registering CR-PRT-003's two sheets and its render gives three sources of the right kinds; registering the plan again with another hash yields `source-revised` and marks its calibration stale.
- [ ] Calibrating each of CR-PRT-003's sheets from its first dimension line gives a scale whose check dimension measures within 0.5 % of its known length, and `sheet-calibrated` carries both values.
- [ ] A check dimension 2 % off is refused with `calibration-check-failed` naming the measured and known lengths; with a caveat it is recorded and the caveat is in the event.
- [ ] Calibrating the render is refused with `not-calibratable`.
- [ ] A data table whose rows cite the calibrated plan, the stale plan and an unknown sheet is recorded with one `uncalibrated-source` and one `unknown-source` fault, naming their rows.
- [ ] `recheck` of a 3000 mm dimension measured at 3010 mm passes at 0.5 % tolerance and fails at 0.2 %, giving the measured value.
- [ ] `parti.units.Calibration` and the domain convert the same sheet points to the same millimetres within 0.01 mm (a shared fixture run by both suites).
- [ ] Caller-existence: `decideSources` is called from `packages/gateway/src` (CR-PRT-012 VERIFY); `parti.units.Calibration` from the library's step cycle (CR-PRT-024 VERIFY).

## Estimated size

5 points.

## Non-goals

Reading or rendering the sheets (the Sources view, CR-PRT-033); the PDF format converters and skewed or non-uniform
scans (CR-PRT-065, 0.6.0); the data tables' format and validation (CR-PRT-024); the agent reading values off a sheet (the
sheet reader, CR-PRT-081).

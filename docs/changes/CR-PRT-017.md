# CR-PRT-017 — End-to-end 0.1.0: the building from CAD

**Status:** PENDING (spec drafted 2026-11-23; rewritten 2026-11-24 for the roadmap; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten: the end-to-end run of the first three phases (the building from CAD); it also sets up the e2e tier (CR-PRT-001).
**Priority:** High
**Depends on:** CR-PRT-013, CR-PRT-023, CR-PRT-030, CR-PRT-031, CR-PRT-032, CR-PRT-033
**Labels:** e2e, acceptance
**Phase:** 0.1.0 · wave 6
**Design reference:** `docs/research/PRD-parti.md` Q9, D23, D33; `docs/research/PRD-domain.md` §1, §11; `docs/research/DN-test-strategy.md` (E2E, live tests); `docs/research/DN-pipeline-prototype-johnnyhouse.md`

## Context

0.1.0 is done when a fresh target project goes from the architect's sheets to a confirmed building derived from its CAD
model, through the Project Environment, the harness and `parti-axi` together (D33), and when JohnnyHouse's own model
gives the building its hand-written declaration describes.

## Scope

### §S1 The e2e tier

This CR sets up the **e2e tier** (CR-PRT-001 leaves it out, owner 2026-11-24): `tests/e2e/__init__.py` and its
`*_tests` folder, the root script `test:e2e` if a Bun e2e test is added, and its run in CI (DN-test-strategy). In CI the
CAD is CR-PRT-024's fake session at the `CadSession` port, replaying `one_house_model()`'s reports (selected by the
test configuration, never by production code), the harness runs on the scripted model runner, and the bus is `local`.

### §S2 The flow

`tests/e2e/test_release_0_1_0.py` (driven by the Python client, a real browser through Playwright): `parti-axi init
--no-nai` on a temporary target project, `parti-axi open` and `agent start`; then, through the Project Environment and
the guided chat: the sources registered and both sheets calibrated in the calibration editor; `one_house()`'s tables
recorded; the feature groups built (the agent running the steps), each step record shown passed in the Model view; the
model read, its objects classified by the rules, one by an accepted proposal; the declaration derived, one surface
renamed in the declaration editor, the gate approved and the declaration confirmed; then the model's second revision
(G4) read, the draft marked stale, derived again and confirmed. At each step the page, the logs and `parti-axi state`
agree. Restarting the gateway and the harness leaves everything as it was.

### §S3 Workstation acceptance

Tagged `live` (`PARTI_LIVE=1`), run on the workstation and reported to Crucible:

- The same flow with SolidCraft headless and a real model runner.
- **JohnnyHouse:** its model is read in place (never copied, nothing written to it: the write-back is off), its
  declaration derived and compared with its hand-written `parti/building/declaration.json` by `compareDeclarations`:
  the four bathrooms' rooms and surfaces (4 rooms, 20 surfaces) agree, or the differences are reported to JohnnyHouse.
  Its migrated `cad/gen` run is CR-PRT-024's acceptance.
- With Nai on the workstation, the flow once more with `bus = "nai"` (CR-PRT-031).

### §S4 CI browser

The release workflow's test jobs install a headless browser so §S2 runs in CI.

## Acceptance criteria

- [ ] §S2's flow passes in CI, each step asserting the page, the logs and `parti-axi state`.
- [ ] After the restarts, the `building` and `model` queries and `model/inventory.json` are as before them (the snapshot byte-identical).
- [ ] The confirmed building equals the G6 oracle with the one renamed surface; its second revision lists the changes the second model revision caused.
- [ ] In the flow the harness sends no `decide-gate` or `confirm-declaration` (H-1); those come from the page.
- [ ] (live, workstation) The flow passes with SolidCraft headless.
- [ ] (live, workstation) JohnnyHouse's derived declaration agrees with its hand-written one on 4 rooms and 20 surfaces, or the differences are reported to JohnnyHouse over Sandesh; no file of JohnnyHouse's changes.
- [ ] (reviewed, not tested) The CI run shows the e2e tier green.

## Estimated size

5 points.

## Non-goals

The Design phase and the finishes (0.2.0); Blender and Unreal (0.3.0, 0.4.0); testing Nai itself (Nai's).

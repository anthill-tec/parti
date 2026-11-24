# CR-PRT-017 — End-to-end 0.1.0

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-013, CR-PRT-015, CR-PRT-016
**Labels:** e2e, acceptance
**Phase:** 0.1.0 · wave 5
**Design reference:** `docs/research/PRD-parti.md` Q9, D23; `docs/research/PRD-domain.md` §1; `docs/research/DN-test-strategy.md` (E2E)

## Context

0.1.0 is done when the finish tool works end to end on a fresh target project, through the page, the mock scene and
`parti-axi` together.

## Scope

### §S1 E2E suite

This CR sets up the **e2e tier** (CR-PRT-001 leaves it out, owner 2026-11-24): `tests/e2e/__init__.py` and its
`*_tests` folder, the root script `test:e2e` if a Bun e2e test is added, and its run in CI once a browser is
provisioned there (DN-test-strategy).

`tests/e2e/test_release_0_1_0.py` (driven by the Python client, a real browser through Playwright): `parti-axi init`
on a temporary target project, then `parti-axi open`; synthetic catalogue built; `oneBath` imported; then, through
the Project Environment: filter, shortlist,
select the east wall, add a dado band, place two products with their setting-out, read the quantities, save a scheme, change and apply it back, set the weather;
the scene reflects each step; `parti-axi state` agrees; restart the gateway and everything is still there; re-import
the building without its floor and resolve the follow-ups.

### §S2 Local acceptance on JohnnyHouse

A tagged `live` test reads JohnnyHouse's `parti/building/declaration.json` and records in place (never copied), imports
them into a temporary target project, and checks the four bathrooms' counts (4 rooms, 20 surfaces). Runs on the
workstation only, reported to Crucible.

### §S3 CI browser

The release workflow's test jobs install a headless browser so §S1 runs in CI.

## Acceptance criteria

- [ ] §S1's flow passes in CI, each step asserting the page, the scene and `parti-axi state`.
- [ ] After the gateway restart, `design.json` is byte-identical to before it.
- [ ] (live, workstation) JohnnyHouse's declaration imports with 4 rooms and 20 surfaces and no faults, or the faults are reported to JohnnyHouse.
- [ ] (reviewed, not tested) The CI run shows the e2e tier green.

## Estimated size

5 points.

## Non-goals

Blender, Unreal and the workflow steps beyond finishes (later releases).

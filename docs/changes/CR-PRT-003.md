# CR-PRT-003 — Synthetic fixtures

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (0.1.0 = the building from CAD); filed on the Crucible board.
**Priority:** High
**Depends on:** CR-PRT-001, CR-PRT-002
**Labels:** fixtures, testing
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/DN-test-strategy.md` §Fixtures; `docs/research/PRD-parti.md` NFR-10; `docs/research/PRD-domain.md` §2.4, §4.1

## Context

The repository is public, so tests use synthetic data only (NFR-10): generated buildings and products, plain-colour
swatches, never makers' images nor a target project's data.

## Scope

### §S1 Building generator

`packages/schema/test-support/buildings.ts` exports `makeBuilding(spec)` returning a valid `parti.building/1`
declaration from a compact spec (rooms with width, depth, height and level; openings and regions per side), computing
anchors so that each wall runs left to right as seen from inside (B-4). Named presets: `oneBath` (one room, four walls,
floor, one door, one mirror region), `twoLevels` (three rooms on two levels), `faulty` (one fault of each of B-1, B-2,
B-4, labelled).

### §S2 Product generator

`makeProducts(n, seed)` returns `n` deterministic synthetic finishes of all seven kinds (tile, wood veneer, laminate, paint, metal, exposed, glaze), covering every
filterable field of PRD-domain §4.3 and the kind-specific fields of §4.1 (scans with real size and grain direction,
stains, licences, paint sheens and effects, colour-only veneers and laminates) (uses, surfaces, makers, colours across the wheel, lightness, warm and cool, patterns, finish classes,
sets with pairs, sizes), with swatch and scan images generated as plain-colour PNGs into a temporary folder (none for paint, metal, exposed or glaze).

### §S3 Shared to Python

The same presets are written as JSON files into `tests/fixtures/` by `bun run --filter @parti/schema fixtures`, so the
Python tests read identical data.

### §S4 The building from CAD (0.1.0's roadmap)

In `tests/fixtures/cad/`, written by `python -m parti.testing.fixtures` (Python, since the SDK is Python):

- **Data tables** for a synthetic two-level house (`oneHouse`): levels, the wall set-out (lines, thickness, height),
  slabs, openings and a few named parameters, in the shape the SDK reads (CR-PRT-024), with the expected volume, bounds
  and body count of each feature group.
- **A model inventory** of the same house as SolidCraft would report it (bodies, components, part properties with a
  class on some and none on others, materials with their looks, faces with their normals and areas), for the model
  inventory's and the model's tests (CR-PRT-025, CR-PRT-026) without SolidCraft; its schema arrives with CR-PRT-025.
- **Drawing sheets**: two plain PNG sheets (a plan and an elevation) with a dimension line of known length and known
  pixel ends, and one render, for Plan onboarding's calibration (CR-PRT-028).

All of it is generated from code, never copied from a target project.

## Acceptance criteria

- [ ] `validateDeclaration(makeBuilding(p))` is ok for `oneBath` and `twoLevels`.
- [ ] `faulty` carries exactly one breach of each of B-1, B-2 and B-4, each identified by a `label` field the building context's tests use.
- [ ] `oneBath`'s east wall anchor runs north to south (start y > end y), its west wall south to north.
- [ ] `makeProducts(200, 1)` is deeply equal across two calls, every value of each filter field in PRD-domain §4.3 appears at least once, and each of the seven kinds appears at least 20 times; some tiles state `sizeIncludesJoint` and `piecesPerBox`.
- [ ] At least two veneers share one source scan with different stains, and no paint or metal has an image.
- [ ] Every swatch PNG is a single colour of the product's declared main colour (pixel check on three points).
- [ ] The JSON files in `tests/fixtures/` equal the generators' output (a test regenerates and compares).
### §S4
- [ ] The `oneHouse` tables' expected volumes equal the sum of their boxes and extrusions computed independently in the test, and its inventory names the same bodies as the tables' feature groups.
- [ ] The inventory has at least one body with a class, one without, one face whose material overrides its body's, and one component whose material its bodies inherit.
- [ ] Each sheet's dimension line, measured from the PNG's pixels, lies within one pixel of its declared ends.

## Estimated size

5 points (3 before the roadmap's §S4).

## Non-goals

Real JohnnyHouse data (read in place by live tests and CR-PRT-017's workstation acceptance run, never committed); a
SolidCraft design file (built from the tables by CR-PRT-024's live test).

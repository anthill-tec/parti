# CR-PRT-003 — Synthetic fixtures

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-001
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

`makeProducts(n, seed)` returns `n` deterministic synthetic finishes of all five kinds (tile, wood veneer, laminate, paint, metal), covering every
filterable field of PRD-domain §4.3 and the kind-specific fields of §4.1 (scans with real size and grain direction,
stains, licences, paint sheens) (uses, surfaces, makers, colours across the wheel, lightness, warm and cool, patterns, finish classes,
sets with pairs, sizes), with swatch and scan images generated as plain-colour PNGs into a temporary folder (none for paint or metal).

### §S3 Shared to Python

The same presets are written as JSON files into `tests/fixtures/` by `bun run --filter @parti/schema fixtures`, so the
Python tests read identical data.

## Acceptance criteria

- [ ] `validateDeclaration(makeBuilding(p))` is ok for `oneBath` and `twoLevels`.
- [ ] `faulty` carries exactly one breach of each of B-1, B-2 and B-4, each identified by a `label` field the building context's tests use.
- [ ] `oneBath`'s east wall anchor runs north to south (start y > end y), its west wall south to north.
- [ ] `makeProducts(200, 1)` is deeply equal across two calls, every value of each filter field in PRD-domain §4.3 appears at least once, and each of the five kinds appears at least 20 times.
- [ ] At least two veneers share one source scan with different stains, and no paint or metal has an image.
- [ ] Every swatch PNG is a single colour of the product's declared main colour (pixel check on three points).
- [ ] The JSON files in `tests/fixtures/` equal the generators' output (a test regenerates and compares).

## Estimated size

3 points.

## Non-goals

Real JohnnyHouse data (used in place by CR-PRT-011 and CR-PRT-017's local acceptance run, never committed).

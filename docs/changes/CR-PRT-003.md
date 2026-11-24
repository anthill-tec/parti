# CR-PRT-003 — Synthetic fixtures

**Status:** PENDING (spec drafted 2026-11-23; gap analysis 2026-11-24 by Track 2, findings G1–G14 folded in or moved; the owner's rulings on F1, F2 and G13; spec pre-review due)
**Pre-review:** due — touches another project's surface (`parti.testing` ships in the public `parti` wheel); needed the owner's rulings.
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (0.1.0 = the building from CAD); filed on the Crucible board.
**Priority:** High
**Depends on:** CR-PRT-001, CR-PRT-002
**Labels:** fixtures, testing
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/DN-test-strategy.md` §Fixtures; `docs/research/PRD-parti.md` NFR-10, D25; `docs/research/PRD-domain.md` §2.4, §2.5

## Context

The repository is public, so tests use synthetic data only (NFR-10): generated buildings and drawing sheets, never
makers' images nor a target project's data. **Each fixture arrives with the CR that defines its format** (owner,
2026-11-24): this CR makes the fixtures whose formats exist by wave 1 (the building declaration, CR-PRT-002) and the
drawing sheets, whose shape is plain images; the CAD data tables come with CR-PRT-024, the model inventory with
CR-PRT-025 and the test products with CR-PRT-005 (see "Moved to other CRs").

## Scope

### §S1 Building generator

`packages/schema/src/test-support/buildings.ts` (exported through `@parti/schema/test-support`) exports
`makeBuilding(spec)` returning a valid `parti.building/1` declaration from a compact spec (rooms with width, depth,
height and level; openings and regions per side), computing anchors so that each wall runs left to right as seen from
inside (B-4). Named presets: `oneBath` (one room, four walls, floor, one door, one mirror region), `twoLevels` (three
rooms on two levels).

`makeFaulty()` returns `{ declaration, breaches }`: a declaration that is valid against the schema but breaks the
rules, and the list of its breaches as `{ rule, code, path }`, one each of B-1, B-2 and B-4. The breaches are held
outside the declaration (the schema is closed, and *label* is the glossary's term for an element's name). Each breach is
placed so that it breaks only its own rule.

### §S2 Shared to Python

The same presets are written as JSON files into `tests/fixtures/` by `bun run --filter @parti/schema fixtures`, so the
Python tests read identical data.

### §S3 Drawing sheets for Plan onboarding

`parti.testing.fixtures.write_sheets(out_dir)` (in the `parti` library, so a target project's tests may use it; it
writes only synthetic data, and the folder is a required parameter) writes, and `python -m parti.testing.fixtures
<out_dir>` runs it; the repository's copy is in `tests/fixtures/cad/`:

- **Two sheets**, a plan and an elevation, as PNGs: black lines on a plain white background. Each carries **two
  dimension lines** in a named colour: one to calibrate from and one to check the calibration against (D25: a scale is
  re-checked; K1 cross-checks each value on two sources).
- **A sidecar JSON per sheet**: its kind (`plan` | `elevation`), its level, and for each dimension line its known
  length in millimetres and its pixel ends.
- **One render**, a PNG with a sidecar of kind `render` and no dimension lines: a render is a texture and style cue,
  never calibrated (D33).

## Acceptance criteria

### §S1
- [ ] `validateDeclaration(makeBuilding(p))` is ok for `oneBath` and `twoLevels`.
- [ ] `validateDeclaration(makeFaulty().declaration)` is ok (valid against the schema), and `breaches` holds exactly one breach of each of B-1, B-2 and B-4, each with its rule, code and path.
- [ ] Each breach in `makeFaulty()` breaks only its own rule: removing any one breach removes exactly that rule's fault (checked against the rules' expected codes; the building context's tests run the rules themselves, CR-PRT-004).
- [ ] `oneBath`'s wall anchors run left to right as seen from inside on all four sides: east north to south (start y > end y), west south to north (start y < end y), north west to east (start x < end x) and south east to west (start x > end x), with the directions stated in a test table; `twoLevels`' upper rooms carry the upper level's `floor_z`.
### §S2
- [ ] The JSON files in `tests/fixtures/` equal the generators' output (a test regenerates and compares).
### §S3
- [ ] On each sheet, both dimension lines, found by scanning the PNG's rows or columns for the named colour, lie within one pixel of their declared ends; the calibrating line's scale applied to the checking line gives its known length within 0.5 %.
- [ ] Each sidecar validates against a schema in the test (kind, level, lines with length and pixel ends); the render's sidecar is of kind `render` and has no lines.
- [ ] `write_sheets(tmp)` called twice gives the same files (PNGs compared as decoded pixels and their size, not as bytes), equal to those in `tests/fixtures/cad/`.
- [ ] Calling `write_sheets` without a folder fails with a usage error, and nothing is written.

## Moved to other CRs (owner, 2026-11-24; Track 2's findings carried with them)

- **The CAD data tables** for a synthetic two-level house (`oneHouse`): to **CR-PRT-024**, with the format the SDK
  reads and its contract tests. Carried: the expected volume needs a stated edge rule (no overlaps by construction, or
  the union) and bounds need their own criterion (G1); *feature group*, *data table*, *model inventory* and *drawing
  sheet* go into the glossary (G2); how bodies are named from the tables is decided there (G3); the tables also carry
  the rooms (identity, level, `floor_z`) and an expected `parti.building/1` for `oneHouse`, the oracle for
  CR-PRT-027's derivation (G6).
- **The model inventory**: to **CR-PRT-025**, as two documents: SolidCraft's raw report (the translator's input) and
  Parti's `parti.model/1` (its output, CR-PRT-026's input) (F2). Carried: a second revision of it (a body split, a body
  renamed, a material changed) for the live re-read and CR-PRT-009 (G4); SolidCraft's units with the declared
  transform (G5).
- **The test products** (`makeProducts`): to **CR-PRT-005**, with the product record and the classification. Carried:
  open or continuous filter fields need an enumerated set or buckets, and *colour strength* and *role in a set* are
  among them (G14).

## Estimated size

5 points (about 4 after the moves, rounded up to the board's scale).

## Non-goals

Real JohnnyHouse data (read in place by live tests and CR-PRT-017's workstation acceptance run, never committed); a
SolidCraft design file (built from the tables by CR-PRT-024's live test); test products, data tables and the model
inventory (moved, above).

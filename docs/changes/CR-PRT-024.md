# CR-PRT-024 — SDK: the step cycle and the SolidCraft translator

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run; to JohnnyHouse for a line-by-line read, as promised on Sandesh #1676)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-001, CR-PRT-003
**Labels:** library, python, workflow, cad, solidcraft
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-parti.md` D25, D26, D27, D33, D34; `docs/research/PRD-domain.md` §2.6 (v0.4); `docs/Architecture.md` B3 (`parti`); `docs/research/DN-pipeline-prototype-johnnyhouse.md` (the prototype; "What the step cycle must also cover"); `docs/research/DN-test-strategy.md` (contract and live tests)

## Context

The prototype built its model from data tables by about thirty generator scripts, each turning tables into SolidCraft
command batches (`DN-pipeline-prototype-johnnyhouse.md`). The `parti` library (D27) generalises that into the **step
cycle** every step runs: read the sources, write the data, generate, apply, check against the expected numbers,
checkpoint, record; on a failed check, fix the data, never the output (D26). This CR builds the cycle, the **data
tables** format, the **SolidCraft translator** for the Model phase's feature groups, and the checks. JohnnyHouse moves
its `cad/gen` scripts onto it once this CR merges; its migrated run is the workstation acceptance (Sandesh #1675). Until
the SolidCraft plugin (CR-PRT-074, 0.2.0), the library drives SolidCraft through its MCP server (D34).

## Scope

### §S1 Data tables (`parti.tables/1`)

A JSON Schema in `packages/schema/v1/tables.schema.json`, validated in Python through `parti.schema` (CR-PRT-002's
route), read by `parti.tools.tables`:

- **units** (millimetres) and **parameters**: named numbers; any numeric value may name a parameter (`"$wall_t"`).
- **levels** (id, name, z); **walls** (id, level, start and end of the centreline, thickness, height); **slabs** (id,
  level, outline, thickness, top at the level's z); **openings** (id, wall, offset along it, width, height, sill);
  **rooms** (id, name, level, `floor_z`, outline); **placements** (a part file at a position and rotation, §S6).
- **feature groups**: each names the rows it builds (`L0.walls`, `L0.slabs`, …); a row belongs to one group.
- per row, optionally, the **sheets it cites** (CR-PRT-028).

**Joints (Track 2's G1):** at an L or T joint the wall listed first runs through and the other stops at its face, so no
two bodies overlap by construction and a group's expected volume is the sum of its rows' volumes less their openings.
**Body names (G3):** `<feature group>.<row id>` (`L0.walls.W3`). The name is a CAD reference; Parti's id is given at
classification (PRD-domain §2.6).

### §S2 The SolidCraft translator

`parti.translators.solidcraft.generate(tables, group) -> Batch`: the group's bodies as a batch of SolidCraft commands
(plain data; the commands SolidCraft's `list_commands` documents, for the version the gap analysis pins), with each body
named by §S1's rule. `expected(tables, group) -> Expectations`: body count, each body's volume and bounds, computed from
the tables alone, independently of SolidCraft. **Provenance:** each body maps back to its table and row, and
`dependents(tables, changed_rows)` names the groups a change touches (a wall's group and the openings in it), so a
correction regenerates only what depends on it (JohnnyHouse's gap 4; what the user points at in the CAD is read
by CR-PRT-025's `pointed`, and the harness starts the correction from it, CR-PRT-029).

### §S3 Applying it

A port `CadSession` (`apply(batch)`, `measure(names)`, `pick(point)`, `save(path)`, `open(path)`), with two adapters
over SolidCraft's MCP server: **headless** (`solidcraft-cli mcp --headless`, Parti's live tests) and **in the running
application** (`solidcraft-cli mcp --connect`, the path JohnnyHouse's sessions use; gap 7). A fake at the port serves
the module tests (DN-test-strategy). SolidCraft's units are mapped to millimetres by the declared transform (D25, G5).

### §S4 Checks

`parti.tools.checks`: the built-in checks, each a **check result** (pass or fail, the measured values, the worst
offender, what it did not prove): **body count** exact; **volume** per body within 0.1 %; **bounds** per body within
0.5 mm (G1: bounds are their own criterion); **interference** (no two bodies of the group overlap, by SolidCraft's
measure). **Project-defined checks** (gap 3) register with `@parti.tools.check` and run beside them: walls meeting at
their ends, a door joining its two rooms, a beam reaching its column; each returns its worst value. **Picks by world
point** (gap 5): `expect_volume_change(before, after, delta)` checks that a fillet, cut or face operation picked by a
point changed the volume as expected (a cut that leaves it unchanged missed).

### §S5 The step cycle

`parti.workflow.Step` names its sources, its tables, its groups and its **targets**: the model's groups and any other
files generated from the same tables (motion tables, placements, a declaration fragment), so nothing drifts from the
model (gap 2). `parti.workflow.run_step(step, session, project)`:

1. **reads** the sources and records their hashes; applies each cited sheet's calibration with `parti.units.Calibration`
   (CR-PRT-028);
2. **writes the data**: validates the tables (faults name the table, the row and the field);
3. **generates** every target;
4. **applies** the batches through the `CadSession`;
5. **checks**: the built-in and the project's checks against the expectations;
6. **checkpoints** (gap 8) only when every check passes: the design saved as `<checkpoints>/CP-<n>.sc` and one row in
   the checkpoint log; no pictures; a clean-up removes only files this step made, never a kept file;
7. **records** the **step record** (`parti.step-record/1`, one JSON line appended to `parti/steps/records.ndjson`,
   which the gateway reads for the workflow's checks, CR-PRT-012): asked, done, checked with numbers, not
   checked, the files written. On a failed check nothing is checkpointed and the record names the worst offender; the
   fix is made in the data and the step is run again.

### §S6 Part files and placements (gap 1)

A step may target a **part file** linked into the building at several **placements** (louvres, doors, a gate, a vent):
it backs up the part file, rebuilds it, relinks it at every placement, and runs the part's checks **at every
placement**; a placement failing fails the step, naming it.

### §S7 Test data (moved here from CR-PRT-003)

`parti.testing.fixtures.one_house()` returns the data tables of a synthetic two-level house (levels, walls, slabs,
openings, rooms, two placements of one part), with its expectations and an expected `parti.building/1`, the oracle for
CR-PRT-027's derivation (G6). The repository's copy is under `tests/fixtures/cad/`, with the golden batches.

## Acceptance criteria

- [ ] `one_house()` validates against `parti.tables/1`; a wall naming an unknown level, an opening wider than its wall and a parameter never defined each give a fault naming the table, the row and the field.
- [ ] `generate(one_house(), "L0.walls")` equals the committed golden batch, and every body in it is named `L0.walls.<row id>` (contract test, in CI).
- [ ] `expected` gives the group's volume as the sum of its rows' volumes less their openings, and each body's bounds, from the tables alone.
- [ ] `dependents` for a changed wall row names that wall's group; for a changed opening, its wall's group; for a changed parameter, every group using it.
- [ ] With the fake session, a step whose checks pass writes `CP-<n>.sc`, one checkpoint-log row and a step record naming every target written; with one body's volume off by 1 %, it writes no checkpoint and its record names that body as the worst offender.
- [ ] A project-defined check registered with `@parti.tools.check` runs in the cycle and its result, with its worst value, is in the step record.
- [ ] `expect_volume_change` fails a cut that left the volume unchanged.
- [ ] A step with two targets (the model's group and a placements file) writes both and its record names both.
- [ ] A part-file step backs the part file up before rebuilding it and checks it at both placements of `one_house()`; a placement made to fail fails the step, naming it.
- [ ] A clean-up after a step leaves a kept file in the checkpoints folder in place.
- [ ] Live (`PARTI_LIVE=1`, a workstation with SolidCraft): `one_house()`'s level 0 built headless passes its checks, and its checkpoint opens again with the same bodies.
- [ ] (reviewed, not tested; workstation) JohnnyHouse's migrated run, through the running application, checkpoints a feature group; no file under Parti's repository changes.
- [ ] Caller-existence: `run_step` is called by `parti-axi model build` (CR-PRT-013) and by the harness's Model step (CR-PRT-029), reviewed at their VERIFY.

## Estimated size

13 points. If the gap analysis finds it larger, §S6 (part files and placements) splits into a CR of its own in wave 3.

## Non-goals

Reading the running model back into an inventory (CR-PRT-025); the SolidCraft plugin and native server (CR-PRT-073,
CR-PRT-074, 0.2.0); **setting-out** of floors and walls (JohnnyHouse's gap 6: from a survey of the scene and the
declaration, not CAD; CR-PRT-019, CR-PRT-020, 0.2.0); the Blender and Unreal translators (CR-PRT-039, CR-PRT-049); the
correction loop as a workflow (CR-PRT-036, 0.2.0).

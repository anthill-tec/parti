# CR-PRT-025 — Model inventory: the live read from SolidCraft

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-024
**Labels:** library, python, cad, solidcraft, schema
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-domain.md` §2.6 (v0.4, DM-12), §8; `docs/research/PRD-parti.md` D25, D31, D33, D34; `docs/research/DN-ubiquitous-language.md` (Model inventory, Feature group)

## Context

Parti works on the model the user has open, not on a copy: it reads the running CAD model into its **model inventory**
(`parti.model/1`) and reads it again whenever the model's revision moves (DM-12). The application's own report and
Parti's inventory are two documents: the translator turns the first into the second (Track 2's F2 on CR-PRT-003). This CR
adds the inventory's schema, the SolidCraft translator's read, the write that keeps Parti's ids and classes with the
objects (M-1), and the watch on the model's revision. Until the SolidCraft plugin (CR-PRT-074, 0.2.0) it reads through
SolidCraft's MCP server, over CR-PRT-024's `CadSession` port.

## Scope

### §S1 The inventory's format (`parti.model/1`)

A JSON Schema in `packages/schema/v1/model.schema.json` (CR-PRT-002's route; read by `@parti/schema` and
`parti.schema`): the application and its version, its **units** and the **declared transform** to the project's world
frame in millimetres (D25), the design's **document id** and **revision**, and

- **bodies**: CAD name (a reference only), volume, bounds, closed or not, the **feature group** that made it (from
  CR-PRT-024's body names, else none), its material, and its stored Parti id and class when it has them;
- **components** and their **placements** (a part file at a position and rotation);
- **part properties** (name and value; the product class among them);
- **materials** with their looks (colour, texture reference, roughness);
- **faces**, each with an id under its body (`<body id>/f<index>`), its kind (plane, cylinder, other), normal, area,
  a point on it and, for a plane, its outline's bounds: the lesser primitives of D31.

### §S2 The read

`parti.translators.solidcraft.read(session) -> (Report, Inventory)`: the **report** is what SolidCraft answered (the
design's inspection, each body's measure and topology, its properties, the document revision; the commands the gap
analysis pins for the version CR-PRT-024 pins), kept as it came; `to_inventory(report, transform)` turns it into
`parti.model/1`, pure and tested on recorded reports. Lengths, areas and volumes are converted by the declared transform
(Track 2's G5: SolidCraft's units with the transform); a report in other units without a transform is refused with
`unsupported-units`. A read that fails part-way returns the fault and no inventory (M-3: the last inventory stays in
force, the caller says why).

### §S3 Keeping Parti's ids with the objects

`parti.translators.solidcraft.tag(session, cad_ref, parti_id, product_class)` stores the id and the class in the
object's part properties (`parti.id`, `parti.class`), as one undoable edit, so they survive renames and are read back
by §S2 (M-1). It refuses an object that already carries another Parti id (`id-conflict`). From 0.2.0 the plugin keeps
them as plugin data instead (D34), and this write moves behind the same call.

### §S4 Watching the revision

`parti.translators.solidcraft.watch(session, on_revision, interval_s=2)` polls `document.revision` and calls
`on_revision` with the inventory each time the revision or the document id moves (a design opened again is a new
document); it reads once at start. The caller posts the inventory to the gateway as `read-model` (CR-PRT-012, CR-PRT-026).
From 0.2.0, SolidCraft's push (`design.changed` through the native server, D34) replaces the poll behind the same call.

### §S5 What the user points at (JohnnyHouse's gap 4)

`parti.translators.solidcraft.pointed(session) -> Pointed`: the CAD's current **selection** (SolidCraft's
`selection.get`: bodies, faces and edges with their points), each mapped to its model object and face id by the last
inventory, with a **picture** of the current view (`screenshot`) when the session has a window. With CR-PRT-024's
provenance it names the table row behind each selected body, so a correction the user points out starts there and
regenerates only what depends on it (the harness's build-from-data skill, CR-PRT-029). Read-only: it changes nothing
in the design.

### §S6 Test data (Track 2's F2, G4, G5)

`parti.testing.fixtures.one_house_model()` gives, for CR-PRT-024's `one_house()`, the two documents: a recorded
SolidCraft **report** (synthetic, written to match what the read gets) and the expected `parti.model/1`. It gives also a
**second revision** in which one wall's body is split in two, one body is renamed and one material is changed, for the
re-read and CR-PRT-009 (G4), and a report in centimetres with its transform (G5). The repository's copies are under
`tests/fixtures/cad/`.

## Acceptance criteria

- [ ] `one_house_model()`'s expected inventory and both revisions validate against `parti.model/1`; an inventory whose face has no body is refused with the schema's fault.
- [ ] `to_inventory` on the recorded report equals the expected inventory, with faces ids `<body id>/f<index>`, each body's feature group read from its name, and the units in millimetres.
- [ ] `to_inventory` on the centimetre report with its transform gives the same inventory within 0.01 mm; without the transform it is refused with `unsupported-units`.
- [ ] With the fake session, a read failing on the third body returns its fault and no inventory.
- [ ] `tag` then `read` gives the body's Parti id and class back; renaming the body and reading again keeps both; tagging it with another id is refused with `id-conflict`.
- [ ] With the fake session's selection holding one face of `L0.walls.W3`, `pointed` gives that object's id, the face's id and, with `one_house()`'s provenance, the row `W3` of the walls table; the session's revision is unchanged.
- [ ] `watch` with the fake session calls `on_revision` once at start, once per revision change and once when the document id changes, and not when the revision is unchanged.
- [ ] Live (`PARTI_LIVE=1`): `one_house()` built headless (CR-PRT-024) and read gives an inventory whose bodies, volumes and bounds equal CR-PRT-024's expectations within its tolerances.
- [ ] Caller-existence: `read` and `watch` are called by `parti-axi model read` and `model watch` (CR-PRT-013), `tag` by `model watch` for the write-back the gateway sends (CR-PRT-012, CR-PRT-026), reviewed at their VERIFY.

## Estimated size

8 points.

## Non-goals

The model objects, their classes and revisions in the domain (CR-PRT-026, CR-PRT-009); the plugin and the push
(CR-PRT-073, CR-PRT-074, 0.2.0); reading Blender or Unreal scenes (CR-PRT-039, CR-PRT-049); lesser primitives below
faces (edges, pieces; DM-9).

# CR-PRT-019 — Setting-out

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-006
**Labels:** domain, design, setting-out
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §3.3 (setting-out, courses), §4.1 (module); JohnnyHouse #1658 (PRD-parti T4)

## Context

A placement at true scale needs its grid fixed on the zone: where the joints fall and what the edge cuts are. One
grid per room or storey is wrong in every room (JohnnyHouse #1658); the setting-out is data of each placement, and the
same grid gives the picture (the scene, Blender, Unreal) and the count (CR-PRT-020). The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.

## Scope

### §S1 Module

`moduleOf(finish, placement)` returns the grid period along x and y in mm: the finish's size (rotated when the
placement's rotation is 90) plus the grout width, or the size alone when the finish states `sizeIncludesJoint: true`.
Veneers and laminates use their scan's real size as the period (for the picture), with no joint.

### §S2 Rules

`setOut(zone cells, module, rule)` returns `{ origin: [x, y], cuts: { left, right, bottom, top } }` in the face frame,
for rules: `centre` (a joint or a tile centre on the zone's centre line in each direction, whichever leaves the wider
smaller cut; the default), `full-start` with an edge (`bottom` | `top` | `left` | `right`: a full tile against that
edge), and `manual` with an origin. Offset bonds shift alternate rows by the bond fraction after the origin is set.

### §S3 In the placement

`place-product` takes an optional `setOut` (`{ "rule": "centre" }` by default); the `product-placed` event carries the
computed `origin` and `cuts`. `resize-zone` and a building revision that changes the zone recompute them
(`set-out-changed` event). A cut under a threshold (default 50 mm, a project setting) carries a warning `sliver-cut`.

## Acceptance criteria

- [ ] A 300 × 600 tile with 3 mm grout, rotation 0, has module [303, 603]; with `sizeIncludesJoint` 600 × 600 the module is [600, 600].
- [ ] `centre` on a 2400 mm wide zone with module 600 puts a joint on the centre line and leaves 0 cuts; on 2100 mm it puts a tile centre on the line and leaves 150 mm at each side.
- [ ] `full-start` with edge `bottom` gives a bottom cut of 0 and a top cut equal to the zone height modulo the module.
- [ ] `manual` keeps the given origin, and the cuts follow from it.
- [ ] Placing on a zone whose centre rule leaves a 20 mm cut carries `warnings: ["sliver-cut"]`.
- [ ] Resizing a zone emits `set-out-changed` with the new origin and cuts.
- [ ] Caller-existence: `setOut` is called by `decideDesign` for `place-product` and `resize-zone` (grep in `packages/domain/src/design`).

## Estimated size

5 points.

## Non-goals

Herringbone and diagonal set-outs; aligning joints across adjacent surfaces (a wall's joints meeting the floor's); the
tile layout drawing for the site (later).

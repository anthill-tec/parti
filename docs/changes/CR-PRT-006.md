# CR-PRT-006 — Design context: zones and placements

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-004, CR-PRT-005
**Labels:** domain, design
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §3.1–§3.3, §3.5 (D-1 to D-3); DM-1, DM-2, DM-4, DM-7

## Context

The design is the user's plan of the finishes layer: zones on each surface and one placement per zone. The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.
Its rules need the building (surfaces, openings, regions) and the catalogue (products), passed in as plain data.

## Scope

### §S1 Zones

`define-zone`, `resize-zone`, `remove-zone`. Kinds and tiers per PRD-domain §3.2: `field` (tier 0, one per surface,
created when a surface first appears and never removed by the user), `band` and `border` (tier 1), `panel` and
`area` (tier 2). A band is a height range across the full width; a border an inset width along a floor's edges;
a panel or area a rectangle. `visibleCells(surface, zones)` returns the rectangles each zone shows, after higher tiers
and the cut-outs of openings and keep-clear regions.

### §S2 Placements

`place-product` (zone, product, and the parameters of its kind, PRD-domain §3.3: for a tile, pattern `stack` |
`offset-half` | `offset-third`, rotation 0 | 90, grout width in mm and colour, offset x and y; for a wood veneer or
laminate, `grain` 0 | 90 and offset; for a paint, nothing more) and `clear-zone`. Parameters of another kind are
refused with `invalid-parameter`. A zone holds at most one placement; placing again replaces it.

### §S3 Rules

D-1 (inside the surface; no overlap within a tier), D-2 (the zone and the product exist; a product whose suitable
surfaces exclude the zone's surface kind is refused with `unsuitable-surface`; a product for another room use is
placed with a `warnings` entry `other-room-use` on the event), D-3 (a command whose `expectedRevision` differs from
the design's revision is refused with `stale-revision`). With DM-7, a placement crossing a step carries a warning
`crosses-step`.

## Acceptance criteria

- [ ] Importing `oneBath` then reading the design gives one field zone per surface.
- [ ] A dado band (0–1200 mm) and a panel inside it are both accepted; a second band overlapping the first is refused with `zones-overlap`.
- [ ] `visibleCells` for field + band + panel + door opening returns cells whose summed area equals the surface's area minus the opening's (no overlap, no gap).
- [ ] A wall-only product placed on a floor zone is refused with `unsuitable-surface`; an outdoor product placed in a bathroom is placed and the event carries `warnings: ["other-room-use"]`.
- [ ] A command with `expectedRevision` one below the design's is refused with `stale-revision`, and the state is unchanged.
- [ ] Placing a second product in a zone replaces the first; the history (events) keeps both.
- [ ] A veneer placed with `grain: 90` is accepted; a veneer placed with a grout width, or a paint with a pattern, is refused with `invalid-parameter`.
- [ ] Caller-existence: `decideDesign` is called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

8 points.

## Non-goals

Placements on parts (with the world builder, DM-9); herringbone and diagonal patterns, tile layout geometry (cut tiles, set-out) and quantities (later); schemes, shortlist
and undo (CR-PRT-007); building changes (CR-PRT-009).

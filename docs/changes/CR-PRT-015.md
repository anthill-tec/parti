# CR-PRT-015 — Project Environment: the design workspace and quantities

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-014
**Labels:** page, ui, design
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-MOD-2, FR-DES-1 to FR-DES-4, FR-STA-1 to FR-STA-3, D25; `docs/research/PRD-domain.md` §3, §5, §6

## Context

The **Design** and **Quantities** tabs of the Project Environment (D22, storyboards 3 and 4): choosing a surface,
dividing it into zones, placing finishes with their setting-out, schemes, undo, quantities, the setting, and the
follow-ups after a building change. They render inside the shell (CR-PRT-021).

## Scope

### §S1 Surface view

Rooms and their surfaces as a list; the selected surface drawn to scale in its face frame (SVG), with its openings,
regions (keep-clear hatched), guides, steps and zones; room dimensions in feet and inches, areas in square feet (D25).

### §S2 Zone editor

Add a band (height range), a border (inset), a panel or area (rectangle, by dragging or by typed values in any unit
`parseLength` accepts, converted to millimetres); resize; remove. Refusals show next to the zone.

### §S3 Placing and schemes

Place a product (from the browser or the shortlist) in the selected zone with pattern, rotation, grout and offset;
clear; save and apply a scheme for the room; undo and redo. The setting-out rule (centre, full start at an edge,
manual) is chosen per placement; the drawing shows the grid at true scale and the edge cuts in mm. The zone's swatch fills it in the drawing. Warnings
(`other-room-use`, `crosses-step`) show on the zone.

### §S3a Quantities

A quantities panel per room and per finish: area in square feet, laid (full, cut), to buy, boxes, with the counting
rule and exclusions shown under the numbers; wastage and rounding changeable as project settings.

### §S4 Setting and follow-ups

Time, date and weather controls; a follow-ups list after a building change, each leading to its zone.

### §S5 Cues

Cues (CR-PRT-021) beside the selection: on a surface *Add a band*, *Add a panel*, *Measure this wall*; on a zone
with a placement *Full at floor* / *Centred*, *Copy to another room*; on quantities *Per room*, *Per trade*,
*Show the counting rule*.

## Acceptance criteria

- [ ] (e2e) Selecting `oneBath`'s east wall draws it with its mirror region, and shows its width as feet and inches.
- [ ] Typing a dado height of `4'` creates a band of 1219.2 mm (read back from the `design` query).
- [ ] Placing a wall-only product on the floor shows the refusal `unsuitable-surface` on the zone, and the design is unchanged.
- [ ] Saving a scheme, changing a placement, applying the scheme and pressing undo returns to the changed placement.
- [ ] Setting the weather to rain in the page appears in the mock scene's status (with CR-PRT-016) and in `parti-axi state --query session`.
- [ ] After re-importing the building without its floor, the follow-ups list shows the orphaned floor zones.
- [ ] Choosing `full-start` at the bottom on the east wall shows a bottom cut of 0 mm in the drawing.
- [ ] After placing a tile, the quantities panel shows laid and to-buy for the room equal to the `quantities` query's, with the counting rule beneath.
- [ ] Selecting the dado band shows the cues *Full at floor* and *Centred*; clicking *Centred* re-sets the placement with equal edge cuts.
- [ ] The surface view's area label for a 3048 × 3048 mm floor reads `100 sq ft`.

## Estimated size

13 points.

## Non-goals

3D views (the scene's job); tile set-out and cut pieces (later).

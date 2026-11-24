# CR-PRT-015 — Project Environment: the surface editor and the BOM

**Status:** PENDING (spec drafted 2026-11-23, reworded 2026-11-24 from the storyboard review; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-014
**Labels:** page, ui, design
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-MOD-2, FR-DES-1 to FR-DES-4, FR-STA-1 to FR-STA-3, D25, D22 (d), D31; `docs/research/PRD-domain.md` §2.1a, §3, §5, §6, §11; `.lavish/storyboards.html` storyboards 3 and 4 and card `#wf-driver-proposal`, approved by the owner (24 November 2026)

## Context

The **surface editor** and the **BOM view** of the Project Environment (D22, storyboards 3 and 4), opened in the
workspace by the workflow step (`show surface`, `show bom`; CR-PRT-022): choosing a surface, dividing it into zones from a
selection, labelling them, placing finishes with their setting-out, schemes, undo, the bill of materials, the
conditions, and the follow-ups after a building change. They render inside the shell (CR-PRT-021) and use its 2D
tools. Parti edits only what it owns: the geometry stays in the CAD.

## Scope

### §S1 Surface view

Rooms and their surfaces as a list (choosing one sets the focus); the selected surface drawn to scale in its face frame (SVG), with its openings,
regions (keep-clear hatched), guides, steps and zones; room dimensions in feet and inches, areas in square feet (D25).

### §S2 Zones

Define a zone from a **selection** on the surface (a rectangle select, or clicks on the cells of the grid), or add a
band (height range), a border (inset), a panel or area by typed values in any unit `parseLength` accepts, converted to
millimetres; resize; remove. Each zone takes a **name and tags** (its label, click-and-edit; `label-zone`), and a click
on a drawn zone selects it. Refusals show next to the zone.

### §S3 Placing and schemes

Place a product with pattern, rotation, grout and offset, four ways (PRD-domain §3.3): dragging from the browser or the
shortlist, right-clicking a zone or surface (*Apply from the shortlist*), pointing, or on a selection of several zones at
once (one placement each, one step to undo);
clear; save and apply a scheme for the room; undo and redo. The setting-out rule (centre, full start at an edge,
manual) is chosen per placement; the drawing shows the grid at true scale and the edge cuts in mm. The zone's swatch fills it in the drawing. Warnings
(`other-room-use`, `crosses-step`) show on the zone.

### §S3a The BOM

The BOM view, grouped by Room › Surface and by finish: area in square feet, laid (full, cut), to buy, boxes, with the counting
rule and exclusions shown under the numbers; wastage and rounding changeable as project settings.

### §S4 Conditions and follow-ups

Time, date and weather controls; a follow-ups list after a building change, each leading to its zone.

### §S5 Cues

Cues (CR-PRT-021) beside the selection: on a surface *Add a band*, *Add a panel*, *Measure this wall*; on a zone
with a placement *Full at floor* / *Centred*, *Copy to another room*; on the BOM *Per room*, *Per trade*,
*Show the counting rule*.

## Acceptance criteria

- [ ] (e2e) Selecting `oneBath`'s east wall draws it with its mirror region, and shows its width as feet and inches.
- [ ] Typing a dado height of `4'` creates a band of 1219.2 mm (read back from the `design` query).
- [ ] Placing a wall-only product on the floor shows the refusal `unsuitable-surface` on the zone, and the design is unchanged.
- [ ] Saving a scheme, changing a placement, applying the scheme and pressing undo returns to the changed placement.
- [ ] Changing the weather to rain in the page appears in the mock scene's status (with CR-PRT-016) and in `parti-axi state --query session`.
- [ ] After re-importing the building without its floor, the follow-ups list shows the orphaned floor zones.
- [ ] Choosing `full-start` at the bottom on the east wall shows a bottom cut of 0 mm in the drawing.
- [ ] Selecting four grid cells on the east wall and defining a zone from them creates one panel zone covering them; naming it `niche` and tagging it `feature` shows both in its label.
- [ ] Selecting two zones and applying a shortlisted tile by right-click places it in both, and one undo clears both.
- [ ] After placing a tile, the BOM view shows laid and to-buy for the room equal to the `quantities` query's, with the counting rule beneath.
- [ ] Selecting the dado band shows the cues *Full at floor* and *Centred*; clicking *Centred* re-sets the placement with equal edge cuts.
- [ ] The surface view's area label for a 3048 × 3048 mm floor reads `100 sq ft`.

## Estimated size

13 points.

## Non-goals

3D views (the scene's job); tile set-out and cut pieces (later).

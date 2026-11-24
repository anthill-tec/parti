# CR-PRT-014 — Project Environment: the asset browser

**Status:** PENDING (spec drafted 2026-11-23, reworked 2026-11-24 from the storyboard review; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012, CR-PRT-021
**Labels:** page, ui, catalogue
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-CAT-2, FR-CAT-3, FR-DES-5, D22 (c), D25, D32; `docs/research/PRD-domain.md` §4.3, §4.4, §7, §11; `docs/Architecture.md` B3 (`page`), B9; `.lavish/storyboards.html` storyboard 2 and card `#wf-driver-proposal`, approved by the owner (24 November 2026)

## Context

The asset browser (D22, storyboard 2), modelled on the prototype's tile browser: a panel docked at the bottom of the
shell (CR-PRT-021), detachable to its own window. It shows finishes of every kind, chosen for a target, and takes the
**signals** the workflow step sends in 0.1.0 (CR-PRT-022) and the agent later.

## Scope

### §S1 Tree and filters

On the left, a **tree of the product classes** (D32; 0.1.0's Finishes branch: Tile, Wood veneer, Laminate, Paint, Metal,
Exposed, Glaze) with counts, scoped to the context the step sets (the focus's surface), with *Show all classes*. Above
the results, a **filter bar** following the chosen class: free-text search, the **palette** (a few colours, picked or
taken from a scheme, CR-PRT-007; a finish matches when its colour is near one of them, whatever its kind) and a
drop-down per filter of PRD-domain §4.3.

### §S2 Results, detail and shortlist

Results as a grid of swatches with their class path, count and sorts (round the colour wheel by default); a detail
(images, size, uses, classification and its confidence, the set) with "Goes with"; add to and remove from the shortlist
with a note and an optional target (room, surface, role); the shortlist, filtered by target. Sizes in millimetres
(component unit, D25). Provisional finishes and licences are shown. Cues (CR-PRT-021) beside the selection:
*Shortlist for…*, *Compare*, *Hide provisional*.

### §S3 Signals and the detached window

The browser applies `set-filters`, `set-palette`, `mark-assets` (marked cards) and `note` (a note above the results).
*Detach* opens it in its own window, kept in step through the gateway; closing that window docks it again.

## Acceptance criteria

- [ ] (e2e, browser) With 200 synthetic products, choosing the class Tile shows only tiles, with the count beside the class.
- [ ] A palette of one blue shows exactly the products whose colour is near it, of every kind.
- [ ] Searching "cafe" shows `Café Latte`.
- [ ] Opening a product's detail and choosing "Goes with" lists its set members first.
- [ ] Adding a product to the shortlist in one browser tab shows it in a second tab's shortlist without a reload.
- [ ] Sizes show as `600 × 300 mm`.
- [ ] Selecting a product shows the cue *Shortlist for…*; choosing bath 1 · east wall · band adds the entry with that target.
- [ ] Shortlisting a tile for `FF_bath1`, role `band`, then filtering the shortlist by `FF_bath1` shows it; filtering by `FF_bath2` does not.
- [ ] A veneer's detail shows its source, licence and stain; a paint's shows its colour and sheen and no image; a metal's shows its treatment, metallic and roughness; a provisional finish is marked `provisional` on its card and its detail.
- [ ] Starting the step *Choose* with focus `bath1 › floor` scopes the tree to floor finishes; `mark-assets` with two ids marks those two cards, and `note` shows its text.
- [ ] Detaching the browser and shortlisting a product in its window shows it in the docked shell's shortlist.
- [ ] Caller-existence: the shell docks this component at the bottom and the step *Choose* opens it (reviewed at VERIFY).

## Estimated size

10 points.

## Non-goals

The client viewer's in-world presentation (after 1.0.0, D22); smart menus (Unreal); prices and offers; classes beyond the
Finishes branch (they grow with their layers).

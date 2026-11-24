# CR-PRT-014 — Project Environment: the asset browser (first form)

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012, CR-PRT-021
**Labels:** page, ui, catalogue
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-CAT-2, FR-CAT-3, FR-DES-5, D22 (designer edition), D25; `docs/research/PRD-domain.md` §4.3; `docs/Architecture.md` B3 (`page`)

## Context

The asset browser's first form, the **Assets** tab of the Project Environment (D22, storyboard 2): finishes of every
kind, chosen for a target. It renders inside the shell (CR-PRT-021) and reads its projection.

## Scope

### §S1 Asset browser

Filter panel with every filter of PRD-domain §4.3, kind first; free-text search; results as a grid of swatches sorted round the
colour wheel by default; a detail view (images, size, uses, classification and its confidence, the set) with "Goes
with"; add to and remove from the shortlist with a note and an optional target (room, surface, role); the shortlist view,
filtered by target. Sizes in millimetres (component unit,
D25). Provisional finishes and licences are shown. Cues (CR-PRT-021) beside the selection: *Shortlist for…*,
*Compare*, *Hide provisional*.

## Acceptance criteria

- [ ] (e2e, browser) With 200 synthetic products, choosing the colour filter "blue" shows exactly the blue products' cards.
- [ ] Searching "cafe" shows `Café Latte`.
- [ ] Opening a product's detail and choosing "Goes with" lists its set members first.
- [ ] Adding a product to the shortlist in one browser tab shows it in a second tab's shortlist without a reload.
- [ ] Sizes show as `600 × 300 mm`.
- [ ] Selecting a product shows the cue *Shortlist for…*; choosing bath 1 · east wall · band adds the entry with that target.
- [ ] Shortlisting a tile for `FF_bath1`, role `band`, then filtering the shortlist by `FF_bath1` shows it; filtering by `FF_bath2` does not.
- [ ] A veneer's detail shows its source, licence and stain; a paint's shows its colour and sheen and no image; a metal's shows its treatment, metallic and roughness; a provisional finish is marked `provisional` on its card and its detail.
- [ ] Caller-existence: the Assets tab of the shell renders this component (reviewed at VERIFY).

## Estimated size

8 points.

## Non-goals

The client viewer's in-world presentation (after 1.0.0, D22); smart menus (Unreal); prices and offers.

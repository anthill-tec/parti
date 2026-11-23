# CR-PRT-014 — Page: catalogue browser

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012
**Labels:** page, ui, catalogue
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-CAT-2, FR-CAT-3, FR-DES-5, D22 (designer edition), D25; `docs/research/PRD-domain.md` §4.3; `docs/Architecture.md` §5 (`page`)

## Context

The designer edition's page (VanJS), served by the gateway; its state is a projection of the shared state it receives
over the WebSocket.

## Scope

### §S1 Connection and state

`packages/page/src/connection.ts` connects to the gateway, applies the `snapshot` then each event to a local
projection, and reconnects with backoff; a banner shows when disconnected.

### §S2 Catalogue browser

Filter panel with every filter of PRD-domain §4.3, kind first; free-text search; results as a grid of swatches sorted round the
colour wheel by default; a detail view (images, size, uses, classification and its confidence, the set) with "Goes
with"; add to and remove from the shortlist with a note and an optional target (room, surface, role); the shortlist view,
filtered by target. Sizes in millimetres (component unit,
D25).

## Acceptance criteria

- [ ] (e2e, browser) With 200 synthetic products, choosing the colour filter "blue" shows exactly the blue products' cards.
- [ ] Searching "cafe" shows `Café Latte`.
- [ ] Opening a product's detail and choosing "Goes with" lists its set members first.
- [ ] Adding a product to the shortlist in one browser tab shows it in a second tab's shortlist without a reload.
- [ ] Stopping the gateway shows the disconnected banner; restarting it clears the banner and the shortlist is unchanged.
- [ ] Sizes show as `600 × 300 mm`.
- [ ] Shortlisting a tile for `FF_bath1`, role `band`, then filtering the shortlist by `FF_bath1` shows it; filtering by `FF_bath2` does not.
- [ ] A veneer's detail shows its source, licence and stain; a paint's shows its colour and sheen and no image; a metal's shows its treatment, metallic and roughness; a provisional finish is marked `provisional` on its card and its detail.
- [ ] Caller-existence: the gateway serves the built page at `/` (reviewed at VERIFY).

## Estimated size

8 points.

## Non-goals

The client viewer's in-world presentation (after 1.0.0, D22); smart menus (Unreal); prices and offers.

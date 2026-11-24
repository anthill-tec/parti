# CR-PRT-016 — Project Environment: the walkthrough (mock scene)

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012
**Labels:** mock-scene, testing
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-SCN-1, Q9, Q17; `docs/Architecture.md` B3 (`mock-scene`); `docs/research/DN-test-strategy.md`

## Context

The mock scene stands in for Unreal in 0.1.0: it draws what the scene would and reports picks, so the whole loop is
tested without Unreal (Q9). It speaks the same messages the Unreal plugin will (Q17).

## Scope

`packages/mock-scene`: a browser page served by the gateway at `/scene`, connecting like any client, and shown in
the Project Environment's **Walkthrough** tab (CR-PRT-021, storyboard 5). It draws each
room's surfaces unfolded (floor in the middle, walls around it), each zone filled with its placement's swatch colour,
and a status line (selection, time, weather). Clicking a surface or a zone sends `select` with its id. It sends an
acknowledgement message `scene-applied` with the revision it has drawn (added to the schema by this CR as the first
of Q17's acknowledgements).

## Acceptance criteria

- [ ] (e2e) Placing a product in the page fills that zone in the scene with the swatch colour (pixel check at the zone's centre).
- [ ] Clicking a zone in the scene selects it in the page (the page's selection shows the zone id).
- [ ] After each design change the scene sends `scene-applied` with the design's new revision.
- [ ] The status line shows `rain` after `set-weather rain`.
- [ ] The Walkthrough tab shows the scene, and a click in it selects the zone in the Design tab.
- [ ] Caller-existence: the gateway serves the scene at `/scene` (reviewed at VERIFY).

## Estimated size

5 points.

## Non-goals

3D rendering; the Unreal plugin (deferred, D5).

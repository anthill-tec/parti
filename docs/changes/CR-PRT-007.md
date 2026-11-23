# CR-PRT-007 — Design context: schemes, shortlist, undo

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-006
**Labels:** domain, design
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §3.4, §3.5 (D-4); DM-5; FR-DES-1, FR-DES-4, FR-DES-5

## Context

Schemes save and re-apply a room's placements; the shortlist sets products aside; undo and redo step through the
user's own design changes. The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.

## Scope

### §S1 Schemes (per room, DM-5)

`save-scheme` (room, name) records the room's zones' placements; `apply-scheme` replaces them in one event
(`scheme-applied`, carrying every replaced and new placement), refusing a scheme of another room with `other-room`.

### §S2 Shortlist

`add-to-shortlist` (product, note, optional `target`: room, surface, role `base` | `band` | `border` | `feature`),
`remove-from-shortlist`; a product is on the list at most once per target (adding again updates the note). A target
naming an unknown room or surface is refused with `unknown-target`. The `shortlist` query filters by room, surface
and role.

### §S3 Undo and redo

`undo` emits the inverse of the last undoable change as events marked `undoOf: <eventId>`; `redo` re-applies with
`redoOf`. Undoable: zone, placement, scheme and shortlist changes made in the current session. A new change clears the
redo stack. Applying a scheme is undone in one step.

## Acceptance criteria

- [ ] Saving a scheme, changing two placements, then applying the scheme restores both, in one `scheme-applied` event.
- [ ] Applying a scheme saved for `FF_bath1` to `FF_bath2` is refused with `other-room`.
- [ ] Undo after `apply-scheme` restores every replaced placement in one step; redo re-applies it.
- [ ] Undo with nothing to undo is refused with `nothing-to-undo`; a new change after an undo makes `redo` refuse with `nothing-to-redo`.
- [ ] Adding a product twice with the same target keeps one entry with the second note; with two targets, two entries.
- [ ] Filtering the shortlist by room `FF_bath1` returns only entries targeting it.
- [ ] Caller-existence: the four commands reach `decideDesign` from the gateway (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

Schemes across rooms (later, DM-5); undo of building imports or setting changes.

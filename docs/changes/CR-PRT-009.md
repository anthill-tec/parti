# CR-PRT-009 — Versioning in 0.1.0

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-004, CR-PRT-006
**Labels:** domain, versioning
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §6; `docs/research/PRD-parti.md` D19

## Context

When the building is imported again, the design must follow the change without anything changing silently (D19's
forward chain, inside this slice). The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.

## Scope

`followBuilding(design, revised)` is the process step run after every `building-revised`: it returns the design events
of PRD-domain §6's table. A removed surface's zones and placements are **orphaned** (`follow-up-raised`, kind
`orphaned`); a resized surface's zones now outside it are flagged (`follow-up-raised`, kind `outside-surface`); a new
surface gets its field zone (`zone-defined`); changed openings and regions need no event (cut-outs are computed).
`resolve-follow-up` is not a command: a follow-up is resolved (`follow-up-resolved`) when the user's own change removes
its cause (the zone resized inside, removed, or re-placed).

## Acceptance criteria

- [ ] Re-importing `oneBath` without its floor raises one `orphaned` follow-up per floor zone, and their placements remain readable in the design (not deleted).
- [ ] Shrinking a wall so a panel lies outside raises `outside-surface` for that panel only; resizing the panel inside resolves it.
- [ ] A surface added in the new revision gets exactly one field zone.
- [ ] Moving the door changes `visibleCells` but raises no follow-up.
- [ ] Caller-existence: the gateway calls `followBuilding` after every accepted `import-building` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

Versions of designs and comparisons between them (later, D19); changes in other layers.

# CR-PRT-027 — Declare: the derived declaration

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-004, CR-PRT-026
**Labels:** domain, building, workflow
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §2.3, §2.4, §2.5, §2.7 (v0.4), §7, §11; `docs/research/PRD-parti.md` D17, D33

## Context

In the prototype the target project wrote its building declaration by hand. From 0.1.0 Parti **derives a draft**
(`parti.building/1`) from the model, the project agent labels it and the user **confirms or corrects** it surface by
surface; the confirmed declaration becomes a building revision under the same rules (PRD-domain §2.7). Rooms are not
bodies, so the derivation takes the data tables' rooms (CR-PRT-024) as its rooms, and finds the rest in the model. The
domain is pure (R1).

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern): commands `derive-declaration`, `confirm-declaration` (whole, or per
surface, with corrections); events `declaration-derived`, `declaration-confirmed`. Stored in the `building` log.

### §S2 Derivation

`deriveDeclaration(model, rooms) -> { draft, faults }`, with `rooms` the data tables' rooms (id, name, level, `floor_z`,
outline):

- **Floors:** the top face of the slab objects under each room's outline at `floor_z`, as the room's floor surface.
- **Walls:** each vertical plane face of a wall object facing into a room (its normal points inside the outline) and
  lying on the outline's edge, as one wall surface, with its side from its normal, its **anchor** (`start` its left end
  as seen from inside the room, B-4) and its face frame (§2.3, DM-6); ids by the recommended form
  (`<room>.wall.<side>`, `<room>.floor`), the CAD faces as references.
- **Openings:** the voids in a wall face: the face's rectangle less its area, located where an opening body or the
  tables' opening rows put them, in the face frame. A difference no opening explains is a fault `unexplained-void`
  naming the face.
- Faults also: `room-without-floor`, `room-without-walls`, `face-unassigned` (a wall face facing no room, listed, not
  refused).

The draft carries the model's revision it was derived from. It is checked with CR-PRT-004's rules before it is shown:
its breaches are listed with it.

### §S3 Confirmation

`decideDeclaration`: `derive-declaration` yields `declaration-derived` with the draft, its faults and its model
revision. `confirm-declaration` confirms the whole draft or the surfaces it names, with **corrections** (a surface's
id, name, aliases, side or use; an opening added or removed); when every surface is confirmed it yields
`declaration-confirmed` and the declaration is imported through CR-PRT-004's `import-building`, as a building revision.
A draft derived from an older model revision than the latest is refused with `stale-draft`. A declaration the project
wrote itself still imports; `compareDeclarations(written, derived)` lists the differences by id (PRD-domain §2.7).

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema.
- [ ] `deriveDeclaration` on `one_house_model()` and `one_house()`'s rooms equals the expected `parti.building/1` of CR-PRT-024's `one_house()` (Track 2's G6 oracle), ids, anchors and openings included.
- [ ] Every derived wall's anchor satisfies B-4 (its direction agrees with its side), on each of the four sides.
- [ ] A wall face with a void no opening explains gives `unexplained-void` naming the face; a room whose slab is missing gives `room-without-floor`.
- [ ] Confirming the draft with one surface renamed yields `declaration-confirmed` and a building revision whose surface has the new name.
- [ ] Confirming a draft derived from model revision 3 when revision 4 has been read is refused with `stale-draft`.
- [ ] `compareDeclarations` of the oracle with one opening moved lists exactly that opening.
- [ ] Caller-existence: `deriveDeclaration` and `decideDeclaration` are called from `packages/gateway/src` (CR-PRT-012 VERIFY); `parti-axi declare derive` calls the gateway (CR-PRT-013 VERIFY).

## Estimated size

8 points.

## Non-goals

Polygonal floors and sloped faces (PRD-domain §2.3's 0.1.0 limits); regions, guides and steps derived from the model
(declared or added by correction in 0.1.0); the agent's labelling (CR-PRT-029); the Building view where the user
confirms (CR-PRT-033).

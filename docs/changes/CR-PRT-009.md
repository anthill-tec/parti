# CR-PRT-009 — Versioning in 0.1.0: building and model revisions

**Status:** PENDING (spec drafted 2026-11-23; rewritten 2026-11-24 for the roadmap; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten: building and model revisions (PRD-domain §6, §2.6); design versions and the design\'s forward chain (`followBuilding`) move to CR-PRT-007 (0.2.0).
**Priority:** High
**Depends on:** CR-PRT-004, CR-PRT-026
**Labels:** domain, versioning, building
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-domain.md` §2.2, §2.6, §2.7, §6 (v0.4); `docs/research/PRD-parti.md` D17, D19, D33

## Context

Nothing changes silently (D19). In 0.1.0 two things are versioned: the **model**, read again whenever its revision moves
(PRD-domain §2.6), and the **building**, revised when a declaration is confirmed or imported (§2.2). A model revision
refreshes the derived declaration's draft and shows the user what changed; once confirmed, it is a building revision.
The forward chain into the design comes with the design (CR-PRT-007, 0.2.0). The domain is pure (R1).

## Scope

### §S1 Model revisions

`diffModels(previous, next) -> ModelChanges`: objects **added**, **removed**, **renamed** (same Parti id, another CAD
name), **split** (one Parti id on several bodies: the largest by volume keeps the id, the others get new ids recorded
as split from it), **material changed** (an effective material differs, §2.6), and **resized** (bounds moved by more
than 0.5 mm). Objects with a Parti id are matched by it (M-1); objects without one by CAD name, and a name matching
nothing is added and removed, never guessed. `read-model` (CR-PRT-026) on a model already read yields `model-revised`
carrying the changes, instead of `model-read`; an unchanged revision yields nothing.

### §S2 A failed read

A read that fails is recorded as `model-read-failed` with its fault; the last inventory stays in force (M-3) and the
query `model` says it is stale and why.

### §S3 The draft follows

After `model-revised`, `followModel(declarationState, changes)` marks the derived draft **stale** (CR-PRT-027) and lists
the surfaces the changes touch (an object removed or resized under a surface's faces); the user re-derives and
confirms. A confirmed declaration's building revision carries CR-PRT-004's changes (`diffBuildings`).

### §S4 History

The query `history` lists the model and building revisions in order, each with its changes and what caused it (a read,
a confirmation, an import), for the Model and Building views and `parti-axi`.

## Acceptance criteria

- [ ] `diffModels` from `one_house_model()` to its second revision (Track 2's G4) gives exactly: one split (the wall, its larger part keeping the id), one rename and one material change.
- [ ] An object without a Parti id whose CAD name changes is reported as one removed and one added.
- [ ] Reading the same revision twice yields one `model-read` and no `model-revised`.
- [ ] A failed read yields `model-read-failed`; `model` then returns the previous inventory marked stale with the fault.
- [ ] After a revision removing a wall body, `followModel` marks the draft stale and names the surfaces made from that body's faces.
- [ ] `history` after a read, a re-read with changes and a confirmation lists three entries in order, each with its cause.
- [ ] Caller-existence: the gateway calls `followModel` after every `model-revised` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

The design's forward chain and design versions (CR-PRT-007, 0.2.0); comparing two arbitrary revisions in the page
(later, D19); revisions of the sources (CR-PRT-028's `source-revised`).

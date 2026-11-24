# CR-PRT-026 — Building context: the model and its products

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-004, CR-PRT-005, CR-PRT-025
**Labels:** domain, building, catalogue
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §2.1a, §2.6 (v0.4, DM-12), §4.4, §7; `docs/research/PRD-parti.md` D31, D32, D33

## Context

The model inventory (CR-PRT-025) says what the CAD model holds; this CR makes it part of the Building context: each
object is a **model object** with its CAD reference and a Parti id, and a **product of its class** (D31, D32): by the
class stored with it, else by the project's rules, else **unclassified** and listed for the user (M-2). Its materials
follow the default precedence unless updated (DM-10). The domain is pure (R1): the inventory comes in as data.

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern): commands `read-model` (the inventory), `classify-object` (an object, a class
of CR-PRT-005's classification); events `model-read`, `object-classified`; query `model`. They are stored in the
`model` log (CR-PRT-010); the latest inventory is its snapshot (`model/inventory.json`).

### §S2 Model objects

`packages/domain/src/building/model/`: `decideModel`, `evolveModel`, `initialModel`. `read-model` yields `model-read`
with the inventory and its **model objects**: one per body (and per component placement), with its CAD reference, its
feature group, its faces as its lesser primitives (`<object id>/f<index>`) and its label (§2.1a: the CAD name as a
reference, the class's name as its kind). An object carrying a stored Parti id keeps it (M-1); an object without one is
given `<feature group or "obj">.<n>`, unique in the model, recorded in the event so a replay gives the same ids, and
listed for write-back (CR-PRT-025's `tag`).

### §S3 Classification

`classifyObjects(model, rules, classification)`: an object's class is the **stored** class when it has one (refused
with `unknown-class` if CR-PRT-005's classification does not hold it, and the object listed unclassified), else the
first matching **project rule** (rules are data: a feature group, a CAD name pattern or a material, and the class they
give; `walls → structure.wall`), else **unclassified**. Nothing is guessed (M-2). `classify-object` sets a class by
hand, yields `object-classified` and lists the object for write-back. The object is then a product of its class:
`effective` and `validateProduct` of CR-PRT-005 apply to it, faults listed per object.

### §S4 Materials by default, unless updated

`effectiveMaterial(model, element)`: a face takes its body's material, the body its component's, the component its
material's, **unless updated** at that level (the same precedence SolidCraft applies, DM-10). The material is a
reference into the inventory's materials; its look is the inventory's.

### §S5 Query

`model` returns the objects with their ids, classes (or unclassified), labels and effective materials, the faces of one
object on request, and the unclassified list.

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema.
- [ ] `read-model` of `one_house_model()`'s inventory gives one model object per body, each with its feature group, its faces `<object id>/f<index>` and a label; replaying `model-read` gives the same ids.
- [ ] Objects without a stored id get `<feature group>.<n>` ids, unique, and are listed for write-back; an object with a stored id keeps it.
- [ ] With the rule `L0.walls → structure.wall`, every wall body of level 0 is a product of `structure.wall`; an object matched by no rule is unclassified and listed; a stored class the classification does not hold is refused with `unknown-class`.
- [ ] `classify-object` on an unclassified slab body with `structure.slab` yields `object-classified` and the object leaves the unclassified list.
- [ ] A face with no material of its own takes its body's; with its own material it keeps it.
- [ ] Caller-existence: `decideModel` and `classifyObjects` are called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

Model revisions and their changes (CR-PRT-009); the derived declaration (CR-PRT-027); the agent proposing classes and
labels (the harness's labelling skill, CR-PRT-029); classes below the first level of each branch (later, with the
catalogue's growth, D32).

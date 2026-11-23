# CR-PRT-004 — Building context

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-002, CR-PRT-003
**Labels:** domain, building, units
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §2 (all), §2.3a, §6; `docs/research/PRD-parti.md` D17, D19, D25

## Context

The building context holds the rooms, surfaces, openings, regions, guides and steps a target project declares, checks
them (B-1 to B-4), and records each re-import as a building revision with its changes. The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`. Units and display
conversions (D25) live here too, as pure functions every other part uses.

## Scope

### §S1 Model

`packages/domain/src/building/`: types `Building`, `Room`, `Surface`, `Opening`, `Region`, `Guide`, `Step`, `Site`,
`Quality` mirroring the declaration (PRD-domain §2.1, §2.4), keyed by declared ids. `initialBuilding` is empty at
revision 0.

### §S2 Import and rules

`decideBuilding(state, command)` handles `import-building` (payload: the declaration). It returns a refusal listing
every fault, or one `building-revised` event carrying the new building and its **changes** (§S3). Fault codes:
`duplicate-id`, `unknown-room` (B-1), `outside-surface` (opening or region outside its surface, B-1),
`openings-overlap` (B-2), `anchor-reversed` (B-4), `unsupported-units` (`units` other than `mm` without a `scale`).
Openings given with `"frame": "world"` are converted into the face frame. Lengths are multiplied by `scale` into
real-world millimetres. `evolveBuilding(state, event)` applies `building-revised`.

### §S3 Revision diff

`diffBuildings(previous, next)` returns `{ added, removed, resized, moved }` lists of ids for surfaces, and the same for
openings and regions, by declared id.

### §S4 Units (D25)

`packages/domain/src/units/`: `parseLength(text): number | Fault` accepts `1200`, `1200 mm`, `1.2 m`, `120 cm`,
`4 ft`, `4'`, `4' 6"`, `4 ft 6 in`, `54 in` and returns millimetres; `formatLength(mm, "ft-in" | "mm" | "m")`;
`formatArea(mm2, "sq ft" | "m2")`; `formatRunning(mm)` (running feet). One foot is exactly 304.8 mm.

### §S5 Steps (DM-7, subject to the owner's decision)

A surface's optional `steps` are kept; `stepsCrossed(surface, rect)` returns the steps a rectangle crosses, for the
design context's warnings.

## Acceptance criteria

### §S2
- [ ] Importing `oneBath` yields one `building-revised` event with revision 1 and five surfaces (`*.wall.N/E/S/W`, `*.floor`).
- [ ] Importing `faulty` yields one refusal with exactly the three labelled faults (`duplicate-id` or `unknown-room`, `openings-overlap`, `anchor-reversed`), and the state stays at the previous revision.
- [ ] An opening declared with `"frame": "world"` at a known world position lands at the expected face-frame x on an east wall and on a west wall (mirror check).
- [ ] A declaration with `"scale": 10` and a width of 347 gives a surface width of 3470.
### §S3
- [ ] Re-importing `oneBath` with the mirror region moved and the floor removed gives `moved` = [mirror id] and surfaces `removed` = [floor id].
### §S4
- [ ] `parseLength("4' 6\"")` = 1371.6; `parseLength("1.2 m")` = 1200; `parseLength("four feet")` is a fault `unparsable-length`.
- [ ] `formatLength(3810, "ft-in")` = `12′ 6″`; `formatArea(9290304, "sq ft")` = `100 sq ft`; `formatRunning(3048)` = `10 rft`.
### §S5
- [ ] `stepsCrossed` returns the step for a rectangle spanning it and none for one beside it.
### Integration
- [ ] Caller-existence: `decideBuilding` is called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

8 points.

## Risk

- DM-7 is proposed, not decided; §S5 changes or drops if the owner decides otherwise before RED.

## Non-goals

Polygonal floors, sloped faces, ceilings (later); the site's map integration (D24, later); reading the file from disk
(the adapter's and `parti-axi`'s job).

# CR-PRT-020 — Quantities

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-019
**Labels:** domain, quantities, units
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §3.4a; `docs/research/PRD-parti.md` D25 (units for bills of materials); JohnnyHouse #1658

## Context

Quantities are computed from the design, never entered: the placements, their setting-outs and the zones' visible cells.
Every number is stated with its counting rule, since the rule and the rounding change the result (676 against 681 in
JohnnyHouse's marble, #1658). The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.

## Scope

### §S1 Tile counts

`countTiles(cells, module, setOut)`: every grid tile of which any part shows inside the visible cells is one tile; a
tile cut by an edge, an opening or a keep-clear region is a whole tile; offcuts are not reused. Returns `full`, `cut`,
`laid` (= full + cut) and the area in mm².

### §S2 Quantities

`quantities(design, building, catalogue, settings)` returns lines per zone, per room and per finish: area (square feet,
D25), laid, **to buy** (laid × (1 + wastage), rounded up once per finish by default, or per room when
`rounding: "per-room"`), boxes when the finish states `piecesPerBox`, and for non-tile kinds the area with the wastage.
The result carries its `countingRule` (text and parameters: wastage, rounding) and `excludes` (thresholds, steps,
skirting unless zoned). Settings: `wastage` (default 0.10), `rounding` (`per-finish` default).

### §S3 Query

A `quantities` query (scope: whole design, a room, or a finish) answers through the gateway (CR-PRT-012) and
`parti-axi state --query quantities` (CR-PRT-013).

## Acceptance criteria

- [ ] A 2400 × 2400 zone, module 600, centre rule, no openings: 16 full, 0 cut; with a 900 × 2100 door cut out at the left edge: full and cut counts equal the hand count in the test (fixture with its drawing).
- [ ] A keep-clear region removes the tiles wholly inside it and leaves those it cuts as cut tiles; a tile-behind region removes none.
- [ ] Two rooms with laid 307 and 308 of one finish at 10 % give to-buy 677 per finish (ceil(615 × 1.1)) and 338 + 339 = 677 or 678 per room exactly as computed per room; the result states which rounding was used.
- [ ] A finish with `piecesPerBox: 4` and to-buy 677 gives 170 boxes.
- [ ] A paint placement gives its area in square feet and no tile count.
- [ ] Every result carries `countingRule` with wastage and rounding.
- [ ] Caller-existence: the gateway answers the `quantities` query by calling `quantities` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

Prices and cost estimates; paint litres and sheet counts (need coverage and sheet sizes in the catalogue); bills of
materials grouped by work-contract role (later).

# CR-PRT-005 — Catalogue context

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-002, CR-PRT-003
**Labels:** domain, catalogue
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §4 (all); `docs/research/PRD-parti.md` FR-CAT-1 to FR-CAT-6

## Context

The catalogue holds finishes as read-only products and answers the browser's queries. The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.

## Scope

### §S1 Model

`packages/domain/src/catalogue/`: type `Product` with the fields of FR-CAT-1 and PRD-domain §4.2's right-hand column,
including `kind` (`tile` | `wood-veneer` | `laminate` | `paint` | `metal`), `suitableUse`, `suitableSurfaces`, `classification`
(basis, confidence), `pictureOrientation` (`landscape` | `portrait` | `square`) and `images` (references, never data);
and by kind (PRD-domain §4.1): `source` (library or maker, asset, address, author, `licence`, retrieved date),
`scan` (`id`, real `widthMm` and `heightMm`, `grain`: `along-x` | `along-y`, `maps` available and used) and `stain`
(colour) for veneers and laminates; `colour` and `sheen` (`matt` | `eggshell` | `satin` | `gloss`) for paint; `treatment` (`plating` | `powder-coat` |
`brushed` | `anodised`), `colour`, `metallic` and `roughness` (each 0 to 1) for metal;
`assetRefs` (Unreal texture, material instance, master material) as references. A finish is a scan plus its stain
(DM-8): its main colour is the colour after the stain.

### §S2 Filters and search

`queryCatalogue(products, filter)` with the filter fields of PRD-domain §4.3, `kind` and `licence` among them (each optional; lists mean any-of), free
text over name, series and maker's code (case- and accent-insensitive), and `sort: "colour-wheel" | "name" | "size"`.
Colour-wheel order sorts by hue, with products under the `minStrength` filter's threshold placed after the coloured
ones, ordered by lightness.

### §S3 Goes with

`goesWith(products, id)` returns, in order: the same `set`'s members, the `pairsWith` products, then products whose hue
is complementary (180° ± 30°) and whose strength passes the threshold, at most 24 in all.

## Acceptance criteria

- [ ] On `makeProducts(200, 1)`, each single-field filter returns exactly the products holding that value (one test per field).
- [ ] Free text `"cafe"` matches a product named `Café Latte`.
- [ ] Filtering `kind: ["paint"]` returns only paints; filtering `licence: ["CC0"]` returns only finishes with that licence.
- [ ] Two veneers sharing a scan but with different stains are two products whose main colours are their stains' colours, and both name the same `scan.id`.
- [ ] A paint without `sheen` is invalid (`missing-field`); a metal with `metallic` 1.5 is invalid (`invalid-value`).
- [ ] Colour-wheel order is non-decreasing in hue for the coloured products, and every product under the strength threshold comes after them.
- [ ] `goesWith` lists set members first, then pairs, then complementary products, and never the product itself.
- [ ] Caller-existence: `queryCatalogue` and `goesWith` are called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

8 points (metal fits within it).

## Non-goals

Building the catalogue from records (CR-PRT-011); products of other layers (furniture, fittings); where each finish is used (with the world builder, DM-9).

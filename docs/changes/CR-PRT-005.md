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
including `suitableUse`, `suitableSurfaces`, `classification` (basis, confidence), `pictureOrientation`
(`landscape` | `portrait` | `square`) and `images` (references, never data).

### §S2 Filters and search

`queryCatalogue(products, filter)` with the filter fields of PRD-domain §4.3 (each optional; lists mean any-of), free
text over name, series and maker's code (case- and accent-insensitive), and `sort: "colour-wheel" | "name" | "size"`.
Colour-wheel order sorts by hue, with products under the `minStrength` filter's threshold placed after the coloured
ones, ordered by lightness.

### §S3 Goes with

`goesWith(products, id)` returns, in order: the same `set`'s members, the `pairsWith` products, then products whose hue
is complementary (180° ± 30°) and whose strength passes the threshold, at most 24 in all.

## Acceptance criteria

- [ ] On `makeProducts(200, 1)`, each single-field filter returns exactly the products holding that value (one test per field).
- [ ] Free text `"cafe"` matches a product named `Café Latte`.
- [ ] Colour-wheel order is non-decreasing in hue for the coloured products, and every product under the strength threshold comes after them.
- [ ] `goesWith` lists set members first, then pairs, then complementary products, and never the product itself.
- [ ] Caller-existence: `queryCatalogue` and `goesWith` are called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

Building the catalogue from records (CR-PRT-011); paint and other product kinds (later).

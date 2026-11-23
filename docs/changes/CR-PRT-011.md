# CR-PRT-011 — JohnnyHouse catalogue translator

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-005
**Labels:** translator, catalogue, python
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-domain.md` §4.2; `docs/research/DN-first-consumer-johnnyhouse.md`; `docs/Architecture.md` §5 (`catalogue-tools`)

## Context

The first target project's tile records become Parti products through a translator (R3), so no JohnnyHouse term
enters the domain. Images are referenced in place and never copied into Parti's repository (NFR-10, Q15).

## Scope

### §S1 Translator

`python/catalogue-tools`: `catalogue_tools.johnnyhouse.translate(records_dir) -> CatalogueBuild` reads the record
format described in DN-first-consumer-johnnyhouse and PRD-domain §4.2's left-hand column and writes products in the
schema's `Product` shape: suitable use and surfaces from the maker's classification (with basis and confidence),
picture orientation from the main image's aspect ratio (within 5 % of square → `square`), colour tags (main colour's
hue, strength, lightness, warm or cool) computed from the main image, images as paths relative to the target project.

### §S2 Output

`catalogue/products.json` in the folder the configuration names, plus `catalogue/report.json` listing every record
skipped and why (`missing-field`, `unreadable-image`), so nothing is dropped silently.

### §S3 Shortlist

`translate_selections(selections_json) -> list[ShortlistEntry]` reads JohnnyHouse's `selections.json` into shortlist
entries (product id, note), read once at import as PRD-domain §3.4 says.

## Acceptance criteria

- [ ] On a synthetic record folder in JohnnyHouse's format (generated in the test, plain-colour images), each record yields one product whose fields equal the expected values, and `validate_message`-level validation of each product passes.
- [ ] A 600 × 600 image gives `square`, 600 × 300 `landscape`, 300 × 600 `portrait`; 600 × 580 `square`.
- [ ] A record without a size and one with an unreadable image appear in `report.json` with `missing-field` and `unreadable-image`, and in no product.
- [ ] A plain red image gives hue within 0 ± 5°, strength above the threshold, `warm`.
- [ ] (reviewed, not tested) A local run on JohnnyHouse's real records in place reports its counts; no file under the repository changes.
- [ ] Caller-existence: `parti-axi catalogue build` calls `translate` (reviewed at CR-PRT-013 VERIFY).

## Estimated size

5 points.

## Non-goals

Other makers' feeds and paint (later); the makers' terms for redistributing images (Q15, an owner action).

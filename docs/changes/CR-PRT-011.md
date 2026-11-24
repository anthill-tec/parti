# CR-PRT-011 — Catalogue translator, with JohnnyHouse's records as first input

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-005
**Labels:** translator, catalogue, python
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-domain.md` §4.2; `docs/research/DN-first-consumer-johnnyhouse.md`; `docs/Architecture.md` §5 (`parti` library, `parti.catalogue`); `docs/research/PRD-parti.md` D27

## Context

A target project's finish records become Parti products through a translator (R3), so no project's term enters the
domain. The translator is part of the `parti` library (D27, `parti.catalogue`) and stays free of any one house (NFR-10):
a project's record format is described by a **mapping** the project owns; JohnnyHouse's records are the first input. Images are referenced in place and never copied into Parti's repository (NFR-10, Q15).

## Scope

### §S1 Translator

`parti.catalogue.translate(records_dir, mapping) -> CatalogueBuild` reads newline-delimited JSON records whose fields
are named by a **mapping** (a TOML file the target project owns: source field → Parti field, value maps such as
JohnnyHouse's `zone` → suitable use, kind names such as `metal_plating` → `metal`), as PRD-domain §4.2 describes and writes products in the
schema's `Product` shape: suitable use and surfaces from the maker's classification (with basis and confidence),
picture orientation from the main image's aspect ratio (within 5 % of square → `square`), colour tags (main colour's
hue, strength, lightness, warm or cool) computed from the main image, images as paths relative to the target project.

### §S1a Finishes database (wood veneer, laminate, paint)

`parti.catalogue.translate_finishes(finishes_dir, mapping)` reads JohnnyHouse's second database
(`data/finishes.ndjson`, `swatches/<id>.jpg`, JohnnyHouse #1648) into finishes of kinds `wood-veneer`, `laminate`,
`paint`, `metal` (JohnnyHouse `metal_plating` → `metal`, treatment `plating`), `exposed` (CN-001) and `glaze`: source and licence, source scan (real size, grain direction, maps), stain, sheen, Unreal asset references;
ids (`WV-001`, `PT-001`, `MT-001`) kept; effect paints carried with their `effect`; a veneer or laminate with
no scan carried as provisional (colour only); scans read from `data/scans.ndjson` (`SC-001`). A record of a kind
Parti does not know is listed in `report.json` as `unsupported-kind`, never dropped silently. `usage.json` is not read in 0.1.0 (DM-9). `translate` merges both sources into one
`products.json`, refusing a duplicate id across them.

### §S2 Output

`catalogue/products.json` in the folder the configuration names, plus `catalogue/report.json` listing every record
skipped and why (`missing-field`, `unreadable-image`), so nothing is dropped silently.

### §S3 Shortlist

`parti.catalogue.translate_selections(selections_json, mapping) -> list[ShortlistEntry]` reads JohnnyHouse's `selections.json` into shortlist
entries (product id, note), read once at import as PRD-domain §3.4 says.

## Acceptance criteria

- [ ] No module under `python/parti/src` names JohnnyHouse or one of its field names (a test greps the source for `johnnyhouse`, `zone`, `primary_surface`).
- [ ] On a synthetic record folder in JohnnyHouse's format (generated in the test, plain-colour images) with a synthetic mapping, each record yields one product whose fields equal the expected values, and `validate_message`-level validation of each product passes.
- [ ] A 600 × 600 image gives `square`, 600 × 300 `landscape`, 300 × 600 `portrait`; 600 × 580 `square`.
- [ ] A record without a size and one with an unreadable image appear in `report.json` with `missing-field` and `unreadable-image`, and in no product.
- [ ] A plain red image gives hue within 0 ± 5°, strength above the threshold, `warm`.
- [ ] On a synthetic finishes folder in #1648's format, a stained veneer record yields a `wood-veneer` product whose main colour is the stain's, with its licence and scan; a paint record yields a `paint` with its sheen and no image; a `metal_plating` record yields a `metal` with treatment `plating`; a record of kind `glass` appears in `report.json` as `unsupported-kind`; an effect paint keeps its two colours and pattern size; a laminate record without `scan_id` yields a provisional laminate.
- [ ] An id present in both the tile and the finishes sources is reported as `duplicate-id` and neither is written.
- [ ] (reviewed, not tested) A local run on JohnnyHouse's real records in place reports its counts; no file under the repository changes.
- [ ] Caller-existence: `parti-axi catalogue build` calls `parti.catalogue.translate` (reviewed at CR-PRT-013 VERIFY).

## Estimated size

8 points.

## Non-goals

Other makers' feeds (later); JohnnyHouse's `usage.json` (with the world builder, DM-9); the makers' terms for redistributing images (Q15, an owner action).

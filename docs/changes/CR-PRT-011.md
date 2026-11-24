# CR-PRT-011 — Catalogue build: the record formats and the library's tools

**Status:** PENDING (spec drafted 2026-11-23, revised 2026-11-24, noted 2026-11-24 for DM-10; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-005
**Labels:** catalogue, schema, python, library
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-domain.md` §4.1, §4.2, §4.2a, §4.4 (DM-10); `docs/research/PRD-parti.md` D27; `docs/Architecture.md` B3 (`parti.catalogue`)

## Context

A target project's records are translated into Parti's formats by **that project's own orchestrator agent**; Parti
provides the formats and the library's tools (D27, PRD-domain §4.2), as it does for the building declaration. This CR
publishes the formats and builds the tools; it contains no translator for any one project (NFR-10). Images are
referenced in place and never copied (NFR-10, Q15).

## Scope

### §S1 Formats

JSON Schemas in `packages/schema/v1/`: `catalogue.schema.json` (`parti.catalogue/1`: one finish per line, the fields of
PRD-domain §4.1 by kind, for all seven kinds), `scan.schema.json` (`parti.scan/1`), `shortlist.schema.json`
(`parti.shortlist/1`: product, note, optional target). Generated types and validation follow CR-PRT-002's pattern, in
TypeScript and in `parti.schema`.

### §S2 Build

`parti.catalogue.build(records, scans=None) -> CatalogueBuild` (the library, D27) validates each record, resolves each
finish's scan, derives the **picture orientation** from the main image's aspect ratio (within 5 % of square →
`square`), the **colour tags** (main colour's hue, strength, lightness, warm or cool) from the main image, or from the
stated colour when there is no image, and thumbnails into the catalogue folder; marks a veneer or laminate without a
scan as provisional; and writes `catalogue/products.json`, plus `catalogue/report.json` listing every record not taken
and why (`invalid-record` with the schema's faults, `unreadable-image`, `unknown-scan`, `duplicate-id`,
`unsupported-kind`), so nothing is dropped silently.

### §S3 Shortlist

`parti.catalogue.read_shortlist(path) -> list[ShortlistEntry]` reads a `parti.shortlist/1` file for the gateway's
one-time import of a project's existing shortlist.

### §S4 Helpers for a project's translator

`parti.catalogue.RecordWriter` writes valid `parti.catalogue/1` lines (refusing an invalid record at write time, with
its faults), so a project's agent writes its translation against the library rather than by hand; documented with a
synthetic example in the library's docstring and in Parti's catalogue skill (CR-PRT-013).

## Acceptance criteria

- [ ] No module under `python/parti/src` names a project (a test greps the source for `johnnyhouse`).
- [ ] A synthetic `parti.catalogue/1` file with one record of each of the seven kinds builds into seven products, each equal to the expected product.
- [ ] A 600 × 600 image gives `square`, 600 × 300 `landscape`, 300 × 600 `portrait`; 600 × 580 `square`.
- [ ] A plain red image gives hue within 0 ± 5°, strength above the threshold, `warm`; a paint with colour `#1E3A8A` and no image gets a blue hue from its stated colour.
- [ ] A record failing the schema, one with an unreadable image, one naming an unknown scan, a duplicate id and a kind `glass` each appear in `report.json` with `invalid-record`, `unreadable-image`, `unknown-scan`, `duplicate-id` and `unsupported-kind`, and in no product.
- [ ] A laminate without a scan is built `provisional`; two veneers naming one scan with two stains are two products.
- [ ] `RecordWriter` refuses a tile without a size, naming the field.
- [ ] `read_shortlist` reads a synthetic file of three entries, one with a target.
- [ ] (reviewed, not tested; workstation) JohnnyHouse's orchestrator's output in `parti.catalogue/1` builds, its report read; no file under the repository changes.
- [ ] Caller-existence: `parti-axi catalogue build` calls `parti.catalogue.build`, and the gateway's shortlist import calls `read_shortlist` (reviewed at CR-PRT-013 and CR-PRT-012 VERIFY).

## Record format (DM-10; owner, 24 November 2026)

The product model (PRD-domain §4.2a, §4.4) structures `parti.catalogue/1`'s records as identity fields (with the `class`, D32) plus **form**, **build-up**, **appearance** and **quantities**; the fields are those above, grouped; `build` also checks each record's class against the Finishes branch. The size is to be
re-estimated at the spec review (the owner).

## Estimated size

8 points.

## Non-goals

Any project's translator (each project's own agent writes it); where finishes are used (with the world builder, DM-9);
the makers' terms for redistributing images (Q15, an owner action).

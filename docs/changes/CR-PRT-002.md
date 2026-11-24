# CR-PRT-002 — Message schema v1

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (0.1.0 = the building from CAD); filed on the Crucible board.
**Priority:** High
**Depends on:** CR-PRT-001
**Labels:** schema, contract
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/PRD-domain.md` §7 (messages), §2.4 (declaration); `docs/Architecture.md` A4 (R5, R6), B2 (R8), B4; `docs/research/DN-ubiquitous-language.md` rule 7

## Context

One versioned message schema is the only contract between the page, the gateway, the scene adapters and `parti-axi`
(R5); types are generated from it, and every incoming message is validated against it (R8). PRD-domain §7 lists
0.1.0's commands, events and queries; §2.4 defines the declaration file, which the schema also covers.

Under the roadmap of 24 November 2026, this CR lays the schema's frame (envelopes, registry names, generation,
validation, the glossary's schema column) with the Building and Session messages. Every later CR adds its own
context's messages to the same files under the same rules: the workflow (CR-PRT-022), the sources (CR-PRT-028), the
model inventory and the model's products (CR-PRT-025, CR-PRT-026), the declaration's derivation (CR-PRT-027); the
design messages arrive in 0.2.0 and the conditions in 0.4.0.

## Scope

### §S1 Schema files

JSON Schema (draft 2020-12) files in `packages/schema/v1/`: `envelope.schema.json`, `commands.schema.json`,
`events.schema.json`, `queries.schema.json`, `snapshot.schema.json`, `declaration.schema.json` (format
`parti.building/1`). Schema version string `parti.messages/1`.

### §S2 Envelopes

- **command:** `{ "type": "command", "name", "commandId" (UUID), "expectedRevision" (integer ≥ 0), "payload" }`.
- **event:** `{ "type": "event", "name", "eventId" (UUID), "aggregate", "sequence" (integer ≥ 1), "at" (RFC 3339),
  "causedBy" (commandId), "payload" }`.
- **refusal:** `{ "type": "refusal", "commandId", "faults": [ { "code", "message", "path"? } ] }`.
- **query / answer:** `{ "type": "query", "name", "queryId", "params" }` → `{ "type": "answer", "queryId", "result" }`.
- **snapshot:** `{ "type": "snapshot", "revision", "building", "session" }`, sent to a client on joining; later CRs add
  their context's part (`model`, `workflow`, `sources`; `design` in 0.2.0) as optional members.

### §S3 The messages of this CR

Commands: `import-building`, `select`. Events: `building-revised`, `selection-changed`. Queries: `building`,
`surface`, `history`. Each payload's fields follow PRD-domain §2 (the building) and §5 (the selection). The other
names of PRD-domain §7 are not in this CR (see Context).

### §S3a Registry-ready

Every command, event and query schema carries a stable registry name and version in its `$id`
(`parti.<context>.<message>/1`, for example `parti.design.zone-defined/1`), so the files can be registered in Nai's
schema registry unchanged when the bus moves there (D9, D29).

### §S4 Generated types and validation

`bun run --filter @parti/schema generate` writes `packages/schema/src/generated/*.ts` from the schema files; the
generated files are committed and a test fails when they are stale. `@parti/schema` exports
`validateMessage(value: unknown): { ok: true, message } | { ok: false, faults }` and
`validateDeclaration(value: unknown)` with the same shape. `parti.schema` (the library, D27) validates the same files in Python
(the `jsonschema` package), so both stacks read one source.

### §S5 The glossary's schema column (rule 7)

The Terms table of `docs/research/DN-ubiquitous-language.md` gains a fourth column, **Schema**, naming for each term
that is data the schema type it names: a message `$id` (`parti.building.building-revised/1`) or a type defined in a
schema file (`parti.building/1#/$defs/surface`). A term that is not data leaves it empty. A repository guard test
(beside the existing ones in `tests/`) reads the column and every schema file, and fails when a schema type or message
`$id` has no term naming it, or when a Schema cell names a type that no schema file defines. Later CRs that add
messages add their terms' Schema cells in the same change.

## Acceptance criteria

### §S1–§S3
- [ ] `validateMessage` accepts one valid example of each of the 2 commands, 2 events and 3 queries of §S3, the answer, the refusal and the snapshot (fixtures in `packages/schema/test/fixtures/valid/`).
- [ ] `validateMessage` refuses: an unknown `name` (fault code `unknown-message`); a missing `commandId` (`missing-field`, path `/commandId`); a negative `expectedRevision` (`invalid-value`); an extra top-level field (`unknown-field`).
- [ ] `validateDeclaration` accepts PRD-domain §2.4's example and a declaration with `references.columns`, quality objects (`{ level, note }`), `guides` with `towards` and `steps`, and refuses a surface without `room` (`missing-field`, path `/surfaces/0/room`) and a `format` other than `parti.building/1` (`unsupported-format`).
### §S3a
- [ ] Every schema file under `packages/schema/v1/` has an `$id` matching `^parti\.[a-z]+\.[a-z-]+/[0-9]+$`, and no two share one.
### §S4
- [ ] The staleness test regenerates into a temporary folder and fails when it differs from `src/generated/`.
- [ ] `parti.schema.validate_message` returns the same fault codes as `validateMessage` for the same invalid fixtures (a shared fixture set, run by both test suites).
### §S5
- [ ] The glossary's Terms table has the Schema column; the guard test passes on the tree, and fails (asserted in the same test against temporary copies) when a message `$id` is added with no term, and when a Schema cell names an unknown type.
- [ ] Every `$id` of this CR's schema files has its term in the glossary.
### Wiring
- [ ] Caller-existence: by 0.1.0's end, `validateMessage` has non-test callers in `packages/gateway/src` and `parti.schema.validate_message` in `python/parti-axi/src` (reviewed at CR-PRT-012 and CR-PRT-013 VERIFY).

## Estimated size

5 points.

## Risk

- Generator choice (`json-schema-to-typescript` or equivalent) is settled in the gap analysis; the ACs hold either way.

## Non-goals

C++, Rust or Avro generation (later, Architecture B3); the other contexts' messages (their own CRs, see Context); messages of later releases (PRD-domain §7, last paragraph).

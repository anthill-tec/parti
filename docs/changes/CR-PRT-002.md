# CR-PRT-002 — Message schema v1

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-001
**Labels:** schema, contract
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/PRD-domain.md` §7 (messages), §2.4 (declaration); `docs/Architecture.md` §3 R5, R6, R8, §6

## Context

One versioned message schema is the only contract between the page, the gateway, the scene adapters and `parti-axi`
(R5); types are generated from it, and every incoming message is validated against it (R8). PRD-domain §7 lists
0.1.0's commands, events and queries; §2.4 defines the declaration file, which the schema also covers.

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
- **snapshot:** `{ "type": "snapshot", "revision", "building", "design", "session" }`, sent to a client on joining.

### §S3 The 0.1.0 messages

Command names: `import-building`, `define-zone`, `resize-zone`, `remove-zone`, `place-product`, `clear-zone`,
`save-scheme`, `apply-scheme`, `add-to-shortlist`, `remove-from-shortlist`, `undo`, `redo`, `select`, `set-time`,
`set-weather` (`place-product` with an optional `setOut`; `add-to-shortlist` with an optional `target`). Event names: `building-revised`, `zone-defined`, `zone-resized`, `zone-removed`, `product-placed`,
`zone-cleared`, `scheme-saved`, `scheme-applied`, `shortlisted`, `unshortlisted`, `selection-changed`,
`setting-changed`, `follow-up-raised`, `follow-up-resolved`, `set-out-changed`. Query names: `building`, `surface`, `design`, `catalogue`,
`goes-with`, `shortlist`, `follow-ups`, `history`, `quantities`. Each payload's fields follow PRD-domain §2–§6.

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

## Acceptance criteria

### §S1–§S3
- [ ] `validateMessage` accepts one valid example of each of the 15 commands, 15 events, 9 queries, the answer, the refusal and the snapshot (fixtures in `packages/schema/test/fixtures/valid/`).
- [ ] `validateMessage` refuses: an unknown `name` (fault code `unknown-message`); a missing `commandId` (`missing-field`, path `/commandId`); a negative `expectedRevision` (`invalid-value`); an extra top-level field (`unknown-field`).
- [ ] `validateDeclaration` accepts PRD-domain §2.4's example and refuses a surface without `room` (`missing-field`, path `/surfaces/0/room`) and a `format` other than `parti.building/1` (`unsupported-format`).
### §S3a
- [ ] Every schema file under `packages/schema/v1/` has an `$id` matching `^parti\.[a-z]+\.[a-z-]+/[0-9]+$`, and no two share one.
### §S4
- [ ] The staleness test regenerates into a temporary folder and fails when it differs from `src/generated/`.
- [ ] `parti.schema.validate_message` returns the same fault codes as `validateMessage` for the same invalid fixtures (a shared fixture set, run by both test suites).
- [ ] Caller-existence: by 0.1.0's end, `validateMessage` has non-test callers in `packages/gateway/src` and `parti.schema.validate_message` in `python/parti-axi/src` (reviewed at CR-PRT-012 and CR-PRT-013 VERIFY).

## Estimated size

5 points.

## Risk

- Generator choice (`json-schema-to-typescript` or equivalent) is settled in the gap analysis; the ACs hold either way.

## Non-goals

C++, Rust or Avro generation (later, Architecture §5); messages of later releases (PRD-domain §7, last paragraph).

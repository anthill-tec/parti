# CR-PRT-010 — Local JSON event store

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: scope kept, plus the new logs and the model snapshot (PRD-domain §8: `sources.ndjson`, `model.ndjson`, `model/inventory.json`).
**Priority:** High
**Depends on:** CR-PRT-002
**Labels:** adapter, storage
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §8; `docs/research/PRD-parti.md` Q11, D9; `docs/Architecture.md` A4 (R2, R6)

## Context

0.1.0 stores events as JSON lines and snapshots in the target project (PRD-domain §8), behind ports so Nai replaces
the store later without touching the domain or the gateway.

## Scope

### §S1 Ports

`packages/domain/src/ports.ts` declares (types only, no implementation): `EventStore { append(aggregate,
expectedSequence, events): Promise<AppendResult>; read(aggregate, fromSequence?): AsyncIterable<Event> }` and
`SnapshotStore { write(name, value): Promise<void>; read(name): Promise<unknown | null> }`.

### §S2 JSON adapter

`packages/adapters-local/src/json-store.ts`: `JsonEventStore(root)` writes `events/<aggregate>.ndjson`, one event per
line; `append` refuses with `sequence-conflict` when the log's last sequence differs from `expectedSequence`; an append
is atomic (the new file content written to a temporary file in the same folder, then renamed). `JsonSnapshotStore`
writes `design.json` and `shortlist.json` the same way. A torn last line (a crash during a write by an older version or
by hand) is reported as `corrupt-log` with its line number, never silently skipped.

### §S3 Rebuild

`rebuildSnapshots(eventStore, snapshotStore, domain)` replays the logs through `evolve` and rewrites the snapshots;
deleting the snapshots and rebuilding gives identical files.

## Acceptance criteria

- [ ] Module tests run the same port contract suite against `JsonEventStore` (in a temporary folder) and an in-memory store: append, read back in order, read from a sequence, `sequence-conflict` on a stale append.
- [ ] Killing the process between the temporary write and the rename (simulated by a failing rename) leaves the previous log intact.
- [ ] A log with a torn last line is reported as `corrupt-log` at that line.
- [ ] Deleting `design.json` and running `rebuildSnapshots` produces a file byte-identical to the one deleted.
- [ ] Caller-existence: the gateway constructs `JsonEventStore` at start-up (reviewed at CR-PRT-012 VERIFY).

## Estimated size

5 points.

## Non-goals

Several writers on one target project at once (one gateway per target project in 0.1.0); the Nai store (later).

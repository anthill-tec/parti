# CR-PRT-012 — Gateway

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-004, CR-PRT-005, CR-PRT-006, CR-PRT-007, CR-PRT-008, CR-PRT-009, CR-PRT-010, CR-PRT-020
**Labels:** gateway, websocket
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/Architecture.md` §5 (gateway), §6 (how a change travels), §3 (R5–R8); `docs/research/PRD-parti.md` NFR-7, NFR-8

## Context

The gateway is the one process the page, the mock scene and `parti-axi` connect to. It runs every command through
the domain, stores the events, and fans them out to every connection (Architecture §6).

## Scope

### §S1 Server

`packages/gateway/src/main.ts` (Bun): `parti-gateway --target <dir> [--port <n>]` reads the target project's
configuration, binds a WebSocket server and an HTTP server to `127.0.0.1` only (NFR-8; default port 4710), serves the
page's built files at `/`, and prints one JSON line `{ "ready": true, "port": <n> }` when listening.

### §S2 Command path

For each message: `validateMessage` (refusal `invalid-message` with the schema's faults otherwise); route by command to
`decideBuilding`, `decideDesign` or `decideSession`; append the events through the event store with the aggregate's
expected sequence; run `followBuilding` after `building-revised` and append its events; send the events to every
connection; rewrite the snapshots. A command id seen before returns the original outcome without new events (safe to
repeat, R6).

### §S3 Queries and joining

Queries answer from the current state (`building`, `surface`, `design`, `catalogue`, `goes-with`, `shortlist`,
`follow-ups`, `history`, `quantities`). A new connection first receives a `snapshot`. On start the state is rebuilt from the logs.

### §S4 Catalogue

The catalogue is read from `catalogue/products.json` at start and on the `catalogue-reload` signal (SIGHUP).

## Acceptance criteria

- [ ] (integration) Two WebSocket clients connect to a gateway on a temporary target project with `oneBath`; client A sends `define-zone`; both receive the `zone-defined` event; `events/design.ndjson` holds it.
- [ ] Sending the same command id twice yields one event in the log and the same reply twice.
- [ ] An invalid message gets a refusal `invalid-message` and the connection stays open.
- [ ] A command with a stale `expectedRevision` gets `stale-revision`, and no event is stored.
- [ ] Restarting the gateway and querying `design` returns the same design as before the restart.
- [ ] A late-joining client's first message is a `snapshot` whose `revision` equals the design's.
- [ ] Re-importing the building without the floor stores the `building-revised` event followed by the `follow-up-raised` events.
- [ ] Connecting from a non-loopback address is impossible: the server's bound address is `127.0.0.1` (asserted from the server object).
- [ ] Caller-existence: grep finds `validateMessage`, `decideBuilding`, `decideDesign`, `decideSession`, `followBuilding`, `queryCatalogue`, `goesWith`, `quantities` and `JsonEventStore` called in `packages/gateway/src`.

## Estimated size

8 points.

## Risk

- Port 4710 may be taken on a workstation; `--port 0` (any free port) is supported and the ready line carries the port.

## Non-goals

Authentication and remote access (later, with the editions); the agent API (D16, later).

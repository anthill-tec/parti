# CR-PRT-012 — Gateway

**Status:** PENDING (spec drafted 2026-11-23, revised 2026-11-24 for the workflow driver, rewritten the same day for the roadmap; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten: 0.1.0's messages (PRD-domain §7), the agent API (D16) as one WebSocket endpoint exchanging CloudEvents (PRD-parti D35), described for Nai's source and sink; the Nai adapter behind the ports is CR-PRT-031's; the design and catalogue commands move to 0.2.0.
**Priority:** High
**Depends on:** CR-PRT-004, CR-PRT-005, CR-PRT-008, CR-PRT-009, CR-PRT-010, CR-PRT-022, CR-PRT-026, CR-PRT-027, CR-PRT-028
**Labels:** gateway, websocket, cloudevents
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/Architecture.md` B3 (gateway), B4 (how a change travels; the message bus), B6, §3 (R5–R8); `docs/research/PRD-parti.md` NFR-7, NFR-8, D16, D29, D33, D35; `docs/research/PRD-domain.md` §5, §7, §8, §11

## Context

The gateway is the one process the page, `parti-axi`, the harness and Nai's generic source and sink connect to. It runs
every command through the domain, stores the events, and sends them to every connection (Architecture B4). Every system
on the bus serves a WebSocket endpoint exchanging CloudEvents (D35); the gateway's is Parti's, and its own fan-out is the
local adapter behind the same ports, for offline work and tests (B6). Nai's source and sink connect to it as clients,
configured by its definition (CR-PRT-031).

## Scope

### §S1 Server

`packages/gateway/src/main.ts` (Bun): `parti-gateway --target <dir> [--port <n>]` reads the target project's
`parti.toml`, binds one HTTP and WebSocket server to `127.0.0.1` only (NFR-8; default port 4710, `0` for any free
port), serves the Project Environment (CR-PRT-021) at `/`, the endpoint at `/events`, its definition at
`/asyncapi.json`, and prints one JSON line `{ "ready": true, "port": <n> }` when listening.

### §S2 The endpoint (D35)

Every message on `/events` is a **CloudEvent 1.0** in structured JSON, over the WebSocket subprotocol
`cloudevents.json`: `type` the message's registry name
(`parti.<context>.<message>/1`, CR-PRT-002), `dataschema` its JSON Schema's `$id`, `source` the sender (`parti/gateway`,
or the connection's participant), `id` the command or event id. A command is a request; its reply (the events, or the
refusal) carries the request's id in the extension attribute `nairequestid`. A connection first says who it is
(`hello`: a participant, `user` or `agent`, with a name; D16: an agent takes part like a person). The **definition**
(`packages/gateway/asyncapi.json`, AsyncAPI 3.0) is generated from the schema registry at build time: one channel, the
messages each way with their schemas, so Nai's generic source and sink can be configured from it.

### §S3 Command path

For each command: `validateMessage` (refusal `invalid-message` with the schema's faults otherwise); route it to
`decideBuilding`, `decideSources`, `decideModel`, `decideDeclaration`, `decideSession` or `decideWorkflow`; append the
events through the `EventStore` port to their log (`building`, `sources`, `model`, `workflow`; CR-PRT-010) with the
aggregate's expected sequence (`stale-revision` otherwise, nothing stored); run `followModel` after `model-revised`
(CR-PRT-009) and append its events; send the events to every connection; rewrite the snapshots. A command id seen before
returns the original outcome without new events (safe to repeat, R6). Events naming objects for **write-back**
(`model-read`, `object-classified`; CR-PRT-026) reach the model watcher (`parti-axi model watch`, CR-PRT-013), which
stores the ids in the CAD (CR-PRT-025's `tag`).

### §S4 The workflow driver and the interaction events

After each change the gateway computes the checks' **facts** (CR-PRT-022 §S4) from its queries and from the **step
records** the library appends (`parti/steps/records.ndjson`, CR-PRT-024; the file is watched and read, never written),
runs `checkWorkflow` and appends the `todo-ticked` events. The workspace commands from `decideWorkflow` are sent to
every connection. Interaction events (`parti.interaction.*/1`) are validated, kept in the session's context through
`recordInteraction` (CR-PRT-008) and sent to every connection; they are never stored in a log.

### §S5 Queries and joining

Queries answer from the current state: `building`, `sources`, `model`, `history`, `workflow`, `context` (the selection
and the interaction events), `classification`. A new connection, after `hello`, first receives a `snapshot` of every
context with its sequence numbers, then the events after them. On start the state is rebuilt from the logs; a log
reported `corrupt-log` stops the start with that fault.

## Acceptance criteria

- [ ] (integration) Two WebSocket clients say `hello` to a gateway on a temporary target project; client A sends `import-building` with `oneBath`; both receive `building-revised`, each a CloudEvent whose `type` and `dataschema` name the registry entry; `events/building.ndjson` holds it.
- [ ] A's reply carries `nairequestid` equal to its command's id.
- [ ] `/asyncapi.json` validates as AsyncAPI 3.0 and names every 0.1.0 message of PRD-domain §7 with its schema.
- [ ] Sending the same command id twice yields one event in the log and the same reply twice.
- [ ] An invalid message gets `invalid-message` and the connection stays open; a stale expected revision gets `stale-revision` and nothing is stored.
- [ ] Restarting the gateway and querying `model` and `building` returns the same state as before the restart; a log with a torn last line stops the start with `corrupt-log`.
- [ ] `read-model` of `one_house_model()` then of its second revision stores `model-read`, then `model-revised` followed by `followModel`'s events.
- [ ] With *Build from data* active, a step record appended for `L0.walls` with its checks passed yields `todo-ticked` for that feature group.
- [ ] A `selected` interaction event from client A reaches client B, `context` returns it, and no log file changes.
- [ ] A late-joining client's first message after `hello` is a `snapshot` whose sequence numbers equal the logs'.
- [ ] The server's bound address is `127.0.0.1` (asserted from the server object).
- [ ] Caller-existence: grep finds `validateMessage`, `decideBuilding`, `decideSources`, `decideModel`, `classifyObjects`, `decideDeclaration`, `deriveDeclaration`, `followModel`, `decideSession`, `recordInteraction`, `decideWorkflow`, `checkWorkflow` and `JsonEventStore` called in `packages/gateway/src`.

## Estimated size

8 points.

## Risk

- Port 4710 may be taken on a workstation; `--port 0` is supported and the ready line carries the port.

## Non-goals

The Nai adapter behind the ports and Nai's source and sink (CR-PRT-031; the connectors are Nai's, D34); the design and
catalogue commands (0.2.0); the mock scene (with the walkthrough, CR-PRT-016, 0.4.0); authentication and remote access
(later, with the editions).

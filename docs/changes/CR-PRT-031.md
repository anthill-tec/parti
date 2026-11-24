# CR-PRT-031 — Nai integration

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run; **depends on Nai's answers** to DN-nai-readiness §5, items 1, 4, 12, 13 and 14, not yet sent: Nai is not on Sandesh)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-010, CR-PRT-012
**Labels:** nai, bus, schema
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` D9, D29, D33, D35, D38, D39; `docs/research/DN-nai-readiness.md` §3, §4, §5; `docs/Architecture.md` B3 (`nai/`), B4, B6

## Context

Nai is the bus from 0.1.0 (D33): every system serves a WebSocket endpoint, and Nai's generic WebSocket source and sink,
written by the Nai project, connect to them, configured by each endpoint's definition (D35). Parti's router, in Nai's
DSL, is part of Parti's main source, and Parti's repository is a Nai project (D38). In 0.1.0 the bus carries the traffic
between Parti's two processes, the gateway and the harness (CR-PRT-012, CR-PRT-029), and takes the interaction events
for the agents' context. The gateway's own fan-out stays as the local adapter, for offline work and tests (B6). The
Nai-facing details are finalised with Nai's orchestrator (DN-nai-readiness §5); this spec is Parti's understanding
from Nai's documentation, and is revised with its answers before the gap analysis.

## Scope

### §S1 Parti as a Nai project

`nai.toml` at the repository's root names Parti, declares its schema namespace (`parti`) and its pipelines in `nai/`.
`nai/schemas/` registers Parti's message schemas from the schema registry (CR-PRT-002), generated, never written by
hand; a guard test keeps them equal to `packages/schema/v1`.

### §S2 The endpoints on the bus

`nai/connectors/`: the configuration (TOML) of a generic source and sink instance for the gateway's endpoint and for
the harness's, each pointing at its AsyncAPI definition (`/asyncapi.json`, CR-PRT-012, CR-PRT-029). Parti writes no
connector (D34).

### §S3 The router's first pipelines

In Nai's DSL, on the payloads the connectors unwrap: **gateway to harness**: the workflow's events, `said`, the
interaction events; **harness to gateway**: its commands, with `nairequestid` kept so the reply finds its request;
**interaction events** also into the bus's store for the agents' context, outside the design's history (item 9). A
message failing its schema goes to the dead-letter queue with a named fault, and nothing reaches the other side.

### §S4 Choosing the bus

`parti.toml`'s `bus = "nai" | "local"`: with `nai`, the harness connects only to its own endpoint and the router carries
its traffic; with `local` (the default when `parti-axi init --no-nai`), it connects to the gateway directly. The
gateway is the same in both.

### §S5 The Parti template

The specification of Parti's template for `nai new` (D39): what it generates (the project's `nai.toml`, its schema
subdomain under Parti's domain, its connector instances pointing at the project's gateway and harness), written in
`nai/template/README.md` and sent to Nai as a CReq (item 14); Nai's tool carries it.

## Acceptance criteria

- [ ] `nai check` passes on the repository (in CI, once Nai's install is available to it).
- [ ] The guard test finds `nai/schemas/` equal to the schema registry; a schema changed in one place only fails it.
- [ ] `nai test` scenarios (`nai/tests/*.test.toml`): a `step-started` from the gateway reaches the harness's sink unchanged in its payload; a harness command reaches the gateway with its `nairequestid`; a `selected` interaction event reaches the harness and the store, and no log of the gateway's; a message failing its schema is dead-lettered with its fault (V4).
- [ ] Live (`PARTI_LIVE=1`, a workstation with Nai): the validation spike's V1, V3 and V7 pass with the gateway and the harness (DN-nai-readiness §4), their measurements recorded in the CR's completion notes.
- [ ] With `bus = "local"`, CR-PRT-029's integration run passes without Nai.
- [ ] (reviewed) `nai/template/README.md` states what the template generates, and the CReq is sent to Nai's orchestrator.
- [ ] Caller-existence: `parti-axi init` runs `nai new` with the template's name (CR-PRT-013 VERIFY); the harness reads `bus` (CR-PRT-029 VERIFY).

## Estimated size

8 points.

## Risk

- **Nai's readiness.** The generic connectors, the registry's namespaces, the request id, pipelines from another
  repository and the template are Nai's work (§5 items 1, 4, 12, 13, 14), needed by 21 December 2026. If they are late,
  0.1.0 ships with `bus = "local"` and this CR moves to 0.2.0, decided at the wave-4 boundary with the owner.

## Non-goals

The connectors themselves (Nai's); EntityStore for the design and the catalogue (CR-PRT-038, 0.2.0); the applications'
endpoints (0.2.0 onwards); project pipelines (CR-PRT-075, 0.5.0); telemetry (CR-PRT-064, 0.6.0); the Nai agents
keeping the router current (D29, later).

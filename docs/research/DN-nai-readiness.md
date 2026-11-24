# DN — Nai and EntityStore readiness for Parti's message bus

**Date:** 2026-11-24
**Status:** Findings from a read-only audit of the code, for the owner and for the request to Nai's team. Nothing was run
or measured. Feeds D9 (reconsidered), D29 and Q13.
**Author:** Parti orchestrator (vidushi-parti)
**Sources:** `~/Documents/data_projects/nai` (code and docs, read only), `~/Documents/data_projects/4pm-EntityStore-service`
(read only); `PRD-parti.md` D9, D21, D29; `../Architecture.md` B4, B6

## 1. What Parti intends (D29)

1. An application's plugin (Unreal, Blender, SolidCraft) sends its state change to Nai over WebSocket. Nai checks it
   against the schema registry, its DSL turns it into a Parti event, and Nai pushes it in near real time to the Parti
   runtime (the Bun gateway).
2. Parti changes state and updates its domain objects in the shared EntityStore through EntityStore's REST API.
3. Nai's source connectors on EntityStore's change streams (CDC) propagate each change to every listener: the
   applications' plugins (by RPC) and the agent in the harness.
4. The Bun gateway and the Python harness, two separate processes, communicate through Nai (inter-process messaging),
   when required only.
5. Nai agents in the harness use Nai's REST interfaces to inspect events and debug the DSL, and configure connectors
   and pipelines in a closed loop.
6. Parti's backend processing may itself be written in Nai's DSL (Q13).

## 2. Findings

| Capability | Status | Evidence |
|---|---|---|
| DSL transforms, keyed ordering and state | Exists | `crates/nai_runtime`, `docs/nai_architecture.md` |
| Schema registry | Exists | `crates/nai_schema_registry`, `crates/nai_schema_store` |
| EntityStore REST API | Exists | `4pm-EntityStore-service` |
| Nai source connector on EntityStore's change streams | **Exists** | `ecosystem/nai_connector_entitystore_source`; CR-NAI-329 and CR-NAI-329b COMPLETED (2026-06-23). Offsets by SSE `Last-Event-ID`; durable consumer-group offsets (EntityStore CReq R1) and `version`/`schemaVersion` on change events (R2) are pending on EntityStore's side |
| Nai sink connector into EntityStore | Exists | `ecosystem/nai_connector_entitystore_sink`; CR-NAI-330 COMPLETED (2026-06-24) |
| Request-reply (RPC-like) connector | Exists | `ecosystem/nai_connector_request_reply` |
| WebSocket as a **client** (Nai connects out to a WebSocket server) | Exists | `crates/nai_runtime/src/connector/http.rs` (`run_websocket`); predates the connector SDK refactor (DN-Wave-10 notes it for modernisation) |
| WebSocket **server** for plugins or the gateway to connect into Nai, and a WebSocket sink | **Missing** | none found; WebSocket in service mode is deferred (`docs/research/PRD-Service-Backend-Mode.md` Q7) |
| Connector for a Python process (the harness) | **Missing** | none specific; the request-reply and HTTP connectors are the nearest |
| Creating and changing connectors and pipelines at runtime through an API (for the Nai agents) | Unconfirmed | to ask Nai's team |
| REST interfaces to inspect events on the wire | To confirm | the owner reports them; their paths were not located in this read |
| Round-trip latency (plugin → Nai → gateway → EntityStore → CDC → Nai → listeners) | **Not measured** | nowhere in the repository |

**The connector SDK.** Nai's connectors are built on its Rust connector SDK and its gRPC bridge
(`crates/nai_bridge_proto/proto/bridge.proto`), which is the bridge **for connectors**. Parti's components do not talk
to Nai through it directly: they talk to the connectors that are built for them.

## 3. What follows (owner, 24 November 2026)

- **New connectors for Parti's backend components, on Nai's Rust connector SDK:** a **WebSocket connector** for the
  Bun gateway (and for the applications' plugins), and a connector for the **Python executable that contains the
  agentic harness**. The inter-process messaging between the gateway and the harness then runs through Nai.
- **They are built in Nai's ecosystem** (`ecosystem/nai_connector_parti_*`), by Nai's team, from Parti's specifications
  sent as requests (CReqs); Parti consumes them. Parti stays Bun and Python, with no Rust stack of its own.
- **SolidCraft too** (owner, 24 November 2026; PRD-parti D34): a SolidCraft connector (a Rust process joining the
  running application to the bus), built by Nai's team as a CReq. The SolidCraft plugin inside the application is Parti's
  own (Rust, in 0.2.0).
- **LangChain is Python (and JavaScript) only**, so the harness stays Python (D21); it reaches Nai through its connector.

## 4. Validation spike (before the first release that connects a real application)

| # | Scenario | Pass |
|---|---|---|
| V1 | A test plugin sends a pick over WebSocket to the Parti connector; the registry accepts it; the DSL turns it into `selection-changed` and pushes it to the gateway | arrives at the gateway; p95 under 100 ms on one workstation |
| V2 | The gateway writes a placement to EntityStore over REST; the CDC source connector emits it; the DSL addresses it to the plugin; the plugin's RPC endpoint receives it | received once, in order per aggregate; p95 under 250 ms end to end |
| V3 | The harness subscribes through its connector and receives V2's change; it sends a command back to the gateway through Nai | both directions arrive; no loss across a harness restart (offsets resumed) |
| V4 | A message failing the schema | refused with a named fault; dead-letter queue holds it; nothing reaches the gateway |
| V5 | A Nai agent changes a DSL transform through the API and re-runs V1 | the new transform applies without restarting Nai, or the restart cost is stated |
| V6 | EntityStore restarts during V2 | no change lost or duplicated once R1 (durable offsets) is in place; stated behaviour before it |
| V7 | Developer workstation | Nai, EntityStore (Redis, MongoDB) and the connectors start with one command on Linux; resources stated |

## 5. The request to Nai's team and EntityStore's owner

Drafted 24 November 2026 and **sent to Nai's Mainline over Sandesh as soon as Nai is on Sandesh** (not yet, 24 November
2026), well ahead of need, so Nai's team can plan the work and ship a usable Nai install (owner, 24 November 2026). Each item is needed by a date set back from the release that uses it
(the targets on the Crucible board are placeholders, PRD-parti D33):

| Needed by | For | Items |
|---|---|---|
| 15 Dec 2026 | the validation spike (§4) before 0.1.0's wave 4 | a **workstation install** of Nai with EntityStore, one command on Linux, versioned (V7); 2 (runtime API, REST paths); 4 (schema registry) |
| 4 Jan 2027 | 0.1.0 (CR-PRT-031, Nai integration; CR-PRT-012 gateway; CR-PRT-029 harness; CR-PRT-025 live read) | 1 (the two connectors), 3 (latency), 9 (interaction events), 12 (the SolidCraft connector) |
| 15 Feb 2027 | 0.2.0 (CR-PRT-038, EntityStore for the design and the catalogue) | 5 (R1, R2), 6 (Q13), 7 (queries outside a pipeline, the event store for D19) |
| 31 Mar 2027 | 0.3.0 (CR-PRT-044, Blender through Nai) | 10 |
| 15 May 2027 | 0.4.0 (CR-PRT-049, the Unreal plugin) | 11 |
| 30 Jun 2027 | 0.5.0 (CR-PRT-058) | 8 (the IFC translator) |
| 15 Aug 2027 | 0.6.0 (CR-PRT-064, telemetry) | 7 (D9's layer roles: telemetry and its distillation) |

The items:

1. Parti's connectors as CReqs: the WebSocket connector (server side, bidirectional, per-system RPC endpoint
   definitions), and the harness process connector; their timing.
2. Whether connectors and pipelines can be created and changed at runtime through an API, and the REST interfaces to
   inspect events; their paths.
3. Measured latency for V1 and V2, or help to measure it.
4. Registering Parti's event schemas (`parti.<context>.<message>/1`) in the schema registry.
5. EntityStore: the status of R1 (durable consumer-group offsets) and R2 (`version`, `schemaVersion` on change events).
6. Q13: how much of Parti's backend processing the DSL can carry (propagation and projections; the domain's own rules).
7. The earlier open items: queries outside a pipeline, the event store for D19, D9's layer roles.
8. **The IFC translator** as a CReq (owner, 24 November 2026; PRD-parti D32): Parti's objects transformed to and from
   IFC-based objects (IFC 4.3, ISO 16739-1:2024), each product class mapped to an IFC entity type and predefined type
   (0.1.0's Finishes branch to `IfcCovering`) and Parti's attributes to IFC property sets by a declared mapping Parti
   provides; for the releases that connect BIM tools, structural and services models, cost estimating and facility
   management. Its timing, and whether it runs as a pipeline on the bus.
9. **Interaction events** (`parti.interaction.*/1`; D29): accepted into the bus for the agents' context and, with D9,
   telemetry, but outside the design's history.
10. **Blender through Nai** (0.3.0): the harness process connector, or a sibling, usable from Blender's embedded Python
    (headless and in the running application), so the Blender translator's commands and events travel on the bus.
11. **The Unreal plugin on the bus** (0.4.0): the WebSocket connector's per-system RPC endpoints serving an Unreal
    plugin (picks and walkthrough events in, scene changes out), with the plugin's message shapes registered.

12. **The SolidCraft connector** (0.1.0; PRD-parti D34): a Rust process on Nai's connector SDK joining SolidCraft's
    running application (its MCP server or its control connection) to the bus: Parti's commands in (command batches, reads, snapshots), and the
    application's events out (the design's revision moving, the selection, the view), registered as Parti's schemas.
Parti asks for: a CReq id and a date for each item; Nai's release schedule; and a notice when each lands in an
installable Nai release. Nai's Mainline needs a cross-project grant to reply over Sandesh (an owner action).

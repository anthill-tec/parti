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
| WebSocket **server** for plugins or the gateway to connect into Nai, and a WebSocket sink | **Missing**, and **no longer needed** (PRD-parti D35: every system serves its own endpoint and Nai connects out as a client) | none found; WebSocket in service mode is deferred (`docs/research/PRD-Service-Backend-Mode.md` Q7) |
| CloudEvents in the connector SDK | **Exists** | Nai's `StreamEvent` is a CloudEvents 1.0 envelope around a typed payload (CR-NAI-101, the CloudEvents SDK migration); config-driven `[event_mapping]` (`docs/research/PRD-Bridge-Client-SDK-Connector-Architecture.md` §3); request-reply correlates by the CloudEvent's id (CR-NAI-323) |
| JSON Schema in the schema registry | **Exists** | CR-NAI-178 (the JSON-Schema codec, Confluent-compatible), beside Avro and Protobuf |
| Connector for a Python process (the harness) | **Missing** | none specific; the request-reply and HTTP connectors are the nearest |
| Creating and changing connectors and pipelines at runtime through an API (for the Nai agents) | Unconfirmed | to ask Nai's team |
| REST interfaces to inspect events on the wire | To confirm | the owner reports them; their paths were not located in this read |
| Round-trip latency (plugin → Nai → gateway → EntityStore → CDC → Nai → listeners) | **Not measured** | nowhere in the repository |

**The connector SDK.** Nai's connectors are built on its Rust connector SDK and its gRPC bridge
(`crates/nai_bridge_proto/proto/bridge.proto`), which is the bridge **for connectors**. Parti's components do not talk
to Nai through it directly: they talk to the connectors that are built for them.

## 3. What follows (owner, 24 November 2026; PRD-parti D34, D35)

- **Every system on the bus serves a WebSocket endpoint**: Parti's gateway (Bun), the harness (Python), and each
  application through its plugin (the Unreal plugin and the Blender add-on in process; SolidCraft through the native
  Rust server shipped with Parti's plugin, since SolidCraft's plugins are WebAssembly with no network).
- **Nai's side is one generic WebSocket source and one generic WebSocket sink**, connecting to those endpoints as
  clients, configured towards each endpoint (custom endpoints, no code per system) by their TOML configuration and the
  endpoint's **definition**, an **AsyncAPI 3.0** document in JSON (the address, the CloudEvent types sent and received,
  the request and reply pairs, their schemas).
- **Every message is a CloudEvent 1.0** in structured JSON mode, over the WebSocket subprotocol `cloudevents.json`;
  commands are request and reply CloudEvents correlated by the request's id, as the request-reply connector does; each
  `dataschema` names a JSON Schema 2020-12 registered in Nai's registry. This builds on what Nai already has (§2). **The connectors unwrap the payload** (owner, 24 November 2026): the source decodes `data` against its schema into
  Nai's typed payload (`NaiRecord`) and keeps the envelope as the `StreamEvent`'s attributes and extensions, so the DSL
  routes and transforms on the payload's fields; the sink wraps it back into a CloudEvent.
- **The connectors are written entirely by the Nai project** (`ecosystem/nai_connector_*`), from Parti's requests
  (CReqs); Parti writes no connector. Parti writes the schemas, the endpoint definitions and its endpoints (the
  gateway, the harness, the plugins); its Rust is only the SolidCraft plugin, from 0.2.0.
- **The router is Parti's, in Nai's DSL** (owner, 24 November 2026; PRD-parti D38, D39): part of Parti's main source
  (`nai/`), and Parti's repository is a Nai project (`nai.toml`); each target project is a Nai project of Parti's kind, created by
  `nai new` from a Parti template added to Nai, with its schemas in a subdomain of Parti's domain and its own connector
  instances run separately; the main Nai process is shared. Nai owns the language, the runtime and the connectors.
- **LangChain is Python (and JavaScript) only**, so the harness stays Python (D21); it reaches Nai through its endpoint.

## 4. Validation spike (before the first release that connects a real application)

| # | Scenario | Pass |
|---|---|---|
| V1 | A test plugin serving its endpoint sends a pick as a CloudEvent; Nai's WebSocket source receives it; the registry accepts it; the DSL turns it into `selection-changed` and pushes it to the gateway | arrives at the gateway; p95 under 100 ms on one workstation |
| V2 | The gateway writes a placement to EntityStore over REST; the CDC source connector emits it; the DSL addresses it to the plugin; the plugin's RPC endpoint receives it | received once, in order per aggregate; p95 under 250 ms end to end |
| V3 | The harness, through its endpoint, receives V2's change; it sends a command back to the gateway through Nai | both directions arrive; no loss across a harness restart (offsets resumed) |
| V4 | A message failing the schema | refused with a named fault; dead-letter queue holds it; nothing reaches the gateway |
| V5 | A Nai agent changes a DSL transform through the API and re-runs V1 | the new transform applies without restarting Nai, or the restart cost is stated |
| V6 | EntityStore restarts during V2 | no change lost or duplicated once R1 (durable offsets) is in place; stated behaviour before it |
| V7 | Developer workstation | Nai, EntityStore (Redis, MongoDB) and the connectors start with one command on Linux; resources stated |

## 5. The request to Nai's team and EntityStore's owner

Drafted 24 November 2026 and **sent to Nai's Mainline over Sandesh as soon as Nai is on Sandesh** (not yet, 24 November
2026), well ahead of need, so Nai's team can plan the work and ship a usable Nai install (owner, 24 November 2026). Each item is needed by a date set back from the release that uses it
(the targets on the Crucible board, re-planned for 1.0.0 by 31 March 2027 on 24 November 2026, PRD-parti D33; each date is a few days before the CR that needs it starts):

| Needed by | For | Items |
|---|---|---|
| 10 Dec 2026 | the validation spike (§4) before 0.1.0's wave 4 | a **workstation install** of Nai with EntityStore, one command on Linux, versioned (V7); 2 (runtime API, REST paths); 4 (schema registry); 12 (the request id, `nairequestid`) |
| 21 Dec 2026 | 0.1.0 (CR-PRT-031, Nai integration; CR-PRT-012 gateway; CR-PRT-029 harness; CR-PRT-013 `parti-axi init`) | 1 (the generic WebSocket source and sink), 3 (latency), 9 (interaction events), 13 (pipelines from Parti's repository), 14 (the Parti template) |
| 6 Jan 2027 | 0.2.0 (CR-PRT-038, EntityStore for the design and the catalogue) | 5 (R1, R2), 6 (Q13), 7 (queries outside a pipeline, the event store for D19) |
| 6 Jan 2027 | 0.2.0 (CR-PRT-076, derived views; CR-PRT-077, intake of finishes) | 16 (derived views), 17 (intake from outside sources) |
| 4 Jan 2027 | 0.2.0 (CR-PRT-074, Parti's SolidCraft plugin and its endpoint) | 10 (SolidCraft's endpoint configured) |
| 25 Jan 2027 | 0.3.0 (CR-PRT-044, Blender through Nai) | 10 (Blender's endpoint configured) |
| 5 Feb 2027 | 0.4.0 (CR-PRT-049, the Unreal plugin) | 10 (Unreal's endpoint configured), 11 |
| 19 Feb 2027 | 0.5.0 (CR-PRT-058; CR-PRT-075, project pipelines; CR-PRT-078, intake for the other layers) | 8 (the IFC translator), 17 (more sources) |
| 8 Mar 2027 | 0.6.0 (CR-PRT-064, telemetry) | 7 (D9's layer roles: telemetry and its distillation) |

**To be finalised with Nai's orchestrator** (owner, 24 November 2026): how PRD-parti D34 to D39 meet Nai (the generic
connectors, CloudEvents and `nairequestid`, the unwrapped payloads, the router and project pipelines, the Parti template,
the registry's domains and subdomains, the connector instances and the shared main Nai process) is Parti's current
understanding from Nai's documentation. Nai's orchestrator confirms or corrects each point in its answers, and Parti's
decisions are finalised then.

The items:

1. **One generic WebSocket source and one generic WebSocket sink**, as CReqs (PRD-parti D35): clients that connect to
   endpoints the systems serve, configured towards each endpoint by TOML and the endpoint's AsyncAPI 3.0 definition in
   JSON; CloudEvents 1.0 structured JSON over the subprotocol `cloudevents.json`; request and reply CloudEvents
   correlated by the request's id; the source **unwrapping each CloudEvent's `data`** into a `NaiRecord` decoded against
   its `dataschema` (the envelope kept as the event's attributes), and the sink wrapping it again; reconnection and
   resumption when an endpoint restarts. The existing WebSocket client
   (`run_websocket`) moved onto the connector SDK may be their start. First endpoints: Parti's gateway and harness.
2. Whether connectors and pipelines can be created and changed at runtime through an API, and the REST interfaces to
   inspect events; their paths.
3. Measured latency for V1 and V2, or help to measure it.
4. Registering Parti's event schemas (`parti.<context>.<message>/1`) in the schema registry.
5. EntityStore: the status of R1 (durable consumer-group offsets) and R2 (`version`, `schemaVersion` on change events).
6. Q13: how much of Parti's backend processing the DSL can carry. Parti's side is decided (PRD-parti D41): propagation
   and derived views only; the domain's own rules stay in Parti. Which other static tooling suits the DSL is still open.
7. The earlier open items: queries outside a pipeline, the event store for D19, D9's layer roles.
8. **The IFC translator** as a CReq (owner, 24 November 2026; PRD-parti D32): Parti's objects transformed to and from
   IFC-based objects (IFC 4.3, ISO 16739-1:2024), each product class mapped to an IFC entity type and predefined type
   (0.1.0's Finishes branch to `IfcCovering`) and Parti's attributes to IFC property sets by a declared mapping Parti
   provides; for the releases that connect BIM tools, structural and services models, cost estimating and facility
   management. Its timing, and whether it runs as a pipeline on the bus.
9. **Interaction events** (`parti.interaction.*/1`; D29): accepted into the bus for the agents' context and, with D9,
   telemetry, but outside the design's history.
10. **More endpoints for the same connectors**, configured, with no new connector: SolidCraft's (0.2.0, the native Rust
    server shipped with Parti's plugin, which drives the running application through its control protocol and receives its `design.changed` events), Blender's
    (0.3.0, Parti's extension in process, PRD-parti D37) and Unreal's (0.4.0, Parti's plugin in process, D36); picks, revisions and walkthrough events
    in, commands and scene changes out, with each endpoint's messages registered.
11. **The Unreal plugin on the bus** (0.4.0): any limit the generic connectors place on a game-engine endpoint
    (frame-rate event volume, binary assets by reference only).
12. **The request id on the wire**: Parti's endpoints carry it as the CloudEvents extension **`nairequestid`** (owner,
    24 November 2026; CloudEvents extension names are lowercase letters and digits), for Nai's `nai-request-id`; please
    map it in the generic connectors, and say how the other `nai-*` trace extensions appear in a structured JSON
    CloudEvent. Examined together during CR-PRT-074.

13. **Pipelines from another repository** (PRD-parti D38): Nai's CLI already has `nai check`, `nai run` and `nai test`
    (scenarios in `tests/*.test.toml`, CR-NAI-302); how their results can be reported to Crucible (for example as JUnit XML), how it deploys them to a
    running Nai and versions them, and how the harness's Nai agents change them at run time. Needed with item 1.

14. **A Parti template for Nai's project-creation tool** (PRD-parti D39), as a CReq: `nai new <project> --template
    <Parti's template>`, run by `parti-axi init`, generating a target project's `nai.toml` (inheriting Parti's router),
    **generating and registering its schemas** in a subdomain of Parti's domain in the schema registry (Parti's own in
    `parti.<context>.<message>`; the naming settled together), and **generating its connector instances** (the generic
    WebSocket source and sink, pointed at the project's endpoints), each run as a separate process with its own
    configuration, against **one shared main Nai process**. Parti specifies the template; it is needed first in 0.1.0
    (CR-PRT-031, CR-PRT-013), with project pipelines in 0.5.0 (CR-PRT-075).

15. **To explore: Nai's checkpointing, rewind and restart on error** (owner, 24 November 2026; not yet a decision).
    Nai checkpoints its pipelines and can rewind and start again from a checkpoint when an error occurs. Parti may use it
    to reset state: undo and redo on the bus, returning to a design version (D19), resuming a workflow run after a failed
    step (the step cycle's checkpoints, D26), and replaying events into a restarted endpoint. Parti asks how it works
    across connectors and EntityStore, and how far it can serve these needs; explored with Nai's orchestrator.

16. **Derived views** (owner, 24 November 2026; PRD-parti D41): stateful pipelines in the DSL that combine several
    event streams (SolidCraft's, Parti's, the harness's) into state kept in a database (EntityStore or SQL) that
    Parti's components query: keyed state, ordering across streams, windows and late events; how the state is
    checkpointed and rebuilt from the streams; how Parti tests such pipelines with `nai test`. Projections only: what
    changes Parti's records returns to Parti as a command.

17. **Intake from outside sources** (D41), as CReqs where a connector is missing: source connectors for HTTP APIs and
    feeds (polling, pagination, authentication with the secret held outside configuration) and for file drops,
    started on request by the harness's intake agents (request and reply) as well as on a schedule; the normalising
    pipelines are Parti's; each source's rate limits and terms recorded with what it brings. First for the finishes
    (0.2.0), then the other product layers (0.5.0).

Parti asks for: a CReq id and a date for each item; Nai's release schedule; and a notice when each lands in an
installable Nai release. Nai's Mainline needs a cross-project grant to reply over Sandesh (an owner action).

# Parti — Architecture

**Date:** 2026-11-22
**Status:** Reviewed by the owner on 22 November 2026: every section agreed, and the review's decisions applied (D16 to D19 in `research/PRD-parti.md` §3). Updated 24 November 2026 for D26 (the workflow's shape), D27 (the `parti` library) and D28 (the ecosystem). Structure is settled where a decision number (D…) is cited; the rest is proposed.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)

This document is the system overview: the parts, how they connect, and the rules that keep them apart. The
reasons and the detailed analysis are in the PRDs and design notes under `research/`; this document does not
repeat them.

## 1. What Parti is

Parti is an **ecosystem in which architects and interior designers create their projects with agentic help** (D28).
Parti provides the coding and logical framework; the **project agent** (the orchestrator agent in each target project)
concentrates on the project's own logic (translating its data into Parti's formats, its rules, its own steps); and the
architects and designers, domain experts rather than programmers, work in their own terms and are never asked to write
code, data or commands. The project agent hides the programming and scripting from them, which is one of the reasons Parti
ships a harness of its own (D21).

| Who | Provides |
|---|---|
| Parti | the domain model and its formats; the workflow (D26); the `parti` library, its tools and translators (D27); the harness (D21); `parti-axi`; the skills and agent definitions; the finish tool, the world builder, the client viewer |
| The project agent | the project's translation into Parti's formats; its rules and data tables; the steps particular to the project, as extensions of the step kinds |
| The architect or interior designer | intent, in their own terms: pointing at things, choosing among options, stating rules, approving at the gates |
| The consumer (home buyer, business buyer, the commissioning client) | nothing to build: they experience the deliverables, the walkthrough with or without VR, the stills and films, and choose among the options offered, in the client viewer (D22) |

At its centre Parti is a guided workflow, installed into a *target project* (a project that owns a building model), that
takes a building from the architect's drawings to a CAD model, a rendered Blender scene and an Unreal
walkthrough. A user and an agent work through its steps together, and each step has tested tools (owner,
22 November 2026). It has three parts:

1. **Guided workflow and toolbase** (the goal). A guided sequence of steps, each with tested tools, from drawings to CAD model, Blender scene and Unreal walkthrough.
2. **Finish tool** (its first major feature). Browse a catalogue of finishes and apply them to walls, floors and parts of them in an Unreal walkthrough; set time of day and weather; one state shared by the interface and the scene.
3. **Installer and agent interface** (`parti-axi`). Installs Parti, scaffolds it into a target project, and gives agents everything a person can do, including joining a live session alongside the user (D16).

Parti's Python side is one library, `parti` (D27, LGPL-3.0-only): the architectural SDK every target project imports,
holding the workflow, the harness, the catalogue tools and the pipeline tools generalised from the prototype's scripts;
the scaffold gives each project Parti's skills and agent definitions, `parti-axi` and the library. Parti ships its own agent harness (D21): a workflow graph built from the domain's Workflow definition, with Parti's agent
definitions and skills, driving the CAD system, Blender and Unreal through their Python APIs and MCP servers. It is
released in two editions from one domain (D22, §7): the **designer edition**, the full workflow for architects and
interior designers, which 1.0.0 delivers through 0.x releases (D23); and the **client viewer**, a self-contained
walkthrough viewer for the building's owner, packaged with a client bundle.

## 2. The whole in one picture

```
 TARGET PROJECT (e.g. JohnnyHouse)                PARTI (installed tool)
 ───────────────────────────────                  ──────────────────────────────────────────────
 parti configuration  ───────────────────────────▶ parti-axi  (Python CLI: install, init, run,
 finish records + images ─────┐                                 catalogue, doctor, state, command,
 surface declarations ────────┤                                 workflow)
 saved designs  ◀─────────────┤                         │ starts / talks to
 pipeline data tables ────────┤                         ▼        ◀── agent (AXI session, Pi plugin, D16)
 step log, checkpoints ◀──────┘                  ┌──────────────── GATEWAY (Bun) ────────────────┐
                                                 │  adapters in: page · scene · CLI · agent API  │
   PAGE (TypeScript, VanJS)  ◀── WebSocket ────▶ │  ───────────────────────────────────────────  │
   overlay · VR panel · browser                  │  DOMAIN (pure TypeScript)                     │
                                                 │   Building · Design · Catalogue · Quantities  │
   SCENE ADAPTER             ◀── WebSocket ────▶ │   · World builder · Session · Workflow        │
   mock scene (now)                              │  ───────────────────────────────────────────  │
   Unreal C++ plugin (later)                     │  ports: catalogue store · design store ·      │
                                                 │         session channel · asset delivery      │
                                                 │  adapters out (v1): local files               │
                                                 │  adapters out (later): EntityStore · Nai      │
                                                 └───────────────────────────────────────────────┘

   CAD · Blender · Unreal editor  ◀── their own agent interfaces ── PIPELINE TOOLS (Python)
```

## 3. Rules that hold everywhere

| Rule | Source |
|---|---|
| The domain is pure: plain functions over plain data, `decide(state, command) → events`, `evolve(state, event) → state`, keyed by aggregate id. No input or output, no library calls, no outside terms. | D8, D10, NFR-1 |
| Everything outside the domain is reached through a port named in domain terms, with an adapter behind it. | NFR-5 |
| Every outside system has its own translator (anti-corruption layer): the scene, the page, each maker's feed, local files, each driven application, later Nai and EntityStore. | D8, NFR-4 |
| Contexts know one another by identifier and published events only. | NFR-3 |
| One message schema, versioned, is the only contract between page, gateway and scene adapters. Types are generated from it. | NFR-6 |
| Commands are safe to repeat; every change is an event with an id and a per-aggregate sequence number; state is rebuilt from events; stale changes are refused. | NFR-2 |
| Nothing of one target project lives in Parti's code. | NFR-10 |
| Servers bind to 127.0.0.1 in version one; every incoming message is validated against the schema. | NFR-8 |

## 4. Contexts

Names follow the glossary, `research/DN-ubiquitous-language.md` (revised in the architecture review, D17, D18).

| Context | Aggregates and main data | Commands (examples) | Publishes |
|---|---|---|---|
| **Workflow** (frames the others) | Workflow definition (versioned data): phases, step definitions of twelve step kinds with their checks, caveats and invalidated-by edges, gates of four kinds. Workflow run (per target project): step runs, check results, corrections, decisions, variants, step records (D26) | start step; record check; pass gate; record decision; raise, resolve correction; branch, choose variant; checkpoint | step started / checked / completed / stale; correction raised / resolved; decision recorded |
| **Building** | Building: levels, rooms, elements, surfaces; each element's 3D object and 2D drawing elements | declare, revise, retire element or surface | element declared / revised / retired |
| **Design** (core: layer planning) | Design: per layer a plan; per surface its zones (area, panel, band, border, …); per zone its placement; schemes; shortlist; offers of options for the client, and the client's selections (D22) | define, resize, remove zone; place, clear product; save, apply scheme | zone defined / resized / removed; product placed / cleared; scheme saved / applied |
| **Catalogue** | Product (per layer); maker; set; matching facts (colour, suitable use) | (queries) filter, search, "goes with" | product added / changed / withdrawn |
| **Quantities** (computational module) | Quantities per plan; bill of materials per work-contract role; cost estimates later | (queries) quantities, bill of materials | — (derived from plans) |
| **World builder** (module) | Scenario: setting (time, date, weather, light, site), moving parts, experience mode, routes, viewpoints | choose scenario; set time; set weather; animate moving part; choose experience mode | setting changed; scenario changed |
| **Session** | Session: participants (users and agents), selection, viewpoint | join, leave; select element / surface / zone / group; clear selection | participant joined / left; selection changed |
| **Asset delivery** | Mapping from a product to what a scene can draw; the client bundle, per client project and revision (D22) | prepare product for a scene | product ready / failed |
| **Identity** (service stage) | Users, access | — | — |

Design refers to products and to building elements by id; it asks Catalogue and Building whether a placement
is allowed through their published facts, never by reading their storage.

Workflow frames the other contexts: a step's outputs (a building, a design) are what the later steps, the
finish tool and the world builder work on. Its shape (D26, `research/DN-workflow-shape.md`): phases of steps, each step
running one step cycle (sources → data → generate → apply → check → checkpoint → record), gates, and the correction and
audit loops across every phase. A correction may land in an earlier phase's step; its revision then flows forward
(D19). The harness compiles the workflow definition into its LangGraph graph; the graph's state is a projection of the
workflow run, and LangGraph's own checkpointer holds the agent's state only, never the project's.

## 5. Components

| Component | Stack | Depends on | Notes |
|---|---|---|---|
| `schema` | schema files → generated TypeScript (later C++, Rust, Avro) | nothing | Commands, events, queries, state snapshots; versioned. |
| `domain` | TypeScript | `schema` types only | One module per context. No imports from anything else in the repository. |
| `gateway` | Bun | `domain`, `schema`, ports | Serves the page; holds the WebSocket links; runs commands through the domain; stores events through the design store; fans events out. |
| `adapters-local` | TypeScript | ports | Catalogue from the target project's records; designs as an event log and a snapshot in a file. |
| `page` | TypeScript, VanJS | `schema` | One page, two presentations (D22): in the designer edition, the **Parti Project Environment**: the **guided chat** with the project agent (through the harness, D21; it follows the embedded workflow and guides the design workflow) beside the workflow view, the **asset browser** (0.1.0: the catalogue browser, detail and shortlist), the zone editor and the setting controls; in the client viewer, the offered options as an in-world panel with smart menus. Its state is a projection of the shared state. Works as overlay, VR panel and plain browser tab. |
| `mock-scene` | TypeScript | `schema` | Stands in for Unreal: draws surfaces and zones, reports picks. The test partner. |
| `parti` (library, D27) | Python, LGPL-3.0-only | `schema` (the generated Python types and validation) | The architectural SDK every target project imports. Modules: `parti.workflow` (the workflow-definition model, step kinds, step cycle, checks and check results, gates, the correction loop, D26); `parti.harness` (D21: the LangGraph builder that compiles a workflow definition, Parti's agent definitions, MCP client connections to SolidCraft, Blender and Unreal; checkpoints and memory behind ports); `parti.catalogue` (catalogue tools: validate and build from records in Parti's format, which the project's own agent translates its records into; colour tags, thumbnails, picture orientation); `parti.tools` (generalised from the prototype's scripts: declared transforms (D25), selectors, rule tables with counts, checks with the worst value, declarations); `parti.translators` (one per application: SolidCraft, Blender, Unreal, the PDF reader); `parti.units` (D25). A project customises by data and by extending step kinds, never by forking. |
| `parti-axi` | Python (installed with `uv`) | `parti` library; gateway (over its local interface and agent API) | Installer, scaffold, agent commands, workflow guide; session verbs (state, watch, command) and a Pi plugin that wakes the agent (D16, FR-AXI-8, FR-AXI-9). Structured output, dry run, a flag for every question. |
| `client-viewer` | Unreal (packaged app) | its client bundle only | Deferred until after 1.0.0 (D22, D23). Self-contained walkthrough viewer (monitor or VR) with the offered options, stills and films; Windows and Linux; built and downloaded from the designer edition. Licence first (PRD Q12). |
| `unreal-plugin` | C++ | `schema` (generated C++ types) | **Deferred** until Model B supports a C++ stack (D5). Scene adapter, pick, zone master material, finish assets, overlay; the Unreal side of the world builder (D18). |

The repository layout that realises this (workspace packages, test folders) is the orchestrator's to propose.

## 6. How a change travels

Assigning a finish, version one:

1. The user picks a zone in the scene. The scene adapter sends *selection requested*; Session produces *selection changed*; page and scene both show it.
2. The user chooses a finish in the page. The page sends *place finish* with the design's expected version and a command id.
3. The gateway validates the message, loads the design's state, calls Design's `decide`. It refuses (unknown zone, finish not valid for this surface, stale version) or returns *finish assigned*.
4. The event is appended through the design store, then sent to every link.
5. The scene adapter asks asset delivery for the finish in drawable form and updates the zone. The page updates through its projection.
6. A link that joins late receives a snapshot, then events from that sequence number.

The same path serves the CLI: `parti-axi` sends the command and prints the events or the refusal.

## 7. Where things run, by stage

| Stage | Page | Gateway and domain | Stores | Scene |
|---|---|---|---|---|
| A. First release | browser tab | local Bun process | files in the target project | mock scene |
| B. Unreal | overlay inside the Unreal app | local Bun process | files | Unreal plugin |
| C. VR | panel in the 3D scene | same | same | same |
| D. Data service | same | local, or served | EntityStore (records), Nai (pipelines, sessions, embeddings) | same |
| E. Streamed | browser, around a streamed picture | served | same as D | Unreal on servers |

Only adapters change between stages. The domain, the schema and the page do not.

### Editions (D22)

Parti is released in editions built from one domain. An edition narrows the contexts, commands and adapters it ships;
the rules are never copied.

| | Designer edition | Client viewer |
|---|---|---|
| Who | Architects, interior designers | The building's owner |
| Platform | Linux first (D2) | Windows and Linux, natively; macOS possibly later. Built and downloaded from the designer edition, per platform (PRD Q14) |
| Workflow, agent harness, CAD, Blender | Yes | No; only a UI helper agent that searches and applies offered sets (tile sets, interior sets) through the viewer's own commands |
| Building | Authoring | Read only, from the bundle |
| Design | Everything, including curating offers | Apply and compare the offered options |
| Catalogue | Every product, search | Only the offered products, in the bundle |
| World builder | Authoring scenarios, setting, site | The walkthrough: navigation, scenarios, VR |
| Renders | Made in the Blender part of the pipeline | Pre-rendered stills and films, in the bundle |
| Page (one page, D1) | Every data library; overlay or browser tab | Only the offered options, as a 2D panel rendered in the 3D world; VR interaction first; loaded from the bundle (PRD T1). Smart menus at the zone pointed at apply its bundled options in place |
| Data | Target project files; later Nai and EntityStore | Its client bundle: a filesystem package (offline), or served by Nai as a client server (online, Stage D) |

The designer publishes a **client bundle** per client project and revision: a filesystem package (asset files, with their
metadata in one SQLite database) holding everything the viewer executable needs to run (the building, the offer, the scenarios, the stills and films, and every asset they use),
with no server or network. Alternatively Nai serves the same bundle remotely, as a client server, and receives the
client's selections and telemetry live; the viewer reads its bundle through one port, so only its adapter differs. The viewer is packaged with its project's bundle; the client's choices return to the designer's
project as a client selection. Proposed: options are validated before publishing and realised as Unreal variant sets,
so the viewer needs no rules engine (PRD Q4). The viewer's licence comes first (PRD Q12).

In a served Parti (D, E) there are several users and sessions, and agents join a session the same way users
do (D16). The backend may move to Nai (D9).

## 8. Later backends

- **EntityStore** (the owner's Quarkus service on Redis and MongoDB, with change streams): system of record for Catalogue, Design, Building and review records, behind the catalogue-store and design-store ports.
- **Nai** (the owner's Rust streaming runtime with its own DSL, connectors and provider plugins): the domain's `decide` and `evolve` functions map onto keyed pipeline stages or a custom provider; session traffic through a two-way session connector; embeddings for search by likeness. Also (D9, owner 2026-11-23): retrieval (RAG) for the agent harness and the knowledge base, which move to Nai as soon as the harness exists; session context and agent memory; a file catalogue, so file operations do not depend on the operating system; geospatial and map data, so the world builder builds the site around the building from map providers. Each role sits behind its own port: knowledge store, session store, file catalogue, geo data.

What Nai lacks today for the interactive loop, and the requests this makes to its team, are listed in
`research/DN-founding-design-record.md`. The owner's assessment (22 November 2026): a WebSocket connector is not a
major issue, since Nai already has HTTP in and out connectors. Nai supports custom connectors that talk to Parti over
WebSockets where needed, usually built with the LangChain agentic SDK, the same toolkit as the agent harness (D21;
owner, 23 November 2026). Neither is used in version one (D9). Retrieval (RAG) and the knowledge base move to Nai
as soon as the agent harness exists; everything else moves when Parti takes on the multi-user, multi-session
implementation. Until then only the local adapters exist.

**What runs where** (owner, 23 November 2026), in three layers:

| Layer | What runs there | How |
|---|---|---|
| Interaction (near real time) | The validation rules (the domain, R1), the agentic workflows and skills (D21), and the work with the CAD system, Blender and Unreal Engine | The applications' Python APIs, alongside their MCP servers, driven through the LangChain SDK |
| Operations | Queued operations kept consistent in time: the forward chain's follow-up actions (D19), background RAG and data-preprocessing pipelines | Nai: its queues and ordering per key, pipelines in its DSL |
| Data | The system of record, retrieval, the knowledge base, session context, the file catalogue, geospatial data, telemetry events (usage, timings such as NFR-11's responsiveness, agent runs) | Nai and EntityStore |

Nai treats all its data as schema-based events. Parti's own changes are already events defined by one versioned schema
(R5, R6), so they map onto Nai's events directly, with no translation of meaning.

How much of the static tooling otherwise written in Python can move to Nai is an open question (`research/PRD-parti.md`
Q13).

## 9. Installing into a target project

Once scaffolded, the architect or designer opens the Project Environment in the browser (served by the gateway); it is
their workspace until the Unreal walkthrough is generated, which then joins it (D22). The first thing the project agent
guides there is the import of the project's sources, such as floor plan drawings (the Intake phase, D26); imports from
other design tools come later, each through its own translator.

`parti-axi init --target <dir>` writes into the target project its configuration, Parti's skills and agent definitions
(which teach the agent to use the `parti` library and `parti-axi`), the agent notes, and the project's dependencies on
`parti` and `parti-axi` (D27), and nothing else. The target keeps its data where it is; Parti reads it in place and writes only where the
configuration says (saved designs, the step log, checkpoints). When the Unreal plugin exists, the scaffold
also connects it to the target's Unreal project.

## 10. Documents

| Document | Holds |
|---|---|
| `Architecture.md` (this) | The overview. |
| `research/PRD-parti.md` | Parti's design contract: decisions, requirements, stages, open questions. |
| `research/DN-ubiquitous-language.md` | The living glossary: the business language shared with architects, designers and users. |
| `research/DN-test-strategy.md` | How Parti is tested: tiers, fakes only at ports, contract and live tests for the applications, synthetic fixtures. |
| `research/PRD-domain.md` | Per-area PRD 1, the domain: building, design and catalogue. Draft, written for the 0.1.0 slice. |
| `research/PRD-<topic>.md` (to be written) | Detailed analysis per area: (1) the domain (above): building, layers, catalogue, quantities and bills of materials, drafted first by the orchestrator with the owner; (2) the message schema and state model; (3) the page; (4) the installer and agent interface, with the agent harness (D21); (5) the pipeline workflow and toolbase; (6) the world builder, the Unreal plugin and finish assets; (7) the client viewer and the client bundle (D22). `PRD-parti.md` then keeps the decisions and the map, and its detailed sections move out. |
| `research/DN-founding-design-record.md` | The original design discussion, including the Nai and EntityStore reviews and the stack findings. |
| `research/DN-first-consumer-johnnyhouse.md` | The first consumer's data, Unreal project and needs. |
| `research/DN-pipeline-prototype-johnnyhouse.md` | The pipeline as JohnnyHouse ran it by hand: steps, tools, scripts, faults. |
| `research/DN-workflow-shape.md` | The workflow generalised into one repeatable graph (D26): step cycle, step kinds, gate kinds, phases, loops. Provisional while the prototype runs. |
| `research/DN-runbook-domain-impact.md` | The prototype's Runbook mapped onto the domain model, context by context (D26). |
| `changes/CR-PRT-NNN-*.md` | Implementation specs, filed on the Crucible board. |
| `.lavish/<document>.html` | **Review pages.** An interactive copy of one specification, built by the orchestrator for the owner's review: annotations, questions and decisions are made there. Every decision is applied to the markdown and committed; the page is a working record on the orchestrator's machine, not versioned and not the source of truth. |

**Order of the design work.** 1. This architecture, reviewed. 2. The glossary (`research/DN-ubiquitous-language.md`).
3. The domain PRD, then the other per-area PRDs, each with its review page. Each is written for the slice the next
release needs (the domain PRD first for 0.1.0), and grows with the releases. 4. CRs, filed on the Crucible board,
last: each implements settled requirements.

## 11. System-design terms

The software's technical vocabulary. These words describe how Parti is built; they are not part of the
business language (`research/DN-ubiquitous-language.md`) and are never needed to discuss the product with
architects, designers or users.

| Term | Meaning |
|---|---|
| Page | The browser interface (TypeScript, VanJS): overlay, VR panel or browser tab. |
| Gateway | The local Bun process the page, the scene adapter, `parti-axi` and agents connect to. |
| Scene adapter | Whatever connects a 3D scene to the gateway: the mock scene, or the Unreal plugin. |
| Agent API | The gateway's local interface through which an agent takes part in a session (D16). |
| Adapter | Code that connects the domain to one outside system; in (a link) or out (a store). |
| Port | The domain-named interface an adapter sits behind. |
| Translator | An adapter that maps an outside system's words and shapes into the domain's (anti-corruption layer). |
| Schema | The versioned definition of every message: commands, events, queries, snapshots. |
| Command, event, query | A request to change state; a recorded change; a request to read. |
| Aggregate | A unit of state with its own id, changed only through `decide` and `evolve`. |
| `decide`, `evolve` | `decide(state, command) → events`; `evolve(state, event) → state`. |
| Parti library (SDK) | The `parti` Python package (D27) that target projects import: the workflow, the harness and the tools. |
| Projection, snapshot | A view of state built from events; a saved copy of state at a sequence number. |

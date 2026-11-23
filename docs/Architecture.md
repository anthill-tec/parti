# Parti — Architecture

**Date:** 2026-11-22
**Status:** Reviewed by the owner on 22 November 2026: every section agreed, and the review's decisions applied (D16 to D19 in `research/PRD-parti.md` §3). Structure is settled where a decision number (D…) is cited; the rest is proposed.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)

This document is the system overview: the parts, how they connect, and the rules that keep them apart. The
reasons and the detailed analysis are in the PRDs and design notes under `research/`; this document does not
repeat them.

## 1. What Parti is

Parti is a guided workflow, installed into a *target project* (a project that owns a building model), that
takes a building from the architect's drawings to a CAD model, a rendered Blender scene and an Unreal
walkthrough. A user and an agent work through its steps together, and each step has tested tools (owner,
22 November 2026). It has three parts:

1. **Guided workflow and toolbase** (the goal). A guided sequence of steps, each with tested tools, from drawings to CAD model, Blender scene and Unreal walkthrough.
2. **Finish tool** (its first major feature). Browse a catalogue of finishes and apply them to walls, floors and parts of them in an Unreal walkthrough; set time of day and weather; one state shared by the interface and the scene.
3. **Installer and agent interface** (`parti-axi`). Installs Parti, scaffolds it into a target project, and gives agents everything a person can do, including joining a live session alongside the user (D16).

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
| **Workflow** (frames the others) | Pipeline: steps, their inputs, outputs, checks, gates; a target project's progress | start step; record check; pass gate; checkpoint | step started / checked / completed |
| **Building** | Building: levels, rooms, elements, surfaces; each element's 3D object and 2D drawing elements | declare, revise, retire element or surface | element declared / revised / retired |
| **Design** (core: layer planning) | Design: per layer a plan; per surface its zones (area, panel, band, border, …); per zone its placement; schemes; shortlist | define, resize, remove zone; place, clear product; save, apply scheme | zone defined / resized / removed; product placed / cleared; scheme saved / applied |
| **Catalogue** | Product (per layer); maker; set; matching facts (colour, suitable use) | (queries) filter, search, "goes with" | product added / changed / withdrawn |
| **Quantities** (computational module) | Quantities per plan; bill of materials per work-contract role; cost estimates later | (queries) quantities, bill of materials | — (derived from plans) |
| **World builder** (module) | Scenario: setting (time, date, weather, light, site), moving parts, experience mode, routes, viewpoints | choose scenario; set time; set weather; animate moving part; choose experience mode | setting changed; scenario changed |
| **Session** | Session: participants (users and agents), selection, viewpoint | join, leave; select element / surface / zone / group; clear selection | participant joined / left; selection changed |
| **Asset delivery** | Mapping from a product to what a scene can draw | prepare product for a scene | product ready / failed |
| **Identity** (service stage) | Users, access | — | — |

Design refers to products and to building elements by id; it asks Catalogue and Building whether a placement
is allowed through their published facts, never by reading their storage.

Workflow frames the other contexts: a step's outputs (a building, a design) are what the later steps, the
finish tool and the world builder work on.

## 5. Components

| Component | Stack | Depends on | Notes |
|---|---|---|---|
| `schema` | schema files → generated TypeScript (later C++, Rust, Avro) | nothing | Commands, events, queries, state snapshots; versioned. |
| `domain` | TypeScript | `schema` types only | One module per context. No imports from anything else in the repository. |
| `gateway` | Bun | `domain`, `schema`, ports | Serves the page; holds the WebSocket links; runs commands through the domain; stores events through the design store; fans events out. |
| `adapters-local` | TypeScript | ports | Catalogue from the target project's records; designs as an event log and a snapshot in a file. |
| `page` | TypeScript, VanJS | `schema` | Catalogue browser, detail, shortlist, zone editor, setting controls. Its state is a projection of the shared state. Works as overlay, VR panel and plain browser tab. |
| `mock-scene` | TypeScript | `schema` | Stands in for Unreal: draws surfaces and zones, reports picks. The test partner. |
| `parti-axi` | Python (installed with `uv`) | gateway (over its local interface and agent API) | Installer, scaffold, agent commands, workflow guide; session verbs (state, watch, command) and a Pi plugin that wakes the agent (D16, FR-AXI-8, FR-AXI-9). Structured output, dry run, a flag for every question. |
| `catalogue-tools` | Python | — | Build a catalogue from a target project's records: thumbnails, colour tags, checks. Later: Unreal editor scripts for finish assets. |
| `agent-harness` | Python | gateway (over its agent API) | Parti's own agent harness (D21): the workflow graph (LangGraph) built from the domain's Workflow definition, whose nodes call domain commands; agent definitions and skills; MCP client connections to SolidCraft, Blender and Unreal. Checkpoints and memory behind ports (local first; Nai and EntityStore later). |
| `pipeline-tools` | Python | — | The toolbase of the workflow: data tables → commands for the CAD and rendering applications, with expected-result checks. One translator per application. |
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

In a served Parti (D, E) there are several users and sessions, and agents join a session the same way users
do (D16). The backend may move to Nai (D9).

## 8. Later backends

- **EntityStore** (the owner's Quarkus service on Redis and MongoDB, with change streams): system of record for Catalogue, Design, Building and review records, behind the catalogue-store and design-store ports.
- **Nai** (the owner's Rust streaming runtime with its own DSL, connectors and provider plugins): the domain's `decide` and `evolve` functions map onto keyed pipeline stages or a custom provider; session traffic through a two-way session connector; embeddings for search by likeness.

What Nai lacks today for the interactive loop, and the requests this makes to its team, are listed in
`research/DN-founding-design-record.md`. The owner's assessment (22 November 2026): a WebSocket connector is not a
major issue, since Nai already has HTTP in and out connectors. Neither is used in version one (D9). Parti migrates to them when it takes on the
multi-user, multi-session implementation; until then only the local adapters exist.

## 9. Installing into a target project

`parti-axi init --target <dir>` writes a configuration file and the agent notes into the target project, and
nothing else. The target keeps its data where it is; Parti reads it in place and writes only where the
configuration says (saved designs, the step log, checkpoints). When the Unreal plugin exists, the scaffold
also connects it to the target's Unreal project.

## 10. Documents

| Document | Holds |
|---|---|
| `Architecture.md` (this) | The overview. |
| `research/PRD-parti.md` | Parti's design contract: decisions, requirements, stages, open questions. |
| `research/DN-ubiquitous-language.md` | The living glossary: the business language shared with architects, designers and users. |
| `research/PRD-<topic>.md` (to be written) | Detailed analysis per area: (1) the domain: building, layers, catalogue, quantities and bills of materials, drafted first by the orchestrator with the owner; (2) the message schema and state model; (3) the page; (4) the installer and agent interface; (5) the pipeline workflow and toolbase; (6) the world builder, the Unreal plugin and finish assets. `PRD-parti.md` then keeps the decisions and the map, and its detailed sections move out. |
| `research/DN-founding-design-record.md` | The original design discussion, including the Nai and EntityStore reviews and the stack findings. |
| `research/DN-first-consumer-johnnyhouse.md` | The first consumer's data, Unreal project and needs. |
| `research/DN-pipeline-prototype-johnnyhouse.md` | The pipeline as JohnnyHouse ran it by hand: steps, tools, scripts, faults. |
| `changes/CR-PRT-NNN-*.md` | Implementation specs, filed on the Crucible board. |
| `.lavish/<document>.html` | **Review pages.** An interactive copy of one specification, built by the orchestrator for the owner's review: annotations, questions and decisions are made there. Every decision is applied to the markdown and committed; the page is a working record on the orchestrator's machine, not versioned and not the source of truth. |

**Order of the design work.** 1. This architecture, reviewed. 2. The glossary (`research/DN-ubiquitous-language.md`).
3. The domain PRD, then the other per-area PRDs, each with its review page. 4. CRs, filed on the Crucible board,
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
| Projection, snapshot | A view of state built from events; a saved copy of state at a sequence number. |

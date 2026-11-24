# Parti — Architecture

**Date:** 2026-11-22
**Status:** Reviewed by the owner on 22 November 2026: every section agreed, and the review's decisions applied (D16 to D19 in `research/PRD-parti.md` §3). Restructured 24 November 2026 into the logical (Part A) and system (Part B) architecture, and updated for D26 (the workflow's shape), D27 (the `parti` library), D28 (the ecosystem), D29 (the message bus) and D30 (project types and templates); updated from the storyboard review for D22's interaction model, D29's event stream, D31 (products classified in the model) and D32 (the product classification). The architecture and features for 1.0.0 are covered (owner, 24 November 2026). Structure is settled where a decision number (D…) is cited; the rest is proposed.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)

This document has an overview and two parts, kept apart on purpose (owner, 24 November 2026):

- **Part A, the domain-driven logical architecture:** the business model in the glossary's language: the bounded
  contexts, how they relate (the context map), the logical rules, versioning, the workflow and project types. It names
  no technology, no process and no store.
- **Part B, the system architecture:** how Parti is built and run: the components and their stacks, ports and adapters,
  how a change travels, the message bus, where things run, the backends, installation, and the system-design terms.

The reasons and the detailed analysis are in the PRDs and design notes under `research/`; this document does not
repeat them.

## 1. What Parti is (overview)

Parti is an **ecosystem in which architects and interior designers create their projects with agentic help** (D28).
Parti provides the coding and logical framework; the **project agent** (the orchestrator agent in each target project)
concentrates on the project's own logic (translating its data into Parti's formats, its rules, its own steps); and the
architects and designers, domain experts rather than programmers, work in their own terms and are never asked to write
code, data or commands. The project agent hides the programming and scripting from them, which is one of the reasons Parti
ships a harness of its own (D21).

| Who | Provides |
|---|---|
| Parti | the domain model and its formats; the workflow (D26); the `parti` library, its tools and translators (D27); the harness (D21); `parti-axi`; the skills and agent definitions; the asset browser (its first layer the finish tool), the world builder, the client viewer |
| The project agent | the project's translation into Parti's formats; its rules and data tables; the steps particular to the project, as extensions of the step kinds |
| The architect or interior designer | intent, in their own terms: pointing at things, choosing among options, stating rules, approving at the gates |
| The consumer (home buyer, business buyer, the commissioning client) | nothing to build: they experience the deliverables, the walkthrough with or without VR, the stills and films, and choose among the options offered, in the client viewer (D22) |

At its centre Parti is a guided workflow, installed into a *target project* (a project that owns a building model), that
takes a building from the architect's drawings to a CAD model, a rendered Blender scene and an Unreal
walkthrough. A user and an agent work through its steps together, and each step has tested tools (owner,
22 November 2026). It has three parts:

1. **Guided workflow and toolbase** (the goal). A guided sequence of steps, each with tested tools, from drawings to CAD model, Blender scene and Unreal walkthrough.
2. **Asset browser** (its central feature, D40). Find and choose every kind of product by the product classification (D32): finishes, structure, openings, joinery, sanitary ware, lighting, furniture, services and landscape; place what is chosen on the model's elements and surfaces, by zone and scheme; count it into bills of materials by trade; see it in an Unreal walkthrough under the chosen time of day and weather; one state shared by the interface and the scene. The **finish tool** is its first layer.
3. **Installer and agent interface** (`parti-axi`). Installs Parti, scaffolds it into a target project, and gives agents everything a person can do, including joining a live session alongside the user (D16).

Parti's Python side is one library, `parti` (D27, LGPL-3.0-only): the architectural SDK every target project imports,
holding the workflow, the harness, the catalogue tools and the pipeline tools generalised from the prototype's scripts;
the scaffold gives each project Parti's skills and agent definitions, `parti-axi` and the library. Parti ships its own agent harness (D21): a workflow graph built from the domain's Workflow definition, with Parti's agent
definitions and skills, driving the CAD system, Blender and Unreal through their Python APIs and MCP servers. It is
released in two editions from one domain (D22, B5): the **designer edition**, the full workflow for architects and
interior designers, which 1.0.0 delivers through 0.x releases (D23); and the **client viewer**, a self-contained
walkthrough viewer for the consumer, packaged with a client bundle.

## Part A — Domain-driven logical architecture

The business model in the glossary's language. Nothing in Part A names a technology, a process or a store.

## A1. The ubiquitous language

Every name in Part A is the glossary's (`research/DN-ubiquitous-language.md`): one meaning each, shared with the
architects, designers and users. The system's own technical vocabulary is Part B's (B8).

**The language is the schema** (owner, 24 November 2026). Every glossary term that is data names a type or a field of
the schema, so plain words are translated into glossary terms and the terms into schema records, validated before
they are stored: "light UV-filtered pane glass" becomes a product of a class, with a form, a build-up and attributes by
aspect. Search is then fast and structured (by class, by attribute), and by meaning later, with embeddings in the
knowledge base. The agent breaks words into records with its skills and the library's decomposers (D21, D27), not by
reasoning it all out, to stay context- and token-efficient. The **product classification** (D32), one versioned tree of
product classes in Parti's words, each mapped to an IFC entity type, is the backbone the catalogue, the tagging of the
model, the asset browser and the bills of materials hang on.

## A2. Bounded contexts

Names follow the glossary, `research/DN-ubiquitous-language.md` (revised in the architecture review, D17, D18).

| Context | Aggregates and main data | Commands (examples) | Publishes |
|---|---|---|---|
| **Workflow** (frames the others) | Workflow definition (versioned data): phases, step definitions of twelve step kinds with their checks, caveats and invalidated-by edges, gates of four kinds. Workflow run (per target project): step runs with their to-dos, check results, corrections, decisions, variants, step records (D26, FR-WF-15) | start step; record check; pass gate; record decision; add, tick to-do; raise, resolve correction; branch, choose variant; checkpoint; set focus; show (a workspace command: a view or an editor, its subject and title) | step started / checked / completed / stale; correction raised / resolved; decision recorded; focus set; shown |
| **Building** | Building: levels, rooms, elements, surfaces; each element's label (name, kind, id, tags), its 3D object and 2D drawing elements; the lesser primitives (a product's parts and faces, a surface's pieces) addressable under their parent (D31) | declare, revise, retire element or surface; label, tag element | element declared / revised / retired / labelled |
| **Design** (core: layer planning) | Design: per layer a plan; per surface its zones (area, panel, band, border, …, defined from a selection and labelled); per zone its placement; schemes; shortlist; offers of options for the client, and the client's selections (D22) | define, resize, remove zone; place, clear product; save, apply scheme | zone defined / resized / removed; product placed / cleared; scheme saved / applied |
| **Catalogue** | Product (per layer): its class, form, build-up and attributes by aspect (appearance, physical, quantities, interaction); material; texture; maker; set; matching facts (colour, suitable use); the product classification (D32) | (queries) filter, search, "goes with", by class, by palette; classify | product added / changed / withdrawn; class added |
| **Quantities** (computational module) | The engine behind every product layer's bills of materials (construction, finishes, lighting, furnishing, plumbing, appliances, D30): quantities per plan; bill of materials per work-contract role; estimates later | (queries) quantities, bill of materials | — (derived from plans) |
| **World builder** (module) | Scenario: conditions (time, date, weather, light, site), moving parts, experience mode, routes, viewpoints | choose scenario; set time; set weather; animate moving part; choose experience mode | conditions changed; scenario changed |
| **Session** | Session: participants (users and agents), selection, viewpoint, the shared context of interaction events (D29) | join, leave; select element / surface / zone / group; clear selection; point; clip | participant joined / left; selection changed; pointed, selected, clipped (interaction events) |
| **Asset delivery** | Mapping from a product to what a scene can draw; the client bundle, per client project and revision (D22) | prepare product for a scene | product ready / failed |
| **Identity** (service stage) | Users, access | — | — |

Design refers to products and to building elements by id; it asks Catalogue and Building whether a placement
is allowed through their published facts, never by reading their storage.

## A3. Context map

How the contexts relate. Design is the core; the others serve it or are derived from it.

| Upstream | Downstream | Relationship |
|---|---|---|
| Building | Design, Quantities, World builder, Asset delivery | published facts (surfaces, openings, regions) by id; a building revision flows forward (D19) |
| Catalogue | Design, Quantities, Asset delivery | published facts (suitable surfaces and use, sizes, kinds); Design never reads the catalogue's storage |
| Design (core) | Quantities, World builder, Asset delivery | placements and schemes by id; quantities are derived, never entered |
| Session | Design, World builder | the selection and the participants |
| Workflow | every context | frames them: a step's outputs (a building, a design, a world) are the inputs of later steps; corrections revise them |
| A target project's records, the applications (CAD, Blender, Unreal), the page, the scene | the contexts | through translators only (R3), speaking the published language (R5) |

## A4. Logical rules

| | Rule | Source |
|---|---|---|
| R1 | The domain is pure: its rules are plain functions over plain data, `decide(state, command) → events` and `evolve(state, event) → state`, keyed by aggregate id. No input or output, no outside terms. | D8, D10, NFR-1 |
| R2 | Everything outside the domain is reached through a **port** named in domain terms (the design store, the catalogue store, the session channel, asset delivery). How a port is implemented is Part B's. | NFR-5 |
| R3 | Every outside system has its own **translator** (anti-corruption layer): the scene, the page, each project's records, local files, each driven application, later Nai and EntityStore. No outside term crosses into the domain. | D8, NFR-4 |
| R4 | Contexts know one another by identifier and published events only. | NFR-3 |
| R5 | One **published language**: one versioned message schema (commands, events, queries, snapshots) is the only contract between the domain and everything outside it. | NFR-6 |
| R6 | Commands are safe to repeat; every change is an event with an id and a per-aggregate sequence number; state is rebuilt from events; a stale change is refused. | NFR-2 |

## A5. Versioning and the forward chain

Everything is versioned and changes flow forward (D19): the building, each plan and each scenario has revisions;
elements keep stable ids across revisions; a change upstream is allowed, and what it affects downstream is marked
stale and listed as follow-up actions; nothing downstream changes, or stays wrong, silently. The detail is in
`research/PRD-domain.md` §2.2 and §6.

## A6. The workflow

Workflow frames the other contexts: a step's outputs (a building, a design) are what the later steps, the
finish tool and the world builder work on. Its shape (D26, `research/DN-workflow-shape.md`): phases of steps, each step
running one step cycle (sources → data → generate → apply → check → checkpoint → record), gates, and the correction and
audit loops across every phase. A correction may land in an earlier phase's step; its revision then flows forward
(D19). How the harness runs it is Part B's (B3, the `parti` library).

## A7. Project types and templates

A project is residential or commercial, each with sub-types; its type's template is data that sets the layers present
(and so the bills of materials), the workflow's phases and steps, catalogues, default rules and gates, chosen at
scaffolding and adaptable after (D30).

## Part B — System architecture

How Parti is built and run: the technical components are defined here, not in Part A (owner, 24 November 2026).

## B1. The whole in one picture

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

## B2. System rules

| | Rule | Source |
|---|---|---|
| R7 | Nothing of one target project lives in Parti's code; a project's own translation is its project agent's work (D27). | NFR-10 |
| R8 | Servers bind to 127.0.0.1 in version one; every incoming message is validated against the schema. | NFR-8 |
| R9 | The domain is implemented as pure TypeScript with no imports beyond the schema's generated types; types for every stack are generated from the one schema (R5). | D8, NFR-1, NFR-6 |
| R10 | Between stages only adapters change; the domain, the schema and the page do not. | D9 |

## B3. Components

| Component | Stack | Depends on | Notes |
|---|---|---|---|
| `schema` | schema files → generated TypeScript (later C++, Rust, Avro) | nothing | Commands, events, queries, state snapshots; versioned. |
| `domain` | TypeScript | `schema` types only | One module per context. No imports from anything else in the repository. |
| `gateway` | Bun | `domain`, `schema`, ports | Serves the page; holds the WebSocket links; runs commands through the domain; stores events through the design store; fans events out. |
| `adapters-local` | TypeScript | ports | Catalogue from the target project's records; designs as an event log and a snapshot in a file. |
| `page` | TypeScript, VanJS | `schema` | One page, two presentations (D22): in the designer edition, the **Parti Project Environment**: the **guided chat** with the project agent (through the harness, D21; it follows the embedded workflow and guides the design workflow) beside the workflow view, the **asset browser** (0.1.0: the catalogue browser, detail and shortlist), the zone editor and the conditions controls; in the client viewer, the offered options as an in-world panel with smart menus. Its state is a projection of the shared state. Works as overlay, VR panel and plain browser tab. |
| `mock-scene` | TypeScript | `schema` | Stands in for Unreal: draws surfaces and zones, reports picks. The test partner. |
| `parti` (library, D27) | Python, LGPL-3.0-only | `schema` (the generated Python types and validation) | The architectural SDK every target project imports. Modules: `parti.workflow` (the workflow-definition model, step kinds, step cycle, checks and check results, gates, the correction loop, D26); `parti.harness` (D21: the LangGraph builder that compiles a workflow definition, Parti's agent definitions, including the Nai agents (D29), MCP client connections to SolidCraft, Blender and Unreal; checkpoints and memory behind ports); `parti.catalogue` (catalogue tools: validate and build from records in Parti's format, which the project's own agent translates its records into; colour tags, thumbnails, picture orientation); `parti.tools` (generalised from the prototype's scripts: declared transforms (D25), selectors, rule tables with counts, checks with the worst value, declarations); `parti.translators` (one per application: SolidCraft, Blender, Unreal, the PDF reader); `parti.converters` (plan onboarding: incoming designs into Parti's metadata, D26); `parti.templates` (project types and templates, D30); `parti.units` (D25). A project customises by data and by extending step kinds, never by forking. |
| `parti-axi` | Python (installed with `uv`) | `parti` library; gateway (over its local interface and agent API) | Installer, scaffold, agent commands, workflow guide; session verbs (state, watch, command) and a Pi plugin that wakes the agent (D16, FR-AXI-8, FR-AXI-9). Structured output, dry run, a flag for every question. |
| `plugins/solidcraft` (D34; 0.2.0) | Rust: a WebAssembly component and a native server | `schema`, the endpoint definition | Parti's SolidCraft plugin: the component inside SolidCraft (ids and classes as plugin data, checks, table import, one-step builds) and the native WebSocket server beside it, SolidCraft's endpoint on the bus, driving the running application through its control protocol. |
| `plugins/blender` (D37; 0.3.0) | Python, a Blender extension | `schema`, the `parti` library's Blender translator, the endpoint definition | Blender's endpoint, served in process on the main thread (timers with a window, its own loop headless); transfer, restore, apply by rule, compose, stills and films, variants. |
| `plugins/unreal` (D36; 0.4.0) | C++, an Unreal plugin (Runtime and Editor modules); licence per Q12 | `schema`, the endpoint definition | Unreal's endpoint, served in process; picks, actors moved and the selection out; placements, conditions and scene loading in. |
| `nai/` (the router, D38) and `nai.toml` | Nai's DSL, GPL-3.0-only | `schema` (the registered schemas), the endpoint definitions (D35) | Part of Parti's main source: the pipelines and logic that route and transform Parti's events between the systems on the bus, on the payloads the connectors unwrap; built, tested and released with Parti, deployed to Nai; kept up to date by the harness's Nai agents (D29). `nai.toml` makes the repository a Nai project. Target projects add their own pipelines in their own Nai projects of Parti's kind, which `parti-axi init` creates with Nai's project-creation tool from a Parti template added to Nai (`nai new --template`, `nai check`); the template registers the project's schemas in a subdomain of Parti's domain and generates its connector instances, which run separately; the main Nai process is shared (D39). Nai owns the language, the runtime and the connectors. |
| `client-viewer` | Unreal (packaged app) | its client bundle only | Deferred until after 1.0.0 (D22, D23). Self-contained walkthrough viewer (monitor or VR) with the offered options, stills and films; Windows and Linux; built and downloaded from the designer edition. Licence first (PRD Q12). |
| `unreal-plugin` | C++ | `schema` (generated C++ types) | **Deferred** until Model B supports a C++ stack (D5). Scene adapter, pick, zone master material, finish assets, overlay; the Unreal side of the world builder (D18). |

The repository layout that realises this (workspace packages, test folders) is the orchestrator's to propose.

The harness compiles the workflow definition (A6) into its LangGraph graph; the graph's state is a projection of the
workflow run, and LangGraph's own checkpointer holds the agent's state only, never the project's. Ports (R2) are
implemented by adapters: local files in version one, EntityStore and Nai later (B6).

## B4. How a change travels, and the message bus

Assigning a finish, version one:

1. The user picks a zone in the scene. The scene adapter sends *selection requested*; Session produces *selection changed*; page and scene both show it.
2. The user chooses a finish in the page. The page sends *place finish* with the design's expected version and a command id.
3. The gateway validates the message, loads the design's state, calls Design's `decide`. It refuses (unknown zone, finish not valid for this surface, stale version) or returns *finish assigned*.
4. The event is appended through the design store, then sent to every link.
5. The scene adapter asks asset delivery for the finish in drawable form and updates the zone. The page updates through its projection.
6. A link that joins late receives a snapshot, then events from that sequence number.

The same path serves the CLI: `parti-axi` sends the command and prints the events or the refusal.

**The message bus and the applications (D29).** The fan-out of step 4 is the bus. Each system (SolidCraft,
Blender, Unreal Engine, and Parti's own gateway and harness) serves a WebSocket endpoint, and Nai's one generic
WebSocket **source** (the system's events into the bus) and **sink** (the bus's events into the system), configured
towards each endpoint by its definition, carry CloudEvents both ways (D35); the **Nai project writes every connector**
(D34). Inside the application, its own piece (Parti's SolidCraft plugin, the
Unreal plugin, Blender's add-on) applies what it can apply deterministically, with no agent and no tokens: a placement
changed sets the material on the faces tagged with that surface's id. Each application's
objects carry Parti's ids (a CAD attribute, a Blender custom property, an Unreal actor tag), so references resolve both
ways. Events from the applications (a pick, a CAD revision) come back through the source connector as commands. Work that
needs judgment goes through the harness's agent loop and the applications' MCP servers (D21) instead. Nai is the bus from 0.1.0 (D33):
the systems serve endpoints and Nai's generic source and sink connect to them (D35), with Parti's router in Nai's DSL
(D38); the gateway's own WebSocket fan-out stays as the local adapter behind the same ports, for offline work and
tests (B6).

**Events both ways** (owner, 24 November 2026; D29). The backend's event stream is the agent's context, and the agent's
actions return the same way, as commands whose events every panel shows. Every click is an event, routed to the agents
and to telemetry; the user's actions on the context shared with the agent and with the 2D tools (pointing, selecting,
clipping) are **interaction events** carrying their elements (ids, names, kinds, tags), the area, the world bounds, the
CAD references, the view and the step (`parti.interaction.*/1`). **Design events** change the design and go into its
history and versions; interaction events change nothing in the design and feed only the context and telemetry, so undo
and versions stay clean. The workspace is driven the same way: the workflow step (0.1.0), later the agent, issues
**workspace commands** (what to show, its subject, its title), which the page obeys.

## B5. Where things run, by stage, and the editions

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
| Who | Architects, interior designers | The consumer: home buyer, business buyer, the commissioning client (D28) |
| Platform | Linux first (D2) | Windows and Linux, natively; macOS possibly later. Built and downloaded from the designer edition, per platform (PRD Q14) |
| Workflow, agent harness, CAD, Blender | Yes | No; only a UI helper agent that searches and applies offered sets (tile sets, interior sets) through the viewer's own commands |
| Building | Authoring | Read only, from the bundle |
| Design | Everything, including curating offers | Apply and compare the offered options |
| Catalogue | Every product, search | Only the offered products, in the bundle |
| World builder | Authoring scenarios, conditions, site | The walkthrough: navigation, scenarios, VR |
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

## B6. Backends

- **EntityStore** (the owner's Quarkus service on Redis and MongoDB, with change streams): system of record for Catalogue, Design, Building and review records, behind the catalogue-store and design-store ports. Its change data capture turns every stored state change into a message for the bus (D29). Parti reaches it through
its **REST API**: the store adapters behind the design-store and catalogue-store ports (R2) are REST clients, so
integrating it as Parti's backend store is a matter of adapters; its CDC then streams the changes to the Nai-driven
bus, which propagates them to the other applications in the cluster (owner, 24 November 2026).
- **Nai** (the owner's Rust streaming runtime with its own DSL, connectors and provider plugins): the domain's `decide` and `evolve` functions map onto keyed pipeline stages or a custom provider; session traffic through the endpoints and Nai's generic WebSocket source and sink (D35); embeddings for search by likeness. Also (D9, owner 2026-11-23): retrieval (RAG) for the agent harness and the knowledge base, which move to Nai as soon as the harness exists; session context and agent memory; a file catalogue, so file operations do not depend on the operating system; geospatial and map data, so the world builder builds the site around the building from map providers. Each role sits behind its own port: knowledge store, session store, file catalogue, geo data.

What Nai lacks today for the interactive loop, and the requests this makes to its team, are listed in
`research/DN-founding-design-record.md`. The owner's assessment (22 November 2026): a WebSocket connector is not a
major issue, since Nai already has HTTP in and out connectors. Nai supports custom connectors that talk to Parti over
WebSockets where needed, usually built with the LangChain agentic SDK, the same toolkit as the agent harness (D21;
owner, 23 November 2026). Neither is used in 0.1.0 (D9). They come in with the first release that connects a real application (Blender or
Unreal connectors, the message bus of D29), after a spike once Nai's team confirms the source and sink connectors and
the schema registry (D9, reconsidered by the owner, 24 November 2026); retrieval (RAG) and the knowledge base move as
soon as the agent harness exists. 0.1.0's event schemas are registry-ready, so the move changes adapters only.

**What runs where** (owner, 23 November 2026), in three layers:

| Layer | What runs there | How |
|---|---|---|
| Interaction (near real time) | The validation rules (the domain, R1), the agentic workflows and skills (D21), and the work with the CAD system, Blender and Unreal Engine | The applications' Python APIs, alongside their MCP servers, driven through the LangChain SDK |
| Operations | Queued operations kept consistent in time: the forward chain's follow-up actions (D19), the message bus between Parti and the applications (D29), background RAG and data-preprocessing pipelines | Nai: its queues and ordering per key, pipelines in its DSL |
| Data | The system of record, retrieval, the knowledge base, session context, the file catalogue, geospatial data, telemetry events (usage, timings such as NFR-11's responsiveness, agent runs), and later their distillation for data mining (a secondary need, D9) | Nai and EntityStore |

**Nai, the platform in the middle (D29).** Between Parti's own processes (gateway, harness), the applications, the
stores and the data services, every message that crosses a process boundary can pass through Nai, which transforms,
routes, stores and observes it; within one process, components call each other directly. **Nai as the message bus.** Each application serves a WebSocket endpoint through its plugin (SolidCraft through
the Rust server shipped with Parti's plugin), and Nai's generic WebSocket source connects to it (D35); the events'
schemas sit in Nai's schema registry; Nai's DSL transforms incoming messages into Parti events and
pushes them to the Parti runtime in near real time through its sink WebSocket connector. Parti changes state and
updates the domain objects in the shared EntityStore; Nai's source connectors listening to EntityStore's CDC streams
fire on each change and propagate Parti's state change to every listening party (the applications, the harness's
agent). The same mechanism can carry Parti's backend itself, written in Nai's DSL (PRD Q13). These mechanisms are used only
where required (owner, 24 November 2026): one such place is the messaging between the Bun gateway and the Python
harness, two separate processes, which can be directed through Nai once both exist; until then the harness uses the
gateway's agent API over WebSocket directly. Parti's components reach Nai the same way: the gateway and the harness each serve a WebSocket
endpoint, and Nai's generic WebSocket **source and sink**, built on its Rust connector SDK (Nai's gRPC bridge is for
connectors), connect to every endpoint as clients, configured by its **AsyncAPI** definition in JSON, with every
message a **CloudEvent** whose `dataschema` names a JSON Schema in Nai's registry (D34, D35). They live in Nai's ecosystem and are **written
entirely by the Nai project** from Parti's requests (`research/DN-nai-readiness.md`); Parti writes no connector, and
specifies only the messages. The inverse runs the same way: Parti's events enter Nai, are transformed into
each application's message and reach the applications through the WebSocket sink. EntityStore, a change data
capture database, makes this automatic: each state change Parti stores becomes a message, and the sink connectors call
the applications by RPC to apply it. MCP connects the harness to the same systems for what needs judgment; the CDC path
saves the agent's tokens. The harness also subscribes to these messages, so events trigger the agent (a building
revised, a check failed, a pick from the walkthrough, a consumer's selection): it works only when there is something
to judge, starting with the event as its context. A state change in any application (an object moved in the Unreal
editor, a material changed in Blender, a body revised in SolidCraft) reaches it the same way, and it can act in any
application through MCP: the loop closes across all of them. One loop then carries change
traversal, workflow state, the agent's context and the UI's updates. **Nai agents:** Nai's REST interfaces show the
events on the wire and help debug its DSL; specialised agents in the harness, part of a Parti project where required,
use them to configure the connectors and update the DSL in a closed loop, so Parti adapts to a project's external data
and to new modular functionality.

```text
Unreal plugin ─┐ endpoints (CloudEvents)
Blender ───────┼─◄ WebSocket ─ Nai WebSocket source ─► schema registry ─► DSL ─► Nai WebSocket sink ─► Parti runtime
SolidCraft ────┘ (Rust server)                                                                                          │ updates
                                                                                                           ▼
         listeners (applications, harness) ◄─ sink / events ◄─ Nai source connectors on CDC ◄─ EntityStore (shared)
                     harness (agent loop) ──MCP──► the applications
                     Nai / EntityStore messages ──► harness: an event triggers an agent run

Inverse:  Parti runtime ─► EntityStore (CDC) ─► Nai ─► DSL transform ─► sink WebSockets (RPC) ─► Unreal plugin, Blender, SolidCraft
```

**IFC through Nai** (owner, 24 November 2026; D32). Parti's objects transform to and from IFC-based objects (IFC 4.3,
ISO 16739-1:2024) through an **IFC translator** Nai provides, built by Nai's team from Parti's request
(`research/DN-nai-readiness.md` §5): each product class maps to an IFC entity type and Parti's attributes to IFC property
sets by a declared mapping, so external systems (BIM tools, structural and services models, cost estimating, facility
management) connect without Parti's model taking IFC's shape.

Nai treats all its data as schema-based events. Parti's own changes are already events defined by one versioned schema
(R5, R6), so they map onto Nai's events directly, with no translation of meaning.

How much of the static tooling otherwise written in Python can move to Nai is an open question (`research/PRD-parti.md`
Q13).

## B7. Installing into a target project

Once scaffolded, the architect or designer opens the Project Environment in the browser (served by the gateway); it is
their workspace until the Unreal walkthrough is generated, which then joins it (D22). The first thing the project agent
guides there is **plan onboarding** (D26): the drawing PDFs, and renders when there are any (texture and style cues);
imports from other sketch and drawing tools come later. Format converters and data pipelines (`parti.converters`; Nai
pipelines later) turn the incoming design into Parti's own metadata.

`parti-axi init --target <dir>` writes into the target project its configuration, Parti's skills and agent definitions
(which teach the agent to use the `parti` library and `parti-axi`), the agent notes, and the project's dependencies on
`parti` and `parti-axi` (D27), and nothing else. The target keeps its data where it is; Parti reads it in place and writes only where the
configuration says (saved designs, the step log, checkpoints). When the Unreal plugin exists, the scaffold
also connects it to the target's Unreal project.

## B8. System-design terms

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
| Message bus | The channel the domain's events travel on, to the page, the scene and the applications' connectors (D29). The gateway in version one; Nai later. |
| Nai agent | A specialised agent in the harness that configures Nai's connectors and updates its DSL in a closed loop, using Nai's REST interfaces to inspect events (D29). |
| Connector | Nai's link between the bus and the systems: a source carries a system's events into the bus, a sink carries the bus's events to it. One generic WebSocket source and sink, configured towards each system's endpoint by its definition; written entirely by the Nai project (D29, D34, D35). |
| Router | Parti's event-processing pipelines and logic in Nai's DSL, part of Parti's main source (`nai/`), routing and transforming events between the systems on the bus (D38). |
| Project pipeline | A Nai pipeline a target project adds in its own Nai project of Parti's kind, for its data-processing extensions and dynamic logic, deployed beside Parti's router without changing it (D39). |
| Endpoint | The WebSocket server a system on the bus offers (the gateway, the harness, each application's plugin), exchanging CloudEvents (D35). |
| Endpoint definition | The AsyncAPI 3.0 document, in JSON, that describes an endpoint: its address, the CloudEvent types it sends and receives, its request and reply pairs, and their schemas (D35). |
| Projection, snapshot | A view of state built from events; a saved copy of state at a sequence number. |

## B9. The user interface: the Project Environment

The designer edition's main interface (D22), opened in the browser once a project is scaffolded (`parti-axi open`)
and the architect's or designer's workspace until the Unreal walkthrough joins it. Its layout and interactions were
reviewed as storyboards with the owner (24 November 2026; D22):

- **Panels.** The **workflow panel** on the left (phases, steps, to-dos; actionable), the **workspace** in the middle,
  the **guided chat** on the right (following the embedded workflow, A6, with **suggestions** at every point), and the
  **asset browser** docked at the bottom. Every panel resizes, minimises, maximises, undocks and attaches again at any
  edge; the layout is kept per user; the asset browser can be detached to its own window.
- **The workspace has no tabs.** It is a viewport commanded by the workflow step in 0.1.0 and by the project agent later
  (B4, workspace commands): it shows a **view** (the project, the BOM, the walkthrough, offers) or an **editor** of what
  Parti owns (labels and tags, zones and placements on a surface, Settings), titled by what it shows (*Design · Bath 1 ›
  East wall*). The project opens first.
- **The asset browser:** a tree of the product classes (D32) scoped to the agent's context, with "show all classes"; a
  filter bar (search, palette, a drop-down per filter); results with their path, count and sorts; a detail with
  "goes with" and the shortlist; the agent's signals (filters, palette, marked assets, a note).
- **The 2D tools** on every 2D display: pointer, select, rectangle select, rectangle clip, tag. The pointer and selection
  are the real-life analogue of pointing at a drawing, a 2D bridge to the 3D model: each point or selection names its
  elements in its interaction event (B4). A selection takes a placement, defines and labels a zone, or is clipped into
  the chat.
- **Settings** (⚙): the project, units and display, world defaults, design defaults, backend connections, the agent and
  skills, layout, telemetry; kept in `parti.toml`, secrets only in the environment.
- **The guiding rule:** Parti augments the CAD, Blender and Unreal with easier, assisted interactions and never
  duplicates their editing; the geometry stays in them.

0.1.0 builds the shell and its workspace driven by the workflow (CR-PRT-021, CR-PRT-022), the asset browser
(CR-PRT-014), the surface editor and the BOM (CR-PRT-015), the mock walkthrough (CR-PRT-016) and Settings (CR-PRT-023).
The client viewer's in-world panel is B5's.

## Documents

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
| `research/DN-nai-readiness.md` | Nai's and EntityStore's readiness for the message bus: findings, validation spike, the request to Nai's team. |
| `research/DN-runbook-domain-impact.md` | The prototype's Runbook mapped onto the domain model, context by context (D26). |
| `changes/CR-PRT-NNN-*.md` | Implementation specs, filed on the Crucible board. |
| `.lavish/<document>.html` | **Review pages.** An interactive copy of one specification, built by the orchestrator for the owner's review: annotations, questions and decisions are made there. Every decision is applied to the markdown and committed; the page is a working record on the orchestrator's machine, not versioned and not the source of truth. |

**Order of the design work.** 1. This architecture, reviewed. 2. The glossary (`research/DN-ubiquitous-language.md`).
3. The domain PRD, then the other per-area PRDs, each with its review page. Each is written for the slice the next
release needs (the domain PRD first for 0.1.0), and grows with the releases. 4. CRs, filed on the Crucible board,
last: each implements settled requirements.

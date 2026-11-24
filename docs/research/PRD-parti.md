# PRD — Parti: a guided workflow from drawings to an Unreal walkthrough

**Version:** 0.2 (architecture review applied, 22 November 2026)
**Date:** 2026-11-22
**Status:** DRAFT, reviewed with the architecture on 22 November 2026. Decisions in §3 are the owner's; items marked "proposed" or "open" are not yet confirmed. Detailed sections move to the per-area PRDs as they are written.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)
**Builds on:** `DN-founding-design-record.md` (the discussion these requirements come from)
**Related:** `DN-first-consumer-johnnyhouse.md` (the data and the Unreal project of the first consumer), `DN-pipeline-prototype-johnnyhouse.md` (the pipeline, tools and scripts of the prototype)

## Change Control

| Date | Change |
|---|---|
| 2026-11-22 | First draft, written from the design discussion held in the JohnnyHouse project. |
| 2026-11-22 | Owner's reframing (architecture review): the guided workflow is the goal and the finish tool its first major feature. Title, §1 and D14 restated; no requirement changed. |
| 2026-11-23 | D25: Parti sets and holds each working model's scale in the project configuration, by statement or calibration against a known dimension, re-checked on every import and export (owner). |
| 2026-11-23 | D18: the interactive tool set of the Unreal world (pick, smart menus, compare, operate, navigate, measuring tape, setting controls, notes, guide) (owner). |
| 2026-11-23 | D25: a virtual measuring tape in the walkthrough, showing feet and inches and metres (owner). |
| 2026-11-23 | D25: bills of materials and estimates in real-world units, primarily feet (sq ft, running ft), SI for the rest (owner). |
| 2026-11-23 | D25: model units and world scale: canonical real-world mm at 1:1; a declared transform per system; known-dimension checks (owner). |
| 2026-11-23 | D25: units: millimetres stored; shown as square feet for areas, feet and inches for room dimensions, millimetres for components (owner). |
| 2026-11-23 | D24 location: true location with OpenStreetMap or Google Maps; Unreal renders the immediate vicinity, extent chosen in step 12 (owner). Domain PRD reviewed. |
| 2026-11-23 | D22: the assistant embodied as a guide in the world, speech and text chat (owner). |
| 2026-11-23 | D22: client review sessions as a menu cum chat assisted flow for VR, with voice input (owner). |
| 2026-11-23 | D17: product layers and information layers; the site and geospatial layer is the first information layer (owner). |
| 2026-11-23 | D24: Nai pipelines prepare the assistant's data (embeddings, derived views, indexes), recomputed per revision. |
| 2026-11-23 | D24: Nai pipelines prepare the assistant's data, recomputed per revision; geospatial cues (geo-reference, true north) for compass questions, sun and site. |
| 2026-11-23 | D24: the assistant answers questions about the building: resolve by embeddings, compute with typed tools, retrieve knowledge by RAG (owner). |
| 2026-11-23 | D18 navigation on request ("take me to the master bath", avatar moved by the plugin); D9 contextual questions answered by semantic search and RAG on Nai; offline viewer search open. |
| 2026-11-23 | Q17: the plugin captures direct interactions and telemetry for guidance and assistance; client consent proposed. |
| 2026-11-23 | Q17: what crosses the Parti–Unreal boundary (domain state only, with applied-revision acknowledgements) and how the agent observes Unreal (MCP at editor time, the plugin through Parti at run time). |
| 2026-11-23 | Q16 decided: C++ for the run-time motion player and navigation (no Rust in Unreal). Q17: the Unreal bridge (ids, picking, state, UI) and the in-world UI's form; environmental physics stays in Unreal. |
| 2026-11-23 | D18: navigation in the world (fixed modes, per-project data derived from the building, checks, telemetry); Q16 covers navigation too. |
| 2026-11-23 | D18: the motion library's purpose (fewer agent tokens), metadata and telemetry in Parti's backends; Q16 (its language: editor Python, run-time C++ or Blueprint). |
| 2026-11-23 | D18: direction for a motion library of generic motion primitives the agent composes into interactive scripts (owner). |
| 2026-11-23 | FR-CAT-5: wood veneer, laminate and paint finishes in 0.1.0 (owner; JohnnyHouse #1648). |
| 2026-11-24 | D22: suggestions everywhere, not only in the chat; short to-dos within a workflow task, FR-WF-15 (owner). |
| 2026-11-24 | D22: the guided chat offers suggestions (one-click prompts) at every point of the workflow (owner, storyboard review). |
| 2026-11-24 | D29 message bus and application connectors (deterministic over the bus, judgment through the agent loop and MCP; Nai later); D30 project types, templates and quantities across all trades (owner, storyboard review). |
| 2026-11-24 | D22: the project agent guides the import of sources such as floor plan drawings; imports from other design tools later (owner). |
| 2026-11-24 | D22: the browser is the workspace from scaffolding until the Unreal walkthrough; storyboards of the UI before the page's specs are locked (owner). |
| 2026-11-24 | D22: the Parti Project Environment, the designer edition's main UI; its chat follows the embedded workflow and guides the design workflow; features proposed (owner). |
| 2026-11-24 | D22: the designer edition's interface is a guided chat with the project agent beside components such as the asset browser (owner). |
| 2026-11-24 | D28: the third kind of user, the consumer (home buyer, business buyer, the commissioning client) of the walkthrough with or without VR; D22's client viewer is theirs (owner). |
| 2026-11-24 | D21: why a harness of our own: the project agent hides the programming and scripting from the domain experts (owner). |
| 2026-11-24 | D28: Parti is an ecosystem for architects and interior designers; Parti provides the framework, the project agent the project's logic; the users are domain experts, never asked for code (owner). |
| 2026-11-24 | D27: a project's own translation is its orchestrator's work; Parti provides the formats and the tools (owner). |
| 2026-11-24 | D27: the `parti` library (SDK) with the workflow, harness, catalogue and pipeline tools, LGPL-3.0-only; the scaffold is skills + agent definitions + `parti-axi` + the library (owner). |
| 2026-11-24 | D26 the workflow's shape: phases, step kinds, step cycle, gate kinds, correction and audit loops, variants; workflow definition and run; LangGraph mapping; FR-WF-11 to FR-WF-14 (owner). |
| 2026-11-24 | §8A: the prototype's Runbook P12 recorded as evidence for step 12 and the workflow system (#1660). |
| 2026-11-24 | T4: doors and French windows as Blueprints; agent-interface evidence recorded (#1655 to #1657); setting-out and quantities in 0.1.0 (#1658, owner). |
| 2026-11-23 | T4 item 2: procedural materials arrive white through glTF; check after import; finishes rebuilt from the catalogue (#1653). |
| 2026-11-23 | T4: the per-part route repeated by script for three parts and eight placements; finishes on imported meshes are lost at re-import (#1649). |
| 2026-11-23 | T4: the sub-assembly as a Blueprint built by script from its motion table; working rule for experimental editor tools (#1645). |
| 2026-11-23 | T4: a CAD sub-assembly as its own Unreal component, driven by a motion table from the CAD generators, works in trial form (#1640). |
| 2026-11-23 | T4: STEP into Unreal on Linux crashes (#1639); per-part glTF from SolidCraft and moving sub-assemblies as Unreal components, to be tried. |
| 2026-11-23 | T4 findings from JohnnyHouse (#1637, #1638), correcting the earlier "no Unreal import yet": glTF via Interchange works; only building and furniture travel; names not stable ids; re-import silently deletes actors; finishes as world-space materials. 8A steps 7 and 12 adjusted. |
| 2026-11-23 | FR-MOD-1 points to the declaration format in the domain PRD (`PRD-domain.md`, draft). |
| 2026-11-23 | T4 run with JohnnyHouse; its trial experience comes before any Unreal-export CR. |
| 2026-11-23 | Print split: future, not in 1.0.0 (8A, §10). Q6 closed: Bun confirmed for the service side. |
| 2026-11-23 | 8A: the workflow outline (13 steps and the print side branch, from the JohnnyHouse runbook), finishes chosen once in the design, design changes and world editing as separate chains. T4 (Unreal 5.9 import). |
| 2026-11-23 | NFR-7 confirmed (WebSocket across network boundaries); Q10 answered by DN-test-strategy.md (approved). |
| 2026-11-23 | Owner's answers: Q9 (0.1.0 scope), Q11 (JSON event store), Q7 (GitHub + parti-axi), Q8 (name check), Q1, Q2, Q12 (MIT lean for viewer and plugin), Q14; Q15 makers' terms; D22 delivery split; D23 owner represents stakeholders; NFR-10 synthetic fixtures. |
| 2026-11-23 | Consistency pass after the review: §1 editions, §7 client viewer, §9 stages vs releases. |
| 2026-11-23 | D23: 1.0.0 is the full designer edition, reached through 0.x minor releases (first: 0.1.0), each reviewed with the stakeholders; client viewer after 1.0.0. §9 note. |
| 2026-11-23 | D22: the client bundle keeps its metadata in SQLite beside the asset files (offer, options, index, client choices until sent). |
| 2026-11-23 | Q11: owner's guidance (JSON events; no SQL for multi-user, EntityStore; with Nai from the start, connectors per schema); open: Nai in version one. |
| 2026-11-23 | D22: build and download of the client viewer from the designer edition (Windows, Linux; macOS later), usually the last workflow step; Q14 per-platform builds. |
| 2026-11-23 | D22: smart menus in the client viewer, at the zone pointed at, applying bundled options in place. |
| 2026-11-23 | D22: one page, two presentations (designer: all data libraries; client viewer: offered options as an in-world 2D panel, VR first); T1 extended to the viewer. |
| 2026-11-23 | D22: the client viewer's agent is a limited UI helper (search and apply offered sets), acting only through the viewer's commands. |
| 2026-11-23 | D22: a second delivery mode, the client bundle served remotely by Nai as a client server; one port, two adapters. |
| 2026-11-23 | D22: the client bundle is a filesystem package with everything the viewer executable needs to run (owner). |
| 2026-11-23 | D22: the client viewer also shows the pre-rendered stills and films from the Blender part of the pipeline; they travel in the client bundle. |
| 2026-11-23 | D22: editions (designer edition; client viewer, Windows and Linux, packaged with a client bundle per project); D2 split by edition; Q4, Q12 amended. |
| 2026-11-23 | D2 and NFR-9: Linux for the first release; no Windows build planned, no lock-in for a later client-side port; server side need not port; Windows users via a container or WSL2. T1 on Linux; Q3 closed. |
| 2026-11-23 | D9: telemetry events hosted on Nai; Nai's schema-based events match Parti's events and schema. |
| 2026-11-23 | D9: the split restated as three layers (interaction: rules, agentic workflows, applications' Python APIs with the LangChain SDK; operations: Nai's queues and temporal consistency, DSL pipelines; data: Nai and EntityStore). |
| 2026-11-23 | D9: the split (Nai DSL for background RAG and preprocessing; rules and CAD operations stay in Parti's agentic workflows and skills); Q13 (static tooling on Nai). |
| 2026-11-23 | D9 extended: Nai's roles (RAG, knowledge base, session context, file catalogue, geospatial and map data); RAG and the knowledge base move to Nai once the agent harness exists. D18 gains the site from geospatial data and map providers. |
| 2026-11-23 | D21: Parti's own agent harness as one bundle (LangGraph workflow graph in Python, AXI, agent definitions and skills; MCP client of SolidCraft, Blender and Unreal; no Parti MCP server). §7 gains the agent harness. |
| 2026-11-22 | D20: licence GPL-3.0-only, repository public; Q12 (Unreal plugin licence compatibility). |
| 2026-11-22 | Terms aligned with the glossary across §4, §7 and §9 (Building, placement, setting); Stage D notes the migration trigger (D9); version 0.2. Requirement ids unchanged. |
| 2026-11-22 | Architecture review, owner-approved: D19 (versioning, changes flow forward; breaking changes allowed and flagged); D17 adds Quantities as a computational module (cost estimates later). |
| 2026-11-22 | Architecture review, owner-approved: D16 (agents through AXI), D17 (building with layers), D18 (world builder); FR-AXI-8, FR-AXI-9; §2 replaced by the glossary `DN-ubiquitous-language.md`; §6 contexts revised; §10 and Q9 amended. |

## 1. Purpose

Parti is an **ecosystem in which architects and interior designers create their projects with agentic help** (D28).
Parti provides the coding and logical framework; the agent in each project (the project agent) concentrates on that
project's own logic; and the architects and designers, who are domain experts and not programmers, work only in their
own terms, never writing code. At its centre is a guided workflow that takes a building from the architect's drawings
to a CAD model, a rendered Blender scene and an Unreal walkthrough. A user and an agent work through its steps together,
and each step has tested tools (owner, 22 November 2026).

Parti is released in two editions from one domain (D22): the **designer edition**, for architects and interior designers, which the first major release 1.0.0 delivers through 0.x releases (D23); and the **client viewer**, a self-contained walkthrough viewer for the building's owner.

**Its first major feature is the finish tool.** A person walking through a building in an Unreal Engine
application should be able to point at a wall, a floor or part of one, browse a catalogue of finishes (tiles
first, paints later), apply a finish, and change the scene settings (time of day, weather), all through one
interface that stays in step with the scene.

Parti is built as a product separate from any one building. It is installed into a *target project*
(a project that owns a building model, an Unreal project and its finish data). The first target project is
JohnnyHouse; its agent is the first consumer of Parti. Parti is developed by its own orchestrator and must reach
a release without help from the JohnnyHouse session.

Why not Blender: Blender gives pre-rendered stills and films only. The interactive part belongs in Unreal.

**Why a workflow, and the finish tool first** (owner, 22 November 2026). JohnnyHouse was
run as a prototype, without Model B, and the path from an architect's drawings to a CAD model, a rendered
Blender scene and an Unreal walkthrough was worked out there by hand, with custom scripts and a runbook. The
deliverables and the pipeline are now clear enough to turn into a product. So, around the finish tool, Parti
provides (§8A):

- a **guided workflow** that leads an agent through those pipeline steps in a new target project, and
- a **toolbase**: the maintained, tested replacements for the one-off scripts the JohnnyHouse agent wrote.

The difference between Parti and the JohnnyHouse agent is exactly this: the agent improvised the tools; Parti
supplies them.

**How these specifications grow** (owner, 22 November 2026). JohnnyHouse continues as the prototype: new
steps are tried there first, by hand. What an experiment settles is then written into Parti's specifications
(this PRD, the per-area PRDs, design notes) by the JohnnyHouse agent or the owner, and Parti's orchestrator
turns it into CRs. So these documents are expected to keep growing; a requirement here that has not yet been
tried in the prototype is marked "proposed" or "open".

## 2. Terms

The business terms are defined in the living glossary, `DN-ubiquitous-language.md`, the project's Ubiquitous
Language shared with architects, designers and users. System-design terms (page, gateway, scene adapter, …)
are listed in `../Architecture.md` §11. Where an older term appears in this PRD, the glossary's replacement
applies: *Model* → Building, *assignment* → placement, *Presentation* → setting (world builder). On a
wall a zone is a band by height (skirting, dado, border, upper) or a rectangle (niche, feature panel); on a
floor, the field, a border inset or a rectangle (shower area).

## 3. Decisions already taken (owner)

| # | Decision |
|---|---|
| D1 | The interface is an overlay inside the Unreal application. It must also work later as an interactive panel placed in the 3D scene, for a virtual-reality tour. Designed for now, built later. |
| D2 | Version one of the **designer edition** (D22) runs on Linux, standalone and local, one user per session (owner, 23 November 2026: Linux is the platform of choice for the first release; a Windows build is not planned). No technology may lock Parti out of a later Windows port of its client side. The backend, server-side parts may never need porting. On Windows, Parti can instead run as a container, or under WSL2, as it does on Linux; the Unreal app then runs on Windows and reaches Parti on the host's 127.0.0.1 (WSL2 forwards localhost; a container publishes its port), to be checked when wanted. The **client viewer** (D22) runs natively on Windows and on Linux; macOS may follow. |
| D3 | Later stages: first a data service (catalogue, users, saved designs) used by installed apps; then Unreal streamed from servers to a browser. The technology chosen now must carry through. Full collaboration (several users on one design) comes later, so the state must be designed for it now. |
| D4 | Interface and service code: TypeScript on Bun. VanJS renders the page. |
| D5 | The Unreal side is a full C++ plugin. No Rust inside Unreal. **The C++ plugin is deferred** until Model B supports a C++ stack; until then this repository is Bun and Python only (see §9). |
| D6 | Finishes are Unreal assets when applied. A core catalogue is built into the app as Unreal assets; further finishes are created at run time from files, behind the same catalogue interface. |
| D7 | The interface works with Unreal's own asset management (Interchange import, primary data assets, Asset Registry, Asset Manager). It does not run a parallel catalogue beside it inside the app. |
| D8 | Domain-Driven Design, with domain boundaries and anti-corruption layers, so the same business logic can later move onto other backends. |
| D9 | Version one has no Nai and no EntityStore. Later the backend migrates to Nai (pipelines in the Nai DSL, connectors, a custom provider if required) and EntityStore. Both are the owner's own projects. The migration is taken on together with the multi-user, multi-session implementation (confirmed by the owner, 22 November 2026); until then the local adapters serve. Nai's roles, with EntityStore (owner, 23 November 2026), each behind its own port: retrieval (RAG) for the agent harness (D21); the project's knowledge base; session context and agent memory; a file catalogue (rich metadata over every file Parti uses, so file operations do not depend on the operating system); geospatial and map data and computation, so the world builder (D18) can build the Unreal world around the building from geospatial data and map providers; and the hosting of telemetry events (usage, timings, agent runs). Nai treats all its data as schema-based events, which matches Parti's own events and versioned schema (R5, R6). **Timing:** retrieval and the knowledge base move to Nai as soon as the agent harness exists, ahead of the multi-user implementation; the other roles move with it. **The split** (owner, 23 November 2026), in three layers: *interaction*, near real time: the validation rules (the domain, R1), the agentic workflows and skills (D21), and the work with the CAD system, Blender and Unreal Engine through their Python APIs (alongside their MCP servers) and the LangChain SDK; *operations*: Nai queues operations and keeps them consistent in time (the forward chain's follow-up actions, D19), and its DSL runs the background RAG and data-preprocessing pipelines; *data*: Nai and EntityStore. How much of the static tooling otherwise written in Python can move to Nai is explored (Q13). **Why semantic search and RAG matter** (owner, 23 November 2026): the user asks the agent contextual questions in the world ("what tile is this, who makes it, what goes with it, how many boxes for this wall"); the context comes from the plugin (what is selected or in view), and the answer from Parti's backends (catalogue, design, quantities, knowledge base) through semantic search and retrieval on Nai. Open: in an offline client viewer, the same needs either the online mode or a small search index inside the client bundle's SQLite. |
| D10 | The pure domain logic is TypeScript, run by Bun. |
| D11 | Parti has its own repository (this one), its own orchestrator registered on Sandesh, and is dog-fooded with JohnnyHouse data. |
| D12 | Parti ships its own scaffold installer, in the manner of `modelb-axi`, so that an AI agent can install it into a target project and work with it (see §8). |
| D14 | Parti is a guided workflow, worked through by a user and an agent together, covering the pipeline steps of the JohnnyHouse runbook, with the toolbase that replaces JohnnyHouse's custom scripts (§8A). The finish tool is its first major feature (restated 22 November 2026: the workflow is the goal). JohnnyHouse stays a prototype outside Model B; Parti is the Model B project. |
| D15 | Stacks of this repository: Bun and Python. The project is registered with Crucible (test reporting and the CR queue) and on Sandesh. |
| D13 | Whether to replace Unreal's built-in browser with another embedded browser is decided after a trial (see §11, T1). |
| D16 | Agents work alongside the user through AXI: `parti-axi` lets an agent join a running session as a participant, and a Pi plugin wakes the agent when the user acts. No MCP server and no embedded agent harness for now. Whether this is in Stage A is decided with Q9. An agent is a session participant like a user, so the same model carries to several users and sessions, to a served Parti and to a Nai backend (D3, D9). |
| D17 | The domain is a building with layers. The building is the base: its geometry, referenced through labelled elements (level, room, wall, floor, opening, …), each tied to its 3D object and to its 2D drawing elements. Layers sit on the building: finishes first (tiles, paints); furniture and cabinetry, electrical and plumbing later. Each layer places products from its catalogue onto the building under its own rules; a layer may change the model (cabinetry adds geometry). Each yields quantities, which roll up into bills of materials for each work-contract role. Quantities is a computational module: it holds the bills of materials and, with price data later, computes cost estimates. The finish tool is the finishes layer. **Two kinds of layer** (owner, 23 November 2026): *product layers* place products from a catalogue onto the building and yield quantities (finishes, furniture and cabinetry, electrical, plumbing); *information layers* describe the building's context and place no products, starting with the **site and geospatial layer** (geo-reference, true north, terrain, surroundings, map data, sun paths), which serves the assistant's compass and orientation questions, the sun position and the world builder's site (D18, D24). Both kinds are versioned (D19), refer to building elements by id, and are prepared by Nai pipelines (D9). |
| D18 | The world builder is a module of Parti. Once the building is modelled in CAD and brought into Unreal Engine, it creates a world there with the building at the centre of all activity, and stages it as an experience. It holds Parti's own metadata over Unreal's data structures, so an architect or designer can change the experience: scenarios; setting state (time of day, date, weather simulation, light); animations of the moving parts of the building and its world; experience mode (VR, or a monitor with peripherals); routes and viewpoints; and the site around the building, built from geospatial data and map providers through Nai (D9). Parti exposes this state to the agents that run the pipeline, alongside Unreal's own MCP, through its agent interface (D16). The current focus is this part of the workflow, after the CAD model exists. The world builder has its own per-area PRD, together with the Unreal plugin and finish assets. **Direction (owner, 23 November 2026):** the world builder provides a **motion library**: generic, reusable motion primitives (hinge, slide, follower or linkage, gear or ratio, lift and fold, telescope, continuous rotation), each with its parameters and limits. A sub-assembly's motion table is a composition of primitives, computed from the CAD generators (T4, #1640); the agent uses the library to compose the motion and to write the interactive scripts that operate it inside Unreal. Proposed: primitives are kinematic (driven exactly by one input, from the CAD numbers, testable), with Unreal's physics simulation as an option on a primitive, not its basis. **Purpose** (owner): agents spend fewer tokens on repeatable steps, because a kinematics library and toolset turn each moving part into data (its motion table) rather than new code. The library's metadata (its primitives, each part's motion table as versioned data, D19) and the telemetry of its use are kept in Parti's backends (Nai later, D9). Which language implements it depends on Unreal's requirements (Q16). **Navigation** in the world follows the same pattern (owner, 23 November 2026): fixed navigation modes written once (walk with collision, stairs and level changes; teleport for VR comfort; orbit or fly for overviews; following a route; jumping to a viewpoint), and per-project navigation data the agent derives from the building rather than code: walkable areas and collision generated from the building data (imported CAD meshes rarely carry usable collision), stairs and levels, doors as passages that open and close with their motion, viewpoints, routes, teleport points, no-go areas. The data is checked (clearance along routes, every room reachable), and where people walk and look is kept as telemetry for the designer. **Navigation on request** (owner, 23 November 2026): the user asks the agent "take me to the master bath"; the agent resolves the room in the Building context and issues a *go to* command (a room, a viewpoint, a surface), and the plugin moves the user's avatar there along a route from the navigation data. The agent acts for the user as a session participant (D16); the message schema gains navigation commands. Detailed in the world builder's PRD. **Interactive tools** (owner, 23 November 2026): the world builder provides a set of interactive tools in the Unreal world, run-time C++ (Q16) that read and write Parti's data through the plugin (Q17): pick and select; smart menus; compare (two options or schemes, side by side or A/B); operate moving parts (motion library); navigate (walk, teleport, go to a room or viewpoint, follow a route); the **measuring tape** (feet and inches and metres together, D25); setting controls (time of day, weather); notes left at a place for the designer; and the guide (D22, D24). The set grows with the releases. **Motion tables** (JohnnyHouse #1640, #1642): as the building declaration is to the finishes layer, a per-assembly motion table (groups of bodies, each a hinge or a follower, driven by one input) is to the motion library; Parti defines its format beside `parti.building/1` when the world builder is specified. |
| D19 | Everything is versioned, and changes flow forward. The building, each plan and each scenario has revisions. Building elements keep stable ids across CAD revisions. Parti keeps the chain building → design → quantities → world builder. When something upstream changes, the change is allowed; Parti works out what downstream is affected, marks it stale, and lists the follow-up actions (re-check placements, recompute quantities, rebuild the scene), which the agent works through with the user (D16). What a change breaks (for example an orphaned placement when its zone is removed) is flagged as a follow-up action. Nothing downstream is changed silently or left wrong silently. The detail (rules, follow-up actions, how ids stay stable) belongs to the domain PRD. |
| D20 | Parti is free software under the GNU GPL v3.0 only (`GPL-3.0-only`, the same as Crucible), and its repository `anthill-tec/parti` is public (owner, 22 November 2026). Crucible's clients are development tooling only and are never copied into this repository or its packages. The `parti` library is the one exception to the licence: LGPL-3.0-only (D27). |
| D21 | Parti ships its own agent harness as one bundle (owner, 23 November 2026): a workflow graph (LangGraph, Python) built from the domain's Workflow definition, whose nodes call domain commands through the agent API, so the domain stays the single source of truth; `parti-axi` (FR-AXI-1 to FR-AXI-9) for agents outside the bundle; and Parti's agent definitions and skills, installed into the target project. The harness integrates with SolidCraft, Blender and Unreal Engine through their Python APIs and, as a client, their MCP servers (D9's interaction layer), so the agentic workflow talks to these tools to carry out its tasks (FR-WF-6, D18). Parti serves no MCP of its own (D16). The harness's checkpoints and memory sit behind ports: local first, Nai and EntityStore for cloud hosting (D9). Detailed in the installer-and-agent-interface PRD; the Workflow definition it is built from, in the domain PRD. **Why a harness of our own** (owner, 24 November 2026): the project agent hides the programming and scripting from the architects and interior designers, who are domain experts (D28); a harness built around Parti's workflow, library and skills is what lets it do so reliably, and with far fewer tokens than an agent improvising scripts (the prototype's lesson, D26). |
| D22 | Parti is released in **editions** built from one domain (owner, 23 November 2026). The **designer edition**, for architects and interior designers, carries the full workflow: the pipeline from drawings to the walkthrough, the agent harness (D21), authoring. Its interface, the **Parti Project Environment** (owner, 24 November 2026), is a **guided chat** with the project agent (the workflow's guide: it says where the project stands and what is next, puts each gate as options with pictures, resolves what the user points at, and reports in the user's own terms and display units, D28), beside components such as the **asset browser** (every kind of asset in one place: the catalogue's finishes, later furniture and fittings, and library assets found but not yet acquired, with licence and the user's permission to acquire; each choice made for a target, a room, surface and role; choosing also inside the walkthrough; the prototype's tile browser is its first form, and 0.1.0's catalogue browser is Parti's), the finish tool's zone editor, the setting controls and the walkthrough itself. The chat **follows Parti's embedded workflow and also guides the design workflow** (owner, 24 November 2026). **At every point it offers suggestions** (owner, 24 November 2026): the likely next replies and actions as one-click prompts, drawn from the workflow's state (the current step's next actions, a gate's options, the selection), so the user types little; a suggestion is also cheaper for the agent than free text to interpret. **Suggestions are available everywhere** (owner, 24 November 2026), not only in the chat: beside the selection in each component (the design workspace, the asset browser, quantities) and in the walkthrough (the smart menus). **Short todos within a workflow task** (owner, 24 November 2026): the user or the agent can add a short to-do to the current step ("ask the client about the band colour", "check the door width on site"); to-dos belong to the workflow run, are shown with their step in the workflow view and the chat, and a step's completion lists any still open (FR-WF-15). Its features (proposed; detailed in the page's PRD): **Guided chat**: the conversation with the project agent, following the embedded workflow (D26): where the project stands, what is next, each gate put as options with pictures, corrections started by pointing; and guiding the design workflow itself: dividing surfaces, choosing finishes, schemes, quantities, in the user's terms (D28); **Workflow view**: the phases and steps with their state, what is stale and the follow-up actions, the decisions taken, the step records and checkpoints; **Asset browser**: every kind of asset, each choice made for a target; library assets acquired only with permission (D22); **Design workspace**: the finish tool: surfaces and zones, placements with their setting-out, schemes, the shortlist with targets, variants to compare; **Quantities**: per room and finish, with the counting rule; bills of materials and estimates later (D25); **Walkthrough**: the live Unreal scene (the mock scene in 0.1.0) with the interactive tools: pick, smart menus, compare, measuring tape, setting controls, notes (D18); **Views**: stills and films, made and compared; **Offers and delivery**: the options offered to consumers, the client bundle and its publishing (D22); **Project**: the sources, imported with the project agent's guidance (floor plans and other drawings first, the Intake phase of D26; **imports from other design tools later** (owner, 24 November 2026)), the building declaration and its quality, the target project's settings (units, scale, D25). **The browser is the workspace** (owner, 24 November 2026): once `parti-axi init` has scaffolded a target project, the architect or designer opens the Project Environment in the browser, and it stays their workspace through every phase until the Unreal real-time walkthrough is generated; from then on the walkthrough joins it (the page as overlay and VR panel). **Storyboards first** (owner, 24 November 2026): the Project Environment's layout and components are designed as storyboards, mocks of the layout and of each component in its states, reviewed with the owner before the page's specifications are locked. The **client viewer**, for the consumer of the project's deliverables (the building's owner, or a home or business buyer, D28), is lightweight and self-contained: a viewer for the Unreal Engine architectural walkthrough, on a monitor or in VR, with pre-bundled options to apply and compare (different tile sets, schemes), and the pre-rendered stills and films made in the Blender part of the pipeline. It runs natively on Windows and on Linux, from the client's own operating system. The designer publishes a **client bundle** per client project and revision (D19): a filesystem package holding everything the viewer executable needs to run, namely the building, the **offer** of options, the scenarios, the stills and films, and every asset they use. Inside it, the assets are plain files and their metadata sits in one SQLite database (owner, 23 November 2026): the offer, its options and defaults, the index of assets, stills and films, and the client's choices and notes until they are sent back. SQLite suits the viewer because it is single-user and local; the multi-user designer side uses EntityStore (Q11). The viewer runs from it on the client's machine, with no server or network; the viewer is packaged with its project's bundle. Alternatively (owner, 23 November 2026), the same bundle content is served remotely by Nai, acting as a client server: the viewer then fetches its project's bundle and sends the client's selections and telemetry back live, and a new revision reaches the client without reshipping (needs a network and a served Nai, Stage D). The viewer reads its bundle through one port, so the two modes differ only in its adapter: filesystem package or Nai. **Delivery split** (owner, 23 November 2026): the heavy assets (cooked geometry, textures, finish assets, stills and films) always travel as files, cached per revision; when online, the light, changing data (the offer, the client's choices and notes, telemetry, the UI helper's retrieval) goes through Nai. Streaming the walkthrough from servers (Stage E) remains an option that needs no install. Agentic help in the viewer is limited (owner, 23 November 2026): a **UI helper** that helps the client search and apply tile sets, interior sets and other offered options. It acts only through the viewer's own commands (apply and compare offered options), never free placement or the building. Where its model runs (online through Nai; offline needs network access or a local model) is open. The client viewer hosts Parti's asset interface, the same page (D1), with a different presentation (owner, 23 November 2026): the designer edition shows every data library, in an overlay or a browser tab; the client viewer shows only the offered options, as a 2D panel rendered in the 3D world, with VR interaction first. In the viewer, **smart menus** open in the world at a zone (or element) the client points at, listing only that zone's offered options; choosing one applies its bundled assets at once. The flat panel keeps the overview and comparison. The designer edition offers a **build and download** of the client viewer (owner, 23 November 2026): it packages the viewer with the project's client bundle for a chosen platform, Windows or Linux now and macOS possibly later, for the designer to hand to the client (Q14). Building and packaging the client viewer is usually the **last step** of a Parti project's workflow, after world building. Since the viewer has no gateway, its in-world panel loads the page from the bundle (or online from Nai); T1 applies to the viewer too. The client's choices return to the designer's project as a **client selection**. An edition narrows the contexts, commands and adapters it ships; the rules are never copied. *Proposed:* the designer edition validates every option before publishing, so the viewer switches between ready-made variants (Unreal variant sets, Q4) and needs no rules engine of its own. The viewer's licence is settled before it is designed (Q12). **Client review sessions** (owner, 23 November 2026): a quasi menu cum chat assisted flow, made for VR. Menus (smart menus at zones, options, scenarios, comparisons) carry the choices; chat carries free questions, by voice in VR, where typing is impractical; the assistant answers (D24) and turns its answer into menu entries (apply this option, go to that room, compare with the earlier scheme), and a spoken request can open the right menu in place. A review moves through rooms or offers as a guided flow, the assistant proposing the next step; the client's choices, notes and approvals become the client selection returned to the designer. The assistant may be embodied as a **guide** placed in the world (owner, 23 November 2026): a figure that walks with the client, listens and speaks (speech recognition and speech synthesis), with text chat as the fallback; in Unreal possibly a digital human with lip sync (for the world builder's and the viewer's PRDs). |
| D23 | The first major release, **1.0.0**, is the full **designer edition** (D22): the guided workflow for architects and interior designers (owner, 23 November 2026). It is reached through **minor releases (0.x)**, each a usable step towards it; the first release is **0.1.0**. Parti is built iteratively with its stakeholders (owner, 23 November 2026): each minor release is reviewed with them (the first consumer, JohnnyHouse, and the architects and designers who will use it), and what is learned shapes the next release and the specifications. The owner represents the external stakeholders' interests to the orchestrator. The client viewer follows 1.0.0. Which minor release carries what is the roadmap's, proposed by the orchestrator and approved by the owner. |
| D24 | **The assistant answers questions about the building** (owner, 23 November 2026), in the viewer and the designer edition: "show me a bird's-eye view from the south-west", "show me the frontage of the drive to the garage", "how many square feet is the master bedroom", "is there sit-out space in the porch", "is there room for a shoe rack in the porch". Each answer takes three jobs: **resolving what is meant** (rooms, uses, aliases, features, site areas and products, held as embeddings with their ids for semantic search); **computing the answer** with typed tools over the building and design data (areas, dimensions, free space after fittings and clearances, camera framing), never from retrieved text; and **retrieving knowledge** (design notes, standards, typical sizes and clearances, product facts) by RAG. An answer may act: move the avatar, set a view, highlight the space. The building model therefore carries room use and aliases, site areas outside the rooms, the world's north, and room outlines. **Nai prepares the data** (owner, 23 November 2026): the transformations behind these answers run as Nai pipelines in the operations layer (D9): embeddings of rooms, aliases, site areas and products; derived views such as room areas, free floor and wall space after fittings, and camera framings; search indexes. They are recomputed on each building or design revision (D19). The typed tools read the derived views; the rules stay in Parti's domain. **Geospatial cues** (owner, 23 November 2026): the building is geo-referenced (latitude, longitude, elevation) and oriented (the angle between plan north and true north), so the assistant answers compass questions ("which rooms get morning sun", "what does the porch face", "show me the north-east corner", orientation questions such as Vastu), the sun position for a date and place is exact (FR-PRE-1), and the world builder takes the site's terrain and surroundings from map providers (D18). **Location** (owner, 23 November 2026): the true location is used, with a map integration (OpenStreetMap or Google Maps) to locate the building in the real world; Unreal renders only the immediate vicinity (the compound and some surrounding area) to keep the experience immersive, the extent being a choice made in the workflow's world-building step. To check before integrating: each provider's terms for using its data in a rendered world (OpenStreetMap's attribution and share-alike licence; Google's terms for its map and 3D data). |
| D25 | **Units** (owner, 23 November 2026). Parti stores every length in one canonical unit, the millimetre, with areas and volumes derived from it, so rules, events and comparisons never mix units. What is shown is a preference of the target project, per kind of quantity: floor space and areas in **square feet**; room and space dimensions in **feet and inches** (decided by the owner, 23 November 2026); component measurements (tiles, fittings, thicknesses, grout, openings) in **millimetres**; **bills of materials and estimates in real-world units, primarily feet** (owner, 23 November 2026): square feet for areas (tiling, painting, flooring), running feet for lengths (skirting, borders, edge profiles, cornices, carpentry edges), and SI for the rest (kilograms for adhesive, grout and cement; litres for paint; metres for cable and pipe; cubic metres for volumes), with counts as pieces and boxes (a box's coverage in square feet). Conversion happens only at the edges: the page, the assistant's answers, `parti-axi` output, and the Unreal plugin (Unreal works in centimetres, T4). Input in any unit is accepted and converted to millimetres on entry. **Measuring tape** (owner, 23 November 2026): in the walkthrough the user has a virtual measuring tape that measures between two points they pick (or along a surface) and shows the result in feet and inches and in metres together; it measures at world scale from the building's own geometry, so it agrees with the declared dimensions, and its readings can be noted for the designer. **Model units and world scale** (owner, 23 November 2026): Parti's canonical unit is the **real building's** millimetre, at world scale 1:1. Each system Parti meets has its own units and scale (the CAD source in millimetres, declared 1:1; Blender in metres, whose object scale can drift, as the prototype found; Unreal in centimetres; a later printed model at 1:50; the map through the site's geo-reference and true north), so each translator applies a **declared transform** (units, scale, axes, origin), never an ad hoc conversion, and a known dimension (a door's height) is checked in each system. The declaration states the source model's units and scale. **Parti sets and holds the scale** (owner, 23 November 2026): each working model's units and scale are part of the target project's configuration, set through `parti-axi` either by stating them or by **calibrating against a known dimension** ("this door is 2100 mm"), during drawing intake (step 1) and when each model (CAD, Blender, Unreal) joins the project; Parti applies them to everything it measures (the measuring tape, areas, bills of materials, the assistant's answers) and re-checks the known dimension on every import and export, so a scale drift is caught at once. |
| D26 | **The workflow's shape** (owner, 24 November 2026), from the prototype's Runbook and log (`DN-workflow-shape.md`, `DN-runbook-domain-impact.md`). The workflow Parti embeds in its harness (D21) is one repeatable graph for any architectural project; a project supplies only data. **Phases** (Intake, Model, Declare, Design, Present, World, Deliver; their order is data, and the owner may change it) hold **steps**, each an instance of one of twelve **step kinds** (intake, build from data, consolidate, declare, transfer, restore after transfer, apply by rule, derive, compose the scene, choose, render or package, trial). Every step runs one **step cycle**: read the sources, write the data, generate, apply, check against the expected numbers, checkpoint, record; on a failed check the data is fixed, never the output. **Gates** are of four kinds: review, option, permission, trial. Two loops cut across: the **correction loop** (trigger, resolve the pointer, find the cause in numbers, fix the data in the step it belongs to, which may be in an earlier phase, check, say what was not checked, the owner tries it, record), the most frequent unit of work in the prototype (48 of 174 CAD log rows), and the **audit loop** feeding it; **variants** branch beside the main line for comparison. The Workflow context holds a **workflow definition** (versioned data: phases, step definitions with their checks, caveats and invalidated-by edges, gates) and a **workflow run** per target project (event-sourced: step runs, check results with what was not checked, corrections, decisions, variants, step records). In the harness: the definition compiles to the LangGraph graph (phase = subgraph, step = node, check = routing node, gate = interrupt, correction loop = subgraph); the graph's state is a projection of the run, and LangGraph's checkpointer holds only the agent's state. **The prototype is still running:** the shape is provisional against it; each new Runbook version is checked against the graph, and a change lands as a new version of the workflow definition (data), not of the harness's code. The 0.1.0 finish tool is the Design phase's choose, apply-by-rule and derive steps. |
| D27 | **Parti's architectural SDK is a library** (owner, 24 November 2026): one Python library, `parti` on PyPI, that every target project Parti scaffolds imports, so its agents call tested functions instead of writing scripts. It holds the workflow (D26: the workflow-definition model, the step kinds, the step cycle, checks and check results, gates, the correction loop, and the builder that compiles a definition into the LangGraph graph), the agent harness built on it (D21), the catalogue tools (translators from a project's records, colour tags, thumbnails), and the tools generalised from the prototype's scripts (RUNBOOK §3.2): declared transforms per application (D25), selection by class, room, face or name pattern, rule tables applied with a count of what they touched, checks returning pass or fail with the worst value, declarations written beside what they describe, and one translator per application (SolidCraft, Blender, Unreal, the PDF reader). A target project customises its workflow by data and by extending the library's step kinds, never by forking it. **What Parti scaffolds into a target project** (`parti-axi init`): Parti's skills and agent definitions (which teach the agent to use the library and `parti-axi`), the configuration, and the dependencies on `parti` and `parti-axi`; the skills + `parti-axi` + the library together serve all of the project's needs. **Licence:** the library is LGPL-3.0-only, so a project's own scripts and workflows may import it under any licence while changes to the library stay free; Parti's applications stay GPL-3.0-only (D20). The library's code stays free of any one house (NFR-10). **Translating a project's own data is that project's orchestrator agent's work** (owner, 24 November 2026): Parti provides the workflow and the tooling foundations (the formats `parti.building/1`, `parti.catalogue/1`, `parti.scan/1`, `parti.shortlist/1`, later `parti.motion/1`; the library's tools to validate, derive and build), and the project's agent, guided by Parti's skills, writes its translation into them. |
| D28 | **Parti is an ecosystem for architects and interior designers working with agentic help** (owner, 24 November 2026). Parti provides the coding and logical framework (the domain model and its formats, the workflow, the `parti` library with its tools and translators, the harness, `parti-axi`, the skills and agent definitions, and the applications: the finish tool and, later, the world builder and the client viewer), so the **project agent** (the orchestrator agent in each target project) concentrates on the project's own logic: translating its own data into Parti's formats, its own rules, the steps particular to it. **The architects and interior designers are domain experts, not language or programming experts:** they work in their own terms (rooms, surfaces, finishes, views, options), by pointing, choosing and stating rules, and are never asked to write code, data files or commands. Everything they see is in the glossary's language, in their display units (D25), with pictures and options where taste decides (FR-WF-9, D26's gates); the agent turns their intent into data, rules and tool calls. Parti's skills teach the project agent this division. **The third kind of user is the consumer** (owner, 24 November 2026): the person who consumes such a project's deliverables, above all the 3D walkthrough experience, with or without VR: the home buyer or business buyer, as well as the client who commissioned the project. Consumers are neither designers nor programmers; they walk, look, compare the options offered and choose, through the client viewer (D22). |
| D29 | **A message bus between Parti and the applications** (owner, 24 November 2026). Everything Parti holds (rooms, surfaces, openings, regions, steps, zones, placements, parts) must be referenceable from SolidCraft, Blender and Unreal Engine, and their state changes are part of the domain's event model. **References:** every element keeps Parti's declared id (D19, PRD-domain §2.2), and each application's translator attaches it to the application's own objects (a CAD body's attribute, a Blender custom property, an Unreal actor tag), so a reference resolves in both directions without searching by name. **The bus:** the domain's events are published on a message bus; per application, a **connector** subscribes and applies the changes it can apply deterministically (a placement changed → the material on the tagged faces; a setting changed → the light), with no agent and no tokens; events from the applications (a pick, a CAD revision, a body moved) come back through the same connectors as commands, validated by the domain. **Two routes, combined:** deterministic propagation goes over the bus, for speed and zero tokens; work that needs judgment (a correction, new geometry, a fault to locate) goes through the harness's agent loop and the applications' MCP servers (D21). Both see the same events. **Where the bus runs:** in 0.1.0 the gateway's fan-out over WebSocket is the bus (§6 of the architecture); later, Nai's event and data processing converts and dispatches the state changes between the applications (D9's operations layer). The goal is fewer tokens and more speed. |
| D30 | **Project types and templates; quantities across all the trades** (owner, 24 November 2026). The quantities module and its engine are the basis of the bills of materials for every product layer (D17): construction, interior and exterior finishes, lighting, furnishing, plumbing, appliances and so on, and so of project estimates (prices later). **Project types:** a project is residential or commercial, each with sub-types (residential: single-family home, apartment block, …; commercial: likewise). What varies between types is which layers (and so which bills of materials) are present, and a **project template** that informs the agentic workflow: the workflow definition's phases and steps (D26), the layers, the catalogues and default rules, the gates. **Configuration-driven:** the template is data, chosen and written when `parti-axi init` scaffolds the project, and adaptable by the project agent afterwards. Parti ships templates per type; 0.1.0 ships one (residential, single-family home, finishes layer only). |

## 4. Functional requirements

### 4.1 Catalogue

- **FR-CAT-1** A finish has: id, maker, name, series, set, role in a set, the finishes it pairs with, maker's code and product address, zone (bathroom, interior, outdoor), surfaces it suits (wall, floor), size in millimetres, thickness, finish name and class (gloss, satin, matt, rustic), body, colour description (dominant colour, accent, palette, strength, lightness, warm or cool, visual texture), and its images (face, room photo, thumbnail). The JohnnyHouse tile record is the first source; see `DN-first-consumer-johnnyhouse.md`.
- **FR-CAT-2** The catalogue answers filter queries on: zone, surface, maker, main colour, colour strength, lightness, warm or cool, pattern, finish class, role in a set, size; plus free-text search on name, series and code; sorted (at least) round the colour wheel.
- **FR-CAT-3** For a chosen finish the catalogue returns what goes with it: the maker's set and the pairs, and finishes of complementary colour.
- **FR-CAT-4** Each maker's feed (and each target project's own records) is translated into the catalogue's finish by its own translation layer. Maker terms do not appear in the domain.
- **FR-CAT-5** Finishes come in kinds: tile, wood veneer, laminate, paint, metal, exposed, glaze (in 0.1.0, owner, 23 November 2026; JohnnyHouse #1648). A wood veneer or laminate is a source scan plus its stain, with its source and licence; a paint is a colour and a sheen; a metal is a treatment, a colour, metallic and roughness (PRD-domain §4.1).
- **FR-CAT-6** A finish can be valid for a surface or not (a wall-only tile on a floor is refused). The rule lives in the domain.

### 4.2 Building: surfaces and zones

- **FR-MOD-1** A target project declares its rooms and its surfaces (the declaration format: `PRD-domain.md` §2.4), each with a stable id, a kind (wall, floor, feature), its room, and its size. (The building's labelled elements and their 3D and 2D references, D17, and ids that stay stable across CAD revisions, D19, are detailed in the domain PRD.)
- **FR-MOD-2** A surface is divided into zones by numbers: wall bands by height and rectangles; floor field, border inset and rectangles. Zones on one surface do not overlap.
- **FR-MOD-3** The user can define, resize and remove zones from the interface (drag a band height, draw a rectangle).

### 4.3 Design

- **FR-DES-1** Commands: define zone, resize zone, remove zone, place a finish on a zone, clear a zone, save a scheme, apply a scheme. Each either produces events or is refused with a stated reason.
- **FR-DES-2** A placement carries: finish id, laying pattern, grout width and colour, offset, rotation.
- **FR-DES-3** A design is saved to a file and loaded again, giving the same scene. The file can be carried to other tools (for JohnnyHouse: replayed in Blender for stills).
- **FR-DES-4** Undo and redo of design changes within a session.
- **FR-DES-5** A shortlist: finishes the user has set aside, each with a note saying where it is meant to go.

### 4.4 Selection

- **FR-SEL-1** Pick the surface under the crosshair, then the zone under the cursor within it. What is selected is highlighted in the scene and shown in the page.
- **FR-SEL-2** Wider picks: all walls of this room; all floors of this room; every zone carrying the same finish.
- **FR-SEL-3** Selection made in the scene appears in the page, and selection made in the page appears in the scene.

### 4.5 Setting (world builder, D18)

- **FR-PRE-1** Time of day: the sun position through the day for a given date and place, and interior lights at night.
- **FR-PRE-2** Weather scenarios: clear, overcast and rain at the least.
- **FR-PRE-3** These are set from the page through the same shared state as the design.

### 4.6 Shared state

- **FR-STA-1** What is selected, what finish is on each zone, and the scene settings are the same data in the page and in the scene, kept in step without the user doing anything.
- **FR-STA-2** Either side can request a change; the result reaches both.
- **FR-STA-3** A page or a scene that connects late, or reconnects, receives the current state and continues.

### 4.7 Scene adapters

- **FR-SCN-1** A **mock scene** adapter, in this repository, that implements the scene side of the message schema without Unreal (a simple 2D or 3D drawing of surfaces and zones in a browser is enough). It is the test partner for the page and the gateway, and it is what makes a release possible before the C++ plugin exists.
- **FR-SCN-2** The **Unreal plugin** (deferred, D5): connects to the gateway; reports surfaces; does the crosshair pick; draws zones through one master material per surface (face texture, true tile size in world space from the size in millimetres, grout, laying pattern, shine from the finish class); applies placements; applies the setting; shows the page as an overlay.
- **FR-SCN-3** Finishes reach Unreal as assets (D6, D7): the core catalogue through Unreal's import pipeline as textures, material instances and one finish data asset per finish, with the filter fields as Asset Registry tags; run-time finishes created from files using the same master material.

## 5. Quality requirements

- **NFR-1 Pure domain.** Each context's rules are plain functions over plain data: `decide(state, command) → events` and `evolve(state, event) → state`, keyed by aggregate id. No classes holding hidden state, no library, file, socket, Unreal, browser, Nai or EntityStore calls inside the domain. This is the part that migrates unchanged (D9).
- **NFR-2 Written for the later backends from the start.** Commands are safe to repeat. Every change is an event with an identifier and a sequence number per aggregate. State is rebuilt from events. Changes carry an expected version and are refused when it is stale.
- **NFR-3 Boundaries.** Contexts refer to one another by identifier only and exchange published events. No context reads another's storage.
- **NFR-4 Anti-corruption layers.** One translator each for: the scene (Unreal objects and assets), the page (controls and view state), each maker's feed, local files, and later Nai and EntityStore. Outside terms never appear inside the domain.
- **NFR-5 Ports named in domain terms:** catalogue store, design store, session channel, asset delivery. Version one supplies local adapters (files, a local connection). Later adapters (EntityStore for records; Nai for pipelines, session traffic and embeddings) replace them without changing the domain, the page or the scene adapter.
- **NFR-6 One published language.** The message schema is defined once, versioned, and is the only thing the page, the gateway and the scene adapters share. TypeScript types are generated from it now; C++ types when the plugin starts; Rust or Avro types when the backends join.
- **NFR-7 One transport (confirmed by the owner, 23 November 2026).** WebSocket, carrying JSON messages, is the protocol for interaction between the frontend and the backend wherever they cross a network or process boundary: overlay, VR panel, external browser, streamed picture, and later Nai's connectors. The embedded browser only displays the page; it is not the bridge.
- **NFR-8 Local only in version one.** Every server Parti starts binds to 127.0.0.1. Input from the page and from scene adapters is validated against the schema before it reaches the domain.
- **NFR-9 Platforms.** Everything in this repository runs on Linux (D2). The client-side parts (page, `parti-axi`, the scene adapter and later the Unreal plugin) use only technologies that also run on Windows and avoid Linux-only assumptions in their code (paths, shells, process handling), so a later Windows port is possible without redesign. The backend, server-side parts need not be portable. A container image (and WSL2) is the route for Windows users before any native port.
- **NFR-10 Reusable.** Nothing specific to JohnnyHouse in this repository's code. JohnnyHouse data enters only through the target project's configuration (§8) and through test fixtures clearly marked as such. The repository is public (D20), so its test fixtures are synthetic (generated records, plain swatches), never makers' images or the target project's data; real data is used only locally, read in place from the target project (owner, 23 November 2026).
- **NFR-11 Responsiveness.** A click in the page should show in the scene without a delay the user notices. A figure is to be set after the first measurement (open, §12).

## 6. Bounded contexts (proposed)

Revised in the architecture review (22 November 2026, D17, D18); names from `DN-ubiquitous-language.md`.

| Context | Owns | Notes |
|---|---|---|
| Workflow | Steps, checks, gates, checkpoints; a target project's progress | Frames the other contexts. |
| Building | Levels, rooms, elements, surfaces; each element's 3D and 2D references | Supplied by the target project. Was "Model". |
| Design (core) | Layer planning: per layer a plan of zones and placements; schemes; shortlist | The finishes layer first. Rules: zones do not overlap; a product is valid for where it is placed. Refers to Catalogue and Building by id. |
| Catalogue | Products of every layer, makers, sets, matching facts, queries | One translator per maker feed. Was finishes only. |
| Quantities | Quantities per plan; bills of materials per work-contract role; cost estimates later | New (D17): a computational module. |
| World builder | Scenarios, setting, moving parts, experience modes, routes | A module (D18). Was "Presentation" (scene settings). |
| Session | Participants (users and agents), selection, viewpoint | One user now; several later (D3, D16). |
| Asset delivery | Turning a product into something a scene can draw | Built-in assets or run-time creation. |
| Identity | Users and access | Service stage only. Out of scope for version one. |

The page, the gateway's connections and the scene adapters are adapters, not contexts.

## 7. Components in this repository

| Component | Stack | Role |
|---|---|---|
| Message schema | schema files, generated TypeScript | The published language (NFR-6). |
| Domain | TypeScript | Pure rules per context (NFR-1). |
| Gateway | Bun | Local server: serves the page, holds the WebSocket connections of the page and the scene adapter, runs the domain, uses the ports. |
| Local adapters | TypeScript | Catalogue from files, designs to a file. |
| Page | TypeScript, VanJS | Catalogue browser, finish detail, shortlist, zone editing, setting controls. Prior art: the JohnnyHouse tile browser (see the consumer note). |
| Mock scene | TypeScript | FR-SCN-1. |
| Installer and agent CLI | Python (run as a `uv` tool) | §8, including the agent session (FR-AXI-8) and the Pi plugin (FR-AXI-9). |
| `parti` library (SDK, D27) | Python, LGPL-3.0-only | The library every target project imports: workflow, harness, catalogue tools, pipeline tools, application translators. The three rows below are its modules. |
| Catalogue tools (module of `parti`) | Python | Build a catalogue from a target project's finish records and images (thumbnails, colour tags); later, the Unreal editor scripts that import finishes (Unreal's Python runs in the editor only). |
| Agent harness (module of `parti`) | Python | D21: the workflow graph (LangGraph) built from the domain's Workflow definition, Parti's agent definitions and skills, and MCP client connections to SolidCraft, Blender and Unreal. Reaches the domain through the agent API. |
| Pipeline tools (module of `parti`) | Python | The workflow's toolbase (§8A): data tables to commands for the CAD and rendering applications, with expected-result checks. |
| Client viewer | Unreal (packaged app) | After 1.0.0 (D22, D23): the self-contained walkthrough viewer, packaged per platform with a client bundle. |
| Unreal plugin | C++ | Deferred (D5). Also the Unreal side of the world builder (D18). |

## 8. Installer and agent interface (D12)

Parti must be installable and operable by an AI agent with no human at the keyboard. The model is `modelb-axi`
(`/home/antonyj/.local/bin/modelb-axi`, run `modelb-axi --help` and `modelb-axi init --help`) and `crucible-axi`:
one command-line entry point, structured output an agent can read, a dry run, and a flag for every question.
The working name is `parti-axi`.

- **FR-AXI-1 Install.** Parti installs as a tool on the machine from a release of this repository (for the Python part, in the way `uv tool install` installs `modelb-axi`), bringing the gateway, the page and the catalogue tools with it.
- **FR-AXI-2 Scaffold into a target project.** `parti-axi init --target <dir>` writes, inside the target project: a Parti configuration file (where the finish records and images are, where the model's surfaces are declared, where designs are saved, where the Unreal project is, the port), and the notes or skill an agent needs to use Parti there. It reports what it wrote and what the consumer still has to do. `--dry-run` writes nothing. It never overwrites a hand-edited file without being told to.
- **FR-AXI-3 Every setup question has a flag**, and `--yes` runs without reading the keyboard. A missing required value is an error that names the flag.
- **FR-AXI-4 Structured results.** Every command prints a machine-readable result (what was done, warnings, what remains) and uses exit codes an agent can rely on.
- **FR-AXI-5 Operate.** Commands to: build or refresh the catalogue from the target project's records; start and stop the gateway; report health and versions (a "doctor"); read the current design and state; send a command (for example, assign a finish to a zone) and see the events or the refusal. An agent must be able to do through the CLI what a person does through the page.
- **FR-AXI-6 Upgrade and removal.** Re-running the scaffold after a Parti upgrade refreshes the files Parti manages and leaves the consumer's own files alone. Removal lists what it would delete and asks first.
- **FR-AXI-7 Unreal hook-up (when the plugin exists).** The scaffold adds the Parti plugin to the target's Unreal project. How (an `AdditionalPluginDirectories` entry in the `.uproject`, or a copy into `Plugins/`) is open and must be checked on Unreal 5.9.

- **FR-AXI-8 Agent session (D16).** `parti-axi` joins a running session as a participant. It reads the current selection, design and scene settings. `watch` waits until the user acts, then returns the events, in the way `lavish-axi poll` does. Commands work as in FR-AXI-5. The gateway serves this through an agent API that is local only (NFR-8), uses the same schema, and runs commands through the same `decide` path as the page.
- **FR-AXI-9 Pi plugin (D16).** A Pi extension turns `watch` into a wake-up for the agent's session, so the agent reacts to the user's actions without polling by hand. Plugins for other harnesses may follow.

The first consumer's needs and data are in `DN-first-consumer-johnnyhouse.md`.

## 8A. Guided workflow and toolbase (D14)

The prototype's pipeline, its tools, its scripts and what went wrong are described in
`DN-pipeline-prototype-johnnyhouse.md`. The requirements below state what Parti must offer; which pipeline
steps are taken up first, and in which release, is the roadmap's (D23), approved by the owner.

**The shape (D26):** the thirteen rows below are the prototype's sequence. In the repeatable graph they group into seven
phases: Intake (1), Model (2 to 5), Declare (the declaration files), Design (8, 9), Present (6, 7, 10, 11), World (12) and
Deliver (13, and the print split); each row's work is a run of steps of the twelve kinds, every step running the step
cycle, with the correction and audit loops across all of them (`DN-workflow-shape.md`).

- **FR-WF-1 Steps.** (Restated by D26: the workflow is phases of steps, each step an instance of a step kind; the list that follows is the prototype's.) The pipeline is a sequence of named steps (in the prototype: drawing intake; parametric shell build; openings and joinery; merge for render; CAD to Blender; reference materials; site and planting; interior furnishing; stills and lighting; movie production; print split; Unreal export). Each step states its inputs, its outputs, the numeric checks that prove it worked, and the owner review gate that follows it, if any.
- **FR-WF-2 Guided.** For a target project, an agent can ask Parti: which step am I on, what does it need, what must I check, what is next. Parti records what was done (one line per step: what changed, how it was checked, what was produced) in the target project.
- **FR-WF-3 Data, not hand-typed commands.** Geometry and scene content live in data tables in the target project; Parti's tools turn data into commands for the CAD and rendering applications. A correction is made in the data and regenerated.
- **FR-WF-4 Checks are part of the tool.** Each tool prints the expected result (for example volume and bounding box after a CAD stage) and compares it with what the application reports. A step is not complete on "ok" alone.
- **FR-WF-5 Checkpoints.** Each step ends in a saved checkpoint that can be returned to.
- **FR-WF-6 Applications stay outside.** The CAD application, Blender and Unreal are driven through their own agent interfaces (in the prototype: the SolidCraft, Blender and Unreal MCP servers, and a PDF reader). Each sits behind its own translation layer in Parti, so a tool's logic does not depend on one application's commands. Parti does not bundle these applications.
- **FR-WF-7 Caveats travel with the step.** The faults found in the prototype (the DN lists them) are carried as checks or warnings in the step they belong to, not left in a document.
- **FR-WF-8 Agent-facing form.** The workflow reaches an agent the same way the rest of Parti does (§8): through the scaffold (notes or skills written into the target project) and through `parti-axi` commands with structured results.
- **FR-WF-9 Owner in the loop.** Where taste decides, the tool produces options to show (rendered views, boards), and the step waits for the owner's choice. Every change to materials, furniture or lighting is shown as a rendered view before the step moves on.
**The workflow outline** (approved by the owner, 23 November 2026; derived from the JohnnyHouse runbook with that project's
corrections, Sandesh #1633). The domain PRD's Workflow definition turns it into data. JohnnyHouse's candidate skills are
sub-steps of these steps.

| # | Step | Owner gate |
|---|---|---|
| 1 | Drawing intake: sheets, calibration, levels, grid, schedules, construction standards. Every view of an element is read before it is built. | Plan accuracy |
| 2 | Parametric shell: massing, structure, walls, openings, stairs | Massing |
| 3 | Facade and joinery | Facade |
| 4 | Fitted interior: cabinets, kitchen, sanitary fixtures | — |
| 5 | CAD ready for export: merge and overlap check, re-run after every CAD correction | The owner closes the CAD |
| 6 | CAD to Blender, including re-import that keeps materials, lighting and the moving-parts rig | — |
| 7 | Scene (Blender): reference cameras first, then materials, lighting, site, planting, furniture, for stills and films | A rendered view after every visual change |
| 8 | Finish catalogue: makers' ranges, classification, boards, shortlist | The owner shortlists |
| 9 | Interior finishes (the finish tool) | The owner chooses finishes |
| 10 | Stills: quick, repeated after every change | — |
| 11 | Films: hours of rendering, only once the scene is frozen | Route and test frames first |
| 12 | Unreal export (building and furniture only) and world building: site and planting built in Unreal from Unreal's own assets (T4); the building located on the map and the rendered surroundings' extent chosen (D24) | Extent of the surroundings |
| 13 | Building and packaging the client viewer (D22) | — |
| side | Print split: a 3D-printed scale model, branching from step 5. A future function, not in 1.0.0 (owner, 23 November 2026). | Test print |

Rules across every step: one checkpoint per feature group, with a numeric check and a log line; a checkpoint before any
risky batch (long runs crashed both CAD and Blender); Blender scene checkpoints are defined by Parti (the prototype kept
log rows only).

**Finishes are chosen once, in the design** (owner, 23 November 2026): Blender and Unreal are two renderers of the same
design, so the order of steps 9 and 12 does not affect the data. Before the Unreal plugin exists, finishes are chosen in
the page against the mock scene, and Blender replays the saved design for stills. A design change (for example a
scheme, a set of finishes, applied across many zones) is a new design revision that follows D19's forward chain:
quantities are recomputed at once; the Unreal scene updates live where it is connected; affected stills, films and the
client bundle are marked stale and their re-rendering or republishing is raised as follow-up actions, films (hours of
rendering) behind an owner gate. **World editing is a separate chain:** the world (site, lighting, scenarios, moving
parts) is built in the Unreal editor, with Parti collaborating through Unreal's MCP (D18, D21); how edits made directly
in the editor reach Parti is for the world builder's PRD.

**Evidence for step 12: the prototype's Runbook P12** (JohnnyHouse #1660, RUNBOOK v0.3, read in place). The owner's
intent: JohnnyHouse is the prototype on which this workflow is being found, so that Parti's own harness with an embedded
workflow (D21) can cut the agent's token use for any architectural project. P12 gives step 12 as eleven sub-steps in
the order that worked: building in; materials lost on import rebuilt from the catalogue by rule; moving sub-assemblies
as Blueprints; moving bodies that are not sub-assemblies (cabinet fronts, gates), motion inferred; activation at the
handle; finishes by rule, recorded with where they are used; tiles set out room by room, with counts; face patches;
site corrections; collision; and faults found in the walkthrough sent back to CAD and returned as a patch of the
changed bodies. What the workflow system takes from it, to be designed with the workflow's and the world builder's
PRDs:
- **Invalidation edges:** sub-steps that live only in the world (materials, finishes, setting-out, face patches) are
  made stale by a new building import and replayed (the glossary's Stale and Follow-up action).
- **A check per step, as a built-in gate:** every body on its counterpart; swing and slide measured; open-and-return; no
  material lost; a door between two different rooms; layer area equals room area; a ball stopped by walls and shut
  doors; the level unsaved before a save and not after.
- **The owner's gate:** scripted checks prove position and motion, not feel: every moving element is tried by the
  owner in play; taste decisions are put as options. The owner's decisions were of four kinds: pointing at a fault,
  choosing among options, giving a rule, choosing from the catalogue.
- **The loop:** owner points (a screenshot) → resolve the pointer to elements → find the cause in numbers → scripted
  fix with a table of what it touches → check by measurement → say what was not checked → owner tries it → one log
  row. **Resolving the owner's pointer** was the largest recurring cost and the cause of two wrong fixes: a step of its
  own at the head of the loop (D24's resolve-by-embeddings, Q17's interaction capture).
- **Standard caveats per step** ("saved; not tried in play; lives in Unreal, re-run after import"), attached to the step
  instead of written out each time; and the Unreal caveats (RUNBOOK §4) carried by the harness.
- **Seeds:** the script index by subsystem (§3.2; the `bp_*.dsl` graphs act on tags only and are the first motion
  primitives, D18), the tile browser's gaps as an asset browser (§3.1: a target per choice, every kind of asset,
  library search with licence, choosing inside the walkthrough), and seven skill candidates (§6).

- **FR-WF-11 Corrections are first-class (D26).** A correction of a done step is recorded with its trigger, the pointer and the elements it resolved to, the cause in numbers, the fix (with what it touched), its checks, and the step it lands in; its revision flows forward (D19).
- **FR-WF-12 Check results say what was not checked (D26).** Every check result is pass or fail with the measured values and the worst offender, and names what it did not prove (play mode, other instances, the lit view).
- **FR-WF-13 Gate kinds (D26).** Review, option, permission (a download, a long render, a print) and trial (the owner tries what scripts cannot prove).
- **FR-WF-14 The pointer is resolved first (D26).** When the owner points at something (a view, a selection, words, a picture), the elements meant are found and confirmed before anything changes (D24, Q17).
- **FR-WF-15 To-dos within a step (D22).** A step run carries short to-dos, added by the user or the agent, each open or done; they are recorded in the workflow run, shown with their step, and listed when the step is completed.
- **FR-WF-10 Nothing of one house in the tools.** Names, dimensions and material choices of JohnnyHouse are data of that target project (NFR-10).

## 9. Stages and what a release means

The owner's instruction: this project's orchestrator runs it independently to a release; the tool is then
installed and used inside JohnnyHouse.

| Stage | Contents | Depends on |
|---|---|---|
| A. First release (Bun and Python only) | Message schema; domain (Building, Design, Catalogue, Session; the setting held as state); gateway; local adapters; page; mock scene; installer and agent CLI; catalogue tools. Demonstrated end to end on JohnnyHouse data with the mock scene: browse, filter, select a surface and a zone, define zones, place finishes, save, reload, set time of day and weather (as state), all through the page and through the CLI. | Nothing outside this repository. |
| B. Unreal | C++ plugin (FR-SCN-2, FR-SCN-3), overlay, finish assets, the three trials of §11; the world builder (D18), detailed in its own PRD. | Model B support for a C++ stack. |
| C. VR panel | The page as an interactive surface in the 3D scene; with B, the basis of the client viewer (D22). | B. |
| D. Data service | Catalogue, users, saved designs served to installed apps; EntityStore as system of record; Nai for pipelines, sessions and embeddings (RAG and the knowledge base reach Nai earlier, with the agent harness, D9). | Requests to the Nai team (see the founding record). Taken on with the multi-user, multi-session implementation (D9). |
| E. Streamed Unreal | Unreal running on servers, shown in a browser, with the same page around it. | D. |

Which CRs make up Stage A, and their order, is the orchestrator's proposal to the owner at wave-open; it is not
written here. **Releases (D23):** 1.0.0 is the full designer edition; the 0.x minor releases lead to it, the first
being 0.1.0. The client viewer (D22) comes after 1.0.0. Stages and releases are not the same thing: a 0.x release carries whatever
slice of the stages the roadmap assigns it, and 1.0.0 needs the full designer workflow through the Unreal walkthrough. The release label and date are the owner's call.

## 10. Out of scope for the first release

- The C++ Unreal plugin and anything that needs it (deferred, not dropped).
- Nai, EntityStore, users, access control, several users on one design.
- Relief and gloss maps for tiles (the images available are makers' web pictures of one tile face).
- Moving parts of the building (doors, drawers, gate, louvres) and walking controls in the first release; the world builder holds them later (D18).
- Print split (a 3D-printed scale model): a future function, not in 1.0.0.
- An MCP server for Parti (D21: Parti serves none). The in-page chat is no longer out of scope: it is the designer edition's guided chat (D22), arriving with the harness.

## 11. Trials owed before or during Stage B

- **T1** Unreal's built-in browser widget as an overlay in a packaged 5.9 build, on Linux (Windows later, D2), showing a page served from a local address. Reports (unverified on 5.9) say it long shipped an old Chromium, and that in packaged Linux builds it loaded web addresses but not local files. Outcome decides D13. This trial needs no C++ and can be run by the first consumer in the JohnnyHouse Unreal project at any time. It now also decides how the client viewer's in-world panel loads the page from its bundle (D22): through Unreal's browser from local files, or a small local web server inside the viewer.
- **T2** A WebSocket connection between a C++ plugin and the gateway, exchanging the state.
- **T3** Finish assets: Asset Registry tag queries in a packaged build (which tags survive packaging), thumbnails in a packaged build, and a finish created at run time from a file.
- **T4** Importing the building into Unreal 5.9, run with JohnnyHouse, which reports on Sandesh (thread #1635). Its trial
  experience comes before any Unreal-export CR. **Findings so far** (JohnnyHouse #1637, #1638, 23 November 2026, Unreal 5.9.0
  preview on Linux; measured unless marked):
  - *Format:* Blender → glTF binary → Interchange works for geometry, scale, axes and material slots (first done on 17
    November, repeated with the CP-123 model: 2,387 meshes, 2.55 million polygons, 67 MB). FBX, USD and Datasmith are untried.
  - *What travels:* only the building and its furniture go from Blender to Unreal. Site and planting are built in Unreal
    from Unreal's own assets, which are dynamic where Blender's are static (owner's judgement); creepers are not converted.
  - *Names:* actor labels are the CAD body names and survive; mesh asset names do not (1,107 arrived suffixed `_001`).
    Between two CAD revisions 360 names were kept, 140 vanished and 2,041 were new, so a name is not a stable id even when
    nothing goes wrong (confirms `PRD-domain.md` §2.2): an id must hang on the actor, through Parti's declared ids.
  - *Re-import:* re-importing the Interchange scene asset updated the assets but **deleted every building actor and
    spawned none, with no error**; a fresh scene import placed the building, and returned `False` although it succeeded.
    Unreal-side work outside the building (site, planting) survived untouched; work on the building (swapped materials)
    did not, and was re-applied by script. The old mesh assets stay behind as orphans. Lesson for the tool: snapshot the
    level before and after and compare; keep everything done to the building in scripts or data that can be re-applied;
    never hand-edit imported building actors. Re-import is a first-class operation for Unreal as for Blender (the first
    import was a look-ahead before the CAD was closed, and went stale).
  - *Moving parts:* nothing carries over (no rig in Blender; every pivot at the world origin); pivots must come from the
    hinge and track positions.
  - *STEP (#1639):* Interchange in 5.9 has no STEP translator. Datasmith's CAD modules load on Linux, but translating a
    1.7 MB STEP of one louvre window (122 bodies) crashed the editor (segmentation fault in the CAD kernel's sew-and-mesh),
    one attempt with default options. **Do not plan on STEP into Unreal on Linux.**
  - *Per-part glTF from the CAD tool (#1639, to be tried):* SolidCraft writes glTF binary itself, per part file, each body a
    named node, cleanly indexed (blades, pivots, links, worm, crank), whereas in the whole-building export the same parts
    lose which window or blade they belong to. Direction under consideration (owner): each **moving sub-assembly**
    (louvre window, sliding door, hinged door, French window, skylight vent, garage gate) is imported once as its own
    Unreal component, inspected and operated on its own, then placed in the building from the CAD generators' placement
    tables, with its kinematics (blade pitch and pivots, worm ratio, sliding travel) from the same generators. This bears
    on the world builder's moving parts (D18) and its PRD.
  - *A sub-assembly as its own Unreal component: works, in trial form (#1640, measured).* The demonstration louvre
    window, written to glTF binary by SolidCraft and imported through Interchange **as assets**, arrived as 122 meshes in
    the part's own frame, correctly sized, names kept (`" (7)"` becoming `__7_`). A **motion table**
    (`<part>.kin.json`), computed from the same generators that build the part, groups the bodies as hinges (axis point,
    axis direction, ratio to the input) or pin-followers, all driven by one input (blade angle 0 to 90 degrees, 5 crank
    turns). A script assembles one pivot per group and sets the input; the pivots match the imported positions and the
    blades and tilt bar move as one mechanism at 0, 35 and 90 degrees. Lessons for Parti's tools: per-part import keeps
    the indexing the whole-building export loses; the motion data belongs with the CAD generator, never measured in
    Unreal; the frame change is fixed (part mm x, y, z to Unreal cm x/10, -y/10, z/10) and the sign of a turn is settled
    once by measurement; check motion with box centres, not bounds; merge the one-material-instance-per-body that
    Interchange creates. Not yet done: placement at the ten windows, and leaving the sub-assemblies out of the building
    export so they do not arrive twice.
  - *The sub-assembly as a Blueprint, built by script from the motion table (#1645, measured).* One scene component per
    moving group at its axis point, tagged by role (`hinge:blade`, `hinge:worm`, `follow:bar`), with the group's meshes
    under it; the graph is written in the editor's Blueprint graph language: one function `Apply` driven by one variable
    (the blade angle), called from the construction script and at begin play; hold E to close, Q to open, within
    reach. At 0, 35 and 90 degrees the mechanism keeps the loose-actor trial's numbers. Key press in play not yet
    tested. Lessons for Parti's tools: the motion table is enough to build the interactive actor without hand work,
    which is D18's purpose. **Working rule for experimental editor tools** (adopted by JohnnyHouse with the owner, after
    an editor crash when a graph referred to variables added in the same session before a compile): save before each
    step; compile before referring to new members; one small step per call; never retry a crashed call unchanged.
    The graph tool's errors are precise and transactional; after an editor crash the connector's port stays held for a
    minute or more, so the agent waits before reconnecting.
  - *The per-part route repeated by script for three more parts and eight placements (#1649, measured).* The CAD tool
    writes each part to glTF; the generator writes its motion table and a **placements file** (part, origin in building
    millimetres, turn about the vertical); the Unreal scripts import the part, build its Blueprint, write its graph,
    match materials, put the chosen finishes on it, spawn it at each placement and hide the loose bodies of the
    whole-building import. At all eight windows the Blueprint and the old loose frame coincide (0.0 cm apart, same
    size); 1,358 loose bodies are now four Blueprints. Lessons for Parti's tools: a placement is an origin plus a turn
    about the vertical, into Unreal (x/10, -y/10, (z + lift)/10) with yaw = minus the turn (D25's declared transform);
    a part type placed several times needs the loose bodies of every placement hidden, and the building export should
    leave them out; two mechanisms in one frame are one table with prefixed group ids; editor tools fail quietly while
    play mode runs, so a tool checks for it first; and **finishes set on the building import's meshes are lost at the
    next import and must be re-applied by rule**, whereas finishes on a part travel with it: the case for the design
    holding the finishes and each renderer applying them (D17, PRD-domain §3).
  - *What the Blender-to-Unreal export loses in materials (#1653, measured; T4 item 2).* Of 49 imported materials in
    use, six arrived plain white with no image, with no warning in the import log: every material whose colour Blender
    makes with nodes (noise, wave, grid): three feature-wall effect paints, a marble-look tile, an oak laminate (127
    cabinet slots), a timber. Values and images survive; node graphs never do. A tool therefore needs a **check after
    import** (a material in use whose base colour is white with no image is a loss) and a **decision per loss**: bake to
    images in Blender (needs UVs, which CAD meshes lack) or rebuild in the target from a recipe or the catalogue finish;
    JohnnyHouse rebuilt the effect paints in Unreal from the Blender recipe (an approximation: the engines' noises
    differ). For Parti: finishes are rebuilt in each renderer from the catalogue (PRD-domain §4.1), never carried
    through an export. Item 7 trap: a material node connected by a wrong pin name fails silently (the call returns
    false); the check is in the picture, not in any error, so editor tools verify results visually or by query.
  - *Doors and French windows as Blueprints (#1655, measured):* eight more part files, 16 placements; with the louvres,
    12 Blueprints at 24 positions, built and placed by script. A motion table has a mechanism (louvre, door) and groups
    of three kinds (hinge, pin-follow, slide); one graph per mechanism acts on tags. A placement carries what differs
    per instance (a hinged door's swing). Proven by comparing every body with the whole-building import (0.0 cm at all
    16; handles and leaves are not symmetric, so position, turn and hand are settled in one test), opening each door
    and measuring the leaf's travel, and moving each slide. Trap: changing an instance setting rebuilds the actor, so
    an earlier component reference reports the old pose. **Owner's note:** placement and asset metadata kept as JSON
    object references with words ("north jamb, opens west into the bedroom") is what Parti's future semantic search
    over asset classes and placements works on (D24), instead of browsing the model.
  - *What cost an agent the most tokens, and the agent API wanted (#1656, #1657; JohnnyHouse DN-010, recorded as
    evidence, owner, 24 November 2026):* answer questions instead of making the agent browse; summaries by default
    with filter, fields and limit, long output to a file; verification as one call returning pass or fail and the worst
    offenders; numbers before pictures; working state kept on the tool's side and each system's transform owned by
    the tool (D25); fail loudly with a named reason and report what was done in numbers; operations by rule with a
    selector and a dry run; learned facts kept with their asset or operation (FR-WF-7); one stable id per element
    (D19). Proposed verbs: find, describe, apply, check, diff, status, look. To be weighed when the agent harness and
    the world builder's agent interface are specified.
  - *Setting-out and quantities (#1658, measured):* 18 tiled rooms, 197.5 m²; the setting-out is per placement, and the
    count needs each room's exact outline (a check: every door has a different room on each side). Taken into 0.1.0
    (PRD-domain §3.3, §3.4a).
  - *Finishes as Unreal assets (T3, first part):* a master material lays a tile at true size in world space from an origin,
    with grout and roughness from the finish class; one instance per tile. It works on two walls of first-floor bath 1, and
    shows that a shared wall body is also tiled on the next room's face: per-face placement needs the face rectangles as
    material parameters or per-face material slots (for the Unreal plugin's PRD).
  - JohnnyHouse's prototype scripts are shared with Parti as prototypes for its generic tools (owner):
    `blender/scripts/johnny_export_ue.py`, `unreal/scripts/jh_reimport.py`, `jh_tiles.py`, `jh_materials.py`, `jh_site.py`,
    `jh_flora.py`, `jh_plants.py`, `jh_creepers.py`.

## 12. Open questions

1. **Scene bridge before the C++ plugin exists.** Could a stop-gap (for example Unreal's Remote Control interface or editor Python, driven by the gateway) let JohnnyHouse see finishes in the Unreal editor during Stage A? Not examined; unverified on 5.9. Owner to say whether it is wanted. **Owner:** the Unreal route for the designer edition (Python API and MCP through the LangChain SDK, or the C++ plugin, D5) is decided before 1.0.0.
2. **Where Unreal assets are made.** FR-SCN-3 needs the Unreal editor; the orchestrator of this project has no Unreal project of its own. Proposed: the consumer runs Parti's editor scripts in its own Unreal project. **Owner:** with the agentic pipeline, the prototype's scripts that are generic enough become tooling the agent uses; which ones, and where Unreal assets are made, is concluded with JohnnyHouse while it prototypes.
3. **Windows testing.** Closed (owner, 23 November 2026): the first release is Linux only (D2); no Windows machine is needed. A later Windows port of the client side would reopen it.
4. **Variant Manager.** Proposed (D22): the client bundle realises the offer as Unreal variant sets, so the client viewer applies options without a rules engine. Also: whether saved schemes should be variant sets in the designer edition (Stage B).
5. **Responsiveness figure** for NFR-11.
6. **Service-side confirmations.** Closed (owner, 23 November 2026): NFR-7 confirmed (WebSocket for frontend-backend interaction across network boundaries) and Bun confirmed for the service side.
7. **Release targets and remote.** The scaffold recorded owner `anthill-tec` (taken from the sibling projects Crucible and Sandesh) and no release targets. The owner confirmed `anthill-tec` (22 November 2026; remote `anthill-tec/parti`, private). Release targets remain open; FR-AXI-1 implies at least one publishing target. **Release targets decided (owner, 23 November 2026):** GitHub releases, and `parti-axi` published as a package (PyPI) for the one-command install (FR-AXI-1).
8. **Name clash.** "Parti" has not been checked against existing products or package names. **Checked (23 November 2026):** `parti` and `parti-axi` are free on PyPI; `parti-axi` is free on npm, `parti` is taken there (an unrelated package), which does not matter while Parti's root package is private. "Parti" is a common architecture term (the parti, a design's organising idea), which suits the product; no product of that name was found among architecture and interior-design tools. Not a trademark search.
9. **Workflow and toolbase in the first release.** §8A arrived after the stages of §9 were drafted. Which pipeline steps become Parti tools first, and whether any of them belongs in Stage A beside the finish tool, is not decided. Proposed: Stage A stays the finish tool plus the workflow skeleton (FR-WF-1, FR-WF-2, FR-WF-8, with the steps described but their tools not yet ported); the tools are ported step by step afterwards, starting with the steps JohnnyHouse still has ahead of it (interior finishes, Unreal export, print split). The agent session (D16, FR-AXI-8, FR-AXI-9) is part of this decision, and so is the owner's current focus on the part of the workflow after the CAD model exists (D18). **Decided (owner, 23 November 2026):** 0.1.0 is the finish tool end to end with the mock scene: browse and filter, select a surface, define zones, place finishes, save and reload, set time and weather as state, all through the page and through `parti-axi`; local JSON store, no Nai. The agent session (FR-AXI-8, FR-AXI-9), the agent harness (D21) and the workflow skeleton follow in a later 0.x release.
10. **Testing tools that drive applications.** How Crucible-reported tests cover tools whose effect is inside SolidCraft, Blender or Unreal (recorded command batches compared with expected ones, or the live application) is not designed. **Answered** (owner approved, 23 November 2026): `DN-test-strategy.md`: contract tests of the generated command batches in CI, live tests against the applications on a workstation, reported to Crucible.
11. **Store per target project.** JSON files (an event log plus a snapshot), one SQLite file per target project, or SQLite as the store with JSON as the exchange format. D17 and D19 (layers, revisions, stale marks, bills of materials) ask more of the store than the first draft assumed; FR-DES-3 keeps a file other tools can read. To be decided in the domain PRD (owner, 22 November 2026). **Owner's guidance (23 November 2026):** Parti's data travels as JSON events (schema-based, like Nai's own); an SQL database will not scale for the multi-user version, which uses EntityStore instead. If Nai is used from the start, persistence is a matter of registering Nai connectors for Parti's schemas and operations. Open: whether version one uses Nai from the start (this would revise D9's "version one has no Nai"). **Decided for 0.1.0 (owner, 23 November 2026):** a JSON event log plus a snapshot file in the target project, behind the design-store port; Nai joins with the agent harness (D9, local first); EntityStore serves the multi-user version; the client viewer uses SQLite (D22).
12. **Unreal plugin under GPL v3 (D20).** The C++ plugin (D5) is built and shipped against Unreal Engine, whose own licence is not open source. Whether GPL-3.0-only code can be linked into, and distributed with, an Unreal build, or whether the plugin needs another licence or a separate process boundary, must be checked against Epic's licence before the plugin is designed (Stage B). **Urgent for the client viewer (D22):** it is distributed to clients with Unreal inside, so its licence must be settled before it is designed: for example the viewer and the Unreal plugin under another licence (the copyright holder may choose), or the viewer kept free of GPL code, talking to nothing but its bundle. **Owner's lean (owner, 23 November 2026):** a separate, less restrictive licence, perhaps MIT, for the client viewer and the Unreal plugin, while the rest of Parti stays GPL-3.0-only; the viewer then carries no GPL code.
13. **Static tooling on Nai.** Which of the static tooling usually written in Python (catalogue ingest and normalising, colour classification, image processing, geospatial preprocessing, derived views such as quantities) can be written as Nai DSL pipelines instead, and which must stay Python (the applications' own scripting, CAD operations run through the agentic workflows). To be explored with the Nai team before the catalogue and pipeline tools are built (owner, 23 November 2026).
14. **Building the client viewer per platform (D22).** Unreal cooks content per target platform, so each client bundle is built per platform. Packaging is generally done on each platform's own host: Windows builds on Windows, macOS on a Mac with Xcode; Linux can be cross-compiled from Windows, not the other way round. To check on Unreal 5.9. With a Linux-first designer edition (D2), the build and download needs per-platform build hosts or CI runners, or a build service. Decide before the viewer is designed. **Owner:** considered when the client viewer is built.
15. **Makers' terms for client bundles (D22).** Whether makers' images and product data may be redistributed to clients inside client bundles depends on each maker's terms. The owner asks the stakeholders (23 November 2026).
16. **Language of the motion library and the navigation modes (D18).** Unreal's Python runs in the editor only (the Python Editor Script Plugin; to verify on 5.9), not in a packaged application. So editor-time tools (import, assemble, place, turn a CAD motion table into an Unreal motion asset) can be Python, like the agent harness (D21) and JohnnyHouse's `jh_parts.py`; the run-time motion player (the primitives that operate parts in the walkthrough and the client viewer) must be C++ or Blueprint. Orchestrator's lean: a fixed player of primitive components written once in C++ (versioned, testable, the plugin's home, D5), each moving part only data; a Blueprint player as an interim if 1.0.0 cannot wait for Model B's C++ support. Decided with the Unreal route before 1.0.0 (Q1). The same split applies to navigation: modes at run time, navigation data prepared at editor time. **Decided (owner, 23 November 2026): C++** for the run-time motion player and navigation modes, manageable from day one and unit-testable; no Blueprint interim planned. Rust is not an option inside Unreal (no official support; Unreal's object system is C++ only; D5 already excludes it).
17. **The in-world UI and the Unreal bridge (D18, D22).** The Unreal plugin is the bridge between Parti's data and the engine: **ids** (Parti's declared ids on Unreal actors as tags, since names do not survive, T4); **picking** (a ray from controller or mouse to actor and face, mapped to Parti's surface and zone, sent as `select`); **state in** (placements as material parameters per face, the setting as weather and lighting parameters, motion inputs to the motion player); **UI** (Parti's offers, options, products and scenarios shown in the world). Open: the in-world UI's form: (a) the page (D1) in Unreal's web-browser widget as a panel (one UI; depends on T1; weaker for VR); (b) native Unreal widgets generated from Parti's data (best for VR and smart menus; a second UI); orchestrator's lean: both, the page as the flat panel, native widgets for smart menus and VR controls, fed by the same data so no rule is duplicated. Environmental effects (rain, splashes, wind on planting, wet surfaces) are Unreal's own (Niagara particles and fluids, Chaos physics, material parameters); Parti holds the setting state, drives a fixed set of engine parameters through the plugin, and gives finishes a wetness input in the finish master material. For the world builder's and the Unreal plugin's PRD. **What crosses the boundary** (orchestrator's proposal, 23 November 2026): only domain state, small and tied to a revision. Parti is the truth for domain state; Unreal for engine state (rendering, physics, per-frame transforms, particles), which never crosses. Down to Unreal: the id map (per building revision), placements with their zone rectangles, finish asset references (ids, never the assets, which travel as files), the setting (about a dozen values), motion tables, navigation data and offers (per revision or bundle), motion inputs (on interaction). Up to Parti: picks, interaction events, a throttled viewpoint (1 to 5 per second), and an **applied revision n** acknowledgement for every change, so Parti, and the agent, know what the scene shows. **How the agent knows what Unreal is doing:** at editor time through Unreal's own MCP (actors found by Parti's id tags, editor Python, screenshots; D21); at run time (walkthrough, client viewer: no editor, no editor Python or MCP in a packaged app) through the plugin's events in Parti, read with the agent API (`parti-axi watch`, D16), which is also the cheaper path in tokens. So the plugin is needed for run time; MCP covers the editor only. **Interactions for guidance and assistance** (owner, 23 November 2026): the plugin captures the user's direct interactions with the world (picks, dwell at a surface, options applied and compared, doors operated, routes walked) together with telemetry, and Parti uses them for guidance and assistance: the agent in the designer edition and the UI helper in the client viewer can suggest, explain or offer a comparison at the moment it helps. Proposed: in the client viewer capture is visible and can be switched off, the client agrees to it, and the data stays with the designer's project.

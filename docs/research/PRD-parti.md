# PRD — Parti: a guided workflow from drawings to an Unreal walkthrough

**Version:** 0.1 (draft for the owner's review)
**Date:** 2026-11-22
**Status:** DRAFT. Decisions marked "decided" are the owner's; items marked "proposed" or "open" are not yet confirmed.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)
**Builds on:** `DN-founding-design-record.md` (the discussion these requirements come from)
**Related:** `DN-first-consumer-johnnyhouse.md` (the data and the Unreal project of the first consumer), `DN-pipeline-prototype-johnnyhouse.md` (the pipeline, tools and scripts of the prototype)

## Change Control

| Date | Change |
|---|---|
| 2026-11-22 | First draft, written from the design discussion held in the JohnnyHouse project. |
| 2026-11-22 | Owner's reframing (architecture review): the guided workflow is the goal and the finish tool its first major feature. Title, §1 and D14 restated; no requirement changed. |
| 2026-11-22 | Architecture review, owner-approved: D19 (versioning, changes flow forward; breaking changes allowed and flagged); D17 adds Quantities as a computational module (cost estimates later). |
| 2026-11-22 | Architecture review, owner-approved: D16 (agents through AXI), D17 (building with layers), D18 (world builder); FR-AXI-8, FR-AXI-9; §2 replaced by the glossary `DN-ubiquitous-language.md`; §6 contexts revised; §10 and Q9 amended. |

## 1. Purpose

Parti is a guided workflow that takes a building from the architect's drawings to a CAD model, a rendered
Blender scene and an Unreal walkthrough. A user and an agent work through its steps together, and each step has
tested tools (owner, 22 November 2026).

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
| D2 | Version one runs on Linux and Windows, standalone and local, one user per session. |
| D3 | Later stages: first a data service (catalogue, users, saved designs) used by installed apps; then Unreal streamed from servers to a browser. The technology chosen now must carry through. Full collaboration (several users on one design) comes later, so the state must be designed for it now. |
| D4 | Interface and service code: TypeScript on Bun. VanJS renders the page. |
| D5 | The Unreal side is a full C++ plugin. No Rust inside Unreal. **The C++ plugin is deferred** until Model B supports a C++ stack; until then this repository is Bun and Python only (see §9). |
| D6 | Finishes are Unreal assets when applied. A core catalogue is built into the app as Unreal assets; further finishes are created at run time from files, behind the same catalogue interface. |
| D7 | The interface works with Unreal's own asset management (Interchange import, primary data assets, Asset Registry, Asset Manager). It does not run a parallel catalogue beside it inside the app. |
| D8 | Domain-Driven Design, with domain boundaries and anti-corruption layers, so the same business logic can later move onto other backends. |
| D9 | Version one has no Nai and no EntityStore. Later the backend migrates to Nai (pipelines in the Nai DSL, connectors, a custom provider if required) and EntityStore. Both are the owner's own projects. |
| D10 | The pure domain logic is TypeScript, run by Bun. |
| D11 | Parti has its own repository (this one), its own orchestrator registered on Sandesh, and is dog-fooded with JohnnyHouse data. |
| D12 | Parti ships its own scaffold installer, in the manner of `modelb-axi`, so that an AI agent can install it into a target project and work with it (see §8). |
| D14 | Parti is a guided workflow, worked through by a user and an agent together, covering the pipeline steps of the JohnnyHouse runbook, with the toolbase that replaces JohnnyHouse's custom scripts (§8A). The finish tool is its first major feature (restated 22 November 2026: the workflow is the goal). JohnnyHouse stays a prototype outside Model B; Parti is the Model B project. |
| D15 | Stacks of this repository: Bun and Python. The project is registered with Crucible (test reporting and the CR queue) and on Sandesh. |
| D13 | Whether to replace Unreal's built-in browser with another embedded browser is decided after a trial (see §11, T1). |
| D16 | Agents work alongside the user through AXI: `parti-axi` lets an agent join a running session as a participant, and a Pi plugin wakes the agent when the user acts. No MCP server and no embedded agent harness for now. Whether this is in Stage A is decided with Q9. An agent is a session participant like a user, so the same model carries to several users and sessions, to a served Parti and to a Nai backend (D3, D9). |
| D17 | The domain is a building with layers. The building is the base: its geometry, referenced through labelled elements (level, room, wall, floor, opening, …), each tied to its 3D object and to its 2D drawing elements. Layers sit on the building: finishes first (tiles, paints); furniture and cabinetry, electrical and plumbing later. Each layer places products from its catalogue onto the building under its own rules; a layer may change the model (cabinetry adds geometry). Each yields quantities, which roll up into bills of materials for each work-contract role. Quantities is a computational module: it holds the bills of materials and, with price data later, computes cost estimates. The finish tool is the finishes layer. |
| D18 | The world builder is a module of Parti. Once the building is modelled in CAD and brought into Unreal Engine, it creates a world there with the building at the centre of all activity, and stages it as an experience. It holds Parti's own metadata over Unreal's data structures, so an architect or designer can change the experience: scenarios; setting state (time of day, date, weather simulation, light); animations of the moving parts of the building and its world; experience mode (VR, or a monitor with peripherals); routes and viewpoints. Parti exposes this state to the agents that run the pipeline, alongside Unreal's own MCP, through its agent interface (D16). The current focus is this part of the workflow, after the CAD model exists. The world builder has its own per-area PRD, together with the Unreal plugin and finish assets. |
| D19 | Everything is versioned, and changes flow forward. The building, each plan and each scenario has revisions. Building elements keep stable ids across CAD revisions. Parti keeps the chain building → design → quantities → world builder. When something upstream changes, the change is allowed; Parti works out what downstream is affected, marks it stale, and lists the follow-up actions (re-check placements, recompute quantities, rebuild the scene), which the agent works through with the user (D16). What a change breaks (for example an orphaned placement when its zone is removed) is flagged as a follow-up action. Nothing downstream is changed silently or left wrong silently. The detail (rules, follow-up actions, how ids stay stable) belongs to the domain PRD. |

## 4. Functional requirements

### 4.1 Catalogue

- **FR-CAT-1** A finish has: id, maker, name, series, set, role in a set, the finishes it pairs with, maker's code and product address, zone (bathroom, interior, outdoor), surfaces it suits (wall, floor), size in millimetres, thickness, finish name and class (gloss, satin, matt, rustic), body, colour description (dominant colour, accent, palette, strength, lightness, warm or cool, visual texture), and its images (face, room photo, thumbnail). The JohnnyHouse tile record is the first source; see `DN-first-consumer-johnnyhouse.md`.
- **FR-CAT-2** The catalogue answers filter queries on: zone, surface, maker, main colour, colour strength, lightness, warm or cool, pattern, finish class, role in a set, size; plus free-text search on name, series and code; sorted (at least) round the colour wheel.
- **FR-CAT-3** For a chosen finish the catalogue returns what goes with it: the maker's set and the pairs, and finishes of complementary colour.
- **FR-CAT-4** Each maker's feed (and each target project's own records) is translated into the catalogue's finish by its own translation layer. Maker terms do not appear in the domain.
- **FR-CAT-5** Paint is a second kind of finish (colour, sheen). No paint data exists yet; the model must allow it without redesign.
- **FR-CAT-6** A finish can be valid for a surface or not (a wall-only tile on a floor is refused). The rule lives in the domain.

### 4.2 Model: surfaces and zones

- **FR-MOD-1** A target project declares its rooms and its surfaces, each with a stable id, a kind (wall, floor, feature), its room, and its size.
- **FR-MOD-2** A surface is divided into zones by numbers: wall bands by height and rectangles; floor field, border inset and rectangles. Zones on one surface do not overlap.
- **FR-MOD-3** The user can define, resize and remove zones from the interface (drag a band height, draw a rectangle).

### 4.3 Design

- **FR-DES-1** Commands: define zone, resize zone, remove zone, assign finish to a zone, clear a zone, save a scheme, apply a scheme. Each either produces events or is refused with a stated reason.
- **FR-DES-2** An assignment carries: finish id, laying pattern, grout width and colour, offset, rotation.
- **FR-DES-3** A design is saved to a file and loaded again, giving the same scene. The file can be carried to other tools (for JohnnyHouse: replayed in Blender for stills).
- **FR-DES-4** Undo and redo of design changes within a session.
- **FR-DES-5** A shortlist: finishes the user has set aside, each with a note saying where it is meant to go.

### 4.4 Selection

- **FR-SEL-1** Pick the surface under the crosshair, then the zone under the cursor within it. What is selected is highlighted in the scene and shown in the page.
- **FR-SEL-2** Wider picks: all walls of this room; all floors of this room; every zone carrying the same finish.
- **FR-SEL-3** Selection made in the scene appears in the page, and selection made in the page appears in the scene.

### 4.5 Presentation

- **FR-PRE-1** Time of day: the sun position through the day for a given date and place, and interior lights at night.
- **FR-PRE-2** Weather scenarios: clear, overcast and rain at the least.
- **FR-PRE-3** These are set from the page through the same shared state as the design.

### 4.6 Shared state

- **FR-STA-1** What is selected, what finish is on each zone, and the scene settings are the same data in the page and in the scene, kept in step without the user doing anything.
- **FR-STA-2** Either side can request a change; the result reaches both.
- **FR-STA-3** A page or a scene that connects late, or reconnects, receives the current state and continues.

### 4.7 Scene adapters

- **FR-SCN-1** A **mock scene** adapter, in this repository, that implements the scene side of the message schema without Unreal (a simple 2D or 3D drawing of surfaces and zones in a browser is enough). It is the test partner for the page and the gateway, and it is what makes a release possible before the C++ plugin exists.
- **FR-SCN-2** The **Unreal plugin** (deferred, D5): connects to the gateway; reports surfaces; does the crosshair pick; draws zones through one master material per surface (face texture, true tile size in world space from the size in millimetres, grout, laying pattern, shine from the finish class); applies assignments; applies presentation settings; shows the page as an overlay.
- **FR-SCN-3** Finishes reach Unreal as assets (D6, D7): the core catalogue through Unreal's import pipeline as textures, material instances and one finish data asset per finish, with the filter fields as Asset Registry tags; run-time finishes created from files using the same master material.

## 5. Quality requirements

- **NFR-1 Pure domain.** Each context's rules are plain functions over plain data: `decide(state, command) → events` and `evolve(state, event) → state`, keyed by aggregate id. No classes holding hidden state, no library, file, socket, Unreal, browser, Nai or EntityStore calls inside the domain. This is the part that migrates unchanged (D9).
- **NFR-2 Written for the later backends from the start.** Commands are safe to repeat. Every change is an event with an identifier and a sequence number per aggregate. State is rebuilt from events. Changes carry an expected version and are refused when it is stale.
- **NFR-3 Boundaries.** Contexts refer to one another by identifier only and exchange published events. No context reads another's storage.
- **NFR-4 Anti-corruption layers.** One translator each for: the scene (Unreal objects and assets), the page (controls and view state), each maker's feed, local files, and later Nai and EntityStore. Outside terms never appear inside the domain.
- **NFR-5 Ports named in domain terms:** catalogue store, design store, session channel, asset delivery. Version one supplies local adapters (files, a local connection). Later adapters (EntityStore for records; Nai for pipelines, session traffic and embeddings) replace them without changing the domain, the page or the scene adapter.
- **NFR-6 One published language.** The message schema is defined once, versioned, and is the only thing the page, the gateway and the scene adapters share. TypeScript types are generated from it now; C++ types when the plugin starts; Rust or Avro types when the backends join.
- **NFR-7 One transport (proposed).** A WebSocket carrying JSON messages, for every setting: overlay, VR panel, external browser, streamed picture. The embedded browser only displays the page; it is not the bridge.
- **NFR-8 Local only in version one.** Every server Parti starts binds to 127.0.0.1. Input from the page and from scene adapters is validated against the schema before it reaches the domain.
- **NFR-9 Platforms.** Everything in this repository runs on Linux and Windows.
- **NFR-10 Reusable.** Nothing specific to JohnnyHouse in this repository's code. JohnnyHouse data enters only through the target project's configuration (§8) and through test fixtures clearly marked as such.
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
| Page | TypeScript, VanJS | Catalogue browser, finish detail, shortlist, zone editing, presentation controls. Prior art: the JohnnyHouse tile browser (see the consumer note). |
| Mock scene | TypeScript | FR-SCN-1. |
| Installer and agent CLI | Python (run as a `uv` tool) | §8. |
| Catalogue tools | Python | Build a catalogue from a target project's finish records and images (thumbnails, colour tags); later, the Unreal editor scripts that import finishes (Unreal's Python runs in the editor only). |
| Unreal plugin | C++ | Deferred (D5). |

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
steps are taken up first, and in which release, is open (§12, question 9) and is the owner's call.

- **FR-WF-1 Steps.** The pipeline is a sequence of named steps (in the prototype: drawing intake; parametric shell build; openings and joinery; merge for render; CAD to Blender; reference materials; site and planting; interior furnishing; stills and lighting; movie production; print split; Unreal export). Each step states its inputs, its outputs, the numeric checks that prove it worked, and the owner review gate that follows it, if any.
- **FR-WF-2 Guided.** For a target project, an agent can ask Parti: which step am I on, what does it need, what must I check, what is next. Parti records what was done (one line per step: what changed, how it was checked, what was produced) in the target project.
- **FR-WF-3 Data, not hand-typed commands.** Geometry and scene content live in data tables in the target project; Parti's tools turn data into commands for the CAD and rendering applications. A correction is made in the data and regenerated.
- **FR-WF-4 Checks are part of the tool.** Each tool prints the expected result (for example volume and bounding box after a CAD stage) and compares it with what the application reports. A step is not complete on "ok" alone.
- **FR-WF-5 Checkpoints.** Each step ends in a saved checkpoint that can be returned to.
- **FR-WF-6 Applications stay outside.** The CAD application, Blender and Unreal are driven through their own agent interfaces (in the prototype: the SolidCraft, Blender and Unreal MCP servers, and a PDF reader). Each sits behind its own translation layer in Parti, so a tool's logic does not depend on one application's commands. Parti does not bundle these applications.
- **FR-WF-7 Caveats travel with the step.** The faults found in the prototype (the DN lists them) are carried as checks or warnings in the step they belong to, not left in a document.
- **FR-WF-8 Agent-facing form.** The workflow reaches an agent the same way the rest of Parti does (§8): through the scaffold (notes or skills written into the target project) and through `parti-axi` commands with structured results.
- **FR-WF-9 Owner in the loop.** Where taste decides, the tool produces options to show (rendered views, boards), and the step waits for the owner's choice. Every change to materials, furniture or lighting is shown as a rendered view before the step moves on.
- **FR-WF-10 Nothing of one house in the tools.** Names, dimensions and material choices of JohnnyHouse are data of that target project (NFR-10).

## 9. Stages and what a release means

The owner's instruction: this project's orchestrator runs it independently to a release; the tool is then
installed and used inside JohnnyHouse.

| Stage | Contents | Depends on |
|---|---|---|
| A. First release (Bun and Python only) | Message schema; domain (Design, Catalogue, Model, Presentation, Session); gateway; local adapters; page; mock scene; installer and agent CLI; catalogue tools. Demonstrated end to end on JohnnyHouse data with the mock scene: browse, filter, select a surface and a zone, define zones, assign, save, reload, set time of day and weather (as state), all through the page and through the CLI. | Nothing outside this repository. |
| B. Unreal | C++ plugin (FR-SCN-2, FR-SCN-3), overlay, finish assets, the three trials of §11. | Model B support for a C++ stack. |
| C. VR panel | The page as an interactive surface in the 3D scene. | B. |
| D. Data service | Catalogue, users, saved designs served to installed apps; EntityStore as system of record; Nai for pipelines, sessions and embeddings. | Requests to the Nai team (see the founding record). |
| E. Streamed Unreal | Unreal running on servers, shown in a browser, with the same page around it. | D. |

Which CRs make up Stage A, and their order, is the orchestrator's proposal to the owner at wave-open; it is not
written here. The release label and date are the owner's call.

## 10. Out of scope for the first release

- The C++ Unreal plugin and anything that needs it (deferred, not dropped).
- Nai, EntityStore, users, access control, several users on one design.
- Paint data. Relief and gloss maps for tiles (the images available are makers' web pictures of one tile face).
- Moving parts of the building (doors, drawers, gate, louvres) and walking controls in the first release; the world builder holds them later (D18).
- An MCP server for Parti, and an agent harness embedded in the page (for example Trueforge) as an in-page chat, so that Parti can become the main UI for the whole workflow. Possible later; not trialled now (D16).

## 11. Trials owed before or during Stage B

- **T1** Unreal's built-in browser widget as an overlay in a packaged 5.9 build, on Linux and on Windows, showing a page served from a local address. Reports (unverified on 5.9) say it long shipped an old Chromium, and that in packaged Linux builds it loaded web addresses but not local files. Outcome decides D13. This trial needs no C++ and can be run by the first consumer in the JohnnyHouse Unreal project at any time.
- **T2** A WebSocket connection between a C++ plugin and the gateway, exchanging the state.
- **T3** Finish assets: Asset Registry tag queries in a packaged build (which tags survive packaging), thumbnails in a packaged build, and a finish created at run time from a file.

## 12. Open questions

1. **Scene bridge before the C++ plugin exists.** Could a stop-gap (for example Unreal's Remote Control interface or editor Python, driven by the gateway) let JohnnyHouse see finishes in the Unreal editor during Stage A? Not examined; unverified on 5.9. Owner to say whether it is wanted.
2. **Where Unreal assets are made.** FR-SCN-3 needs the Unreal editor; the orchestrator of this project has no Unreal project of its own. Proposed: the consumer runs Parti's editor scripts in its own Unreal project.
3. **Windows testing.** No Windows machine has been named for testing.
4. **Variant Manager.** Whether saved schemes should also be Unreal variant sets (Stage B).
5. **Responsiveness figure** for NFR-11.
6. **Service-side confirmations.** NFR-7 (one WebSocket transport) and "Bun for the service side" were recommended to the owner and not objected to, but not explicitly confirmed.
7. **Release targets and remote.** The scaffold recorded owner `anthill-tec` (taken from the sibling projects Crucible and Sandesh) and no release targets. The owner confirmed `anthill-tec` (22 November 2026; remote `anthill-tec/parti`, private). Release targets remain open; FR-AXI-1 implies at least one publishing target.
8. **Name clash.** "Parti" has not been checked against existing products or package names.
9. **Workflow and toolbase in the first release.** §8A arrived after the stages of §9 were drafted. Which pipeline steps become Parti tools first, and whether any of them belongs in Stage A beside the finish tool, is not decided. Proposed: Stage A stays the finish tool plus the workflow skeleton (FR-WF-1, FR-WF-2, FR-WF-8, with the steps described but their tools not yet ported); the tools are ported step by step afterwards, starting with the steps JohnnyHouse still has ahead of it (interior finishes, Unreal export, print split). The agent session (D16, FR-AXI-8, FR-AXI-9) is part of this decision, and so is the owner's current focus on the part of the workflow after the CAD model exists (D18).
10. **Testing tools that drive applications.** How Crucible-reported tests cover tools whose effect is inside SolidCraft, Blender or Unreal (recorded command batches compared with expected ones, or the live application) is not designed.

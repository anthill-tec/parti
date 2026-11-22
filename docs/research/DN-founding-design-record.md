# DN — Founding design record (moved from JohnnyHouse)

**Date:** 2026-11-22
**Status:** Historical record. Superseded as a contract by `PRD-parti.md`; kept for the reasoning and the order in which decisions were taken.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)
**Related:** `PRD-parti.md`, `DN-first-consumer-johnnyhouse.md`

This is the text of the design discussion of 22 November 2026, moved unchanged from
`/home/antonyj/Documents/bals/JohnnyHouse/docs/research/render-pipeline-notes.md`, where it was written before
this project had a name. "The finish tool" and "the tool" in this text mean Parti. Relative paths
(`blender/...`, `unreal/...`) are relative to `/home/antonyj/Documents/bals/JohnnyHouse`.
Two later decisions are not in this text and are in the PRD: the name and repository (Parti, this folder), and
the deferral of the C++ Unreal plugin until Model B supports a C++ stack.

## Unreal walkthrough: features list (owner, 22 November 2026)

Blender gives only pre-rendered pictures and films, so the interactive part belongs in the Unreal executable
(`unreal/WalkthruDemo`). Features the owner has asked for, none built yet:

1. **Walking and interactive controls** (doors, drawers, gate, louvres), as already planned.
2. **In-app finish browser.** While walking, point at a wall, floor or feature, open a browser of the tile
   database, filter (bathroom / interior / outdoor, wall / floor, maker, colour, finish, size), and apply the
   chosen tile to that surface. Should also show the tiles that go with the chosen one (maker's set,
   complementary colour).
3. **Time of day control** (sun position through the day, interior lights at night).
4. **Weather scenarios** (clear, overcast, rain at the least).

How the tile database maps onto Unreal (proposal, not yet tried):

- **Data:** `blender/assets/reference/tiles/data/tiles.ndjson` (or `index.csv`) loads as it is: either imported
  as a Data Table in the editor, or read as JSON at run time so new tiles need no rebuild. The record fields
  are the filter fields of the browser.
- **Pictures:** `swatches/<id>.jpg` are the textures; `thumbs/<id>.jpg` (260 px) are the browser icons. Either
  imported as texture assets by an editor Python script, or loaded from disk at run time.
- **Material:** one tile master material with parameters: face texture, tile width and height in mm (from
  `size_mm`, so the tile repeats at true size in world space), grout width and colour, laying pattern, and
  roughness from `finish_class` (gloss / satin / matt / rustic). Applying a tile is setting these parameters on
  a dynamic material instance of the surface under the crosshair.
- **Surfaces:** each tileable wall, floor or feature needs its own material slot or mesh piece, so a choice
  changes that surface only. This has to be prepared at export (bathroom walls and floors first).
- **Choices:** saved to a small JSON file (surface name to tile id) so a session's selections survive and can be
  carried back to Blender for stills.
- **Limits:** the swatches are makers' web pictures of one tile face (up to 1200 px, no relief or gloss maps),
  good for choosing, not a substitute for a sample in hand.

A desktop version of the browser exists for choosing before the Unreal one is built:
`blender/assets/reference/tiles/browser/index.html` (rebuild its data with `tools/build_browser.py`).
Run `python3 blender/assets/reference/tiles/tools/serve_browser.py` and open http://127.0.0.1:8765/browser/ ;
the shortlist, with a note per tile saying where it is meant to go, is kept in `data/selections.json`, which is
the same surface-to-tile file the Unreal browser should read and write.

### Owner's requirements for the in-app finish tool (22 November 2026)

- **Finishes are Unreal assets.** A tile or paint swatch must exist as an Unreal texture and material before it
  can be applied; the database record is the source the asset is made from.
- **Selection goes below the wall.** A whole wall or floor can be selected, and so can a part of it. A bathroom
  wall may carry a main tile, a border band and a highlighter panel; a floor may carry a field and a border.
  This needs proper selection tools acting on the model.
- **One shared state between the Unreal scene and the browser interface.** What is selected, what finish is on
  each part, and the scene settings must be the same data on both sides, kept in step without the user noticing.
- **The interface also sets scene parameters** such as weather and time of day through the same state.

Proposed design (not yet built or tried):

1. **Asset pipeline.** An editor script reads the tile records and, per tile, imports the swatch as a texture and
   creates a material instance of one tile master material (face, true size from `size_mm`, grout, shine from
   `finish_class`), plus a lookup table from tile id to that instance. Paints get the same treatment from a
   paint record (colour, sheen); a paint database does not exist yet.
2. **Surfaces and zones.** Each tileable wall face or floor is a *surface* with a stable id. A surface is divided
   into *zones* described by numbers, not by cutting the model: for a wall, bands by height (skirting, dado,
   border, upper) and rectangles (niche, feature panel); for a floor, field, border inset and rectangles (shower
   area). The master material draws each zone with its own finish. Zones can be edited in the interface (drag a
   band height, draw a rectangle on the wall).
3. **Selection tools.** Crosshair pick of a surface, then of the zone under the cursor; highlight of what is
   selected; wider picks (all walls of this room, every surface with the same finish). Room membership comes
   from the measured room boxes already used for the bathrooms.
4. **State document.** One versioned JSON document, owned by the Unreal scene: `environment` (time of day, date,
   weather, lights), `selection` (surface, zone), `surfaces` (per surface: its zones, each with finish id,
   laying pattern, grout, offset, rotation). Unreal sends changes to the interface and the interface sends
   requested changes back over a local socket (or the embedded page bridge). The interface's VanJS state is
   bound to this document. Saved to disk it is the design itself, and can be replayed in Blender for stills.
   `data/selections.json` grows into this.
5. **Order of work.** State schema and message set first, tested in the browser against a mock scene; then the
   one-wall Unreal trial (embedded page, pick, zones, apply); then the asset pipeline at scale; then
   environment controls.

### Use Unreal's own asset management (owner, 22 November 2026)

The owner's instruction: the interface must connect to and work with Unreal's asset management tooling and
pipelines, not run a parallel catalogue beside it. The design above changes as follows (to be checked against
the Unreal 5.9 documentation before building; the project is `EngineAssociation` 5.9, Blueprint-only, with the
Interchange, Python and Variant Manager plugins already enabled):

- **Ingest through Unreal's import pipeline.** Swatches come in through the Interchange import framework
  (scripted from editor Python), so they are ordinary texture assets under `Content/JohnnyHouse/Finishes/...`
  with Unreal's own compression, streaming and source-file tracking (re-import when a swatch changes).
- **One data asset per finish.** Each tile or paint becomes a finish data asset (a primary data asset type,
  e.g. `Finish`) that references its texture and material instance and carries the record's fields. The tile
  JSON is then only the source the assets are generated from; in the app, Unreal is the catalogue.
- **Searchable through the Asset Registry.** The filter fields (zone, surface, maker, colour family, finish,
  size) are written as asset-registry tags, so the browser's filters are asset-registry queries answered
  without loading the assets. Content Browser collections mirror the main groups (bathroom wall, and so on).
- **Loaded and packaged by the Asset Manager.** Finishes are loaded on demand when applied (not all 1,554 at
  start) and are included in the packaged executable by Asset Manager rules, not by hard references.
- **The interface asks Unreal.** The page no longer reads `tiles.js` in the app: it sends a query, Unreal answers
  from the Asset Registry with the matching finish ids, fields and thumbnails. The desktop browser with the
  Python server stays as the tool for use outside Unreal, behind the same message set.
- **Variants.** Unreal's Variant Manager already switches materials on actors and is enabled in the project;
  check whether saved finish schemes (e.g. "Bath 1 scheme A / B") should be variant sets, not our own format.
- **Open points:** which registry tags survive into a packaged build; how the page gets thumbnails from
  Unreal (editor thumbnails are not in a packaged build, so probably our `thumbs/` images shipped as files);
  a primary data asset class normally needs a small C++ module or a Blueprint data asset class.

### Stack decisions for the finish tool (owner's answers, 22 November 2026)

To move to the tool's own repository once that exists.

Decided by the owner:

- **Interface placement:** an overlay inside the Unreal app. It must also work later as an interactive panel in
  the 3D scene for a virtual-reality tour (designed for now, built later).
- **Stages:** version one is standalone and local, on **Linux and Windows**. Later a web service: first a data
  service (catalogue, users, saved designs) for installed apps, then Unreal streamed from servers to a browser.
  The technology chosen now must carry through all stages.
- **Scope:** JohnnyHouse first, with clean boundaries so it can be reused for other models. Other review and
  presentation tools may follow; the finish tool is one of several.
- **Unreal side:** a full C++ plugin (no Rust inside Unreal).
- **Interface:** TypeScript on Bun (VanJS for rendering).
- **Finish delivery:** a core catalogue built into the app as Unreal assets; further finishes created at run
  time from downloaded files, behind the same catalogue interface.
- **Users:** one user per session now; the state document must be designed so a server can synchronise several
  sessions later (full collaboration).
- **Repository:** its own git repository, separate from JohnnyHouse (name and location to be given).
- **Embedded browser fallback:** decide after a trial of the built-in browser on the 5.9 Linux build.

Recommended (not yet confirmed by the owner):

- **Service side: Bun and TypeScript**, sharing the message and state types with the interface. Rust is kept in
  reserve for parts that later need it (bulk image preparation, a high-load synchronisation server).
- **One transport for every setting: a WebSocket carrying JSON messages**, defined schema-first with types
  generated for TypeScript and C++. The embedded browser is used only to display the page, not as the bridge,
  so the same page works as overlay, VR panel, external browser and around a streamed picture.
- **Run-time finishes** use the same master material with textures created from downloaded files; such
  textures are transient in Unreal (no streaming or texture-group settings), which is acceptable for swatches.

Findings from a first web check (forum reports, to be verified on 5.9):

- Unreal's built-in web browser widget long shipped Chromium 90; a newer engine (128) was planned as the
  default from 5.7. A user reports that in 5.6 packaged Linux builds the widget loads web addresses but not
  local files. Third-party embedded-browser plugins exist that list Linux support (e.g. UCefView).
- Pixel Streaming 2 (the route for the later streamed stage) has a TypeScript front-end library and a data
  channel for custom messages; it runs on Linux, with some reported faults.

Trials to run before building (in this order): (1) built-in browser as overlay in a packaged 5.9 build on Linux
and Windows, page served from a local address; (2) a WebSocket server inside a C++ plugin exchanging the state
document with the page; (3) finish assets: asset-registry tag queries and a run-time-created finish in a
packaged build.

### Domain model and Nai as backend (22 November 2026)

Owner: use Domain-Driven Design for the architecture, and examine Nai (`~/Documents/data_projects/nai`, the
owner's Rust streaming-pipeline runtime with its own DSL, connectors and provider plugins) as the backend.

**Bounded contexts proposed:** Design (core: a design's surfaces, zones, finish assignments, saved schemes),
Catalogue (finishes, makers, sets, colour classification), Model (rooms and surfaces that can take a finish),
Presentation (time of day, weather, lighting), Session (who is connected, selection, viewpoint), Asset delivery
(finish to Unreal asset, built in or at run time), Identity (users, access; service stage only). The Unreal
plugin and the browser page are adapters; the message schema is the published language; each maker's feed sits
behind a translation layer; Design refers to Catalogue and Model by identifier only.

**Nai review (read of code and documents by a sub-agent, nothing run or measured):**

- Built and usable: per-key state with per-key ordering (`keyed_by`), tables and views in RocksDB, synchronous
  HTTP request and reply through a pipeline (30 s default timeout), push to clients by GraphQL subscriptions over
  WebSocket or by server-sent events, checkpointing, a single binary that runs standalone, embedding and
  vector-search provider plugins (qdrant, pgvector, onnx).
- Missing for our interactive loop: no WebSocket input from clients (input is HTTP POST only; the in-engine
  `websocket` mode is a stub), no latency design or figures, at-least-once delivery by default (commands must be
  safe to repeat), tables cannot be queried from outside a pipeline, no event store or aggregate versioning, no
  access control or tenancy inside Nai, each connector is a separate process, the connector SDK is Rust only.
- Planned, not built: "service backend mode" (endpoints declared in the DSL), with WebSocket deferred.
- Unknown: real latency end to end; whether the runtime and RocksDB work on Windows (built in release, not
  tested in CI); availability of the external EntityStore service the entity connectors depend on.

**Proposed split (to be confirmed by the owner):** a thin session gateway (Bun, TypeScript) holds the live
WebSocket connections of the page and the Unreal plugin and owns the interactive loop; Nai sits behind it for
what is durable, shared or heavy: design event log and projections keyed by design, catalogue ingest pipelines
per maker, embeddings and similarity search, review streams. Version one (local, single user) can run without
Nai behind the same gateway interface; Nai joins at the service stage.

**Owner's note on Nai (22 November 2026):** Nai is the owner's own project, run by a different team, so new
plugins and connectors can be built to meet our needs. The gaps above therefore become requests to that team,
not reasons to keep Nai out of the interactive loop: (1) a two-way WebSocket session connector (commands in,
events and state out, per session and per design), which could replace the separate Bun gateway; (2) queries
on tables from outside a pipeline, or the planned service-backend mode; (3) measured end-to-end latency through
bridge, pipeline and connector, with a target for interactive use; (4) Windows build tested, including RocksDB;
(5) message types generated for TypeScript and C++ from the same schema. Until (3) is measured, whether Nai can
sit directly in the click-to-scene loop is unproven.

**EntityStore (22 November 2026):** the owner states EntityStore (`~/Documents/data_projects/4pm-EntityStore-service`)
is also their own. From its README only (not run, code not read): a Quarkus service on Redis Stack (cache and
RediSearch), MongoDB (source of truth) and an Avro schema registry; create, read, update, delete; search by TAG,
TEXT and NUMERIC fields; registered queries with projections and joins; change streams over server-sent events
(FULL, INCREMENTAL, LIVE); schema evolution. Nai already has source and sink connectors for it.

Fit: it is the natural system of record at the service stage for Catalogue (a `Finish` entity type whose index
fields are our filter fields), Design (saved designs and schemes), Model (surfaces) and review records, with its
change stream feeding Nai pipelines and the pages. Poor fit for the local version one: it needs Redis, MongoDB
and a schema registry running, which is too much to install beside a desktop app on other people's Windows
machines. Not established from the README: vector search, storage of the swatch images themselves, access
control and tenancy.

**Resulting architecture (proposed):** ports and adapters around the domain. The domain talks to a catalogue
store, a design store and a session channel through interfaces; version one plugs in local adapters (finishes
built into the app plus files, designs saved to a file, a local connection), and the service stage plugs in
EntityStore for records and Nai for pipelines, session traffic and embeddings, without changing the domain,
the page or the Unreal plugin.

**Decision (owner, 22 November 2026):** start without Nai. Build the local, standalone, single-user app first to
settle the customer's experience; migrate the backend later to a robust multi-user, multi-session environment
such as Nai (with EntityStore). So version one uses the local adapters, and the domain, message schema, page and
Unreal plugin are written so that the later move changes only what sits behind the store and session
interfaces. Still open: repository name and folder; Windows test machine; the embedded-browser trial.

**Design rules for the exercise (owner, 22 November 2026):** follow Domain-Driven Design with anti-corruption
layers and domain boundaries, so the same business logic can later be moved onto backends such as Nai and
EntityStore. In practice:

1. **The domain is pure.** Each context's rules (aggregates, commands, events) are plain logic with no knowledge
   of Unreal, the browser, files, sockets, Nai or EntityStore. A command plus the current state gives events;
   events give the new state. This is the part that migrates unchanged.
2. **Each context owns its words and its data.** Contexts refer to one another by identifier only and exchange
   published events; no context reads another's storage.
3. **Everything outside is behind an anti-corruption layer.** One translator each for: Unreal (engine objects
   and assets), the page (controls and view state), each maker's feed, local files, and later Nai (stream events,
   DSL records) and EntityStore (entities, queries, change streams). Outside terms never appear inside the domain.
4. **Ports are named in domain terms** (catalogue store, design store, session channel, asset delivery), with
   adapters per stage: local now, Nai and EntityStore later.
5. **The message schema is the published language**, defined once, versioned, with generated types for
   TypeScript and C++ (and Rust or Avro when the backends join).
6. **Written for the later backends from the start:** commands safe to repeat, every change an event with an
   identifier and a sequence number per aggregate, state rebuilt from events, optimistic version checks.
7. **Open choice:** which language holds the pure domain logic in version one (it runs beside the Unreal plugin
   and the page), given it must later run inside Nai. To be decided in the next design step.

**Decision (owner, 22 November 2026), closing rule 7:** version one is a TypeScript / Bun stack with a C++ plugin
inside Unreal Engine. The pure domain logic is therefore TypeScript, run by Bun. At a later stage it is migrated
using Nai's architectural approach: pipelines in the Nai DSL, connectors, and a custom provider if required.
Consequence for how the TypeScript domain is written: as small pure functions over plain data (decide: state and
command to events; evolve: state and event to state), keyed by aggregate id, with no classes holding hidden
state and no library calls inside, so each maps onto a keyed Nai stage or a provider call without redesign.

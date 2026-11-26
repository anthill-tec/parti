# DN — Parti's Ubiquitous Language (living glossary)

**Date:** 2026-11-22
**Status:** Living document. First version approved by the owner in the architecture review (22 November 2026).
**Author:** antonyj (owner)
**Co-author:** Parti orchestrator (vidushi-parti)
**Related:** `PRD-parti.md` (D17, D18), `../Architecture.md` A2 (contexts) and B8 (system-design terms)

## What this is

The business language of Parti: the words used to discuss the project with the people it serves, namely
architects, designers and the project's beneficiaries (its users), and the words the domain model is named
with. It holds no software terms: the system-design words (page, gateway, adapter, port, event, aggregate, …)
are listed in `Architecture.md` B8 and are never needed to discuss the product.

## Rules

1. Each term has **one meaning**, written in plain words.
2. Each term has **one owning context**.
3. A context is named only with a word from this glossary.
4. A term found to carry two meanings is split or renamed, and every document is updated in the same change.
5. A source system's word with another meaning never enters the domain: its translator maps it (FR-CAT-4).
6. Names marked *proposed* are not yet confirmed by the owner.
7. **The language is the schema** (owner, 24 November 2026): every term that is data names a type or a field of a
   backend schema (`parti.<context>.<message>/1`), so plain words are translated into these terms and the terms into
   schema records, validated before they are stored. A column naming each such term's schema type arrives with the
   schemas themselves (CR-PRT-002), kept in step by a guard test: every schema type has its term here.

## Terms

| Term | Meaning | Context |
|---|---|---|
| Target project | A building project Parti is installed into. It owns the building, its drawings, its Unreal project and its data. | — |
| Project type | The kind of building project: residential (single-family home, apartment block, …) or commercial (its sub-types); it decides which layers and bills of materials a project has (D30). | — |
| Project template | The configuration a project type brings at scaffolding: its workflow's phases and steps, its layers, catalogues, default rules and gates; adaptable afterwards (D30). | — |
| Project agent | The agent working in one target project with Parti's framework: it turns the architect's or designer's intent into data, rules and tool calls, and writes the project's own logic (D28). It is the **orchestrator** the user talks to in the guided chat: it follows the workflow and calls up the role agents at their steps (D43). | — |
| Agent role | A kind of agent the project agent calls up for a set of tasks, with its own context, tools and rights: the sheet reader, the CAD builder, the model checker, and so on through the phases. A checker never shares a maker's reasoning (D43). | — |
| Authoring skill | A skill by which an agent writes code the project needs, within its role, against the library's extension points, tested and reviewed by a checker before use (D44). | — |
| Project tool | Code written for one project by an authoring skill, checked and registered in the project, so later steps call it instead of writing it again (D44). | — |
| Product catalogue | The products a project uses, each with its type, maker, model, sources, assumptions and every place it is used, so the bills of materials count from placements (D45). | Catalogue |
| Size source | Where a size in the data tables came from: read from a sheet, taken from a rule, or an assumption for the owner to ratify (D42). | Workflow |
| Skill | One useful step an agent can take: it wraps one or more tools and changes the state of one thing the project holds (a source's calibration, a data table, a feature group in the model, a check result, the declaration) (D43). | — |
| Building | The architectural model of one building: its geometry, referenced through labelled elements. The base every layer sits on. (Replaces "Model", which had three meanings.) | Building |
| Room | A declared space of the building (a bathroom, a bedroom), with its id, name, storey and floor level. Rooms are declared before their surfaces. | Building |
| Room use | What a room is for (bedroom, bathroom, porch, kitchen), with the names people call it by (aliases). | Building |
| Site area | A part of the site outside the rooms: the drive, the garden, the approach. | Building |
| True north | The geographic north, given as an angle from the drawings' north (plan north); with the site's latitude and longitude it places the building on the map and the sun in the sky. | Building |
| Element | Any bounded unit Parti identifies and labels, with a name, a kind, an id and tags: a part of the building (level, room, wall, floor, ceiling, opening, stair), a surface, a zone, a region, a product in the model, and their lesser primitives (a product's parts and faces, a surface's pieces), each with an id under its parent. Tied to its 3D object and to its 2D drawing elements; what the pointer points at (D31). | Building |
| Label | An element's name, kind and tags; labelling is how elements are defined. Populated early from the CAD model and the drawings, proposed by the project agent, confirmed by the user (D31). | Building |
| Surface | A face of a room that can take a finish (a wall face, a floor), declared from inside the room. One wall or slab may carry faces of several rooms, so a surface is never just one CAD object. | Building |
| World scale | The real size of the building. Parti keeps every length at world scale (1:1) in millimetres; each system it works with (CAD, Blender, Unreal, a printed model, the map) has its own declared units and scale. | — |
| Drawing sheet | One page of the architect's drawings (a plan, an elevation, a section), registered as a source and calibrated from a known dimension before anything is read from it (D25, D33). | Workflow |
| Data table | The project's numbers a model is built from: levels, the wall set-out, slabs, openings and named parameters, read from the sources; a model is generated from its data tables, never edited by hand (D33). | Workflow |
| Feature group | The bodies one build step makes from the data tables (the walls of a level, the slabs), built, checked and checkpointed together. | Workflow |
| Model inventory | What the CAD model holds, read from the running CAD application: its bodies, components, part properties, materials with their looks, and faces; read again when the model's revision moves (`parti.model/1`, D33). | Building |
| Calibration | Setting a working model's scale from a known dimension ("this door is 2100 mm"); the same dimension is re-checked on every import and export. | Workflow |
| Display units | How a quantity is shown to the user, by kind: areas in square feet, room dimensions in feet and inches, components in millimetres; in bills of materials and estimates, square and running feet, SI for the rest (kg, litres, metres), pieces and boxes. Parti always stores millimetres. | — |
| Interactive tool | A tool the user handles in the Unreal world: pick and select, smart menu, compare, operate a moving part, navigate, measuring tape, conditions controls, notes, guide. | World builder |
| Measuring tape | The walkthrough's tool for measuring between two points or along a surface, read in feet and inches and in metres together. | World builder |
| Running foot | A length of one foot along an edge (skirting, border, cornice), the usual unit for linear items in a bill of materials. | Quantities |
| Face frame | A surface's own 2D frame: origin at its bottom-left corner as seen from inside the room, x along the face, y up; zones, openings and regions are rectangles in it, in millimetres. | Building |
| Opening | A part of a surface that takes no finish: a door, a window, a ventilator, a niche. | Building |
| Region | A part of a surface marked by a fitting or a moving part: keep clear (no tiles) or tile behind (tiled though covered). | Building |
| Declaration | The file in which a target project declares its rooms, surfaces, openings and regions, in the format Parti defines; reading it again gives a building revision. | Building |
| Zone | A part of a surface, described by numbers in its face frame. Kinds: field (the whole surface), band (a height range on a wall), panel (a rectangle on a wall), area (a rectangle on a floor), border (an edge inset on a floor). Zones lie in tiers; the upper shows. | Design |
| Tier | The stacking order of zones on a surface: the field below, bands and borders above, panels and areas on top. Not to be confused with a layer. | Design |
| Layer | One kind of information on the building. A *product layer* places products from a catalogue (finishes, furniture and cabinetry, electrical, plumbing) and yields quantities; an *information layer* describes the building's context and places no products (the site and geospatial layer). | Design |
| Design | The user's layer planning for the building: one plan per layer, with its schemes and shortlist. What the user is making. (Not the architect's design of the building, which is "the building".) The business word; in code, each layer's plan is a `LayerPlan`. | Design |
| Plan | The placements of one layer within a design (the finishes plan, the furniture plan). In code: `LayerPlan`. | Design |
| Revision | A numbered state of the building, of a plan or of a scenario (D19). | each owning context |
| Stale | Downstream of a change and not yet brought up to date (D19). | Workflow |
| Follow-up action | One thing to do to bring something stale up to date: re-check placements, recompute quantities, rebuild the scene (D19). | Workflow |
| Orphaned placement | A placement whose zone or surface is gone; flagged for the user to re-place or drop (D19). | Design |
| Placement | A product put on an element, a surface or a zone, with its details (for a finish: laying pattern, grout, offset, rotation). (Generalises "assignment".) | Design |
| Laying pattern | How the tiles of a placement are set out: stack (grid) or an offset bond (half, third), at 0 or 90 degrees; herringbone and diagonal later. | Design |
| Scheme | A named, saved set of placements that can be applied again ("Bath 1, scheme A"). | Design |
| Shortlist | Products set aside, each with a note and, optionally, its target: the room, surface and role (base, band, border, feature) it is chosen for. | Design |
| Setting-out | How a placement's grid is fixed on its zone: a rule (centre, full start, manual), the origin it gives and the edge cuts it leaves. Data of the placement. | Design |
| Module | The period of a tile grid: the tile's size plus the joint, or the size alone when it includes the joint. | Design |
| Product | Something a layer can place: a tile, a paint, a cabinet, a socket, a basin. Comes from a catalogue. A composite: its form, its build-up and its attributes by aspect (DM-10). Objects of the CAD model are tagged as products as soon as the model is generated (D31). | Catalogue |
| Product class | A class of the product classification, Parti's own tree in its own words (Finishes › Tile › Wall, Lighting › Pendant): it decides a product's attributes in each aspect, inherited down the tree, and is mapped to an IFC entity type (D32). | Catalogue |
| Form | A product's shape and dimensions (a tile 300 × 300 × 9 mm; a bottle of 750 ml) (DM-10). | Catalogue |
| Material | What an element or a part is made of (teak, MDF, brick, concrete, granite, ceramic, glass, steel), with its own properties (texture, colour, roughness, sheen; later density, fire class), which an element made of it takes by default unless updated separately (DM-10). | Catalogue |
| Build-up | An element's or a product's materials, coatings and finishes in order from the core outwards (concrete, 15 mm of plaster, paint); the outermost exposed one gives the look, the whole the physical facts and the quantities. Not *layer*, which names a product layer (DM-10). | Catalogue |
| Texture | The image maps a renderer uses (colour, normal, roughness), with the real size they cover. A source scan is one kind; a finish is a texture plus its stain (DM-10). | Catalogue |
| Aspect | One set of a product's attributes, read by the modules that need it: appearance (the renderers), physical (Unreal's world physics), quantities (the bill of materials), interaction (motion, what can be picked up or opened). Optional, with defaults: a product fills only what its use needs (DM-10). | Catalogue |
| Finish | A product of the finishes layer, of one kind: a tile, a wood veneer, a laminate, a paint, a metal, an exposed material (a material left as built: concrete, plaster, brick) or a glaze. It sits on the outside of a build-up. | Catalogue |
| Source scan | The texture a wood veneer or laminate is made from, with the real size it covers, its grain direction and its maps; one scan can back several finishes. | Catalogue |
| Stain | A tint applied over a source scan; a finish is a scan plus its stain, and its colour is the colour after the stain. | Catalogue |
| Catalogue | The products available to a layer, with the facts used to filter and match them. | Catalogue |
| Product draft | A product found and described from an outside source (a maker's site or feed, another system), with its source and the terms its data and images come under, waiting for a person to accept it into the catalogue; a draft is never placed or counted (D41). | Catalogue |
| Intake agent | An agent of the project's harness that fills the catalogue from outside sources when the project agent calls it up: it searches, fetches and extracts, and writes product drafts (D41). | — |
| Suitable use | Where a product may be used: room use (bathroom, interior, outdoor) and surface kind (wall, floor). *Proposed*: the JohnnyHouse tile records call the room use `zone`; their translator maps it here. | Catalogue |
| Quantity | How much of a product a plan needs, wastage included, computed from the placements and their setting-outs, and always stated with its counting rule. | Quantities |
| Counting rule | How a quantity was counted: for tiles, every grid tile of which any part shows is one, cut tiles are whole, offcuts not reused; the wastage and where the rounding is applied. | Quantities |
| Bill of materials | The quantities of one or more plans, grouped for one work-contract role. Shown to the user as the **BOM**, of what the workflow is on (the active room › surface; a surface laid house-wide as a whole). | Quantities |
| Work-contract role | A trade engaged on the building project: tiling contractor, painter, carpenter, electrician, plumber, furniture supplier. | Quantities |
| Semantic search | Finding products, rooms, design decisions or knowledge by meaning rather than by exact words ("warm matt tiles like this one"). | Catalogue |
| Knowledge base | The project's lasting knowledge that agents draw on: workflow lessons, product knowledge, the trades' rules. | Workflow |
| File catalogue | Every file Parti uses (drawings, models, textures, designs, exports), known by an id and its metadata rather than by a path on one machine. | Building |
| Telemetry | Records of how Parti is used and how it performs: actions taken, timings, agent runs. Kept to improve the product, never part of a design. | Workflow |
| Cost estimate | The price of a bill of materials, computed once price data exists. Later. | Quantities |
| World builder | The module that, once the building is modelled in CAD and brought into Unreal, creates a world there with the building at the centre of all activity, and stages it as an experience (D18). | World builder |
| Scenario | One way of experiencing the building: which layers and schemes show, the conditions, the experience mode, the routes. | World builder |
| Conditions | The state of the world around the building: time of day, date, weather simulation, light, site. (Replaces "Setting", owner, 24 November 2026, so that *Settings* can name the menu; earlier "Presentation".) | World builder |
| Site | The land and surroundings of the building in its world: terrain, neighbours, roads, vegetation, built from geospatial data and map providers. | World builder |
| Moving part | A part of the building or its world that can be animated: door, drawer, gate, louvre. | World builder |
| Sub-assembly | A moving part built as its own CAD part (a louvre window, a sliding door, the garage gate), brought into Unreal once as its own component and placed in the building from the CAD's placement tables. | World builder |
| Motion table | The kinematics of a sub-assembly, computed from the same CAD generators that build it: which bodies turn or slide, about which axis, driven by one input; a composition of motion primitives. A product's motion table is kept with it as its motion definition (D46). | World builder |
| Animatable | Said of a product that can move (an appliance, a cabinet, furniture, a door or gate, a mechanism): a core attribute, defaulted by its product class; an animatable product carries a motion definition (D46). | Catalogue |
| Motion definition | An animatable product's motion, kept with the product and reused wherever it is placed: which bodies move, how (a motion primitive), which way, how far, about which pivot, what rides along, where it stops; measured from the CAD once (D46). | Catalogue |
| Motion primitive | A generic, reusable motion with its parameters and limits: hinge, slide, follower or linkage, gear or ratio, lift and fold, telescope, continuous rotation. | World builder |
| Motion library | The world builder's set of motion primitives, which the agent composes into a sub-assembly's motion and its interactive scripts in Unreal. | World builder |
| Experience mode | How a person experiences a scenario: a VR walkthrough, or a monitor with keyboard, mouse or gamepad. | World builder |
| Route, viewpoint | A path, or a fixed place, that a scenario offers to move along or look from. | World builder |
| Navigation mode | A way of moving through the world: walk, teleport, orbit or fly, follow a route, jump to a viewpoint. | World builder |
| Avatar | The user's presence in the walkthrough (a mannequin, or the first-person camera), which navigation moves, also on the agent's request. Not the assistant (see Guide). | World builder |
| Guide | The assistant embodied as a figure in the world, which walks with the user and talks with them by voice or text. Not the user's avatar. | Session |
| Navigation data | A project's walkable areas, collision, stairs and levels, doors as passages, viewpoints, routes, teleport points and no-go areas, derived from the building. | World builder |
| Edition | A packaging of Parti for one kind of user: the designer edition or the client viewer (D22). | — |
| Designer edition | Parti for architects and interior designers: the full workflow and authoring, through the guided chat and components such as the asset browser. | — |
| Suggestion | A one-click prompt offered at each point of the workflow (a next action, a gate's option), in the chat and beside the selection everywhere in the Project Environment, so the user types little (D22). | — |
| To-do | A short task within a workflow step, open or done, listed when the step is completed: seeded from the step's checklist, or added by the user or the agent (FR-WF-15). | Workflow |
| Checklist | The validation items a step definition carries, held in the skill behind its step kind; they guide the agent and become the step run's to-dos (FR-WF-15). | Workflow |
| Project Environment | The designer edition's main interface, where the architect or interior designer works: the workflow panel, the workspace and the guided chat, with the asset browser docked at the bottom; every panel resizes, minimises, undocks and attaches again at any edge (D22). It augments the CAD, Blender and Unreal with assisted interactions and never duplicates their editing. | — |
| Workspace | The Project Environment's middle panel, a viewport the project agent commands (the workflow step in 0.1.0): it shows what the current step needs, a view or an editor of what Parti owns, never the geometry, titled by what it shows (*Design · Bath 1 › East wall*) (D22). | — |
| Workspace command | What the workspace is told to show: a view or an editor, its subject and its title; issued by the workflow step in 0.1.0, by the project agent later (D22). | Workflow |
| View | What the workspace shows to be looked at and acted on, not edited: the project, the BOM, the walkthrough, offers (D22). | — |
| Editor | What the workspace shows to change something Parti owns (labels and tags, zones and placements on a surface, Settings), never the geometry, which stays in the CAD, Blender or Unreal (D22). | — |
| Interaction event | A user's pointing, selection, clip or click, recorded with its elements, area, world bounds, CAD references, view and step: it gives the agent its context and feeds telemetry, and changes nothing in the design, unlike a design event, which goes into the design's history and versions (D29). | Session |
| Clip | An area taken with the rectangle clip, or any selection, sent into the guided chat with the elements it holds, for a question or an action by the agent (D22). | Session |
| Settings | The menu where a project is configured: the project, units and display, world defaults, design defaults, backend connections, the agent and skills, layout, telemetry (D22). | — |
| Guided chat | The Project Environment's conversation with the project agent: it follows the embedded workflow and guides the design workflow, puts each decision as options with pictures, in the user's own terms (D22). | — |
| Asset browser | Parti's central feature (D40): where every kind of product is found and chosen, across the whole product classification (finishes first; then structure, openings, joinery, sanitary ware, lighting, furniture, services, landscape, appliances and library assets), each choice made for a target. A tree of the product classes scoped to the agent's context, a filter bar with a palette over the results, a detail and the shortlist; it can be detached to its own window (D22). | Catalogue |
| Palette | A few colours picked by the user, taken from a scheme or proposed by the agent, on which every kind of asset in the asset browser can be filtered (D22). | Catalogue |
| Consumer | A person who consumes a project's deliverables, above all the walkthrough with or without VR: a home buyer, a business buyer, or the client who commissioned the project (D28). | — |
| Client viewer | Parti for the consumer: a self-contained walkthrough viewer, on a monitor or in VR, with the offered options, on Windows or Linux. | — |
| Smart menu | In the client viewer, a menu that opens in the 3D world at the zone or element the client points at, listing only its offered options; choosing one applies it at once. | World builder |
| UI helper | The client viewer's limited agent: it helps the client search and apply offered sets (tile sets, interior sets), and does nothing the client could not do. | Session |
| Offer | What the designer lets the client decide, per zone or element: a set of options with a default. | Design |
| Option | One choice within an offer: a placement or a whole scheme. | Design |
| Client bundle | A filesystem package, published for one client project and revision, holding everything the client viewer needs to run: the building, the offer, the scenarios, the stills and films, and every asset they use. Delivered as a filesystem package (offline: asset files plus their metadata in SQLite) or served remotely by Nai (online); the content is the same. | Asset delivery |
| Render | A still or a film made in the Blender part of the pipeline, for review and for the client viewer. | Workflow |
| Client selection | The client's choices among the offered options, returned to the designer's project. | Design |
| Session | One sitting in which participants work on the target project together. | Session |
| Participant | A user or an agent taking part in a session. | Session |
| Client review session | A session in which the client walks the building and decides among the offered options, guided by menus and by the assistant in chat or by voice; it ends in a client selection. | Session |
| Selection | What a participant has picked: an element, a surface, a zone or a group, by a click, a shift-click or a rectangle select. It can take a placement, define and label a zone on a surface, or be clipped into the chat (D22). | Session |
| Workflow definition | The workflow as data, versioned: its phases, step definitions, checks, caveats and gates. The same for every architectural project; a target project may adapt it (D26). | Workflow |
| Workflow run | What has happened in one target project's workflow: step runs, check results, corrections, decisions, variants and step records (D26). | Workflow |
| Plan onboarding | The first phase: the project's design brought into Parti, guided by the project agent: drawing PDFs, renders (texture and style cues), later other design tools' files, converted into Parti's metadata (D26). | Workflow |
| Phase | A broad, ordered, gated part of the workflow: Plan onboarding, Model, Declare, Design, Present, World, Deliver. Its order is data the owner may change (D26). | Workflow |
| Step | One unit of work within a phase, an instance of a step kind, run through the step cycle (D26). | Workflow |
| Step kind | One of the twelve kinds every step is an instance of: intake, build from data, consolidate, declare, transfer, restore after transfer, apply by rule, derive, compose the scene, choose, render or package, trial (D26). | Workflow |
| Step cycle | What every step does: read the sources, write the data, generate, apply, check against the expected numbers, checkpoint, record; on a failed check, fix the data, never the output (D26). | Workflow |
| Check | A measurement that proves a step worked, with its pass rule (body count and bounds exact; layer area equals room area). | Workflow |
| Human-use check | A check that people can use the building as modelled: the clear width and height of doorways, passages and stairs, measured on the built model against the check figure and pass figures (D42). | Workflow |
| Check figure | The person the human-use checks are made for, declared by the project with its source (an adult about 1.80 m tall, slightly portly); the walkthrough's character is the same figure (D42). | Workflow |
| Widening survey | What comes with a failed human-use check: how far the opening or passage can grow, and what stops it (a column, a fixture, a screen, a wall end, the open leaf) (D42). | Workflow |
| Check result | A check's outcome: pass or fail, the measured values, the worst offender, and what it did not prove. | Workflow |
| Caveat | A known trap of a step or a tool, carried with it and stated with its results ("lives in the world; replayed after an import"). | Workflow |
| Gate | A point where the owner decides before the workflow goes on, of one of four kinds: review, option, permission, trial (D26). | Workflow |
| Decision | An owner's decision recorded in the workflow run: pointing at a fault, choosing an option, giving a rule, or choosing from the catalogue. | Workflow |
| Pointer | What the owner refers to (a view, a selection, words, a picture), resolved to elements and confirmed before anything changes. With the pointer and selection tools on every 2D display, a point or a selection names its elements itself, the 2D bridge to the 3D model (D22, FR-WF-14). | Workflow |
| Correction | A revision of a step already done: its trigger, pointer, cause, fix, checks, and the step it lands in, which may be in an earlier phase. Its revision flows forward (D19, D26). | Workflow |
| Audit | A systematic re-check of a phase against its sources, run on purpose; its findings become corrections. | Workflow |
| Variant | An alternative kept beside the main line for comparison, never replacing it until chosen. (An option is what the client is offered; a variant is the designer's.) | Workflow |
| Step record | The log entry a step run writes itself: asked, done, checked with numbers, not checked, files. | Workflow |
| Checkpoint | A saved state of the target project after a step (a CAD file, a Blender scene, an Unreal level). Not the harness's own saved agent state. | Workflow |

## Change log

| Date | Change |
|---|---|
| 2026-11-22 | First version, from the architecture review. Owner's names: Zone kept (kinds: area, panel, …); Design kept (character: layer planning; Layer and Plan as terms); Session kept. |
| 2026-11-22 | Added Revision, Stale, Follow-up action, Orphaned placement (D19) and Cost estimate (D17). Design is the business word; `LayerPlan` is its name in code (owner). |
| 2026-11-23 | Added Knowledge base, File catalogue (D9) and Site (D18). |
| 2026-11-23 | Added Telemetry (D9). |
| 2026-11-23 | Added Edition, Designer edition, Client viewer, Offer, Option, Client bundle, Client selection (D22). |
| 2026-11-23 | Added Render; Client bundle carries stills and films (D22). |
| 2026-11-23 | Client bundle: a filesystem package with everything the viewer needs to run. |
| 2026-11-23 | Client bundle: offline (filesystem package) or online (served by Nai). |
| 2026-11-23 | Added UI helper (D22). |
| 2026-11-23 | Added Smart menu (D22). |
| 2026-11-23 | Step: building and packaging the client viewer is usually the last step. |
| 2026-11-23 | From the domain PRD (draft): Room, Face frame, Opening, Region, Declaration, Tier, Laying pattern; Surface and Zone sharpened. |
| 2026-11-23 | Added Sub-assembly, Motion table (T4 trial, JohnnyHouse #1640). |
| 2026-11-23 | Added Motion primitive, Motion library (D18 direction). |
| 2026-11-23 | Added Navigation mode, Navigation data (D18). |
| 2026-11-23 | Added Avatar (D18), Semantic search (D9). |
| 2026-11-23 | Added Room use, Site area (D24). |
| 2026-11-23 | Added True north (D24). |
| 2026-11-23 | Layer: product layers and information layers (D17). |
| 2026-11-23 | Added Client review session (D22). |
| 2026-11-23 | Added Guide (D22); Avatar distinguished from it. |
| 2026-11-23 | Added Display units (D25). |
| 2026-11-23 | Added World scale (D25). |
| 2026-11-23 | Display units extended to bills of materials; added Running foot (D25). |
| 2026-11-23 | Added Measuring tape (D25). |
| 2026-11-23 | Added Interactive tool (D18). |
| 2026-11-23 | Added Calibration (D25). |
| 2026-11-23 | Finish widened to four kinds; added Source scan and Stain (DM-8). |
| 2026-11-23 | Finish: fifth kind, metal. |
| 2026-11-24 | Added Setting-out, Module, Counting rule; Shortlist with targets; Finish kinds exposed and glaze. |
| 2026-11-24 | D26: Step narrowed to a unit within a phase; Gate gains its kinds; Checkpoint distinguished from the harness's state; added Workflow definition, Workflow run, Phase, Step kind, Step cycle, Check, Check result, Caveat, Decision, Pointer, Correction, Audit, Variant, Step record. |
| 2026-11-24 | Added Project agent (D28). |
| 2026-11-24 | Added Consumer; Client viewer is the consumer's (D28). |
| 2026-11-24 | Added Guided chat, Asset browser; Designer edition through them (D22). |
| 2026-11-24 | Added Project Environment; Guided chat follows the workflow and guides the design (D22). |
| 2026-11-24 | Added Project type, Project template (D30). |
| 2026-11-24 | Added Suggestion (D22). |
| 2026-11-24 | Suggestion available everywhere; added To-do (FR-WF-15). |
| 2026-11-24 | Added Checklist; To-do seeded from it. |
| 2026-11-24 | Added Plan onboarding; first phase renamed from Intake. |
| 2026-11-24 | Setting renamed Conditions, so that Settings names the menu (owner); added Settings. |
| 2026-11-24 | Element widened to every bounded unit and its lesser primitives; added Label (D31). |
| 2026-11-24 | Added Product class (D32); Form, Material, Build-up, Texture, Aspect (DM-10); Finish, Source scan reworded. |
| 2026-11-24 | Added Workspace, Workspace command, View, Editor, Interaction event, Clip, Palette; Project Environment, Asset browser, Selection, Pointer, Bill of materials (BOM) sharpened (D22). |
| 2026-11-24 | Rule 7: the language is the schema. |
| 2026-11-24 | Added Drawing sheet, Data table, Feature group and Model inventory (the building from CAD, D33; CR-PRT-003's gap analysis); Asset browser restated as the central feature (D40). |
| 2026-11-25 | Added Agent role, Skill; Project agent is the orchestrator (D43). Added Human-use check, Check figure, Widening survey (D42). |
| 2026-11-26 | Added Authoring skill, Project tool (D44), Product catalogue (D45), Size source (D42). |
| 2026-11-26 | Added Animatable, Motion definition; Motion table kept with the product (D46). |

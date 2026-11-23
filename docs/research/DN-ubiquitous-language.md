# DN — Parti's Ubiquitous Language (living glossary)

**Date:** 2026-11-22
**Status:** Living document. First version approved by the owner in the architecture review (22 November 2026).
**Author:** antonyj (owner)
**Co-author:** Parti orchestrator (vidushi-parti)
**Related:** `PRD-parti.md` (D17, D18), `../Architecture.md` §4 (contexts) and §11 (system-design terms)

## What this is

The business language of Parti: the words used to discuss the project with the people it serves, namely
architects, designers and the project's beneficiaries (its users), and the words the domain model is named
with. It holds no software terms: the system-design words (page, gateway, adapter, port, event, aggregate, …)
are listed in `Architecture.md` §11 and are never needed to discuss the product.

## Rules

1. Each term has **one meaning**, written in plain words.
2. Each term has **one owning context**.
3. A context is named only with a word from this glossary.
4. A term found to carry two meanings is split or renamed, and every document is updated in the same change.
5. A source system's word with another meaning never enters the domain: its translator maps it (FR-CAT-4).
6. Names marked *proposed* are not yet confirmed by the owner.

## Terms

| Term | Meaning | Context |
|---|---|---|
| Target project | A building project Parti is installed into. It owns the building, its drawings, its Unreal project and its data. | — |
| Building | The architectural model of one building: its geometry, referenced through labelled elements. The base every layer sits on. (Replaces "Model", which had three meanings.) | Building |
| Room | A declared space of the building (a bathroom, a bedroom), with its id, name, storey and floor level. Rooms are declared before their surfaces. | Building |
| Room use | What a room is for (bedroom, bathroom, porch, kitchen), with the names people call it by (aliases). | Building |
| Site area | A part of the site outside the rooms: the drive, the garden, the approach. | Building |
| True north | The geographic north, given as an angle from the drawings' north (plan north); with the site's latitude and longitude it places the building on the map and the sun in the sky. | Building |
| Element | A labelled part of the building (level, room, wall, floor, ceiling, opening, stair, …), tied to its 3D object and to its 2D drawing elements. | Building |
| Surface | A face of a room that can take a finish (a wall face, a floor), declared from inside the room. One wall or slab may carry faces of several rooms, so a surface is never just one CAD object. | Building |
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
| Shortlist | Products set aside, each with a note on where it is meant to go. | Design |
| Product | Something a layer can place: a tile, a paint, a cabinet, a socket, a basin. Comes from a catalogue. | Catalogue |
| Finish | A product of the finishes layer: a tile or a paint. | Catalogue |
| Catalogue | The products available to a layer, with the facts used to filter and match them. | Catalogue |
| Suitable use | Where a product may be used: room use (bathroom, interior, outdoor) and surface kind (wall, floor). *Proposed*: the JohnnyHouse tile records call the room use `zone`; their translator maps it here. | Catalogue |
| Quantity | How much of a product a plan needs, wastage included. | Quantities |
| Bill of materials | The quantities of one or more plans, grouped for one work-contract role. | Quantities |
| Work-contract role | A trade engaged on the building project: tiling contractor, painter, carpenter, electrician, plumber, furniture supplier. | Quantities |
| Semantic search | Finding products, rooms, design decisions or knowledge by meaning rather than by exact words ("warm matt tiles like this one"). | Catalogue |
| Knowledge base | The project's lasting knowledge that agents draw on: workflow lessons, product knowledge, the trades' rules. | Workflow |
| File catalogue | Every file Parti uses (drawings, models, textures, designs, exports), known by an id and its metadata rather than by a path on one machine. | Building |
| Telemetry | Records of how Parti is used and how it performs: actions taken, timings, agent runs. Kept to improve the product, never part of a design. | Workflow |
| Cost estimate | The price of a bill of materials, computed once price data exists. Later. | Quantities |
| World builder | The module that, once the building is modelled in CAD and brought into Unreal, creates a world there with the building at the centre of all activity, and stages it as an experience (D18). | World builder |
| Scenario | One way of experiencing the building: which layers and schemes show, the setting, the experience mode, the routes. | World builder |
| Setting | The state of the world around the building: time of day, date, weather simulation, light, site. (Replaces "Presentation".) | World builder |
| Site | The land and surroundings of the building in its world: terrain, neighbours, roads, vegetation, built from geospatial data and map providers. | World builder |
| Moving part | A part of the building or its world that can be animated: door, drawer, gate, louvre. | World builder |
| Sub-assembly | A moving part built as its own CAD part (a louvre window, a sliding door, the garage gate), brought into Unreal once as its own component and placed in the building from the CAD's placement tables. | World builder |
| Motion table | The kinematics of a sub-assembly, computed from the same CAD generators that build it: which bodies turn or slide, about which axis, driven by one input; a composition of motion primitives. | World builder |
| Motion primitive | A generic, reusable motion with its parameters and limits: hinge, slide, follower or linkage, gear or ratio, lift and fold, telescope, continuous rotation. | World builder |
| Motion library | The world builder's set of motion primitives, which the agent composes into a sub-assembly's motion and its interactive scripts in Unreal. | World builder |
| Experience mode | How a person experiences a scenario: a VR walkthrough, or a monitor with keyboard, mouse or gamepad. | World builder |
| Route, viewpoint | A path, or a fixed place, that a scenario offers to move along or look from. | World builder |
| Navigation mode | A way of moving through the world: walk, teleport, orbit or fly, follow a route, jump to a viewpoint. | World builder |
| Avatar | The user's presence in the walkthrough (a mannequin, or the first-person camera), which navigation moves, also on the agent's request. Not the assistant (see Guide). | World builder |
| Guide | The assistant embodied as a figure in the world, which walks with the user and talks with them by voice or text. Not the user's avatar. | Session |
| Navigation data | A project's walkable areas, collision, stairs and levels, doors as passages, viewpoints, routes, teleport points and no-go areas, derived from the building. | World builder |
| Edition | A packaging of Parti for one kind of user: the designer edition or the client viewer (D22). | — |
| Designer edition | Parti for architects and interior designers: the full workflow and authoring. | — |
| Client viewer | Parti for the building's owner: a self-contained walkthrough viewer with the offered options, on Windows or Linux. | — |
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
| Selection | What a participant has picked: an element, a surface, a zone or a group. | Session |
| Step | One stage of the guided workflow (drawing intake, shell build, …, finishes, world building, and usually last, building and packaging the client viewer). | Workflow |
| Gate | A point where the owner decides before the workflow goes on. | Workflow |
| Checkpoint | A saved state of the target project after a step. | Workflow |

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

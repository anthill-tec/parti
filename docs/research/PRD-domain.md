# PRD — The domain: building, design and catalogue (slice for 0.1.0)

**Version:** 0.4 (re-sliced 24 November 2026 for the roadmap, PRD-parti D33)
**Date:** 2026-11-23
**Status:** Reviewed by the owner (23 November 2026): DM-1 to DM-9 decided; §4 and §5–6 agreed; revised 24 November 2026 (finish kinds, setting-out and quantities, the record formats a project's own agent fills; the storyboard review: elements and labels, the product model (DM-10), the workflow slice (DM-11)). Written for the slice release 0.1.0 needs (D23, `../Architecture.md`, Documents); it grows with each
release. Items marked **DM-n** are decisions for the owner; the text shows the recommended option.
**Author:** Parti orchestrator (vidushi-parti), with the owner
**Builds on:** `PRD-parti.md` (D17, D19, D22, D23, §4, Q9, Q11), `DN-ubiquitous-language.md`, `DN-test-strategy.md`
**Evidence:** JohnnyHouse's answers on its bathrooms and workflow (Sandesh #1631, #1633), its tile records
(`DN-first-consumer-johnnyhouse.md`), its RUNBOOK

## Change Control

| Date | Change |
|---|---|
| 2026-11-23 | First draft, for 0.1.0. |
| 2026-11-24 | **Version 0.4, re-sliced for the roadmap** (PRD-parti D33, owner): 0.1.0 is the building from CAD. §1 rewritten; §2.6 the model and its inventory (DM-12); §2.7 the derived declaration; §2.1a labels from the model; §4.4 0.1.0 ships the first level of every branch; §6 model revisions; §7 and §8 the new message families and logs; §11 widened to the first three phases. The design (§3), the finishes catalogue (§4.1 to §4.3), setting-out and quantities move to 0.2.0, the conditions to 0.4.0; their text stays as the draft for those releases, re-reviewed before each. |
| 2026-11-24 | From the storyboard review (owner): elements and labels (§2.1a); zones defined by a selection and labelled (§3.2); the product model and the classification (§4.4, DM-10, PRD-parti D32), so 0.1.0's finish records are structured as form, build-up, appearance and quantities; interaction events (§5, §7); the Workflow context's 0.1.0 slice (§11, DM-11); version 0.3. |
| 2026-11-24 | "Setting" renamed "Conditions" (owner). |
| 2026-11-23 | DM-3 and DM-6 decided as recommended. |
| 2026-11-23 | §2.3a units (D25). |
| 2026-11-23 | DM-7 decided as recommended (owner). |
| 2026-11-24 | §4.2: a project's records are translated by its own orchestrator into Parti's formats (`parti.catalogue/1`, `parti.scan/1`, `parti.shortlist/1`); Parti provides the formats and the library's tools (owner). |
| 2026-11-24 | Setting-out per placement (rule, origin, edge cuts, module) and quantities (counting rule, wastage, to buy) in 0.1.0; shortlist targets; kinds exposed and glaze (owner; JohnnyHouse #1658). |
| 2026-11-23 | Effect paints; colour-only (provisional) finishes; cabinetry classes; renderers rebuild finishes from the catalogue (JohnnyHouse #1653). |
| 2026-11-23 | Fifth kind: metal (owner; JohnnyHouse #1651); scans as records of their own. |
| 2026-11-23 | Non-tile finishes in 0.1.0: wood veneer, laminate, paint (owner); DM-8 finish = scan + stain, DM-9 placements on parts later (JohnnyHouse #1648). |
| 2026-11-23 | Guides carry `towards`, the side where the fitting's area lies (JohnnyHouse #1644). |
| 2026-11-23 | From JohnnyHouse's first declaration (#1642): anchor direction fixed in the example (start = left end seen from inside), B-4 added; quality objects; references.columns; floor side; guides; steps; DM-7 proposed. |
| 2026-11-23 | DM-1, DM-2, DM-4, DM-5 decided as recommended; §4, §5–6 agreed; §7 notes that the schema and storage grow with each release (owner). |
| 2026-11-23 | Optional room use, aliases and outline, site areas, and the site's geo-reference and true north in the declaration (D24). |
| 2026-11-23 | Picture orientation in the catalogue translator; ids confirmed by the Unreal trial (JohnnyHouse #1638). |

## 1. What 0.1.0 needs from the domain

Release 0.1.0 is **the building from CAD** (PRD-parti D33, owner, 24 November 2026): the first three phases of the
workflow, Plan onboarding, Model and Declare, with the user interface that serves them.

- **Plan onboarding:** the architect's drawing sheets and renders are registered as **sources**; each sheet is
  **calibrated** from a known dimension (D25); the project's numbers are held as **data tables** (§2.6).
- **Model:** the model is built from the data tables, **feature group** by feature group, by the `parti` library's step
  cycle and its SolidCraft translator; the running CAD model is **read live** into a **model inventory** and read again
  whenever its revision moves; the model's objects are **products of their class** (D31, D32), with their materials and
  faces (§2.6, DM-12).
- **Declare:** a draft **declaration** is **derived** from the model inventory (rooms from slabs and walls, surfaces from
  their faces) and confirmed or corrected by the user; a declaration a project writes itself still imports (§2.7).

So this slice covers the **Building** context (the declaration, now with the model), the **Catalogue** context's product
model and classification only (§4.4), the **Session**'s selection and interaction events (§5), and the **Workflow**
context's first three phases (§11). JohnnyHouse is the test bed: its own orchestrator moves its CAD scripts onto the
library, and its run is the workstation acceptance; Parti's tests use synthetic buildings, drawing sheets and models
(NFR-10).

**Moved by the roadmap** (D33): the **Design** context (§3: zones, placements, schemes, the shortlist), the **finishes
catalogue** (§4.1 to §4.3), **setting-out** and **quantities** (§3.3, §3.4a) come in **0.2.0**; the **conditions** (§5)
in **0.4.0**. Their sections stay below as the draft for those releases, re-reviewed with the owner before each.

All terms are the glossary's. A term used here and not yet in the glossary is added to it with this PRD.

## 2. Building (context)

### 2.1 What it holds

The building's base for the finishes layer: **rooms**, and the **surfaces** that can take a finish, each with its
**openings** and its **regions**.

- **Room:** a declared id (for example `FF_bath1`), a name, a level (storey) and its floor level; optionally its **use**
  (bedroom, bathroom, porch), **aliases** ("master bedroom") and its floor **outline**, which the assistant needs to resolve
  and measure rooms (PRD-parti D24). Cheap to declare now; required later.
- **Site** (the first entries of the site and geospatial *information layer*, PRD-parti D17): the building's geo-reference (latitude, longitude, elevation) and the angle from plan north (the world
  frame's +Y) to true north; optional in 0.1.0, needed for compass questions, the sun position and map data (PRD-parti D24).
- **Site area:** a part of the site outside the rooms (drive, garden, approach), with id, name, use and outline
  (optional in 0.1.0; for D24).
- **Surface:** a face of a room that can take a finish, declared *from inside the room*: a wall face, a floor (a
  ceiling later). One CAD body may carry faces of several rooms, and one slab carries every floor of a storey, so a
  surface is never "one CAD object" (JohnnyHouse #1631 §2).
- **Opening:** a part of a surface that takes no finish: a door, a window, a ventilator, a niche (a niche may take a
  finish of its own later).
- **References:** the CAD bodies behind a surface, which may be walls or columns (part of some bathroom perimeters
  is a column face), listed as references, not as the surface.
- **Region:** a part of a surface marked by a fixed fitting or a moving part: **keep clear** (no tiles: behind a mirror, a cistern
  housing) or **tile behind** (tiled though covered: behind a vanity; the span a sliding door leaf travels over, since JohnnyHouse's
  bathroom leaves hang on the bathroom face of the wall). Regions affect layout and, later, quantities.

### 2.1a Elements and their labels (owner, 24 November 2026; PRD-parti D31)

An **element** is any bounded unit Parti identifies: a room, a surface, a zone, an opening, a region, a fitting, a
feature, a product in the model, and later their **lesser primitives** (a product's parts and faces, a surface's pieces,
each with an id under its parent). Each has a **label**: a name, a kind, an id and tags, which is what the pointer and a
selection report (§7) and how the user and the agent speak of it.

- **0.1.0:** the labels come from the model inventory (CAD names as references, the products' classes, §2.6) and the
  declaration (ids, names, aliases, uses, §2.4, §2.7); the project agent proposes labels and tags with its labelling
  skill and the user confirms or renames them (the harness, PRD-parti D21). Zones are labelled when defined (§3.2, 0.2.0).
- **Later:** the drawings' own labels (read from the sheets) join them; lesser primitives get their labels as they
  become addressable (DM-9).

### 2.2 Identity and revisions (D17, D19)

- Every room, surface, opening and region has a **declared id**, chosen by the target project and stable across CAD
  revisions. CAD body names are kept only as **references** (attributes), never as ids: body names split, swap their
  `(1)` suffixes and repeat (JohnnyHouse #1631 §2).
- JohnnyHouse's Unreal trial confirms this (`PRD-parti.md` T4): between two CAD revisions 140 body names vanished and
  2,041 were new, and Unreal's mesh asset names differ from the object names. In the scene, an id hangs on the actor.
- Recommended id form: `<room>.<kind>.<side>` for surfaces (`FF_bath1.wall.E`, `FF_bath1.floor`), and
  `<surface>/<name>` for openings and regions. A target project may use any unique ids; the form is a convention.
- **The building is versioned.** A declaration read again produces a **building revision**: Parti compares it with the
  previous revision and records what was added, removed, resized or moved.

### 2.3 Geometry

- **Face frame:** every surface has its own 2D frame: origin at its **bottom-left corner as seen from inside the
  room**, x along the face, y up (walls) or x east, y north (floors). Zones, openings and regions are rectangles in
  this frame, in millimetres. (DM-6, decided.)
- **World anchor:** each surface also records where it sits in the target project's world frame (for a wall, its two
  end points in plan and its floor level; for a floor, its outline). **A wall's `start` is its left end as seen from inside
  the room**, and x is measured from it: a north wall runs west to east, an east wall north to south, a south wall east
  to west, a west wall south to north (JohnnyHouse #1642). The anchor's direction must agree with the side (B-4), so the scene and Blender can find it and
  openings given in world coordinates can be converted.
- **0.1.0 limits:** surfaces are rectangles (walls) or rectangles (floors); walls are vertical. Polygonal floors and
  sloped faces come later. JohnnyHouse's four bathrooms fit.

### 2.3a Units (PRD-parti D25)

Every length in the domain and in events is in **millimetres of the real building** (world scale 1:1); areas are derived.
The declaration states the units and scale of its source model (`"units": "mm"`, `"scale": 1`), and `parti-axi`
converts on import. Every other system (Blender, Unreal, a printed model, the map) is reached through its translator's
declared transform: units, scale, axes and origin (PRD-parti D25).
What the user sees follows the target project's display preferences: areas in square feet, room dimensions in feet and
inches, component measurements in millimetres. A command may carry a length in another unit; it is converted on entry.
The configuration written by `parti-axi init` holds the preferences, with those defaults, and **the scale of each working
model**, which Parti sets: stated, or calibrated against a known dimension ("this door is 2100 mm"), and re-checked on
every import (PRD-parti D25).

### 2.4 The declaration file

The building reaches Parti as a **declaration file** written by the target project (FR-MOD-1), JSON, in the folder the
configuration names. Parti defines the format; the target project fills it; `parti-axi` checks it and imports it. In
0.1.0 the file is the only source of the building: Parti does not edit it (DM-3, decided).

```json
{
  "format": "parti.building/1",
  "units": "mm",
  "scale": 1,
  "world": "X east from the west face of column C1, Y north from the south face of the west block, Z up from the ground-floor finished floor",
  "site": { "latitude": null, "longitude": null, "elevation_m": null,
            "true_north_deg": null, "note": "angle from plan +Y to true north, clockwise; to be given by the target project" },
  "rooms": [
    { "id": "FF_bath1", "name": "First-floor bath 1", "level": "FF", "floor_z": 3100,
      "use": "bathroom", "aliases": ["bath 1", "upstairs bathroom"] }
  ],
  "surfaces": [
    {
      "id": "FF_bath1.wall.E", "room": "FF_bath1", "kind": "wall", "side": "E",
      "width": 3470, "height": 2980,
      "anchor": { "start": [5680, 3700], "end": [5680, 230], "z": 3100 },
      "references": { "cad": ["W_FF_bath_div"], "columns": [] },
      "openings": [],
      "regions": [
        { "id": "FF_bath1.wall.E/mirror", "kind": "keep-clear", "x": 900, "y": 1050, "width": 700, "height": 800,
          "fitting": "MR_FF_bath1" }
      ],
      "quality": { "anchor": "measured",
                   "regions": { "level": "derived", "note": "from the fitting generator" } }
    }
  ]
}
```

(The example follows JohnnyHouse's first-floor bath 1: its east face is one side of `W_FF_bath_div`, shared with bath 2,
and carries the mirror; its ventilator is on the south face. The world frame is JohnnyHouse's own.) Openings may also be given in world
coordinates, with `"frame": "world"`; Parti converts them. Each block (`anchor`, `openings`, `regions`) may carry a
**quality**, shown to the user, because a target project's data is often partly known (JohnnyHouse's first-floor doors):
one of `measured`, `derived`, `assumed`, or an object `{ "level": <one of those, or null>, "note": "<why>" }` when it
needs explaining (an empty block with a reason has level null and a note).

Conventions settled with JohnnyHouse's first file (#1642):
- **References** hold named lists: `cad` (CAD body names) and `columns` (the grid names of columns behind the face,
  e.g. `C2R2`, which stay stable when column bodies are merged or split). Both are references, never ids.
- **Floors** carry `"side": "floor"`, so the field is always present.
- **A fitting touching two faces** (a corner vanity) is declared as one region per face with the same `fitting` name.
- **A sliding door leaf** is a `tile-behind` region on the door's own wall, covering the span the open leaf travels over;
  its track is not declared in 0.1.0.
- **Fitting footprints on a floor** are regions on the floor surface, like those on walls.
- **Guides** (optional): lines on a surface that a zone may follow, each with an id, a fitting, a position (`x` on a
  wall, `y` on a floor) and `towards` (`"+"` or `"-"`: the side of the line, in the face frame, where the fitting's
  area lies, so a shower area can be drawn on the right side), e.g. a shower's glass line (FF_bath1 at Y 1290). They are not zones; Parti offers them when a zone is drawn.
- **A face that is not one plane** (a 10 mm step where a column meets a wall) is declared as one flat rectangle at its
  main plane, with optional `steps`: `{ "x": <from>, "width": <span>, "offset": <mm, + towards the room> }`, which Parti
  shows the user as a warning on the zones and placements crossing them (DM-7, decided).
- Not in 0.1.0: floor falls and drains, wall-mounted taps and shower heads.

### 2.5 Rules

- **B-1** Ids are unique within the building; every surface names an existing room; every opening and region lies
  inside its surface.
- **B-2** Openings on one surface do not overlap one another.
- **B-4** A wall's anchor runs left to right as seen from inside the room, as its side requires (a north wall west to
  east, and so on, §2.3); a wall whose anchor runs the other way is a fault, since it would mirror the face.
- **B-3** A declaration that breaks B-1, B-2 or B-4 is refused as a whole, with every fault listed; the previous revision
  stays in force.

### 2.6 The model and its inventory (DM-12; owner, 24 November 2026, PRD-parti D33)

- **Data tables** hold the project's numbers (levels, the wall set-out, slabs, openings, named parameters), read from the
  sources; the model is generated from them, **feature group** by feature group, and never edited by hand (a correction
  edits a table row and regenerates what depends on it; PRD-parti D26).
- **The model inventory** (`parti.model/1`) is what the running CAD model holds, read through the application's
  translator (SolidCraft first): its **bodies** (name as a reference only, volume, bounds, the feature group that made
  them), its **components** and their placements, **part properties** (among them the product class), **materials** with
  their looks, and **faces** (each with an id under its body, its plane or surface kind, normal and area: the lesser
  primitives of D31). It carries the application's units and the declared transform (D25), and the design's
  **revision**. The application's own report and Parti's inventory are two documents: the translator turns the first
  into the second.
- **The model in the Building context:** each object of the inventory is a **model object** with its CAD reference and a
  Parti id given at its first classification and kept in the design (in part properties until the SolidCraft plugin
  keeps it as plugin data, PRD-parti D34), so it survives renames; it is a **product of its class** (D31, D32), by the
  class stored with it, else by the project's rules, else **unclassified** and listed for the user. A face takes its
  body's material, the body its component's, the component its material's, **by default, unless updated** (DM-10; the
  same precedence SolidCraft applies).
- **Read again** whenever the model's revision moves: the new inventory is compared with the last and gives a **model
  revision** with its changes (objects added, removed, renamed, split; a material changed), §6.
- **Rules:** **M-1** a model object's Parti id never changes once given; **M-2** an object whose class is unknown is
  unclassified, never guessed silently; **M-3** a read that fails leaves the last inventory in force and says why.

### 2.7 The derived declaration (owner, 24 November 2026, PRD-parti D33)

From the model inventory Parti **derives a draft declaration** (`parti.building/1`, §2.4): rooms from the slabs and walls
that bound them, each surface from the faces that make it, with its anchor and face frame (§2.3, DM-6), openings from the
voids in it. The project agent labels it (§2.1a); the user **confirms or corrects** it in the page, surface by surface,
and the confirmed declaration becomes a building revision (§2.2) under the same rules (§2.5). A declaration a project
writes itself still imports, and is compared with the derived one.

## 3. Design (context, core) — from 0.2.0 (PRD-parti D33)

### 3.1 What it holds

The user's layer planning (glossary: Design). In 0.1.0 one layer exists: **finishes**, so the design holds one
**plan**: the **zones** on each surface, the **placement** in each zone, the **schemes**, and the **shortlist**.

### 3.2 Zones

A zone is a part of a surface, described by numbers in the face frame (FR-MOD-2). Kinds in 0.1.0:

| Kind | On | Defined by |
|---|---|---|
| **field** | wall, floor | the whole surface (every surface has one, created with the surface) |
| **band** | wall | a height range across the full width: skirting, dado, border, upper |
| **panel** | wall | a rectangle: feature panel, niche face |
| **area** | floor | a rectangle: shower area, a rug-like inset |
| **border** | floor | an inset of given width along the edges |

**Tiers (DM-1, recommended):** zones lie in **tiers**: the field at the bottom, bands and borders above it,
panels and areas on top. Where zones overlap, the upper one shows. Zones **of the same tier** do not overlap (FR-MOD-2
read as "per tier"). (*Tier*, not *layer*: a layer is finishes, furniture, electrical and so on, D17.) Openings and keep-clear regions are cut out of every zone automatically. This matches how a
designer works (a feature panel *on* a dado band) and keeps the geometry rectangles.

*Alternative:* a strict partition (no overlaps at all; a panel splits the band into pieces), simpler to compute but
awkward to edit.

**Defining a zone** (owner, 24 November 2026): in the Design view, the user draws a selection on the surface (a
rectangle select, or clicks on the cells of a grid) and defines the zone from it, or asks the agent to; the zone takes a
**name** and **tags** (its label, §2.1a), set by the agent or by click-and-edit. A drawn zone is clickable: a click
selects it, as an element.

### 3.3 Placements

A **placement** puts one **product** (in 0.1.0, a finish) in one zone, with: laying pattern, grout width and colour,
offset (x, y) of the pattern's origin, rotation (0 or 90 degrees) (FR-DES-2).

- **Laying patterns in 0.1.0 (DM-4, recommended):** stack (grid), offset by a fraction (half, third: brick bonds),
  each at 0 or 90 degrees. Herringbone and diagonal come later.
- **Validity (DM-2, recommended):** a product whose suitable surfaces exclude the zone's surface kind is **refused**
  (a wall-only tile on a floor, FR-CAT-6). A product whose **suitable use** is another room use (an outdoor tile in a
  bathroom) is **placed with a warning**, since a designer may choose it on purpose.
- **Setting-out** (owner, 24 November 2026): every tile, veneer or laminate placement has a setting-out, which is data: the **rule** that
  places the grid, the grid **origin** it gives in the face frame, and the **edge cuts** it leaves (left, right, bottom,
  top, in mm). Rules in 0.1.0: **centre** (a joint or a tile on the zone's centre line, whichever leaves the wider edge
  cuts; the default), **full start** (a full tile at a named edge: the floor of a wall, the top of a stair), and
  **manual** (the origin given). The grid's period is the **module**: the tile's size plus the joint (the grout width),
  or the size alone when the maker states it with the joint included. One grid per room or storey is wrong in every
  room (JohnnyHouse #1658): the setting-out belongs to each placement.
- **Courses and tiled height** are zones, not finish properties: a wall tiled to 2100 mm with a decor course is a field
  zone, a band zone for the decor course (its own placement) and an upper band in paint; openings and regions are cut
  out as everywhere (#1658 used the declaration's openings and regions unchanged).
- **By kind:** a tile takes the pattern, grout, offset and rotation above; a wood veneer or laminate takes a grain
  direction (0 or 90 degrees) and an offset, no grout; a paint takes nothing more.
- **Ways to place** (owner, 24 November 2026): a shortlisted finish is placed by telling the agent, by right-clicking
  a zone or surface ("Apply from the shortlist"), by pointing, or on a selection of several zones at once (one placement
  each, one step to undo). Each is the same `place product` command.
- A zone holds at most one placement; placing again replaces it (the replaced placement stays in the history).
- **Placements on parts come with the world builder** (DM-9, decided (owner, 23 November 2026)): a finish placed on a movable part (the
  louvre's slats, JohnnyHouse #1648) applies to every instance of the part, with its grain in the part's own frame so it
  follows a blade as it tilts. Parts arrive with their motion tables (PRD-parti D18); 0.1.0 places finishes on room
  surfaces only. JohnnyHouse's record of where each finish is used (`usage.json`) is read then.

### 3.4 Schemes and the shortlist

- **Scheme:** a named, saved set of placements (FR-DES-1). In 0.1.0 a scheme is **per room** (DM-5, recommended):
  saved from a room's zones, applied to the same room. Applying replaces those zones' placements in one step and can be
  undone in one step. Applying a scheme to *another* room (matching zones by kind and side) comes later.
- **Shortlist:** products set aside, each with a note (FR-DES-5) and, optionally, a **target** (owner, 24 November 2026): the room, the
  surface and the role (base, band, border, feature) it is chosen for, since twice JohnnyHouse had to ask which bathroom
  and which course a shortlisted tile was for (#1658). The shortlist can be filtered by target. A project's existing shortlist is read once, in `parti.shortlist/1` (JohnnyHouse's orchestrator translates its `selections.json`), into the
  shortlist so its existing shortlist is not lost (DN-first-consumer, need 3).

### 3.4a Quantities (owner, 24 November 2026)

Quantities are computed from the design, never entered: a pure function of the placements, their setting-outs and the
zones' visible cells (openings and keep-clear regions taken out, tile-behind regions kept).

- **Tiles:** counted on the placement's grid. **Counting rule, stated with every number** (JohnnyHouse #1658): every grid
  tile of which any part shows is one tile; a cut tile is a whole tile; offcuts are not reused. **Laid** = full + cut;
  **to buy** = laid plus the **wastage** (10 % by default, a project setting), rounded up **once per finish** (the
  default; per room is the alternative, and the record says which: 676 against 681 in #1658's marble). Boxes when the
  finish states its pieces per box.
- **Veneers, laminates, paint, metal, exposed:** the area in square feet (D25), with the wastage for sheet goods; paint
  in litres and sheets in pieces come when coverage and sheet sizes are in the catalogue.
- **Per zone, room and finish**, with the area (square feet), and what is **not included** stated (thresholds, steps,
  skirting unless zoned). Prices and cost estimates later: the record keeps a place for a price per finish.

### 3.5 Rules

- **D-1** Zone geometry lies inside its surface; zones of the same tier do not overlap (DM-1).
- **D-2** A placement names an existing zone and an existing product; validity per §3.3.
- **D-3** Every command carries the design revision it expects; a stale command is refused (R6).
- **D-4** Undo and redo apply to the user's own design changes within a session (FR-DES-4).

## 4. Catalogue (context)

**In 0.1.0, §4.4 only** (the product model and the classification, CR-PRT-005); the finishes catalogue (§4.1 to §4.3)
comes in 0.2.0 (PRD-parti D33).

### 4.1 Finishes

In 0.1.0 the catalogue holds **finishes** of seven **kinds**: **tile**, **wood veneer**, **laminate**, **paint**, **metal**,
**exposed** and **glaze** (owner, 23 and 24 November 2026),
from JohnnyHouse's second finishes database (#1648) beside its tiles. A finish has the fields of FR-CAT-1, and by kind:

| Kind | Carries | Placed with |
|---|---|---|
| tile | maker, size, thickness, finish class, swatch and room images; whether the stated size includes the joint (a house tile of 600 including a 4 mm joint) and the pieces per box when known | laying pattern, grout, offset, rotation (§3.3) |
| wood veneer, laminate | **source and licence** (library or maker, asset name, address, author, licence, date retrieved); the **source scan**: the real size the image covers (e.g. 1000 × 1000 mm), which way the grain runs in it, which maps exist (colour, roughness, relief) and which are used; the **stain** applied over the scan | grain direction (0 or 90 degrees in the face frame) and offset; no grout |
| paint | a colour and a sheen (matt, eggshell, satin, gloss); a maker's code when there is one; no image; optionally an **effect** (a special-effect paint: type, two colours, pattern size; JohnnyHouse PT-002 to PT-004) | nothing more |
| exposed | a material left as built, with no product: concrete, plaster, brick (JohnnyHouse CN-001); a colour and a roughness; no maker needed | nothing more |
| glaze | the glazed colour of sanitary ware: a colour, a sheen, a maker's code when there is one; no image; suitable for no wall or floor, so it waits for the fittings layer to be placed | — |
| metal | a treatment (plating, powder coat, brushed, anodised), a colour, metallic (0 to 1) and roughness (0 to 1); a maker's code when there is one; no image (JohnnyHouse MT-001, chromium-plated steel on the guard rails) (owner, 23 November 2026) | nothing more; mostly placed on parts, with the world builder (DM-9) |

**A finish is what is used: a source scan plus its stain** (DM-8, decided (owner, 23 November 2026)). Its colour is the colour after the
stain, so the catalogue shows the stained look; one scan can back several finishes (one pale scan, unstained and
stained dark). Scans are records of their own, with ids (JohnnyHouse `scans.ndjson`, #1651).

**A finish may be colour only** until its scan is chosen (JohnnyHouse LM-001, LM-002, WV-003, #1653): a wood veneer or
laminate without scan or stain is valid, carries just its colour, and is shown as **provisional** (like a block of
assumed quality, §2.4). **Furniture and cabinetry finishes** fall in three classes (owner, via JohnnyHouse #1653):
laminate, natural (wood veneer and, later, solid timber) and painted, which are kinds above.

**The renderers rebuild finishes from the catalogue, not from an export** (JohnnyHouse #1653, T4): glTF carries
colour values and images but never a material's node graph, so a procedural material (an effect paint, a marble-look
tile) arrives white, silently. Since the design holds the finishes (D17), each renderer's translator builds its
materials from the catalogue finish and checks after every import that no material in use is white without an image. Where a finish's assets sit in Unreal (texture, material instance, master material) is kept
as a **reference**, like CAD body names (§2.2).
Products are **read-only** in Parti: the catalogue is built by importing records, never edited by the user.

### 4.2 A target project's records: Parti's format, the project's translation (FR-CAT-4)

**Who translates** (owner, 24 November 2026): a target project's own records are translated by **that project's orchestrator agent**, never by
Parti. Parti provides the foundations: the **catalogue record format** (`parti.catalogue/1`, in the schema beside
`parti.building/1`), and the library's tools (`parti.catalogue`, D27) to validate the records, derive what can be derived
(picture orientation, colour tags, thumbnails), build the catalogue and report every record it could not take. It is
the same division as the building declaration (§2.4): Parti defines the format, the project fills it.

**The record format** `parti.catalogue/1`: newline-delimited JSON, one record per finish, with the fields of §4.1 by kind
(id, kind, maker or source and licence, name, series, set, role in set, pairs with, maker's code, product address,
suitable use, suitable surfaces, classification basis and confidence, size, whether it includes the joint, pieces per
box, thickness, finish class, colour, scan and stain, sheen and effect, treatment, metallic and roughness, images as
paths relative to the target project, asset references); scans as records of their own (`parti.scan/1`); and shortlist
entries (product, note, target) for a project's existing shortlist (`parti.shortlist/1`).

**JohnnyHouse, the first project** (evidence for the format, and guidance for its orchestrator's translation; none of it
in Parti's code):

| JohnnyHouse field | Parti | Note |
|---|---|---|
| `id`, `brand`, `name`, `series`, `set_id`, `role`, `pairs_with`, `sku`, `product_url` | id, maker, name, series, set, role in set, pairs with, maker's code, product address | as is |
| `zone` (bathroom, interior, outdoor), `rooms` | **suitable use** | the glossary's term; "zone" means a part of a surface in Parti |
| `surface`, `primary_surface` | suitable surfaces, filed under | |
| `classification.basis`, `.confidence` | how the suitable use was decided, and how sure | carried and shown, not hidden: 778 records were filed by a size rule |
| `size_mm`, `thickness_mm`, `finish`, `finish_class`, `body`, `design`, `colour.*` | size, thickness, finish, finish class, body, design, colour description | |
| `images.swatch`, `.room`, thumbnails | images | **referenced in place** in the target project, never copied (NFR-10) |
| (finishes database, #1648) `finishes.ndjson`: kind, source, licence, scan, stain, sheen, Unreal assets | kind, source and licence, source scan, stain, sheen, asset references | a second source beside the tiles, translated by JohnnyHouse's orchestrator; ids `WV-`, `LM-`, `PT-` kept |
| (missing) | **picture orientation** | `size_mm` does not say which way the swatch picture is laid (NW-021: 300 × 600, picture 1000 × 500 px, landscape). The library's catalogue build derives it from the picture's pixel size and records it; a record whose picture and size disagree beyond a tolerance is flagged (JohnnyHouse #1638). |

### 4.2a Records structured by the product model (DM-10)

From 0.1.0 a finish record is structured as the product model's parts (§4.4): **form** (size, thickness, whether the size
includes the joint, pieces per box), **build-up** (the finish on its material: a veneer on its board, a glaze on its
ceramic; one entry for a tile, a paint or an exposed material), **appearance** (colour, sheen, finish class, source scan
and stain, effect, metallic and roughness, images, asset references) and **quantities** (the counting unit, pieces per
box, coverage when known). The fields are those of §4.1 and the table above, grouped; the identity fields (id, kind,
class, maker or source and licence, name, series, set, maker's code, suitable use and surfaces) stay at the top. The
physical and interaction aspects come with the world builder.

### 4.3 Queries (FR-CAT-2, FR-CAT-3)

Filter on: kind, licence, suitable use, surface, maker, main colour, colour strength, lightness, warm or cool, pattern, finish class,
role in a set, size; free text on name, series and code; sorted round the colour wheel (with the colour-strength filter
the prototype found necessary). "Goes with": the maker's set and pairs, and finishes of complementary colour.
**Palette** (owner, 24 November 2026): a few colours, picked or taken from a scheme; a finish matches when its colour is
near one of them, whatever its kind. Results can be narrowed to a **product class** (§4.4).

### 4.4 The product model and the classification (DM-10; PRD-parti D32; owner, 24 November 2026)

**A product is its form, its build-up and its attributes by aspect.**

- **Form:** its shape and dimensions.
- **Build-up:** its materials, coatings and finishes in order from the core outwards (concrete, plaster, paint). The
  outermost exposed one gives the rendered look; the whole build-up gives the physical facts and the quantities (an
  unpainted plastered concrete column looks like its plaster and is as strong as its concrete). *Build-up*, not *layer*,
  which names a product layer.
- **Material:** what an element or a part is made of (teak, MDF, brick, concrete, granite, ceramic, glass, steel). Every
  material carries its own properties (texture, colour, roughness, sheen; later density, fire class), which an element
  made of it takes **by default, unless updated separately**: a finish placed on it, or a property changed on that
  element, overrides the default there only. So assigning a material brings a default finish (natural, or *exposed*)
  and its texture.
- **Texture:** the image maps a renderer uses (colour, normal, roughness) with the real size they cover. A source scan
  is one kind; a finish is a texture plus its stain (DM-8).
- **Aspects:** sets of attributes each module reads: **appearance** (the renderers), **physical** (Unreal's world
  physics), **quantities** (the bill of materials), **interaction** (motion, states, what can be picked up or opened).
  One schema per aspect, shared by every product layer; attributes are **optional, with defaults**, so a static product
  carries few physical attributes and an object one can pick up carries them all. Most state changes are updates of
  these attributes.
- **Applications only realise it:** a CAD material, a Blender or Unreal shader is its translator's realisation of the
  material, finish and texture, kept linked by id (PRD-parti D29).
- **Plain words** ("light UV-filtered pane glass", "red stainless-steel water bottle"), from the user, a drawing note or a
  maker's sheet, are decomposed by the agent into these parts, with the library's decomposers (PRD-parti D21, D27), as
  records the user confirms.

**The product classification** (PRD-parti D32): one versioned tree of **product classes** in Parti's words. A class
defines the attributes of each aspect, inherited down the tree; it drives the tagging of CAD objects (D31), the asset
browser's tree and filters, the grouping of bills of materials by trade, the agent's context and search. Each class maps
to an IFC entity type and predefined type (IFC 4.3, ISO 16739-1:2024; `IfcCovering` · `FLOORING`); attributes map to
IFC property sets by a declared mapping; Uniclass 2015 or OmniClass codes may be carried as references. A new class is a
change the owner approves. **0.1.0 ships the first level of every branch** (owner, 24 November 2026, PRD-parti D33), so
the model's objects can be tagged: Structure, Openings, Joinery, Sanitary ware, Lighting, Furniture, Services, Landscape,
each with its first-level classes, and the **Finishes** branch (Tile, Wood veneer, Laminate, Paint, Metal, Exposed,
Glaze; mapped to `IfcCovering`), each class mapped to its IFC entity type, as data in the schema (CR-PRT-005). Deeper
levels and the materials beyond those named grow with their layers (0.2.0, 0.5.0).

## 5. Session (context) and the conditions

- **Session:** in 0.1.0 one participant (a user) and the mock scene. It holds the **selection** (a surface or a zone,
  picked in the page or in the mock scene; FR-SEL-1 to FR-SEL-3).
- **Conditions** (world builder, D18; **from 0.4.0**, PRD-parti D33): time of day, date, place, weather (clear,
  overcast, rain). They are first **state only**: set from the page or `parti-axi`, shared with the mock scene, stored with the session; nothing is
  rendered from them until the Unreal plugin exists.
- **Interaction events** (owner, 24 November 2026; PRD-parti D29): a pointing, a selection or a clip in the page is an
  event carrying its elements (ids, names, kinds, tags), the area, the world bounds, the CAD references, the view and
  the step. It changes nothing in the design: it is held in the session as the shared context (for the workflow and,
  later, the agent), outside the design's history, so undo and versions stay clean. Collecting it for telemetry comes
  with Nai (D9).

## 6. Versioning in 0.1.0 (D19)

**Model revisions** (§2.6): a model read again records a model revision with its changes; the derived declaration's
draft is refreshed from it and what changed is shown for the user to confirm, after which it is a building revision as
below. The forward chain into the design (the table below) applies from 0.2.0, when the design exists.

When a declaration is imported again (§2.2), Parti records a building revision and follows the forward chain inside
this slice:

| Change in the building | Effect on the design | Handling |
|---|---|---|
| Surface removed | its zones and placements have nowhere to go | **orphaned**: listed as follow-up actions; the user re-places or drops them |
| Surface resized | zones may now lie outside it | zones outside are flagged; the user resizes or removes them |
| Opening or region added, moved or resized | cut-outs change | applied at once (cut-outs are computed); placements stay |
| Surface added | gets its field zone | applied at once |

Nothing is changed silently: every flagged item is a follow-up action shown in the page and listed by `parti-axi`.

## 7. Messages (the published language, R5)

The schema (`schema` component) defines, versioned:

| Kind | 0.1.0 messages |
|---|---|
| Commands | `import building`; `define zone`, `resize zone`, `remove zone`, `label zone`; `place product`, `clear zone`; `save scheme`, `apply scheme`; `add to shortlist`, `remove from shortlist`; `undo`, `redo`; `select`; `set time`, `set weather` |
| Events | `building revised` (with its changes); `zone defined / resized / removed`; `product placed / cleared`; `scheme saved / applied`; `shortlisted / unshortlisted`; `selection changed`; `conditions changed`; `follow-up raised / resolved`; `zone labelled` |
| Interaction events (`parti.interaction.*/1`) | `pointed`, `selected`, `clipped`: each with its elements, area, world bounds, CAD references, view and step (§5) |
| Workflow (§11) | commands `start step`, `complete step`, `tick to-do`, `set focus`; events `step started / completed`, `to-do added / ticked`, `focus set`; the **workspace commands** (`show` a view or an editor, with its subject and title) and the asset browser's **signals** (`set filters`, `set palette`, `mark assets`, `note`) |
| Queries | `building`, `surface`, `design` (whole or per room), `catalogue` (filtered), `goes with`, `shortlist`, `follow-ups`, `history` |
| Plan onboarding (§1; 0.1.0) | commands `register source`, `calibrate sheet`, `record data table`; events `source registered`, `source revised`, `sheet calibrated`, `data table recorded`; query `sources` |
| Model (§2.6; 0.1.0) | commands `read model`, `classify object`; events `model read`, `model revised` (with its changes), `model read failed`, `object classified`; query `model` |
| Declare (§2.7; 0.1.0) | commands `derive declaration`, `confirm declaration` (whole or per surface); events `declaration derived`, `declaration confirmed` |

**Which release carries which** (PRD-parti D33): 0.1.0 carries the Building, Session (`select`, `selection changed`),
interaction, Workflow, Plan onboarding, Model and Declare messages; the Design and Catalogue messages come with 0.2.0,
the conditions with 0.4.0.

Every command carries a command id and the expected revision; every event carries an id and a sequence number per
aggregate (R6).

**The schema grows with the releases** (owner, 23 November 2026). The messages above are 0.1.0's; each later release
adds those its interactivity needs, among them: navigation (*go to* a room, viewpoint or surface; set a view, D18),
the assistant's questions and answers and the actions they take (D24), motion inputs (D18), interaction events and
the applied-revision acknowledgements from the Unreal plugin (Q17), telemetry, offers and client selections (D22),
and the guide's speech and text (D22). The storage (§8) grows with them, as further event logs behind the same ports.

## 8. Storage in 0.1.0 (Q11)

In the folder the configuration names inside the target project:

```text
parti/
  building/declaration.json     written by the target project (§2.4)
  events/building.ndjson        building revisions (one JSON event per line)
  events/design.ndjson          the design's events
  events/workflow.ndjson        the workflow run's events (§11)
  events/sources.ndjson         sources, calibrations and data tables (§1)
  events/model.ndjson           model reads and revisions (§2.6)
  model/inventory.json          snapshot of the latest model inventory (parti.model/1)
  design.json                   snapshot of the current design: what Blender and other scripts read (FR-DES-3)
  shortlist.json                snapshot of the shortlist
```

The event logs are the truth; the snapshots are rebuilt from them and can be deleted. Appends are atomic (write, then
rename). All of it sits behind the design-store and building-store ports, so Nai replaces it later (D9).

## 9. Decisions for the owner

| # | Decision | Recommended |
|---|---|---|
| DM-1 | Zone overlaps | **Decided (owner, 23 November 2026):** tiers: field, then bands and borders, then panels and areas; the upper shows; no overlaps within a tier |
| DM-2 | Product not suited to the surface or the room | **Decided (owner, 23 November 2026):** refuse a wrong surface kind; warn on another room use |
| DM-3 | Where the building comes from in 0.1.0 | **Decided (owner, 23 November 2026):** the declaration file only; Parti reads it, never edits it |
| DM-4 | Laying patterns in 0.1.0 | **Decided (owner, 23 November 2026):** stack and offset bonds (half, third), at 0 or 90 degrees |
| DM-5 | Scheme scope | **Decided (owner, 23 November 2026):** per room in 0.1.0; across rooms later |
| DM-7 | A face that is not one plane (a step where a column meets a wall) | **Decided (owner, 23 November 2026):** declare one flat rectangle at the main plane with optional `steps`; Parti warns on the zones and placements crossing a step; layout on stepped faces later |
| DM-8 | A stained veneer | **Decided (owner, 23 November 2026):** a finish is a source scan plus its stain; the catalogue shows the stained look; one scan can back several finishes |
| DM-9 | Placements on parts | **Decided (owner, 23 November 2026):** with the world builder; 0.1.0 places finishes on room surfaces only. Widened by PRD-parti D31 (owner, 24 November 2026): a product's parts and faces and a surface's pieces are addressable and take their own finish, with the CAD connection |
| DM-6 | Face frame origin | **Decided (owner, 23 November 2026):** bottom-left as seen from inside the room; x along the face, y up |
| DM-10 | Material, texture and the product model | **Decided (owner, 24 November 2026):** a product is its form, build-up and attributes by aspect (appearance, physical, quantities, interaction), optional with defaults; materials carry their own properties, taken by default unless updated separately; textures are the renderers' maps; 0.1.0's finish records are structured this way (§4.2a, §4.4) |
| DM-12 | The model and its inventory | **Decided (owner, 24 November 2026, with the roadmap, PRD-parti D33):** the CAD model is read live into a model inventory (`parti.model/1`) and read again when its revision moves; its objects are products of their class (stored class, else project rules, else unclassified), with materials taken by default unless updated, and faces as lesser primitives; a Parti id kept in the design survives renames (§2.6) |
| DM-11 | The workflow in 0.1.0 | **Decided (owner, 24 November 2026):** the Workflow context's slice of §11: a definition shipped with the template and an event-sourced run; the step drives the workspace until the agent does |

## 10. Requirements traced

FR-MOD-1 to 3 (§2, §3.2), FR-DES-1 to 5 (§3), FR-CAT-1 to 6 (§3.3, §4), FR-SEL-1 to 3 (§5), FR-STA-1 to 3 (§5, §7),
FR-AXI-4 and FR-AXI-5 (through §7), NFR-1, NFR-2, NFR-10 (§1, §4.2, §8), D17, D19 (§2.2, §6), Q9, Q11;
D22, D29, D31, D32 (§2.1a, §3.2, §4.4, §5, §7), D26, FR-WF-14, FR-WF-15 (§11).

## 11. Workflow (context): the 0.1.0 slice (DM-11; owner, 24 November 2026)

In 0.1.0 the workflow step drives the Project Environment's workspace (PRD-parti D22); the project agent takes over with
the harness, issuing the same commands.

- **Workflow definition:** data shipped with the project template (residential, single-family home; D30): the seven
  phases (D26) and, in 0.1.0, the steps of the first three (owner, 24 November 2026, PRD-parti D33):
  **Plan onboarding**: intake the sources (K1), calibrate each sheet, record the data tables (K1);
  **Model**: build from data, one step per feature group (K2), consolidate (K3);
  **Declare**: derive the declaration (K4), confirm it (a review gate).
  Each step runs the step cycle (read the sources, write the data, generate, apply, check against the expected numbers,
  checkpoint, record), names its checklist and checks, and the view or editor it opens in the workspace. The Design
  phase's steps (catalogue intake, choose, place and set out, BOM, trial in the walkthrough) come with 0.2.0.
- **Workflow run:** event-sourced like the rest: step started, step completed, to-do added, to-do ticked, and the
  **focus** (room › surface) the step works on. A project that imports a declaration it wrote itself shows Plan onboarding, Model and
  Declare as done.
- **Checklist items** the domain can check are ticked by their check (a finish in every zone, no sliver cut under 50 mm,
  the BOM stated with its counting rule); the rest by the user (FR-WF-15).
- **The page:** in the workflow panel the user picks a step or completes it; its view or editor opens in the workspace,
  titled by what it shows (*Design · Bath 1 › East wall*); selecting a surface sets the focus; the step *choose* opens
  the asset browser filtered for its target (the browser's signals, §7).
- **Workspace commands:** what to show (a view: the project, the BOM, the walkthrough; or an editor of what Parti owns:
  labels and tags, zones and placements on a surface, the settings), for which subject, with its title. Never the
  geometry, which stays in the CAD, Blender or Unreal.
- **Rules:** **W-1** one step is active at a time; **W-2** a step completes only when its checklist's checked items pass,
  or the user overrides with a caveat (D26); **W-3** the run's events append to their own log (§8).

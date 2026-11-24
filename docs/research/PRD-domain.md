# PRD — The domain: building, design and catalogue (slice for 0.1.0)

**Version:** 0.2 (reviewed; revised 24 November 2026)
**Date:** 2026-11-23
**Status:** Reviewed by the owner (23 November 2026): DM-1 to DM-9 decided; §4 and §5–6 agreed; revised 24 November 2026 (finish kinds, setting-out and quantities, the record formats a project's own agent fills). Written for the slice release 0.1.0 needs (D23, `../Architecture.md`, Documents); it grows with each
release. Items marked **DM-n** are decisions for the owner; the text shows the recommended option.
**Author:** Parti orchestrator (vidushi-parti), with the owner
**Builds on:** `PRD-parti.md` (D17, D19, D22, D23, §4, Q9, Q11), `DN-ubiquitous-language.md`, `DN-test-strategy.md`
**Evidence:** JohnnyHouse's answers on its bathrooms and workflow (Sandesh #1631, #1633), its tile records
(`DN-first-consumer-johnnyhouse.md`), its RUNBOOK

## Change Control

| Date | Change |
|---|---|
| 2026-11-23 | First draft, for 0.1.0. |
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

Release 0.1.0 is the finish tool end to end with the mock scene (PRD-parti Q9): a target project declares its rooms
and surfaces; the user browses and filters a catalogue of finishes, selects a surface, divides it into zones, places
finishes, saves and reloads, and sets the time of day and the weather as state; all of it through the page and through
`parti-axi`, stored locally as JSON events. JohnnyHouse's four bathrooms are the first real data; the tests use
synthetic buildings and products (NFR-10).

This slice therefore covers four contexts in part (Building, Design, Catalogue, Session) and the setting of the world
builder. It also covers the **setting-out** of each placement and the **quantities** it needs (owner, 24 November 2026), since placing a finish at
true scale with a setting-out gives both the picture and the count (JohnnyHouse #1658). It leaves out: other layers
than finishes, prices and cost estimates, offers and client bundles, the
workflow, and the agent session (all later releases).

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

## 3. Design (context, core)

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

### 4.3 Queries (FR-CAT-2, FR-CAT-3)

Filter on: kind, licence, suitable use, surface, maker, main colour, colour strength, lightness, warm or cool, pattern, finish class,
role in a set, size; free text on name, series and code; sorted round the colour wheel (with the colour-strength filter
the prototype found necessary). "Goes with": the maker's set and pairs, and finishes of complementary colour.

## 5. Session (context) and the setting

- **Session:** in 0.1.0 one participant (a user) and the mock scene. It holds the **selection** (a surface or a zone,
  picked in the page or in the mock scene; FR-SEL-1 to FR-SEL-3).
- **Setting** (world builder, D18): time of day, date, place, weather (clear, overcast, rain). In 0.1.0 these are
  **state only**: set from the page or `parti-axi`, shared with the mock scene, stored with the session; nothing is
  rendered from them until the Unreal plugin exists.

## 6. Versioning in 0.1.0 (D19)

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
| Commands | `import building`; `define zone`, `resize zone`, `remove zone`; `place product`, `clear zone`; `save scheme`, `apply scheme`; `add to shortlist`, `remove from shortlist`; `undo`, `redo`; `select`; `set time`, `set weather` |
| Events | `building revised` (with its changes); `zone defined / resized / removed`; `product placed / cleared`; `scheme saved / applied`; `shortlisted / unshortlisted`; `selection changed`; `setting changed`; `follow-up raised / resolved` |
| Queries | `building`, `surface`, `design` (whole or per room), `catalogue` (filtered), `goes with`, `shortlist`, `follow-ups`, `history` |

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
| DM-9 | Placements on parts | **Decided (owner, 23 November 2026):** with the world builder; 0.1.0 places finishes on room surfaces only |
| DM-6 | Face frame origin | **Decided (owner, 23 November 2026):** bottom-left as seen from inside the room; x along the face, y up |

## 10. Requirements traced

FR-MOD-1 to 3 (§2, §3.2), FR-DES-1 to 5 (§3), FR-CAT-1 to 6 (§3.3, §4), FR-SEL-1 to 3 (§5), FR-STA-1 to 3 (§5, §7),
FR-AXI-4 and FR-AXI-5 (through §7), NFR-1, NFR-2, NFR-10 (§1, §4.2, §8), D17, D19 (§2.2, §6), Q9, Q11.

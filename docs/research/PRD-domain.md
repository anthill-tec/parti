# PRD — The domain: building, design and catalogue (slice for 0.1.0)

**Version:** 0.1 (draft for the owner's review)
**Date:** 2026-11-23
**Status:** Reviewed by the owner (23 November 2026): DM-1 to DM-6 decided as recommended; §4 and §5–6 agreed. Written for the slice release 0.1.0 needs (D23, `../Architecture.md` §10); it grows with each
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
builder. It leaves out: other layers than finishes, quantities and bills of materials, offers and client bundles, the
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
  end points in plan and its floor level; for a floor, its outline), so the scene and Blender can find it and
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
The configuration written by `parti-axi init` holds the preferences, with those defaults.

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
      "anchor": { "start": [5680, 230], "end": [5680, 3700], "z": 3100 },
      "references": { "cad": ["W_FF_bath_div"] },
      "openings": [],
      "regions": [
        { "id": "FF_bath1.wall.E/mirror", "kind": "keep-clear", "x": 900, "y": 1050, "width": 700, "height": 800,
          "fitting": "MR_FF_bath1" }
      ],
      "quality": { "openings": "measured", "regions": "from fitting table" }
    }
  ]
}
```

(The example follows JohnnyHouse's first-floor bath 1: its east face is one side of `W_FF_bath_div`, shared with bath 2,
and carries the mirror; its ventilator is on the south face. The world frame is JohnnyHouse's own.) Openings may also be given in world
coordinates, with `"frame": "world"`; Parti converts them. Each block may carry a **quality** note (measured, derived,
assumed), shown to the user, because a target project's data is often partly known (JohnnyHouse's first-floor doors).

### 2.5 Rules

- **B-1** Ids are unique within the building; every surface names an existing room; every opening and region lies
  inside its surface.
- **B-2** Openings on one surface do not overlap one another.
- **B-3** A declaration that breaks B-1 or B-2 is refused as a whole, with every fault listed; the previous revision
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
- A zone holds at most one placement; placing again replaces it (the replaced placement stays in the history).

### 3.4 Schemes and the shortlist

- **Scheme:** a named, saved set of placements (FR-DES-1). In 0.1.0 a scheme is **per room** (DM-5, recommended):
  saved from a room's zones, applied to the same room. Applying replaces those zones' placements in one step and can be
  undone in one step. Applying a scheme to *another* room (matching zones by kind and side) comes later.
- **Shortlist:** products set aside, each with a note (FR-DES-5). JohnnyHouse's `selections.json` is read once into the
  shortlist so its existing shortlist is not lost (DN-first-consumer, need 3).

### 3.5 Rules

- **D-1** Zone geometry lies inside its surface; zones of the same tier do not overlap (DM-1).
- **D-2** A placement names an existing zone and an existing product; validity per §3.3.
- **D-3** Every command carries the design revision it expects; a stale command is refused (R6).
- **D-4** Undo and redo apply to the user's own design changes within a session (FR-DES-4).

## 4. Catalogue (context)

### 4.1 Finishes

In 0.1.0 the catalogue holds **finishes** (tiles; paint later, FR-CAT-5). A finish has the fields of FR-CAT-1.
Products are **read-only** in Parti: the catalogue is built by importing records, never edited by the user.

### 4.2 Reading a target project's records (FR-CAT-4)

Each source has its own **translator**. JohnnyHouse's tile records (`tiles.ndjson`, `tile.schema.json`) are the first.
Notable mappings:

| JohnnyHouse field | Parti | Note |
|---|---|---|
| `id`, `brand`, `name`, `series`, `set_id`, `role`, `pairs_with`, `sku`, `product_url` | id, maker, name, series, set, role in set, pairs with, maker's code, product address | as is |
| `zone` (bathroom, interior, outdoor), `rooms` | **suitable use** | the glossary's term; "zone" means a part of a surface in Parti |
| `surface`, `primary_surface` | suitable surfaces, filed under | |
| `classification.basis`, `.confidence` | how the suitable use was decided, and how sure | carried and shown, not hidden: 778 records were filed by a size rule |
| `size_mm`, `thickness_mm`, `finish`, `finish_class`, `body`, `design`, `colour.*` | size, thickness, finish, finish class, body, design, colour description | |
| `images.swatch`, `.room`, thumbnails | images | **referenced in place** in the target project, never copied (NFR-10) |
| (missing) | **picture orientation** | `size_mm` does not say which way the swatch picture is laid (NW-021: 300 × 600, picture 1000 × 500 px, landscape). The translator derives it from the picture's pixel size and records it; a record whose picture and size disagree beyond a tolerance is flagged (JohnnyHouse #1638). |

### 4.3 Queries (FR-CAT-2, FR-CAT-3)

Filter on: suitable use, surface, maker, main colour, colour strength, lightness, warm or cool, pattern, finish class,
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
| DM-6 | Face frame origin | **Decided (owner, 23 November 2026):** bottom-left as seen from inside the room; x along the face, y up |

## 10. Requirements traced

FR-MOD-1 to 3 (§2, §3.2), FR-DES-1 to 5 (§3), FR-CAT-1 to 6 (§3.3, §4), FR-SEL-1 to 3 (§5), FR-STA-1 to 3 (§5, §7),
FR-AXI-4 and FR-AXI-5 (through §7), NFR-1, NFR-2, NFR-10 (§1, §4.2, §8), D17, D19 (§2.2, §6), Q9, Q11.

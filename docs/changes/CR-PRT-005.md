# CR-PRT-005 — Catalogue context: the product model and the classification

**Status:** PENDING (spec drafted 2026-11-23; rewritten 2026-11-24 for the roadmap and DM-10; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten for the narrowed scope, the product model (DM-10) and the classification (the first level of every branch and the Finishes branch, each mapped to IFC; PRD-domain §4.4), with the test products moved here from CR-PRT-003; the queries and *goes with* moved to CR-PRT-011 (0.2.0).
**Priority:** High
**Depends on:** CR-PRT-002, CR-PRT-003
**Labels:** domain, catalogue, schema
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/PRD-domain.md` §4.2a, §4.4 (DM-10), §2.6 (DM-12); `docs/research/PRD-parti.md` D31, D32, D33, D40, D46; FR-CAT-1

## Context

Release 0.1.0 builds the building from CAD (PRD-parti D33). The model's objects are **products of their class** (D31,
D32): to tag them, the **classification** must exist, and to hold what they are made of, the **product model** must.
The asset browser (D40) later browses the same tree, layer by layer; the finishes catalogue, its queries and *goes with*
come with it in 0.2.0 (CR-PRT-011, CR-PRT-014).

This CR gives the classification as **data in the schema** and the product model as **types and pure functions** in the
domain (R1: no input or output, no imports beyond `@parti/schema`).

## Scope

### §S1 The classification (data)

`packages/schema/v1/classification.json` (`$id` `parti.catalogue.classification/1`, CR-PRT-002's pattern), validated by
`classification.schema.json`, read by `@parti/schema` and by `parti.schema` from the same file (CR-PRT-002's route).
One versioned tree (`version: 1`) of **product classes**, each with: `id` (dotted, `<branch>.<class>`), `name` (Parti's
words), `parent`, `ifc` (`entity`, `predefinedType`, and `objectType` when the type is `USERDEFINED`), optional
`references` (Uniclass 2015 or OmniClass codes), and `attributes` per aspect (§S2), inherited down the tree.

**Proposed classes of version 1** (for the owner's approval at the spec review: a new class is his change, D32). Every
IFC name below is from the IFC 4.3 schema's published enumerations (buildingSMART, `IFC4.x-development`); the gap
analysis re-checks them.

| Branch | First-level classes → IFC entity · predefined type |
|---|---|
| **Structure** | Wall → `IfcWall` · `STANDARD`; Partition → `IfcWall` · `PARTITIONING`; Slab → `IfcSlab` · `FLOOR`; Roof slab → `IfcSlab` · `ROOF`; Roof → `IfcRoof` · `NOTDEFINED`; Column → `IfcColumn` · `COLUMN`; Beam → `IfcBeam` · `BEAM`; Lintel → `IfcBeam` · `LINTEL`; Stair → `IfcStair` · `NOTDEFINED`; Ramp → `IfcRamp` · `NOTDEFINED`; Railing → `IfcRailing` · `BALUSTRADE` |
| **Openings** | Door → `IfcDoor` · `DOOR`; Gate → `IfcDoor` · `GATE`; Window → `IfcWindow` · `WINDOW`; Skylight → `IfcWindow` · `SKYLIGHT`; Opening → `IfcOpeningElement` · `OPENING`; Recess → `IfcOpeningElement` · `RECESS` |
| **Joinery** | Kitchen cabinet, Wardrobe, Vanity unit → `IfcFurniture` · `USERDEFINED` (their names as object type); Shelving → `IfcFurniture` · `SHELF`; Worktop → `IfcSystemFurnitureElement` · `WORKSURFACE`; Panelling → `IfcCovering` · `CLADDING`; Skirting → `IfcCovering` · `SKIRTINGBOARD` |
| **Sanitary ware** | WC → `IfcSanitaryTerminal` · `TOILETPAN`; Wash basin → `WASHHANDBASIN`; Shower → `SHOWER`; Bath → `BATH`; Sink → `SINK`; Bidet → `BIDET`; Tap → `IfcValve` · `FAUCET`; Floor drain → `IfcWasteTerminal` · `FLOORTRAP` |
| **Lighting** | Downlight → `IfcLightFixture` · `DIRECTIONSOURCE`; Pendant, Wall light, Lamp → `IfcLightFixture` · `POINTSOURCE`; Strip light → `IfcLightFixture` · `USERDEFINED` |
| **Furniture** | Seat → `IfcFurniture` · `CHAIR`; Sofa → `SOFA`; Table → `TABLE`; Desk → `DESK`; Bed → `BED`; Storage → `USERDEFINED` |
| **Services** | Power outlet → `IfcOutlet` · `POWEROUTLET`; Data outlet → `IfcOutlet` · `DATAOUTLET`; Switch → `IfcSwitchingDevice` · `TOGGLESWITCH`; Dimmer → `IfcSwitchingDevice` · `DIMMERSWITCH`; Air terminal → `IfcAirTerminal` · `NOTDEFINED`; Fan → `IfcFan` · `NOTDEFINED`; Appliance → `IfcElectricAppliance` · `NOTDEFINED` (its predefined type from the product: `FRIDGE_FREEZER`, `DISHWASHER`, …) |
| **Landscape** | Planting → `IfcGeographicElement` · `VEGETATION`; Terrain → `IfcGeographicElement` · `TERRAIN`; Paving → `IfcSlab` · `PAVING`; Fence → `IfcRailing` · `FENCE` |
| **Finishes** | Tile, Wood veneer, Laminate, Paint, Metal, Exposed, Glaze → `IfcCovering`, the predefined type **by the surface covered**: floor `FLOORING`, wall `CLADDING`, ceiling `CEILING` |

The branch roots carry no IFC mapping of their own. An object the project's rules cannot place is **unclassified**
(PRD-domain §2.6, M-2), never put in a class by guess.

### §S2 The product model (types)

`packages/domain/src/catalogue/`, per PRD-domain §4.4 and §4.2a:

- **`Product`**: identity (`id`, `class`, `name`, maker or source and `licence`, `series`, `set`, maker's code, suitable
  use and surfaces), **`animatable`** (a core attribute, defaulted by the class: true for appliances, cabinetry and
  furniture, doors and gates; D46) with its **`motion`** slot (a motion definition's reference, empty in 0.1.0), **`form`** (shape and dimensions; for tiles `sizeIncludesJoint`, `piecesPerBox`), **`buildUp`**
  (materials, coatings and finishes from the core outwards, each naming its `Material`), and **`aspects`**:
  `appearance` (colour, sheen, finish class, `scan` and `stain`, `effect`, `metallic`, `roughness`, images and asset
  references, never data), `quantities` (counting unit, pieces per box, coverage), and `physical` and `interaction`,
  present as optional, empty in 0.1.0 (they come with the world builder).
- **`Material`** (teak, MDF, brick, concrete, granite, ceramic, glass, steel, …) with its own appearance properties;
  **`Texture`** (maps and the real size they cover; a source scan is one kind).
- **Finishes** keep their kinds' fields (PRD-domain §4.1), now grouped: `kind` (`tile` | `wood-veneer` | `laminate` |
  `paint` | `metal` | `exposed` | `glaze`) agrees with the class (`finishes.<kind>`). A finish is a scan plus its stain
  (DM-8): its main colour is the colour after the stain; a veneer or laminate without a scan is valid and `provisional`.

### §S3 Functions (pure)

- `classes()`, `classById(id)`, `ancestors(id)`, `isA(id, ancestorId)`.
- `ifcOf(id, context?)`: the class's entity, predefined type and object type; for a finish, `context.surface` gives the
  predefined type (§S1).
- `attributesFor(id, aspect)`: the aspect's attributes with their defaults, inherited down the tree, the nearest class's
  definition winning.
- `effective(material, overrides)`: a property of an element takes the material's value **by default, unless updated**
  on that element (DM-10); removing an override restores the default.
- `validateProduct(value)` → `{ ok: true, product } | { ok: false, faults }` with the fault codes `missing-field`,
  `invalid-value`, `unknown-class`, `class-mismatch`.

### §S4 Test products (moved here from CR-PRT-003; owner, 24 November 2026)

`makeProducts(n, seed)` in `packages/schema/src/test-support/products.ts` (CR-PRT-001's location), with the product
record it builds, so the two never drift. Deterministic by seed. Every open or continuous field gets an enumerated set
or buckets (licence, maker, size, lightness, main colour, colour strength, role in a set, product class), so "every
value appears" is testable; the classes drawn cover every first-level class of every branch.

## Acceptance criteria

- [ ] `classification.json` validates against `classification.schema.json`; ids are unique; every `parent` exists; the tree has no cycle.
- [ ] The nine branches exist (Structure, Openings, Joinery, Sanitary ware, Lighting, Furniture, Services, Landscape, Finishes), and each has the first-level classes the owner approved at the spec review.
- [ ] Every class below a branch root names an IFC entity and a predefined type found in the test's list of IFC 4.3 names (names only, taken from the published enumerations); every `USERDEFINED` type carries an `objectType`.
- [ ] `ifcOf("finishes.tile", { surface: "floor" })` gives `IfcCovering` · `FLOORING`; on a wall `CLADDING`; on a ceiling `CEILING`.
- [ ] `isA("sanitary-ware.wc", "sanitary-ware")` is true; `isA("sanitary-ware.wc", "furniture")` is false; `ancestors` returns the chain to the root.
- [ ] An attribute with a default on a branch applies to its classes; a class redefining it wins for itself and its descendants only.
- [ ] Version 1's class ids are pinned in a test: adding, removing or renaming a class fails it until the version and the pinned set change together (a new class is the owner's change, D32).
- [ ] A Python test loads the same file through `parti.schema` and gets the same class ids and IFC mappings as the TypeScript test (a shared expected list).
- [ ] `effective(teak, { sheen: "gloss" })` gives teak's colour and a gloss sheen; with the override removed, teak's sheen.
- [ ] A product of an animatable class (`openings.door`, an appliance, furniture) is `animatable` by default and one of `finishes.tile` is not; a product may override its class's default; a `motion` reference on a product that is not animatable is invalid (`not-animatable`).
- [ ] A product naming an unknown class is invalid (`unknown-class`); a paint whose class is `finishes.tile` is invalid (`class-mismatch`).
- [ ] A paint without `sheen` is invalid (`missing-field`); a metal with `metallic` 1.5 is invalid (`invalid-value`); a paint `effect` of one colour is invalid (`invalid-value`).
- [ ] Two veneers sharing a scan with different stains are two products whose main colours are their stains' colours, naming the same `scan.id`; a laminate with a colour and no scan is valid and `provisional`, and with a scan is not.
- [ ] `makeProducts(200, 1)` is equal on two calls; every product it makes is valid; every enumerated value and every first-level class appears in it.
- [ ] Caller-existence: `isA` and `ifcOf` are called from `packages/domain/src/building` (CR-PRT-026), and the classification is read through `parti.schema` by the library's model inventory (CR-PRT-025); reviewed at their VERIFY.

## Estimated size

8 points.

## Non-goals

The finishes catalogue, its build, queries, palette and *goes with* (CR-PRT-011, 0.2.0); the asset browser (CR-PRT-014,
0.2.0); levels below the first and the physical and interaction attributes (with their layers and the world builder); the
motion definitions themselves (CR-PRT-050, 0.4.0, D46);
classifying a model's objects (CR-PRT-026); the IFC translator (CR-PRT-058, through Nai).

# DN — The pipeline prototype: what JohnnyHouse worked out by hand

**Date:** 2026-11-22
**Status:** Reference for `PRD-parti.md` §8A. A map of the prototype, not a design for Parti's tools.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)
**Related:** `PRD-parti.md`, `DN-first-consumer-johnnyhouse.md`

## Why this note exists

JohnnyHouse (`/home/antonyj/Documents/bals/JohnnyHouse`) was run as a prototype, without Model B: no CRs, no
test suite, scripts written as the need arose. It took a house from the architect's drawings to a parametric
CAD model, a Blender scene with stills and films, and the start of an Unreal walkthrough. The owner's decision
(22 November 2026) is that Parti turns that path into a guided workflow for agents and a maintained toolbase.
This note tells Parti's orchestrator where everything is. Read the sources; do not copy them wholesale: they
carry one house's names and numbers throughout.

## Sources to read (all under the JohnnyHouse folder)

| Path | What it is |
|---|---|
| `docs/research/RUNBOOK.md` | The method, the phases P0 to P12 with their checkpoints, the owner review gates G1 to G6, the tools table, the caveats (§4), the working loop with the owner (§5) and a first list of steps that could become skills (§6). The primary source. |
| `docs/research/PRD-001-model-spec.md` | What the model had to be. |
| `docs/research/DN-001` … `DN-009` | Per topic: drawings and calibration, levels, structural grid, construction standards, facade and materials, print and Blender pipeline, window schedule, cabinets, furniture. |
| `docs/research/progress/LOG.md` | One line per step: what changed, how it was checked, what was produced. |
| `docs/research/render-pipeline-notes.md` | State after the Blender import, materials still to do. |
| `cad/gen/` | About 30 Python generators: data tables (`house_data.py`) turned into SolidCraft command batches (`build.py <phase>`), plus one script per feature group (joinery, rails, louvres, cabinets, baths, skylight, …) and checks (`check_joins.py`). |
| `cad/checkpoints/` | Saved model per checkpoint (CP-00 to CP-123). |
| `blender/scripts/` | `johnny_materials.py`, `johnny_lighting.py`, `johnny_cameras.py`, `johnny_site.py`, `johnny_planting.py`, `johnny_furniture.py`, `johnny_fittings.py`, `johnny_rig.py`, `johnny_walk.py`, `johnny_movie.py`, `render_stills.py`, `extract_reference_textures.py`. |
| `blender/assets/reference/tiles/tools/` | The tile database tools: `normalise_makers.py`, `build_tile_db.py`, `build_browser.py`, `serve_browser.py`. |

## The pipeline as run

| Step | In the prototype | Checks that proved it |
|---|---|---|
| Drawing intake | PDF sheets read and rasterised; scale calibrated; levels, grid and schedules written into DNs | each element cross-checked on plan, sections, elevations and renders; disagreements recorded |
| Parametric shell build | data tables → one command batch per checkpoint → SolidCraft | expected volume and bounding box per checkpoint; parameter check |
| Openings and joinery | window and door schedule → voids, frames, glass, hardware, swings | elevation sill and head; swing against the plan; no clash with cabinets |
| Merge for render | structural overlaps merged; parts needing different materials kept apart | zero interference pairs at nominal and at changed parameters |
| CAD to Blender | export, import, scale and level normalisation, collections, rig for moving parts | bounding box match; rig limits |
| Reference materials | palette and textures from the architect's renders; procedural glass, tiles, accent walls | side by side with the reference camera |
| Site and planting | HDRI, ground, regional plants | scale against the house; owner's taste |
| Interior furnishing | furniture and fittings from the plans; colour schemes offered as options | overlap test |
| Stills and lighting | reference cameras, interior views, sun presets, exposure for natural light | every view looked at before delivery |
| Movie production | route, door timing, clearance, metering, frame-by-frame render, encode | clearance of 25 cm or more; frame count and duration read back |
| Interior finishes | tile database from makers' sites, boards, browser, shortlist | (in progress; the finish tool of the PRD grew from this) |
| Print split | not started | to be defined |
| Unreal export | building and furniture: Blender → glTF → Interchange, first on 17 November (see the correction below) | names kept on actors; re-import tested 23 November |

## Applications and how they were driven

| Application | Interface used | Role |
|---|---|---|
| SolidCraft (parametric CAD) | its MCP server: batches of generated commands, measure, parameter check, interference, save, export | the model |
| Blender | its MCP server: run project scripts, render a view | scene, stills, films |
| Unreal Engine 5.9 | its MCP server (not connected at the time of writing) | walkthrough |
| PDF reader (pdfcraft) | its MCP server | drawings |
| Poly Haven | its public API, from Blender Python | HDRI, textures, plants, furniture |

These interfaces are what FR-WF-6 puts behind translation layers.

## What went wrong, in short (full list: RUNBOOK §4)

- Most rework came from building before every sheet had been read.
- Scale and transform side effects on import into Blender (objects at 0.001 scale; a reset multiplies by 1000).
- Long blocking calls lose work when the application closes: one render per call, save before long jobs.
- Starting Blender's animation render through the MCP crashed Blender; frames are rendered one per timer tick.
- Positions in plan were literal numbers; only levels and sizes followed parameters.
- A re-import of the model dropped the rig for moving parts; it has not been rebuilt.
- GPU rendering in Blender has been closing Blender since a system update of 21 November 2026 (handed to another agent); stills render on the CPU meanwhile.

FR-WF-7 asks for these to live in the step they belong to.

## What is specific to one house, and must become data

File and object names prefixed `johnny_`; the level heights, grid and room boxes; material choices; camera
positions; the plant list; the tile makers chosen. A tool taken into Parti takes none of these with it.

## Correction (23 November 2026)

This note said the Unreal export had not started. It had: the 16 November model was imported into `WalkthruDemo` on
17 November (glTF binary through Interchange), and site and planting were rebuilt in Unreal by editor scripts. The
CP-123 model replaced it on 23 November. JohnnyHouse corrected itself on Sandesh (#1637); the findings are in
`PRD-parti.md` §11, T4.

## What the step cycle must also cover (JohnnyHouse, 24 November 2026)

JohnnyHouse's orchestrator agreed to move its `cad/gen` scripts onto the `parti` SDK once CR-PRT-024 merges, on its own
schedule; its migrated run is the on-the-workstation acceptance of each SDK CR, and live tests may read its files in
place (Sandesh #1675, the owner's agreement). It named what the step cycle (sources, data, generate, apply, check,
checkpoint, record) would miss, from its working knowledge of the scripts; CR-PRT-024's spec takes each up, or names
the CR that does:

1. **Part files and their placements.** Movable things (louvres, doors, the garage gate, a skylight vent) are separate
   part files linked into the building at many positions (28 today). A step can span several files: rebuild a part,
   relink it, check it **at every placement**, with the part file backed up before it is rebuilt.
2. **More than one output per step.** The same generators write the motion tables, the placements and the building
   declaration from the same data tables; the step generates every target together and its record names them all, so
   nothing drifts from the model.
3. **Project-defined checks** beside the built-in ones (volume, bounds, body count, interference): walls meeting at
   their ends, each door joining its two rooms, beams reaching their columns (three fixes on 24 November were beams
   stopping short that volume and bounds had passed). Each returns pass or fail with its worst value.
4. **Corrections pointed out live.** The user selects a face or shows a view in the running application; the agent
   reads the selection and the view, finds the data-table row behind the body, edits it and regenerates only what
   depends on it. The cycle needs this entry as well as the one from the sources (with CR-PRT-025's live read).
5. **Picks by world point.** Fillets, cuts and face operations pick an edge or face by a world point that snaps to the
   nearest; the check after a pick is that the volume changed as expected (a cut that leaves it unchanged missed).
6. **Setting-out is not CAD.** The floor and wall setting-out scripts work from a survey of the Unreal level and from
   the declaration; they belong with setting-out and quantities (CR-PRT-019, CR-PRT-020), not the SolidCraft
   translator.
7. **Headless or in the application.** JohnnyHouse's runs go through the running application's MCP server (the
   command-line runner is not allowed in its sessions); its acceptance exercises that path, and the headless path is
   Parti's own live test.
8. **Its checkpoint conventions:** a `.sc` file and a log row, no pictures; some kept files must never be removed by a
   clean-up (a clean-up step removes only what the step itself made).

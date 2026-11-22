# DN — The first consumer: JohnnyHouse

**Date:** 2026-11-22
**Status:** Reference. Facts as of the date above; check the files before relying on a detail.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)
**Related:** `PRD-parti.md` §8 (installer), §9 (stages)

## What JohnnyHouse is

A house project at `/home/antonyj/Documents/bals/JohnnyHouse` (not a git repository): CAD model, a Blender
scene for stills, and an Unreal project for a walkthrough. Its own agent session does that work and will be
the first to install and use Parti. Parti's orchestrator must not edit anything in that folder; it may read it.
Requests between the two go through Sandesh once both are registered.

## What it supplies to Parti

### Tile records (the first catalogue source)

Folder: `/home/antonyj/Documents/bals/JohnnyHouse/blender/assets/reference/tiles/` (about 600 MB).

| Path | Contents |
|---|---|
| `data/tiles.ndjson` | 1,554 records, one per line |
| `data/<maker>.json` | The same, per maker |
| `schema/tile.schema.json` | JSON schema of a record |
| `index.csv` | Flat table of the main fields |
| `swatches/<id>.jpg` | Tile face, up to 1200 px |
| `rooms/<id>.jpg` | Maker's room photo, where one exists |
| `thumbs/<id>.jpg` | 260 px thumbnails |
| `boards/<zone>-<surface>-N.png` | 55 contact sheets |
| `data/selections.json` | The shortlist: `[{"id": "KW-001", "note": "Bath 1 wall"}, ...]` |

Record fields: `id`, `brand`, `name`, `series`, `set_id`, `role`, `pairs_with`, `sku`, `product_url`, `zone`,
`rooms`, `surface`, `primary_surface`, `classification` (`basis`, `confidence`, ...), `size_mm` (`w`, `h`),
`thickness_mm`, `finish`, `finish_class`, `body`, `design`, `colour` (`dominant` with `hex`, `hue_family`,
`neutral`, `chroma`, `value`, `temperature`, `lab`; `accent`; `palette`; `mean_lightness`; `visual_texture`;
`harmony`; `maker_colour`), `images`, `retrieved`.

Ids are two letters and three digits: maker letter (S Somany, O Orientbell, J Johnson, N Nitco, K Kajaria) and
W or F for wall or floor.

Counts: Kajaria 407, Johnson 400, Nitco 399, Somany 230, Orientbell 118. Bathroom wall 579, bathroom floor 301,
interior wall 106, interior floor 296, outdoor wall 44, outdoor floor 228.

Known weaknesses, which the catalogue must carry rather than hide: 778 records were filed under a zone by a
size-and-finish rule (`classification.basis` = `format_rule`, medium confidence), so some are in the wrong zone;
Johnson, Nitco and Kajaria are slices of about 400 each, not full ranges; the images are makers' web pictures,
with no relief or gloss maps.

These records are in JohnnyHouse's own shape. Under FR-CAT-4 they enter Parti through a translator; Parti's
finish is not required to copy this shape. For tests, take a small fixture (a few dozen records with their
thumbnails) into this repository and mark it as JohnnyHouse sample data; do not copy the whole folder.

### Prior art: the desktop tile browser

A working VanJS page over these records, written before Parti existed. Read it for what the owner has already
seen and accepted; it is a prototype, not Parti's architecture.

| Path (under the tiles folder) | What it is |
|---|---|
| `browser/index.html` | The page: filters on the left (where, surface, maker, main colour, colour strength, lightness, warm or cool, pattern, finish, role in a set, size), grid sorted round the colour wheel with paging, a detail panel (face, room photo, details, "goes with", complementary colour) and a shortlist tab with a note per tile |
| `browser/van.min.js` | VanJS 1.5.5 |
| `tools/build_browser.py` | Builds `browser/tiles.js` and the thumbnails from `data/tiles.ndjson` |
| `tools/serve_browser.py` | Local server on 127.0.0.1:8765; `GET` and `POST /api/selections` |

One lesson from it: the colour-wheel groups alone were too loose (pale beige tiles filed under "red"), so a
colour-strength filter was added. Keep it.

### Surfaces

Not yet declared anywhere. The house has four bathrooms, which are the first rooms to be finished. Room boxes
have been measured in the Blender scene for the bathrooms. Producing the surface declarations Parti needs
(FR-MOD-1) is the consumer's job, in the format Parti's scaffold defines.

### Unreal project

`/home/antonyj/Documents/bals/JohnnyHouse/unreal/WalkthruDemo/WalkthruDemo.uproject`: engine 5.9, Blueprint
only (no `Source` folder), with these plugins enabled among others: Interchange editor, Python script plugin,
Variant Manager, Sun Position, HDRI Backdrop, Datasmith, PCG, Fab. Nothing of Parti is built in it. Unreal 5.9
is newer than the co-author's first-hand knowledge: check every engine detail against the 5.9 documentation.

## What the consumer needs from Parti's first release

1. Install Parti on this machine with one command, and scaffold it into JohnnyHouse with one command, both
   runnable by an agent (`PRD-parti.md` §8).
2. Point it at the tile folder above without moving or copying the data.
3. Browse, filter and shortlist as the desktop browser does now; `data/selections.json` must be readable so the
   existing shortlist is not lost.
4. Declare the bathroom surfaces, define zones on them, assign tiles, save the design to a file inside
   JohnnyHouse, and read that file from a script (to replay the choices in Blender for stills).
5. Do all of the above from the command line as well as from the page.

## Conventions of the owner worth knowing

- Browser interfaces use VanJS; quick local servers bind to 127.0.0.1.
- A page shown to the owner must open as a new tab in their own running Chrome, never in a hidden browser.
- Documents and messages for the owner are in plain language, with full absolute paths.
- Downloaded files are untrusted; maker sites are fetched slowly and with a generic browser identity. The
  owner's name, email and project names are not sent to outside services.

# DN — What the prototype's Runbook means for Parti's domain model

**Date:** 2026-11-24
**Status:** Proposed, for the owner's decisions (§4). Nothing here changes the PRDs until decided.
**Author:** Parti orchestrator (vidushi-parti)
**Source:** JohnnyHouse `docs/research/RUNBOOK.md` v0.3 (read in place; Sandesh #1660), its LOG, and #1640 to #1658
**Related:** `../Architecture.md` §4 (contexts), `PRD-parti.md` §8A (workflow outline), D17, D18, D19, D21, D24, Q17;
`PRD-domain.md` (the 0.1.0 slice); `DN-ubiquitous-language.md`

## 1. Why

The owner's direction (24 November 2026): the Runbook updates from JohnnyHouse are a prototype of what Parti's workflow
design should serve, so they may change the domain model. JohnnyHouse is where the workflow is being found by hand,
so that Parti's own harness, with the workflow embedded (D21), can do it for any architectural project at a fraction
of the agent's tokens. The question for this note: which of the prototype's working concepts are domain concepts Parti
must model, in which context, and when.

## 2. What the prototype actually did

Phases P0 to P12, each a run of steps; each step a script function followed by a numeric check; a checkpoint per
feature group; owner gates G1 to G7. In the Unreal phase (P12), eleven steps in the order that worked, four of them
living only in the world and re-run after every building import (↻). A short loop ran about fifty times in two days:
the owner points, the agent finds the bodies, finds the cause in numbers, fixes by a scripted rule with a table of what
it touches, checks by measurement, says what was not checked, the owner tries it, one log row. Its own analysis: most
rework came from acting before the bodies the owner meant were identified, from silent failures, and from finishes
living only in Unreal; most reading went on finding where things are and which way they move.

## 2a. Phases, steps and corrections (the LOG, 279 rows)

The owner pointed at the shape (24 November 2026): broad **phases**, and within them minor **steps**, and the
**corrections** ("revisions") made along the way to fix issues. The LOG shows it exactly:

- **Phases** P0 to P12, broad and ordered, each with an owner gate at its end (G1 to G7). The order is itself a decision:
  print preparation (P9) was moved after the Blender scene (P10) by the owner.
- **Steps**: a planned checkpoint per feature group (`CP-03` columns, `CP-04` slabs, …), 126 of them in CAD, each closed
  by a numeric check (volume and bounding box exact, body count) and a saved file.
- **Corrections**: a revision of a step already done, logged under the same number with a letter (`CP-06b`, `CP-13b` to
  `CP-13d`, `CP-16b` to `CP-16o`): **48 of the 174 CAD rows (28 %)**. One step (`CP-16`, the roof and stair hall) took
  fourteen corrections. Each correction has a **trigger**, a **cause**, a **fix** and its own **check**:

  | Trigger | CAD corrections | Example |
  |---|---|---|
  | found by the agent re-reading the sources (sheets, sections, elevations, renders) | 28 | `CP-16k` entrance rebuilt as a ramp per the ground-floor sheet, the south elevation and render R2 |
  | pointed at by the owner | 13 | `CP-34c` "the render is not dimensionally right, the lattice must cover the whole opening" |
  | seen in a rendered view or the live window | 4 | `CP-16b` "seen in the user's SolidCraft window" |
  | a systematic audit | 3 | `CP-13b` doorway audit level by level; `SA-1` structural audit |

- **In the Unreal phase** the balance turns: 31 of its 48 rows were started by the owner, mostly by pointing at a fault
  in the walkthrough.
- **Corrections cross phases**: faults found in the walkthrough (P12) were fixed at the source in CAD (`CP-126` to
  `CP-128`), then carried forward as a **patch** of the changed bodies (`UE-32`), making the world-only steps stale.
- **Variants**: `VAR-1`, a comparison copy kept beside the main model ("model it for comparison, do not take away the
  current"), is an option, not a correction.

What this means for the model: the workflow is not a list of steps done once. It is **phases of planned steps, each step's
result revised by corrections**, where a correction may land in an earlier phase's step and then flows forward through
the revision chain (D19). The correction is the most frequent unit of work in the whole project, so it must be
first-class, not a free-text log line.

## 3. The mapping

Each prototype concept, the Parti context it belongs to, whether Parti already has it, and the proposal.

### 3.1 Workflow (the context that frames the others)

| Prototype | Parti today | Proposal |
|---|---|---|
| Phase (P0 to P12), with its gate | Step (glossary), Pipeline (Architecture §4) | **Phase**: an ordered, gated group of steps; the order is a decision the owner may change |
| Step (`CP-03`, `T12.3`), closed by a check and a saved checkpoint | Step, Checkpoint | keep: a step is planned, has its checks, and its result is a revision |
| Correction (`CP-16b` … `CP-16o`): a revision of a done step's result, with trigger, cause, fix and check | Revision (D19), Follow-up action | **Correction**: a revision of a step's result, recording its trigger (agent re-reading the sources, owner pointing, seen in a view, audit), cause, fix, check, and the step it lands in, which may be in an earlier phase than the one being worked; it makes later steps' results stale |
| Variant (`VAR-1`), a comparison copy | Option, offer (D22) | **Variant**: an alternative kept beside the main line for comparison, never replacing it until chosen |
| A numeric check closing each step (counts and bounds; swing measured; no material lost; door between two rooms; layer area = room area; a ball stopped by walls) | "record check" command, no model | **Check**: a named check a step definition carries; its **result** is pass or fail, the measured values, the worst offender, and what was **not checked** |
| ↻ steps made stale by a new building import | Stale, Follow-up action (D19) | **Invalidation edges** in the step definition: "building revised" makes these steps stale; their follow-up is to replay them |
| Owner gates G1 to G7; G7: scripts prove position and motion, the owner tries feel | Gate | a gate names its **kind**: owner review, owner trial (play), taste option |
| Owner decisions: point at a fault, choose among options, give a rule, choose from the catalogue | — | **Decision**: a recorded owner decision of one of those four kinds, linked to the step and to what it changed |
| LOG row: asked · done · checked (numbers) · not checked · files | — | **Step record**: the log entry the workflow writes itself from the step's command, check results and artefacts |
| "Saved; not tried in play; lives in Unreal, re-run after import", written thirty times | — | **Standard caveats** attached to a step definition and stated with every result |
| Caveats per tool (RUNBOOK §4) | FR-WF-7 (learned facts) | the harness's knowledge base, per tool and per step (D21) |
| Skill candidates (RUNBOOK §6, 20) | — | the first catalogue of the workflow's steps and the agent skills behind them |

### 3.2 Building

| Prototype | Parti today | Proposal |
|---|---|---|
| Rooms found from the model, with outlines; check "every door stands between two different rooms" | Room, optional outline (PRD-domain §2.1) | a door **connects** two rooms (or a room and outside): declared or derived, and checked (a building rule) |
| Movable sub-assembly as a part file, placed several times (`placements.json`: origin, turn about the vertical, per-instance settings such as a door's hand) | Element; parts later (DM-9) | **Part** (a type) and its **part placements** (instances), in the Building context |
| Motion table (`*.kin.json`): mechanism; groups (hinge, follower, slide) driven by one input | D18 motion library | **Motion table**, declared beside the building declaration (`parti.motion/1`), as #1642 proposed |
| Bodies that are not parts but move (cabinet fronts, gates): motion inferred | — | **Operable element**: an element with an inferred motion, reviewed and then declared |
| Handle point; activation within 1.3 m (owner rule) | — | a part or operable element has a **handle**; activation is a world-builder rule |
| Faults found in the walkthrough fixed in CAD, returned as a patch of the changed bodies only | building revision (D19) | a **patch revision**: a revision that changes some elements only, followed like any other revision |
| Face patches: wall end faces at clad corners, slab edges facing a void, a terrace left plain | surfaces are faces of rooms | surfaces **outside rooms**: exterior faces, edges and site surfaces, beside the room faces |

### 3.3 Design

| Prototype | Parti today | Proposal |
|---|---|---|
| Finishes applied **by rule** (`BUILDING_RULES`: a selector by class, room, face or name pattern → a finish), with a count returned; re-applied after every import | placements per zone; schemes per room | **Rule**: a selector (room use, surface kind, side, part type, element class) and a product with its placement parameters. A rule expands into placements, says how many it touched, and is re-evaluated at every building revision. A placement made by hand overrides it |
| Finishes recorded with **where used** (`usage.json`) | derivable from placements | a **where-used** query: per product, the zones, parts and rooms it is placed on |
| Owner rules beyond finishes ("set out as a tiler would", "10 % wastage") | setting-out rule, wastage setting (0.1.0) | already modelled |

### 3.4 Catalogue

| Prototype | Parti today | Proposal |
|---|---|---|
| Every kind of asset in one browser: tiles, finishes, scans found but not downloaded (`candidates.json`), library models | finishes of seven kinds | the catalogue holds **assets** of more kinds than finishes, per layer (D17), as the layers arrive |
| A download needs the owner's permission (file, source, size); licence shown | source and licence on a finish | a **candidate** asset: found in a library, with licence and download size, not yet acquired; acquiring it is an owner decision (a gate) |
| Seeing a tile against the room, its count and cost, before choosing | quantities (0.1.0) | a **preview** of a choice: the quantities it would give before it is placed |

### 3.5 Session and the owner's pointer

| Prototype | Parti today | Proposal |
|---|---|---|
| The owner points: a screenshot or a sentence; the agent reads the viewport camera and selection, then finds the bodies by query | selection, viewpoint (Session) | **Pointer**: what the owner refers to (viewpoint, selection, words, a picture), and its **resolution** to element, surface or zone ids, confirmed before any change. The loop's first step; D24's resolve-by-embeddings and Q17's interaction capture serve it |
| A fault reported, its cause found in numbers, fixed, checked, possibly sent back to CAD | follow-up action | **Finding**: a fault the owner points at, with its pointer, the elements resolved, the cause, the fix, the checks, and where it was fixed (Parti, the world, or the source) |

### 3.6 World builder

| Prototype | Parti today | Proposal |
|---|---|---|
| Graphs acting on tags only (`bp_*.dsl`: blade linkage, hinge, slide, pivot, fold) | motion primitives (D18) | confirmed: the first motion primitives |
| Collision pass and probe | — | a world-builder step with its check |
| A frame conversion per tool (mm ↔ cm, mirrored Y, the level lift) | D25 declared transforms | confirmed |

## 4. Decisions for the owner

0. **The workflow's shape:** Phase → Step → Correction, with Variant beside it (§2a): adopt as the Workflow context's
   model and the glossary's terms.

1. **Does any of this enter 0.1.0?** 0.1.0's slice (the finish tool against the mock scene) is not contradicted by any
   of it: placements per zone already follow building revisions (CR-PRT-009), setting-out and quantities are in.
   Candidates that would be cheap now: the door-connects-two-rooms check (a building rule), the where-used query, the
   check-result shape (pass or fail, values, worst offender, not checked) used by `parti-axi`'s checks.
2. **Rules (finish by selector):** 0.1.0, or with the workflow in 0.2.0.
3. **The Workflow PRD:** written next, with this Runbook as its primary evidence, for 0.2.0; or after 0.1.0 ships.
4. **Where the building concepts go** (parts, placements, motion tables, operable elements, surfaces outside rooms):
   recorded in Architecture §4 and the glossary now as decided names, specified with the world builder's PRD.

## 5. What recurs, and would be the engine's core

From RUNBOOK §3.2: a frame conversion per tool; selecting elements by class, room, face or name pattern; a table of
rules applied with a count returned; a check returning pass or fail with the worst value; a JSON record written beside
the thing it describes. In Parti terms: D25's transforms, selectors, rules, checks, and declarations.

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
| Element | A labelled part of the building (level, room, wall, floor, ceiling, opening, stair, …), tied to its 3D object and to its 2D drawing elements. | Building |
| Surface | One face of an element that can take a finish (a wall face, a floor). | Building |
| Zone | A part of a surface, described by numbers. Zones come in kinds: area, panel, band (by height), border, … | Design |
| Layer | One kind of information placed on the building: finishes, furniture and cabinetry, electrical, plumbing, … | Design |
| Design | The user's layer planning for the building: one plan per layer, with its schemes and shortlist. What the user is making. (Not the architect's design of the building, which is "the building".) The business word; in code, each layer's plan is a `LayerPlan`. | Design |
| Plan | The placements of one layer within a design (the finishes plan, the furniture plan). In code: `LayerPlan`. | Design |
| Revision | A numbered state of the building, of a plan or of a scenario (D19). | each owning context |
| Stale | Downstream of a change and not yet brought up to date (D19). | Workflow |
| Follow-up action | One thing to do to bring something stale up to date: re-check placements, recompute quantities, rebuild the scene (D19). | Workflow |
| Orphaned placement | A placement whose zone or surface is gone; flagged for the user to re-place or drop (D19). | Design |
| Placement | A product put on an element, a surface or a zone, with its details (for a finish: laying pattern, grout, offset, rotation). (Generalises "assignment".) | Design |
| Scheme | A named, saved set of placements that can be applied again ("Bath 1, scheme A"). | Design |
| Shortlist | Products set aside, each with a note on where it is meant to go. | Design |
| Product | Something a layer can place: a tile, a paint, a cabinet, a socket, a basin. Comes from a catalogue. | Catalogue |
| Finish | A product of the finishes layer: a tile or a paint. | Catalogue |
| Catalogue | The products available to a layer, with the facts used to filter and match them. | Catalogue |
| Suitable use | Where a product may be used: room use (bathroom, interior, outdoor) and surface kind (wall, floor). *Proposed*: the JohnnyHouse tile records call the room use `zone`; their translator maps it here. | Catalogue |
| Quantity | How much of a product a plan needs, wastage included. | Quantities |
| Bill of materials | The quantities of one or more plans, grouped for one work-contract role. | Quantities |
| Work-contract role | A trade engaged on the building project: tiling contractor, painter, carpenter, electrician, plumber, furniture supplier. | Quantities |
| Cost estimate | The price of a bill of materials, computed once price data exists. Later. | Quantities |
| World builder | The module that, once the building is modelled in CAD and brought into Unreal, creates a world there with the building at the centre of all activity, and stages it as an experience (D18). | World builder |
| Scenario | One way of experiencing the building: which layers and schemes show, the setting, the experience mode, the routes. | World builder |
| Setting | The state of the world around the building: time of day, date, weather simulation, light, site. (Replaces "Presentation".) | World builder |
| Moving part | A part of the building or its world that can be animated: door, drawer, gate, louvre. | World builder |
| Experience mode | How a person experiences a scenario: a VR walkthrough, or a monitor with keyboard, mouse or gamepad. | World builder |
| Route, viewpoint | A path, or a fixed place, that a scenario offers to move along or look from. | World builder |
| Session | One sitting in which participants work on the target project together. | Session |
| Participant | A user or an agent taking part in a session. | Session |
| Selection | What a participant has picked: an element, a surface, a zone or a group. | Session |
| Step | One stage of the guided workflow (drawing intake, shell build, …, finishes, world building). | Workflow |
| Gate | A point where the owner decides before the workflow goes on. | Workflow |
| Checkpoint | A saved state of the target project after a step. | Workflow |

## Change log

| Date | Change |
|---|---|
| 2026-11-22 | First version, from the architecture review. Owner's names: Zone kept (kinds: area, panel, …); Design kept (character: layer planning; Layer and Plan as terms); Session kept. |
| 2026-11-22 | Added Revision, Stale, Follow-up action, Orphaned placement (D19) and Cost estimate (D17). Design is the business word; `LayerPlan` is its name in code (owner). |

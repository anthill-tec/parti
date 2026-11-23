# Parti

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**A guided workflow that takes a building from the architect's drawings to an interactive Unreal Engine
walkthrough, worked through by a person and an AI agent together.**

> **Status: design stage.** The architecture has been reviewed and agreed (22 November 2026). The domain
> PRD comes next. There is no application code yet, and nothing is released.

---

## What Parti is

Parti is installed into a *target project*: a building project that owns its drawings, its CAD model, its
Unreal project and its data. It then guides the work on that building step by step, with tested tools at
every step. An agent works alongside the user in the same live session: it sees what the user selects,
follows what they do, and can do everything a person can.

Parti comes in two editions built from one domain: the **designer edition**, the full workflow for architects and
interior designers, and the **client viewer**, a self-contained walkthrough viewer (monitor or VR) that the designer
builds and hands to the building's owner, packaged with that project's options, stills and films.

Its first major feature is the **finish tool**. You point at a wall, a floor or part of one in the
walkthrough, browse a catalogue of finishes (tiles first, paints later), apply one, and change the time of
day and the weather. The page and the 3D scene always show the same state.

Parti grew out of **JohnnyHouse**, a house project where the whole path (drawings → parametric CAD model →
Blender stills and films → Unreal walkthrough) was first worked out by hand, with one-off scripts. Parti
turns that path into a product: a guided workflow, plus the maintained toolbase that replaces the scripts.
JohnnyHouse is its first user.

## The ideas it is built on

- **A building with layers.** The building is the base: its geometry, referenced through labelled elements
  (levels, rooms, walls, floors, openings), each tied to its 3D object and to its 2D drawings. Layers sit on
  it: finishes first, then furniture and cabinetry, electrical and plumbing.
- **Bills of materials by trade.** Every layer yields quantities. They roll up into bills of materials for
  each work-contract role (tiling contractor, painter, carpenter, electrician, plumber, furniture supplier),
  and later into cost estimates.
- **A world builder.** Once the building is in Unreal, Parti creates a world around it and stages it as an
  experience: scenarios, time of day, weather, light, moving parts, routes, in VR or on a monitor with
  keyboard, mouse or gamepad.
- **Everything is versioned, and changes flow forward.** When the building changes, Parti works out what
  downstream is affected (the design, the quantities, the scene), marks it stale, and lists the follow-up
  actions the agent works through with the user. Nothing is changed or left wrong silently.
- **One business language.** Every term has one meaning, and it is the language used with architects,
  designers and users. See the [glossary](docs/research/DN-ubiquitous-language.md).

## How it is built

```text
 page (VanJS) ─┐                       ┌──────────────── gateway (Bun) ───────────────┐
 scene adapter ┼── WebSocket ─────────▶│ adapters in → pure TypeScript domain → ports │──▶ local files
 parti-axi ────┤                       │ (Building · Design · Catalogue · Quantities  │    (later: EntityStore,
 agent (AXI) ──┘                       │  · World builder · Session · Workflow)       │     Nai)
                                       └──────────────────────────────────────────────┘
```

- **Domain-Driven Design.** The business rules are plain functions over plain data
  (`decide(state, command) → events`, `evolve(state, event) → state`), with no input or output and no
  library calls. Every outside system (Unreal, the page, makers' catalogues, files, the CAD and rendering
  applications) is reached through its own translator.
- **Local first, Nai next.** The designer edition runs on Linux first (on Windows in a container or under WSL2);
  the client viewer runs on Windows and Linux. Retrieval (RAG) and the knowledge base move to the owner's Nai
  (streaming runtime) as soon as the agent harness exists; the rest of the data layer moves to Nai and EntityStore
  (system of record) when Parti takes on several users and sessions. Only the adapters change.
- **Its own agent harness.** A workflow graph (LangGraph, Python) built from the domain's workflow, with Parti's
  agent definitions and skills, drives the CAD system, Blender and Unreal through their Python APIs and MCP servers.
- **Agent-first interface.** `parti-axi` installs Parti, sets it up inside a target project, and gives an
  agent every action a person has, including joining a live session. A Pi plugin wakes the agent when the
  user acts.
- **Unreal.** The Unreal side is a C++ plugin, deferred until the toolchain supports a C++ stack. Until then
  a mock scene stands in for Unreal, so the first release can be built and tested without it.

| Part | Stack |
|---|---|
| Message schema, domain, gateway, page, mock scene | TypeScript on Bun; VanJS for the page |
| `parti-axi` (installer and agent interface), catalogue tools, pipeline tools | Python (installed with `uv`) |
| Unreal plugin | C++ (deferred) |

## Stages

Releases: **0.1.0** first, then 0.x minor releases, each reviewed with stakeholders, up to **1.0.0**, the full
designer edition. The client viewer follows 1.0.0.

| Stage | What it adds |
|---|---|
| **A. First release** | The finish tool end to end with the mock scene, on JohnnyHouse data: browse, filter, select, define zones, place finishes, save and reload, set time and weather; installer and agent interface |
| **B. Unreal** | The C++ plugin, the overlay, finish assets, the world builder |
| **C. VR** | The page as a panel inside the 3D scene |
| **D. Data service** | Several users and sessions; EntityStore and Nai as the backend |
| **E. Streamed** | Unreal running on servers, shown in a browser |

## Documentation

| Document | What it holds |
|---|---|
| [`docs/Architecture.md`](docs/Architecture.md) | The system overview: parts, rules, contexts, components, stages |
| [`docs/research/PRD-parti.md`](docs/research/PRD-parti.md) | The design contract: the owner's decisions (D1–D23), requirements, stages, open questions |
| [`docs/research/DN-ubiquitous-language.md`](docs/research/DN-ubiquitous-language.md) | The living glossary: the business language |
| [`docs/research/DN-test-strategy.md`](docs/research/DN-test-strategy.md) | How Parti is tested |
| [`docs/research/DN-founding-design-record.md`](docs/research/DN-founding-design-record.md) | The original design discussion |
| [`docs/research/DN-first-consumer-johnnyhouse.md`](docs/research/DN-first-consumer-johnnyhouse.md) | The first user: its data, its Unreal project, its needs |
| [`docs/research/DN-pipeline-prototype-johnnyhouse.md`](docs/research/DN-pipeline-prototype-johnnyhouse.md) | The pipeline as it was run by hand |

The design work runs in this order: the architecture (done) → the glossary → the domain PRD → the other
per-area PRDs → change requests (CRs), which are implemented last.

## How the project is run

Parti is developed with the **Model B** workflow: an orchestrator agent turns the specifications into change
requests and drives them through test-first cycles (red, green, verify), with sub-agents per stage. Test runs
are reported to **Crucible**, which also holds the CR queue. Sessions coordinate over **Sandesh**.

- Branching follows **git flow**: features on `feature/*`, releases on `release/*`, `master` for releases
  only. Project setup and documentation changes land on `develop`.
- Tests: Bun's test runner for the TypeScript parts, Python `unittest` under `tests/` for the Python parts,
  both run and reported through the project's Crucible clients.
- Releases are cut with `git flow release`, and the GitHub release workflow publishes them.

## Repository layout

```text
docs/                 architecture, PRDs, design notes; changes/ for CR specs
tests/                Python unittest modules
hooks/                agent harness hook instances
.agents/skills/       project skills (e.g. the bootstrap/shutdown services extension)
.github/workflows/    the release workflow
AGENTS.md             conventions for agents working in this repository
CHANGELOG.md          release notes
```

The workspace packages (schema, domain, gateway, page, mock scene, `parti-axi`, tools) arrive with the first
CRs.

## Licence

Parti is free software under the [GNU General Public License v3.0](LICENSE) only (SPDX: `GPL-3.0-only`).
You may use, study, change and share it. If you distribute Parti or a work based on it, you must do so
under the same licence and make the complete source available.

Copyright 2026 [anthill-tec](https://github.com/anthill-tec).

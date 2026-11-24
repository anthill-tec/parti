# Parti

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**An ecosystem in which architects and interior designers create their projects with agentic help: a guided
workflow from the architect's drawings to an interactive Unreal Engine walkthrough, worked through by a person and
an AI agent together.**

> **Status: design stage.** The architecture (22 November 2026) and the domain PRD for 0.1.0 (23 November) are
> reviewed; the workflow's shape, the `parti` library and the ecosystem were decided on 24 November (D26 to D30).
> The roadmap to 1.0.0 was approved on 24 November ([PRD-parti D33](docs/research/PRD-parti.md)) and its change
> requests are filed; the first are in their design checks. There is no application code yet, and nothing is released.

---

## What Parti is

Parti provides the coding and logical framework (the workflow, the `parti` library, the agent harness, the skills);
the agent in each project (the project agent) concentrates on that project's own logic; and the architects and
designers, domain experts rather than programmers, work in their own terms and never write code. The consumers of a
project's deliverables (home buyers, business buyers, the client) walk the result, with or without VR.

Parti is installed into a *target project*: a building project that owns its drawings, its CAD model, its
Unreal project and its data. The architect or designer then works in the **Parti Project Environment** in the browser:
a guided chat that follows the workflow and offers suggestions at every step, beside the asset browser, the design
workspace, quantities and the walkthrough. It then guides the work on that building step by step, with tested tools at
every step. An agent works alongside the user in the same live session: it sees what the user selects,
follows what they do, and can do everything a person can.

Parti comes in two editions built from one domain: the **designer edition**, the full workflow for architects and
interior designers, and the **client viewer**, a self-contained walkthrough viewer (monitor or VR) that the designer
builds and hands to the consumer, packaged with that project's options, stills and films.

At its heart is the **finish tool**. You point at a wall, a floor or part of one in the
walkthrough, browse a catalogue of finishes (tiles, wood veneers, laminates, paints, metals and more), set them out
as a tiler would and count what to buy, apply one, and change the time of
day and the weather. The page and the 3D scene always show the same state.

Parti grew out of **JohnnyHouse**, a house project where the whole path (drawings → parametric CAD model →
Blender stills and films → Unreal walkthrough) was first worked out by hand, with one-off scripts. Parti
turns that path into a product: a guided workflow, plus the maintained toolbase that replaces the scripts.
JohnnyHouse is its first user, and the test bed for Parti's library.

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
 parti-axi ────┤                       │ (Building · Design · Catalogue · Quantities  │    (or EntityStore
 agent (AXI) ──┘                       │  · World builder · Session · Workflow)       │     or Nai)
                                       └──────────────────────────────────────────────┘
```

- **Domain-Driven Design.** The business rules are plain functions over plain data
  (`decide(state, command) → events`, `evolve(state, event) → state`), with no input or output and no
  library calls. Every outside system (Unreal, the page, makers' catalogues, files, the CAD and rendering
  applications) is reached through its own translator.
- **Nai as the message bus, local adapters behind the same ports.** The designer edition runs on Linux first (on
  Windows in a container or under WSL2); the client viewer runs on Windows and Linux. Nai (the owner's streaming
  runtime) carries the messages between the gateway, the agent harness and the applications, and EntityStore is the
  system of record, with change data capture; retrieval (RAG) and the knowledge base move to Nai too. Local adapters
  (the gateway as the bus, events as JSON files) stay behind the same ports, for offline work and tests. Only the
  adapters change.
- **A message bus to the applications.** Parti's events reach SolidCraft, Blender and Unreal through per-application
  connectors with no agent and no tokens; work that needs judgment goes through the agent and the applications' MCP
  servers, and events from any application can trigger the agent.
- **Its own agent harness and library.** A workflow graph (LangGraph, Python) built from the domain's workflow
  (phases, step kinds, checks, gates, the correction loop), with Parti's agent definitions and skills, drives the CAD
  system, Blender and Unreal. It and the tools generalised from the prototype's scripts (the step cycle, and a
  translator per application, SolidCraft first) ship as the `parti` Python library, which every project imports. It
  hides the programming from the architect or designer. The model is chosen in Settings: the Anthropic API, an
  OpenAI-compatible endpoint, or the user's own installed Claude Code, signed in with their own subscription.
- **Agent-first interface.** `parti-axi` installs Parti, sets it up inside a target project, and gives an
  agent every action a person has, including joining a live session. A Pi plugin wakes the agent when the
  user acts.
- **Unreal.** The Unreal side is a C++ plugin, deferred until the toolchain supports a C++ stack. Until then
  a mock scene stands in for Unreal, so the walkthrough can be built and tested without it.

| Part | Stack |
|---|---|
| Message schema, domain, gateway, page, mock scene | TypeScript on Bun; VanJS for the page |
| `parti` library (workflow, harness, catalogue and pipeline tools, translators, connectors) and `parti-axi` | Python (installed with `uv`) |
| Unreal plugin | C++ (deferred) |

## Releases

Parti is released as 0.x minor releases up to **1.0.0**, the full designer edition; the client viewer follows 1.0.0.
Each release is reviewed with the stakeholders, and ends with a major review that re-plans the releases after it.
The roadmap is decision **D33** in [`docs/research/PRD-parti.md`](docs/research/PRD-parti.md); the change requests,
their order and the target dates are held on the Crucible board.

## Documentation

| Document | What it holds |
|---|---|
| [`docs/Architecture.md`](docs/Architecture.md) | Overview; Part A, the domain-driven logical architecture; Part B, the system architecture |
| [`docs/research/PRD-parti.md`](docs/research/PRD-parti.md) | The design contract: the owner's decisions (D1–D36, the roadmap among them), requirements, open questions |
| [`docs/research/PRD-domain.md`](docs/research/PRD-domain.md) | The domain: building, design and catalogue (reviewed, 0.1.0 slice) |
| [`docs/research/DN-ubiquitous-language.md`](docs/research/DN-ubiquitous-language.md) | The living glossary: the business language |
| [`docs/research/DN-test-strategy.md`](docs/research/DN-test-strategy.md) | How Parti is tested |
| [`docs/research/DN-founding-design-record.md`](docs/research/DN-founding-design-record.md) | The original design discussion |
| [`docs/research/DN-first-consumer-johnnyhouse.md`](docs/research/DN-first-consumer-johnnyhouse.md) | The first user: its data, its Unreal project, its needs |
| [`docs/research/DN-pipeline-prototype-johnnyhouse.md`](docs/research/DN-pipeline-prototype-johnnyhouse.md) | The pipeline as it was run by hand |
| [`docs/research/DN-workflow-shape.md`](docs/research/DN-workflow-shape.md) | The workflow generalised into one repeatable graph |
| [`docs/research/DN-runbook-domain-impact.md`](docs/research/DN-runbook-domain-impact.md) | The prototype's Runbook mapped onto the domain model |
| [`docs/research/DN-nai-readiness.md`](docs/research/DN-nai-readiness.md) | Nai's and EntityStore's readiness for the message bus, and the validation spike |

The design work runs in this order: the architecture (reviewed) → the glossary → the domain PRD (reviewed, for
0.1.0) → the other per-area PRDs → change requests (CRs), which are implemented last. Each PRD is written for the
slice the next release needs.

## How the project is run

Parti is developed with the **Model B** workflow: an orchestrator agent turns the specifications into change
requests and drives them through test-first cycles (red, green, verify), with sub-agents per stage. A Mainline
orchestrator plans and writes the specifications; Track orchestrators each work one CR at a time in its own git
worktree. Test runs are reported to **Crucible**, which also holds the CR queue. Sessions coordinate over **Sandesh**.

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
.worktrees/           one git worktree per CR in progress (not committed)
```

The workspace packages (`packages/`: schema, domain, gateway, local adapters, page; `python/`: the `parti` library
and `parti-axi`) arrive with the first CR.

## Licence

Parti is free software under the [GNU General Public License v3.0](LICENSE) only (SPDX: `GPL-3.0-only`).
The `parti` library is the one exception: LGPL-3.0-only, so a project's own scripts may import it under any licence
(D27).
You may use, study, change and share it. If you distribute Parti or a work based on it, you must do so
under the same licence and make the complete source available.

Copyright 2026 [anthill-tec](https://github.com/anthill-tec).

# Parti — Architecture

**Date:** 2026-11-22
**Status:** DRAFT for the owner's review. Structure is settled where a decision number (D…) from `research/PRD-parti.md` §3 is cited; the rest is proposed.
**Author:** antonyj (owner)
**Co-author:** JohnnyHouse session agent (first consumer of Parti)

This document is the system overview: the parts, how they connect, and the rules that keep them apart. The
reasons and the detailed analysis are in the PRDs and design notes under `research/`; this document does not
repeat them.

## 1. What Parti is

A suite installed into a *target project* (a project that owns a building model). It has three parts:

1. **Finish tool.** Browse a catalogue of finishes and apply them to walls, floors and parts of them in an Unreal walkthrough; set time of day and weather; one state shared by the interface and the scene.
2. **Pipeline workflow and toolbase.** A guided sequence of steps, with tested tools, that takes an agent from drawings to CAD model, Blender scene and Unreal walkthrough.
3. **Installer and agent interface** (`parti-axi`). Installs Parti, scaffolds it into a target project, and lets an agent do everything a person can.

## 2. The whole in one picture

```
 TARGET PROJECT (e.g. JohnnyHouse)                PARTI (installed tool)
 ───────────────────────────────                  ──────────────────────────────────────────────
 parti configuration  ───────────────────────────▶ parti-axi  (Python CLI: install, init, run,
 finish records + images ─────┐                                 catalogue, doctor, state, command,
 surface declarations ────────┤                                 workflow)
 saved designs  ◀─────────────┤                         │ starts / talks to
 pipeline data tables ────────┤                         ▼
 step log, checkpoints ◀──────┘                  ┌──────────────── GATEWAY (Bun) ────────────────┐
                                                 │  adapters in:  page link · scene link · CLI   │
   PAGE (TypeScript, VanJS)  ◀── WebSocket ────▶ │  ───────────────────────────────────────────  │
   overlay · VR panel · browser                  │  DOMAIN (pure TypeScript)                     │
                                                 │   Design · Catalogue · Model · Presentation   │
   SCENE ADAPTER             ◀── WebSocket ────▶ │   · Session                                   │
   mock scene (now)                              │  ───────────────────────────────────────────  │
   Unreal C++ plugin (later)                     │  ports: catalogue store · design store ·      │
                                                 │         session channel · asset delivery      │
                                                 │  adapters out (v1): local files               │
                                                 │  adapters out (later): EntityStore · Nai      │
                                                 └───────────────────────────────────────────────┘

   CAD · Blender · Unreal editor  ◀── their own agent interfaces ── PIPELINE TOOLS (Python)
```

## 3. Rules that hold everywhere

| Rule | Source |
|---|---|
| The domain is pure: plain functions over plain data, `decide(state, command) → events`, `evolve(state, event) → state`, keyed by aggregate id. No input or output, no library calls, no outside terms. | D8, D10, NFR-1 |
| Everything outside the domain is reached through a port named in domain terms, with an adapter behind it. | NFR-5 |
| Every outside system has its own translator (anti-corruption layer): the scene, the page, each maker's feed, local files, each driven application, later Nai and EntityStore. | D8, NFR-4 |
| Contexts know one another by identifier and published events only. | NFR-3 |
| One message schema, versioned, is the only contract between page, gateway and scene adapters. Types are generated from it. | NFR-6 |
| Commands are safe to repeat; every change is an event with an id and a per-aggregate sequence number; state is rebuilt from events; stale changes are refused. | NFR-2 |
| Nothing of one target project lives in Parti's code. | NFR-10 |
| Servers bind to 127.0.0.1 in version one; every incoming message is validated against the schema. | NFR-8 |

## 4. Contexts

| Context | Aggregates and main data | Commands (examples) | Publishes |
|---|---|---|---|
| **Design** (core) | Design: per surface its zones; per zone its assignment; schemes | define, resize, remove zone; assign, clear finish; save, apply scheme | zone defined / resized / removed; finish assigned / cleared; scheme saved / applied |
| **Catalogue** | Finish; maker; set; colour classification | (queries) filter, search, "goes with" | finish added / changed / withdrawn |
| **Model** | Room; surface (id, kind, room, size) | declare, retire surface | surface declared / retired |
| **Presentation** | Scene settings: date, time, place, weather, lights | set time; set weather; set lights | setting changed |
| **Session** | Session: participants, selection, viewpoint | select surface / zone / group; clear selection | selection changed |
| **Asset delivery** | Mapping from finish to what a scene can draw | prepare finish for a scene | finish ready / failed |
| **Identity** (service stage) | Users, access | — | — |
| **Workflow** (suite) | Pipeline: steps, their inputs, outputs, checks, gates; a target project's progress | start step; record check; pass gate; checkpoint | step started / checked / completed |

Design refers to finishes and surfaces by id; it asks Catalogue and Model whether an assignment is allowed
through their published facts, never by reading their storage.

## 5. Components

| Component | Stack | Depends on | Notes |
|---|---|---|---|
| `schema` | schema files → generated TypeScript (later C++, Rust, Avro) | nothing | Commands, events, queries, state snapshots; versioned. |
| `domain` | TypeScript | `schema` types only | One module per context. No imports from anything else in the repository. |
| `gateway` | Bun | `domain`, `schema`, ports | Serves the page; holds the WebSocket links; runs commands through the domain; stores events through the design store; fans events out. |
| `adapters-local` | TypeScript | ports | Catalogue from the target project's records; designs as an event log and a snapshot in a file. |
| `page` | TypeScript, VanJS | `schema` | Catalogue browser, detail, shortlist, zone editor, presentation controls. Its state is a projection of the shared state. Works as overlay, VR panel and plain browser tab. |
| `mock-scene` | TypeScript | `schema` | Stands in for Unreal: draws surfaces and zones, reports picks. The test partner. |
| `parti-axi` | Python (installed with `uv`) | gateway (over its local interface) | Installer, scaffold, agent commands, workflow guide. Structured output, dry run, a flag for every question. |
| `catalogue-tools` | Python | — | Build a catalogue from a target project's records: thumbnails, colour tags, checks. Later: Unreal editor scripts for finish assets. |
| `pipeline-tools` | Python | — | The toolbase of the workflow: data tables → commands for the CAD and rendering applications, with expected-result checks. One translator per application. |
| `unreal-plugin` | C++ | `schema` (generated C++ types) | **Deferred** until Model B supports a C++ stack (D5). Scene adapter, pick, zone master material, finish assets, overlay. |

The repository layout that realises this (workspace packages, test folders) is the orchestrator's to propose.

## 6. How a change travels

Assigning a finish, version one:

1. The user picks a zone in the scene. The scene adapter sends *selection requested*; Session produces *selection changed*; page and scene both show it.
2. The user chooses a finish in the page. The page sends *assign finish* with the design's expected version and a command id.
3. The gateway validates the message, loads the design's state, calls Design's `decide`. It refuses (unknown zone, finish not valid for this surface, stale version) or returns *finish assigned*.
4. The event is appended through the design store, then sent to every link.
5. The scene adapter asks asset delivery for the finish in drawable form and updates the zone. The page updates through its projection.
6. A link that joins late receives a snapshot, then events from that sequence number.

The same path serves the CLI: `parti-axi` sends the command and prints the events or the refusal.

## 7. Where things run, by stage

| Stage | Page | Gateway and domain | Stores | Scene |
|---|---|---|---|---|
| A. First release | browser tab | local Bun process | files in the target project | mock scene |
| B. Unreal | overlay inside the Unreal app | local Bun process | files | Unreal plugin |
| C. VR | panel in the 3D scene | same | same | same |
| D. Data service | same | local, or served | EntityStore (records), Nai (pipelines, sessions, embeddings) | same |
| E. Streamed | browser, around a streamed picture | served | same as D | Unreal on servers |

Only adapters change between stages. The domain, the schema and the page do not.

## 8. Later backends

- **EntityStore** (the owner's Quarkus service on Redis and MongoDB, with change streams): system of record for Catalogue, Design, Model and review records, behind the catalogue-store and design-store ports.
- **Nai** (the owner's Rust streaming runtime with its own DSL, connectors and provider plugins): the domain's `decide` and `evolve` functions map onto keyed pipeline stages or a custom provider; session traffic through a two-way session connector; embeddings for search by likeness.

What Nai lacks today for the interactive loop, and the requests this makes to its team, are listed in
`research/DN-founding-design-record.md`. Neither is used in version one (D9).

## 9. Installing into a target project

`parti-axi init --target <dir>` writes a configuration file and the agent notes into the target project, and
nothing else. The target keeps its data where it is; Parti reads it in place and writes only where the
configuration says (saved designs, the step log, checkpoints). When the Unreal plugin exists, the scaffold
also connects it to the target's Unreal project.

## 10. Documents

| Document | Holds |
|---|---|
| `Architecture.md` (this) | The overview. |
| `research/PRD-parti.md` | The suite's design contract: decisions, requirements, stages, open questions. |
| `research/PRD-<topic>.md` (to be written) | Detailed analysis per area. Expected: the message schema and state model; the finish tool's domain; the page; the installer and agent interface; the pipeline workflow and toolbase; the Unreal plugin and finish assets. `PRD-parti.md` then keeps the decisions and the map, and its detailed sections move out. |
| `research/DN-founding-design-record.md` | The original design discussion, including the Nai and EntityStore reviews and the stack findings. |
| `research/DN-first-consumer-johnnyhouse.md` | The first consumer's data, Unreal project and needs. |
| `research/DN-pipeline-prototype-johnnyhouse.md` | The pipeline as JohnnyHouse ran it by hand: steps, tools, scripts, faults. |
| `changes/CR-PRT-NNN-*.md` | Implementation specs, filed on the Crucible board. |

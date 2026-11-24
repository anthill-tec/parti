# CR-PRT-029 — Agentic harness

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012, CR-PRT-022, CR-PRT-024
**Labels:** harness, python, agent, workflow
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` D16, D21, D26, D28, D29, D33, D35; `docs/research/PRD-domain.md` §11 (DM-11); `docs/Architecture.md` B3 (`parti.harness`), B4, B6

## Context

Parti ships its own agent harness (D21): a workflow graph (LangGraph, Python) compiled from the domain's workflow
definition, whose nodes act only through the domain's commands, so the domain stays the single source of truth. The
project agent hides the programming from the architect or designer (D28): it writes the data tables, runs the steps,
labels and classifies, and asks the user only what needs their judgment, in their terms. In 0.1.0 it drives the first
three phases, issuing the same workspace commands the workflow step does (DM-11). It reaches the gateway through its
agent API over WebSocket (CR-PRT-012) and serves its own endpoint for Nai (D35, CR-PRT-031).

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern): the chat's command `say` (who, text, attachments: a clip, an element, a
sheet) and event `said`; `agent-status` (idle, working on a step, waiting for the user, with what it waits for). Chat
messages are kept in the `workflow` log, so a reload shows the conversation (CR-PRT-030 renders it).

### §S2 The graph

`parti.harness.compile(definition) -> Graph`: one node per step of the workflow definition (CR-PRT-022), in its order,
each node running the step's **skill**; a **review gate** compiles to an interrupt that waits for the user's
`gate-decided`. The graph's state is a projection of the workflow run read from the gateway; LangGraph's checkpointer
holds the agent's own state only (its place in the graph, its working notes), never the project's (Architecture B3).
Checkpoints and memory sit behind ports, local files in 0.1.0 (`parti/.harness/`).

### §S3 Acting only through the domain

The harness joins the gateway as a participant of kind `agent` (`hello`, D16) and acts through its tools only:
the domain's commands and queries (CR-PRT-012), the library (`parti.workflow.run_step`, `parti.tools.tables`,
CR-PRT-024), the model read and write-back (CR-PRT-025), and SolidCraft's MCP server as a client for what needs judgment
(D21). Rules: **H-1** the agent never sends `decide-gate`, `confirm-declaration` or a caveat on the user's behalf: it
proposes, the user decides (D26); **H-2** every change it makes is a command whose events every panel shows (D29); **H-3**
it never edits the model by hand: a correction edits a table row and runs the step again (D26). It sends the workspace
commands (`show`, `set-focus`) as the workflow step does, so the workspace follows it (DM-11).

### §S4 Skills for 0.1.0

`parti.harness.skills` (installed into the target project by `parti-axi init`, CR-PRT-013), each holding its method,
its checklist and when to ask the user (D21): **intake** (register the sources, ask for a missing licence or level),
**read a sheet** (propose the calibration's dimension lines and the table values off a sheet, each value cross-checked
on two sources, K1), **build from data** (write or correct the tables, run each feature group's step, explain a failed
check by its worst offender), **label and classify** (propose labels, tags and classes for unclassified objects, the
user confirming), **declare** (derive, explain the faults, prepare the confirmation). Each skill speaks in the glossary's
terms and the display units, and never asks the user for code, data or commands (D28).

### §S5 The model runner

A port `ModelRunner` with two adapters: the **Claude Code runner** (the user's own Claude Code login, as a subprocess,
for Anthropic Max accounts) and an **API provider** (a LangChain chat model with a key from the environment); a
scripted fake serves the tests. The runner is chosen in `parti.toml`; no credential is stored by Parti.

### §S6 The harness's endpoint

`parti-harness --target <dir>` serves a WebSocket endpoint on `127.0.0.1` (CloudEvents over `cloudevents.json`, as
CR-PRT-012), with its AsyncAPI 3.0 definition: it receives the events the router sends it (`said`, `step-started`,
interaction events) and sends its commands back; until Nai routes them (CR-PRT-031), it connects to the gateway
directly (`bus = "local"`).

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema.
- [ ] `compile` of the `residential/single-family-home` definition gives one node per step of the first three phases, in order, and an interrupt at *Confirm the declaration*.
- [ ] (integration, the gateway on a temporary target project, the scripted runner, the fake CAD session) A run from *Intake the sources* registers CR-PRT-003's sheets, calibrates them, records `one_house()`'s tables, builds `L0.walls`, reads the model, classifies it and derives the declaration, every change visible as events in the gateway's logs, then stops at the gate with `agent-status` waiting.
- [ ] In that run the harness sends no `decide-gate`, `confirm-declaration` or caveat (asserted over its outgoing messages).
- [ ] With one table row made wrong so `L0.walls` fails its volume check, the build-from-data skill corrects the row (the table file changes, no CAD command is sent outside the step) and the step's second record passes.
- [ ] A `say` from the user while the harness waits at the gate is answered with a `said`, and `gate-decided` approve resumes the graph to its end.
- [ ] Killing the harness mid-step and starting it again resumes from its checkpoint at the same node, and the project's state comes from the gateway, not the checkpoint.
- [ ] Starting *Build from data* makes the harness send `show` of `model`, and the gateway relays it to the page's connection.
- [ ] (reviewed, not tested) each skill of §S4 states its checklist and when it asks the user, in the glossary's terms.
- [ ] Live (`PARTI_LIVE=1`, a workstation with SolidCraft and a model runner): the same run on `one_house()` with SolidCraft headless reaches the gate.
- [ ] Caller-existence: `parti-axi agent start` (CR-PRT-013) starts `parti-harness`; the guided chat (CR-PRT-030) sends `say` and renders `said`, reviewed at their VERIFY.

## Estimated size

13 points. If the gap analysis finds it larger, §S4's skills split into a CR of their own in wave 5.

## Non-goals

The Design phase's skills (zoning, setting-out, the BOM: CR-PRT-037, 0.2.0); Blender and Unreal through MCP (with
their releases); the Nai agents that keep the router current (with Nai, D29); several agents in a session (CR-PRT-070,
1.0.0); answering questions about the building (D24, later).

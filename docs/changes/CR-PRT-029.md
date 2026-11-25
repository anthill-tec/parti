# CR-PRT-029 — Agentic harness: the orchestrator

**Status:** PENDING (spec drafted 2026-11-24; narrowed to the orchestrator 2026-11-25, D43; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-012, CR-PRT-022, CR-PRT-024, CR-PRT-081
**Labels:** harness, python, agent, workflow
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-parti.md` D43, D16, D21, D26, D28, D29, D33, D35; `docs/research/PRD-domain.md` §11 (DM-11); `docs/Architecture.md` B3 (`parti.harness`), B4, B6

## Context

Parti ships its own agent harness (D21): a workflow graph (LangGraph, Python) compiled from the domain's workflow
definition, whose agents act only through the domain's commands, so the domain stays the single source of truth. The
**orchestrator** is the project agent the user talks to in the guided chat (D43): it follows the definition, briefs the
role agent that runs each step (CR-PRT-081), keeps only their reports, and asks the user only what needs their judgment,
in their terms (D28). In 0.1.0 it drives the first three phases, issuing the same workspace commands the workflow step
does (DM-11). It reaches the gateway through its agent API over WebSocket (CR-PRT-012) and serves its own endpoint for
Nai (D35, CR-PRT-031).

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern): the chat's command `say` (who, text, attachments: a clip, an element, a
sheet; from the agent, **proposals**: commands it prepared for the user to send, CR-PRT-030) and event `said`; `agent-status` (idle, working on a step, waiting for the user, with what it waits for). Chat
messages are kept in the `workflow` log, so a reload shows the conversation (CR-PRT-030 renders it).

### §S2 The graph and the dispatch

`parti.harness.compile(definition) -> Graph`: one node per step of the workflow definition (CR-PRT-022), in its order;
a node briefs the step's **role** with `run_role` (CR-PRT-081) and its own skills where the step is the orchestrator's,
and records the role's **report**; a step naming a maker then a checker runs the checker on the maker's result, and a
failed check sends the correction back to the maker with the checker's findings (the correction loop, DN-workflow-shape
§6.1), at most three rounds before it asks the user. A **review gate** compiles to an interrupt that waits for the user's
`gate-decided`. The orchestrator's context holds the conversation, the workflow run's projection and the reports, never
a role's working context. The graph's state is a projection of the workflow run read from the gateway; LangGraph's
checkpointer holds the agent's own state only (its place in the graph, the reports), never the project's (Architecture
B3). Checkpoints and memory sit behind ports, local files in 0.1.0 (`parti/.harness/`).

### §S3 Acting only through the domain

The harness joins the gateway as a participant of kind `agent` (`hello`, D16) and acts through its tools only:
the domain's commands and queries (CR-PRT-012), the library (`parti.workflow.run_step`, `parti.tools.tables`,
CR-PRT-024), the model read, write-back and what the user points at (CR-PRT-025), and SolidCraft's MCP server as a client for what needs judgment
(D21). Rules, binding the orchestrator and every role agent: **H-1** an agent never sends `decide-gate`, `confirm-declaration` or a caveat on the user's behalf: it
proposes, the user decides (D26); **H-2** every change it makes is a command whose events every panel shows (D29); **H-3**
it never edits the model by hand: a correction edits a table row and runs the step again (D26). It sends the workspace
commands (`show`, `set-focus`) as the workflow step does, so the workspace follows it (DM-11).

### §S4 Proposals to the user

What a role reports as needing the user (a calibration, labels and classes, a correction, a human-use finding) the
orchestrator brings to the chat as **proposals** (CR-PRT-030), in the glossary's terms and the display units; the user's
answer is the command, never the agent's (H-1).

### §S5 The harness's endpoint

`parti-harness --target <dir>` serves a WebSocket endpoint on `127.0.0.1` (CloudEvents over `cloudevents.json`, as
CR-PRT-012), with its AsyncAPI 3.0 definition: it receives the events the router sends it (`said`, `step-started`,
interaction events) and sends its commands back; until Nai routes them (CR-PRT-031), it connects to the gateway
directly (`bus = "local"`).

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema.
- [ ] `compile` of the `residential/single-family-home` definition gives one node per step of the first three phases, in order, each with its role, and an interrupt at *Confirm the declaration*.
- [ ] (integration, the gateway on a temporary target project, the scripted runner, the fake CAD session) A run from *Intake the sources* registers CR-PRT-003's sheets, calibrates them, records `one_house()`'s tables, builds `L0.walls`, reads the model, classifies it and derives the declaration, every change visible as events in the gateway's logs, then stops at the gate with `agent-status` waiting.
- [ ] In that run the harness sends no `decide-gate`, `confirm-declaration` or caveat (asserted over its outgoing messages).
- [ ] With one table row made wrong so `L0.walls` fails its volume check, the model checker's report sends the correction back to the CAD builder, which corrects the row (the table file changes, no CAD command is sent outside the step), and the checker passes the step's second record.
- [ ] The orchestrator's checkpointed context holds the roles' reports and none of their working messages.
- [ ] A `say` from the user while the harness waits at the gate is answered with a `said`, and `gate-decided` approve resumes the graph to its end.
- [ ] Killing the harness mid-step and starting it again resumes from its checkpoint at the same node, and the project's state comes from the gateway, not the checkpoint.
- [ ] Starting *Build from data* makes the harness send `show` of `model`, and the gateway relays it to the page's connection.
- [ ] Live (`PARTI_LIVE=1`, a workstation with SolidCraft and a model runner): the same run on `one_house()` with SolidCraft headless reaches the gate.
- [ ] Caller-existence: `parti-axi agent start` (CR-PRT-013) starts `parti-harness`; the guided chat (CR-PRT-030) sends `say` and renders `said`, reviewed at their VERIFY.

## Estimated size

8 points.

## Non-goals

The role agents, their skills and the model runner (CR-PRT-081); the Design phase's roles and skills (CR-PRT-037, CR-PRT-077, 0.2.0); Blender and Unreal through MCP (with
their releases); the Nai agents that keep the router current (with Nai, D29); several agents in a session (CR-PRT-070,
1.0.0); answering questions about the building (D24, later).

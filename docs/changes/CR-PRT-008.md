# CR-PRT-008 — Session: selection

**Status:** PENDING (spec drafted 2026-11-23; rewritten 2026-11-24 for the roadmap; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten: the selection and the interaction events (PRD-domain §5); the conditions moved to CR-PRT-048 (0.4.0); the interaction events moved here from CR-PRT-022, since the session holds them.
**Priority:** High
**Depends on:** CR-PRT-002
**Labels:** domain, session, interaction
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/research/PRD-domain.md` §2.1a, §5, §7 (v0.4); `docs/research/PRD-parti.md` D29, D31; FR-SEL-1 to FR-SEL-3

## Context

In 0.1.0 the session has one participant (a user) and holds what is **selected** and the **interaction events**: a
pointing, a selection or a clip in the page, each carrying the elements it touches. They change nothing in the design or
the building: they are the shared context the workflow and the project agent read (PRD-parti D29), kept outside every
history so undo and versions stay clean. The domain is pure (R1): plain functions over plain data, no input or output,
no imports beyond `@parti/schema`.

## Scope

### §S1 Messages

Added to the schema (CR-PRT-002's pattern): command `select` and event `selection-changed`; the interaction events
`parti.interaction.pointed/1`, `parti.interaction.selected/1` and `parti.interaction.clipped/1`, each carrying its
**elements** (id, name, kind, tags: the labels of PRD-domain §2.1a), the **area** (in the view's frame), the **world
bounds** (mm), the **CAD references**, the **view** and the **step**.

### §S2 Selection

`packages/domain/src/session/`: `select` names one or more **elements** by id (a room, a surface, an opening, a region,
a model object or one of its faces; zones from 0.2.0), or nothing, with where it was made (`page`, `cad`); it yields
`selection-changed`, refusing an id the building and the model (passed in as data) do not hold with `unknown-target`,
listing the ids. `decideSession`, `evolveSession`, `initialSession` (nothing selected).

### §S3 Interaction context

`recordInteraction(session, event)` keeps the interaction events in the session as its **context**: the last 50, newest
first, never in an event log of the design or the building. `context(session)` returns them with the current selection,
for the workflow and the agent.

## Acceptance criteria

- [ ] Each message of §S1 validates against its schema; a `pointed` event without its elements is refused with the schema's fault.
- [ ] Selecting a surface, then a model object's face, then nothing, yields three `selection-changed` events, and the final selection is empty.
- [ ] Selecting two elements at once gives a selection of both, in the order given; selecting `nope` is refused with `unknown-target` naming `nope`.
- [ ] After 60 interaction events, `context` returns the last 50, newest first, with the current selection.
- [ ] Recording an interaction event changes neither the building's nor the model's state, and yields no event for their logs.
- [ ] Caller-existence: `decideSession` and `recordInteraction` are called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

3 points.

## Non-goals

The conditions (CR-PRT-048, 0.4.0); several participants and agents joining a session (1.0.0, CR-PRT-070); telemetry
from the interaction events (with Nai, CR-PRT-064); selecting zones (with the design, 0.2.0).

# CR-PRT-021 — Project Environment: the shell

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-002
**Labels:** page, ui, project-environment
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-parti.md` D22 (the Project Environment, suggestions), D25, D28; `docs/Architecture.md` B3 (`page`); `.lavish/storyboards.html` storyboard 0 (the layout), reviewed with the owner

## Context

The Parti Project Environment is the architect's or designer's workspace in the browser, from scaffolding until the
Unreal walkthrough joins it (D22). 0.1.0's components (the asset browser, the design workspace, quantities, the mock
walkthrough) live inside one shell, the layout the owner reviewed as storyboard 0. The guided chat and the workflow
view need the harness and arrive later; the shell keeps their places.

## Scope

### §S1 Layout

`packages/page`: three columns that never move: the **workflow rail** (left; in 0.1.0 the project template's phases,
D30, with the Design phase current), the **workspace** (middle; tabs Assets, Design, Quantities, Walkthrough, Views,
Offers, Project; in 0.1.0 Views and Offers show "arrives later"), and the **chat panel** (right; in 0.1.0 a notice
that the guided chat arrives with the harness, and the suggestions area). A top bar shows the project, the current
phase, the display units (D25) and the connection.

### §S2 Connection and state

The page connects to the gateway over WebSocket through a **session-channel port**, applies the `snapshot` then each
event to a local projection, and reconnects with backoff; a banner shows while disconnected. Components read the
projection only.

### §S3 Suggestions

A `Cues` component, shown beside the selection in each workspace component, renders up to five one-click
suggestions (D22) given by the component for its current state; clicking one sends its command or opens its view.

## Acceptance criteria

- [ ] (module, the session-channel port faked) The shell renders the three columns, the seven tabs and the top bar with `sq ft · ft-in · mm` from the project's settings.
- [ ] Applying a snapshot and three events through the fake channel gives the same projection as the domain's `evolve` over the same events.
- [ ] Dropping the channel shows the disconnected banner within 1 s; restoring it clears the banner and replays from the last sequence number.
- [ ] A component that gives three cues shows three; clicking one sends its command through the channel (asserted on the fake).
- [ ] (e2e, with CR-PRT-012) `parti-axi open` serves the shell at `/`, and the browser shows it connected.
- [ ] Caller-existence: CR-PRT-014, CR-PRT-015 and CR-PRT-016 render inside the shell's workspace (reviewed at their VERIFY).

## Estimated size

5 points.

## Non-goals

The guided chat and the workflow view (with the harness); visual design beyond the storyboards' layout.

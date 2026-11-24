# CR-PRT-021 — Project Environment: the shell

**Status:** PENDING (spec drafted 2026-11-24, reworked 2026-11-24 from the storyboard review; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-002, CR-PRT-022
**Labels:** page, ui, project-environment
**Phase:** 0.1.0 · wave 3
**Design reference:** `docs/research/PRD-parti.md` D22 (the Project Environment, its interaction model (a) to (f), suggestions), D25, D28, D29, FR-WF-14; `docs/research/PRD-domain.md` §2.1a, §7, §11; `docs/Architecture.md` B3 (`page`), B4, B9; `.lavish/storyboards.html` storyboards 0 to 2 and card `#wf-driver-proposal`, approved by the owner (24 November 2026)

## Context

The Parti Project Environment is the architect's or designer's workspace in the browser, from scaffolding until the
Unreal walkthrough joins it (D22). Its components (the asset browser, the surface editor, the BOM, the mock walkthrough,
Settings) live inside one shell, reviewed with the owner as storyboards. The workspace has no tabs: it is a viewport
the workflow step commands in 0.1.0 (CR-PRT-022) and the project agent later. Parti augments the CAD, Blender and
Unreal and never duplicates their editing (D22 (f)).

## Scope

### §S1 Layout and panels

`packages/page`: the **workflow panel** (left), the **workspace** (middle), the **chat panel** (right; in 0.1.0 a
notice that the guided chat arrives with the harness, and the suggestions area) and the **asset browser** (docked at the
bottom, CR-PRT-014). Every panel resizes, minimises, maximises, undocks and attaches again at any edge; the layout is
kept per user (in the browser's storage) and can be reset. A top bar shows the project, the current phase and step,
the display units (D25), the connection and ⚙ (Settings, CR-PRT-023).

### §S2 The workspace, commanded

The workspace obeys the **workspace commands** (`show`: a view or an editor, its subject, its title; CR-PRT-022),
rendering the registered component (`project`, `bom`, `walkthrough`, `surface`, `labels`, `settings`) with the title
(*Design · Bath 1 › East wall*). It opens on **Project** (the template, its phases, the declaration's state, the units
and the catalogue's presence). The **labels** editor lists the elements with their labels (name, kind, id, tags) and
edits a zone's name and tags.

### §S3 The workflow panel, actionable

The phases and the Design phase's steps of the run (CR-PRT-022), with their to-dos and the done marks. Picking a step
sends `start-step`; completing it sends `complete-step` (a refusal `checklist-open` lists the open items, with *Complete
with a caveat*); ticking a to-do sends `tick-todo`. Selecting a surface anywhere sends `set-focus`.

### §S4 The 2D tools

One toolbar shared by every 2D display: **pointer**, **select**, **rectangle select**, **rectangle clip**, **tag**.
Pointing, selecting and clipping send the interaction events (`pointed`, `selected`, `clipped`, CR-PRT-022) with their
elements, area, world bounds, CAD references, view and step; the gateway relays them unstored (CR-PRT-012). A clip is
attached to the chat panel; tagging opens the element's label.

### §S5 Connection and state

The page connects to the gateway over WebSocket through a **session-channel port**, applies the `snapshot` then each
event to a local projection, and reconnects with backoff; a banner shows while disconnected. Components read the
projection only.

### §S6 Suggestions

A `Cues` component, shown beside the selection in each workspace component, renders up to five one-click
suggestions (D22) given by the component for its current state; clicking one sends its command or opens its view.

## Acceptance criteria

- [ ] (module, the session-channel port faked) The shell renders the four panels and the top bar with `sq ft · ft-in · mm` from the project's settings, and the workspace opens on Project.
- [ ] A `show` of `surface` with title `Design · Bath 1 › East wall` from the fake channel renders the surface editor with that title; a `show` of `bom` replaces it.
- [ ] Picking *Place and set out* in the workflow panel sends `start-step`; completing it with an open item shows the items and *Complete with a caveat*.
- [ ] Undocking the asset browser and attaching it at the right edge keeps it there after a reload; *Reset the panels* returns it to the bottom.
- [ ] With the rectangle select tool, dragging over two zones sends one `selected` event naming both zones' ids, names, kinds and tags and the view and step.
- [ ] A rectangle clip appears in the chat panel with its elements listed.
- [ ] Applying a snapshot and three events through the fake channel gives the same projection as the domain's `evolve` over the same events.
- [ ] Dropping the channel shows the disconnected banner within 1 s; restoring it clears the banner and replays from the last sequence number.
- [ ] A component that gives three cues shows three; clicking one sends its command through the channel (asserted on the fake).
- [ ] (e2e, with CR-PRT-012) `parti-axi open` serves the shell at `/`, and the browser shows it connected.
- [ ] Caller-existence: CR-PRT-014, CR-PRT-015, CR-PRT-016 and CR-PRT-023 render inside the shell (reviewed at their VERIFY).

## Estimated size

10 points.

## Non-goals

The guided chat and the agent issuing the workspace commands (with the harness); detaching a panel to its own window
other than the asset browser's (CR-PRT-014); editing geometry (it stays in the CAD, Blender and Unreal); visual design
beyond the storyboards.

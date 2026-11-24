# CR-PRT-030 — Project Environment: the guided chat

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-021, CR-PRT-029
**Labels:** page, ui, project-environment, harness
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` D21, D22, D26, D28, D29; `docs/Architecture.md` B3 (`page`: the guided chat); `.lavish/storyboards.html` storyboards 0 and 6, approved by the owner (24 November 2026)

## Context

The guided chat is where the architect or designer talks to the project agent (D22): it follows the workflow, asks what
needs their judgment, and shows its proposals for them to accept. The user never writes code, data or commands (D28):
what the agent proposes, they accept or change with a click, and every decision is theirs (H-1, CR-PRT-029). It fills
the shell's chat panel (CR-PRT-021).

## Scope

### §S1 Conversation

The conversation from the `workflow` log (`said`, CR-PRT-029), newest at the bottom, kept across reloads; the input
sends `say`, with **attachments**: a clip from the 2D tools (CR-PRT-021 §S4), the selection, a sheet. Each message
shows who said it and when; an element named in a message is a link that selects it.

### §S2 The agent's state

`agent-status` shown above the input: idle, working on a step (with its name), or waiting for the user (with what for).
When the harness is not connected, the panel says so and gives the command that starts it (`parti-axi agent start`).

### §S3 Proposals and gates

A message from the agent may carry **proposals**: commands the agent prepared for the user to send (labels, classes, a
calibration, a correction), each shown as a card in the glossary's terms and the display units with *Accept*, *Change*
(opening the editor it belongs to) and *Decline*; *Accept* sends the command as the user. When the run waits at a review
gate, the chat shows the gate with *Approve* and *Send back* (with a note), sending `decide-gate` (CR-PRT-022).

## Acceptance criteria

- [ ] (module, the session-channel port faked) The panel renders a conversation of four `said` events in order, and after a reload the same four.
- [ ] Typing a message with a clip attached sends one `say` carrying the clip's elements.
- [ ] An agent message proposing three classes shows three cards; *Accept* on one sends its `classify-object` as the user, and the card shows it accepted.
- [ ] *Change* on a proposed calibration opens the calibration editor for that sheet.
- [ ] With `agent-status` waiting at *Confirm the declaration*, the chat shows *Approve* and *Send back*; *Send back* with a note sends `decide-gate` with the note.
- [ ] With the harness disconnected, the panel shows the notice with `parti-axi agent start`.
- [ ] Caller-existence: the shell renders the chat panel (CR-PRT-021), and the harness sends the proposals (CR-PRT-029), reviewed at VERIFY.

## Estimated size

5 points.

## Non-goals

Voice and the guide's speech (later, D22); several agents in one conversation (CR-PRT-070, 1.0.0); the agent's answers
about the building (D24, later).

# CR-PRT-023 — Project Environment: Settings

**Status:** PENDING (spec drafted 2026-11-24; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: **to be rewritten**: the model provider (the Anthropic API, OpenAI-compatible, the Claude Code runner; PRD-parti D21, D33), Nai and SolidCraft.
**Priority:** Medium
**Depends on:** CR-PRT-013, CR-PRT-021, CR-PRT-029, CR-PRT-031
**Labels:** page, ui, configuration
**Phase:** 0.1.0 · wave 5
**Design reference:** `docs/research/PRD-parti.md` D22 (e), D25, D30; `docs/Architecture.md` B9; `.lavish/storyboards.html` storyboard 8 and card `#wf-driver-proposal`, approved by the owner (24 November 2026; the menu named **Settings**)

## Context

**Settings** (⚙ in the top bar) is the editor of the project's configuration, kept in `parti.toml` (written by
`parti-axi init`, CR-PRT-013); secrets are only ever in the environment. It opens in the workspace like any editor
(CR-PRT-021, the workspace command `show settings`, CR-PRT-022).

## Scope

### §S1 Sections

Shown in order: **Project** (name, type and template, layers; read only in 0.1.0), **Units and display** (area and
length units, D25), **World defaults** (date, time, weather at start), **Design defaults** (setting-out rule, grout,
wastage, rounding), **Backend connections** (the gateway's address; EntityStore and Nai shown as "later"), **Agent and
skills** ("arrives with the harness"), **Layout** (reset the panels), **Telemetry** (off; "arrives with Nai").

### §S2 Saving

Changes are sent as a `set-settings` command; the gateway validates them, writes `parti.toml` (keeping its comments and
unknown keys) and sends `settings-changed` to every connection, which the page applies (units change at once). A value
that names a secret (a key, a token, a password) is refused with `secret-in-config`.

## Acceptance criteria

- [ ] (e2e) Opening ⚙ shows the eight sections in order, with Project read only.
- [ ] Changing the length unit to `mm` rewrites `length_unit = "mm"` in `parti.toml`, keeps its comments, and a second tab shows lengths in mm without a reload.
- [ ] Setting wastage to 12 % changes the to-buy quantity in the BOM view to match the `quantities` query.
- [ ] Entering an API key in a connection field is refused with `secret-in-config`, and `parti.toml` is unchanged.
- [ ] *Reset the panels* returns the layout to its default (asset browser at the bottom).
- [ ] Caller-existence: the shell's ⚙ issues `show settings`, and the gateway handles `set-settings` (reviewed at VERIFY).

## Estimated size

3 points.

## Non-goals

Editing the project type or layers; the connections to EntityStore and Nai, the agent's settings and telemetry (later);
user accounts.

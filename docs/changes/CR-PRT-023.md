# CR-PRT-023 — Project Environment: Settings

**Status:** PENDING (spec drafted 2026-11-24; rewritten the same day for the roadmap; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten: the model provider (the Claude Code runner, an API provider; PRD-parti D21, D33), the bus (Nai or local), SolidCraft; the design and world defaults move with their releases.
**Priority:** Medium
**Depends on:** CR-PRT-013, CR-PRT-021, CR-PRT-029, CR-PRT-031
**Labels:** page, ui, configuration
**Phase:** 0.1.0 · wave 5
**Design reference:** `docs/research/PRD-parti.md` D21, D22 (e), D25, D30, D33, D35; `docs/Architecture.md` B9; `.lavish/storyboards.html` storyboard 8 and card `#wf-driver-proposal`, approved by the owner (24 November 2026; the menu named **Settings**)

## Context

**Settings** (⚙ in the top bar) is the editor of the project's configuration, kept in `parti.toml` (written by
`parti-axi init`, CR-PRT-013); secrets are only ever in the environment or the tool's own login (the Claude Code
runner's). It opens in the workspace like any editor (CR-PRT-021, the workspace command `show settings`, CR-PRT-022).

## Scope

### §S1 Sections

Shown in order: **Project** (name, type and template; read only in 0.1.0), **Units and display** (area and length
units, D25; the calibration tolerance), **CAD** (the application, SolidCraft; how the library reaches it, the running
application or headless; its units and the declared transform, D25), **Agent** (the model runner: the Claude Code
runner or an API provider, with the name of the environment variable holding its key, never the key; CR-PRT-029),
**Bus** (`nai` or `local`, CR-PRT-031; Nai's address, shown with the connection's state), **Layout** (reset the panels).
Sections for the design, the world and telemetry arrive with their releases.

### §S2 Saving

Changes are sent as a `set-settings` command; the gateway validates them, writes `parti.toml` (keeping its comments and
unknown keys) and sends `settings-changed` to every connection, which the page applies (units change at once). A value
that is a secret (a key, a token, a password, recognised by its form) is refused with `secret-in-config`. A change the
harness or a connection reads at start (the runner, the bus, the CAD's connection) is marked *applies after a restart*,
with a button that restarts the harness (`parti-axi agent`, CR-PRT-013).

## Acceptance criteria

- [ ] (module) Opening ⚙ shows the six sections in order, with Project read only.
- [ ] Changing the length unit to `mm` rewrites `length_unit = "mm"` in `parti.toml`, keeps its comments, and a second connection shows lengths in mm without a reload.
- [ ] Choosing the API provider with the variable name `ANTHROPIC_API_KEY` stores the name only; entering a key itself in that field is refused with `secret-in-config`, and `parti.toml` is unchanged.
- [ ] Changing the bus to `local` is marked *applies after a restart*, and the restart button restarts the harness, which then connects to the gateway directly.
- [ ] Changing the CAD's units to `cm` without a transform is refused with `unsupported-units`.
- [ ] *Reset the panels* returns the layout to its default.
- [ ] Caller-existence: the shell's ⚙ issues `show settings`, and the gateway handles `set-settings` (reviewed at VERIFY).

## Estimated size

3 points.

## Non-goals

Editing the project type (CR-PRT-056, 0.5.0); the design defaults (setting-out, grout, wastage: 0.2.0); the world
defaults (0.4.0); telemetry (CR-PRT-064, 0.6.0); user accounts.

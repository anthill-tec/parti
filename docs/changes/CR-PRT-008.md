# CR-PRT-008 — Session and setting

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-002
**Labels:** domain, session, world-builder
**Phase:** 0.1.0 · wave 2
**Design reference:** `docs/research/PRD-domain.md` §5; `docs/research/PRD-parti.md` D18, FR-SEL-1 to FR-SEL-3, FR-STA-1 to FR-STA-3

## Context

The session holds what is selected and the world builder's setting (time, date, weather) as shared state; nothing is
rendered from the setting until the Unreal plugin exists. The domain is pure (R1): plain functions over plain data, no input or output, no imports beyond `@parti/schema`.

## Scope

- `select` (a surface id, a zone id, or nothing) → `selection-changed`, refusing an unknown id with `unknown-target`
  (the building and design passed in as data).
- `set-time` (date `YYYY-MM-DD`, time of day `HH:MM`) and `set-weather` (`clear` | `overcast` | `rain`) →
  `setting-changed` with the whole setting. The place is the building's site (null when undeclared).
- `evolveSession` and `initialSession` (nothing selected; noon, today's date given by the caller, clear).

## Acceptance criteria

- [ ] Selecting a surface, then a zone of it, then nothing, yields three `selection-changed` events and the final selection is empty.
- [ ] Selecting `nope` is refused with `unknown-target`.
- [ ] `set-time` with `25:00` is refused with `invalid-value`; `set-weather` `rain` gives a setting with `weather: "rain"` and the earlier time kept.
- [ ] Caller-existence: `decideSession` is called from `packages/gateway/src` (reviewed at CR-PRT-012 VERIFY).

## Estimated size

3 points.

## Non-goals

Several participants, agents joining a session (later, D16); rendering the setting (Unreal plugin).

# CR-PRT-013 — parti-axi

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-011, CR-PRT-012
**Labels:** cli, python, installer
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-AXI-1 to FR-AXI-6, D16, D25; `docs/Architecture.md` §5 (`parti-axi`), §9; `docs/research/PRD-domain.md` §2.3a, §8

## Context

`parti-axi` installs Parti into a target project and gives an agent everything a person can do (D16): structured
output, a dry run, and a flag for every question.

## Scope

### §S1 Commands

- `parti-axi init --target <dir> [--parti-dir parti] [--area-unit sq-ft|m2] [--length-unit ft-in|mm|m] [--yes]`
  writes `<dir>/parti.toml` (folder, display units with D25's defaults, gateway port, the working models' scales,
  empty) and `<dir>/parti/` with its sub-folders; writes Parti's skills (`.agents/skills/parti-*`: in 0.1.0, using
  `parti-axi` and the finish tool, and translating the project's own records into Parti's formats with the library
  and building the catalogue) and agent definitions; records the
  project's dependencies on `parti` and `parti-axi` (D27); and appends Parti's section to the target project's
  `AGENTS.md` (created if absent). Re-running is safe: existing values are kept unless a flag changes them.
- `parti-axi doctor` checks Bun, the configuration, the declaration's validity and the catalogue's presence, one line
  per check.
- `parti-axi gateway start|stop|status` runs the gateway in the background with a pid file under `parti/.run/`.
- `parti-axi catalogue build --from <records.ndjson> [--scans <scans.ndjson>]` builds the catalogue from records in
  Parti's format (CR-PRT-011) and prints the report's counts.
- `parti-axi building import [--file <path>]` sends `import-building` and prints the events or the faults.
- `parti-axi scale set <model> (--units <u> --scale <s> | --known "<label>=<mm>" --measured <value>)` records a working
  model's scale (D25), calibration computing `scale = known / measured`.
- `parti-axi state [--query <name>] ` and `parti-axi command <name> --json <payload>` send queries and commands.

### §S2 Output

Every command takes `--json`, printing one JSON object (`ok`, the result or the faults); without it, a short human
summary in the display units. Exit codes: 0 ok, 1 refused or failed check, 2 usage error. `--dry-run` on `init`,
`building import` and `command` prints what would change and changes nothing.

## Acceptance criteria

- [ ] `init --yes` on an empty temporary folder creates `parti.toml` with `area_unit = "sq-ft"` and `length_unit = "ft-in"`, the `parti/` sub-folders of PRD-domain §8, and an `AGENTS.md` with the Parti section, the `parti-*` skills and agent definitions; a second run changes nothing (files byte-identical).
- [ ] `init --dry-run` creates nothing and lists the files it would write.
- [ ] (integration) `gateway start`, then `building import` of `oneBath`, then `state --query building --json` returns five surfaces; `gateway stop` leaves no process (pid gone).
- [ ] `building import` of `faulty` exits 1 and its `--json` output lists the three faults.
- [ ] `scale set blender --known "door=2100" --measured 2.1` stores `scale = 1000` for `blender`.
- [ ] `command define-zone --json '{...}'` prints the `zone-defined` event; an unknown command name exits 2.
- [ ] Caller-existence: `parti_axi` calls `parti.schema.validate_message` before sending and `parti.catalogue.build` in `catalogue build`.

## Estimated size

8 points.

## Non-goals

`watch`, the Pi plugin and agents joining a live session (FR-AXI-8, FR-AXI-9, later); publishing to PyPI (a release
step); the workflow guide (later).

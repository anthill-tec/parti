# CR-PRT-013 — parti-axi

**Status:** PENDING (spec drafted 2026-11-23; rewritten 2026-11-24 for the roadmap; gap analysis not yet run)
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (PRD-parti D33), as on the Crucible board: rewritten: sources and calibration, the model build, read and watch, classification, declare; `parti-axi init` sets up the Nai part with Nai's tools (PRD-parti D39); the catalogue build moves to CR-PRT-011 (0.2.0).
**Priority:** High
**Depends on:** CR-PRT-012, CR-PRT-024, CR-PRT-027, CR-PRT-028
**Labels:** cli, python, installer, nai
**Phase:** 0.1.0 · wave 4
**Design reference:** `docs/research/PRD-parti.md` FR-AXI-1 to FR-AXI-6, D16, D25, D28, D30, D33, D39; `docs/Architecture.md` B3 (`parti-axi`), B7; `docs/research/PRD-domain.md` §1, §2.3a, §2.6, §2.7, §8

## Context

`parti-axi` installs Parti into a target project and gives an agent everything a person can do (D16): structured
output, a dry run, and a flag for every question. In 0.1.0 it carries the first three phases: the sources and their
calibration, the model built from data and read live, its classification, and the declaration derived and confirmed.
A target project is also a Nai project of Parti's kind, set up with Nai's own tools (D39).

## Scope

### §S1 Scaffolding

- `parti-axi init --target <dir> [--type residential/single-family-home] [--parti-dir parti] [--cad solidcraft]
  [--cad-units mm] [--area-unit sq-ft|m2] [--length-unit ft-in|mm|m] [--no-nai] [--yes]` writes `<dir>/parti.toml` (the
  project type and its template, D30: 0.1.0 ships one, an unknown type refused with the list of known ones; the folder;
  the display units with D25's defaults; the gateway port; the CAD application, its units and the declared transform;
  the calibration tolerance, 0.5 %; the bus, `nai` or `local` with `--no-nai`, CR-PRT-031; the harness's model runner,
  CR-PRT-029) and `<dir>/parti/` with the sub-folders of PRD-domain §8 and `steps/`; writes
  Parti's skills (`.agents/skills/parti-*`: using `parti-axi`, writing data tables and steps with the library, labelling
  and classifying; the harness's own skills come with CR-PRT-029) and agent definitions. The skills teach D28's
  division: the agent speaks to the architect or designer in the glossary's terms and display units, offers options
  and pictures, and never asks them to write code, data or commands. It records the project's dependencies on `parti`
  and `parti-axi` (D27) and appends Parti's section to the project's `AGENTS.md` (created if absent).
- **The Nai part (D39):** unless `--no-nai`, `init` runs `nai new <project> --template <Parti's template>` then `nai
  check`, and never writes Nai's files by hand; Nai's absence or a failed check stops `init` with Nai's own message and
  the hint `--no-nai` (the template is Nai's, at Parti's request, CR-PRT-031).
- Re-running is safe: existing values are kept unless a flag changes them.

### §S2 Running

- `parti-axi doctor`: one line per check: Bun, `parti.toml`, the gateway, SolidCraft's MCP server reachable, Nai (or
  `--no-nai` recorded), the logs readable.
- `parti-axi gateway start|stop|status` runs the gateway in the background with a pid file under `parti/.run/`.
- `parti-axi agent start|stop|status` runs the harness (`parti-harness`, CR-PRT-029) the same way.
- `parti-axi open` starts the gateway if it is not running and prints the Project Environment's address, opening it in
  the default browser unless `--no-browser`.

### §S3 The first three phases

- **Sources:** `sources add <path> --kind plan|elevation|section|detail|render|document [--level L] [--page N]`,
  `sources list`; `sheet calibrate <source> --from x1,y1 x2,y2 --mm <len> --check x1,y1 x2,y2 --check-mm <len>
  [--caveat <text>]`; `tables record <file>` (reads it with `parti.tools.tables`, CR-PRT-024, and sends
  `record-data-table` with the sheets each row cites).
- **Model:** `model build <step> [--app|--headless]` runs `parti.workflow.run_step` (CR-PRT-024) and prints the step
  record; `model read` reads the inventory once and sends `read-model`; `model watch` runs CR-PRT-025's `watch`, sends
  each inventory, and applies the **write-back** the gateway sends (`tag`, CR-PRT-012); `model classify <object>
  <class>`; `model rules` lists the project's classification rules (in `parti.toml`).
- **Declare:** `declare derive` (with the data tables' rooms), `declare confirm [--surface <id>] [--set field=value]`,
  `declare compare <file>` (a declaration the project wrote itself); `building import [--file <path>]` still imports
  one.
- `parti-axi state [--query <name>]` and `parti-axi command <name> --json <payload>` send queries and commands.

### §S4 Output

Every command takes `--json`, printing one JSON object (`ok`, the result or the faults); without it, a short human
summary in the display units. Exit codes: 0 ok, 1 refused or failed check, 2 usage error. `--dry-run` on `init`,
`building import`, `declare confirm` and `command` prints what would change and changes nothing. Every message is a
CloudEvent on the gateway's endpoint (CR-PRT-012), validated with `parti.schema` before it is sent.

## Acceptance criteria

- [ ] `init --no-nai --yes` on an empty temporary folder creates `parti.toml` with `area_unit = "sq-ft"`, `length_unit = "ft-in"` and `cad = "solidcraft"`, the `parti/` sub-folders, an `AGENTS.md` with the Parti section, the `parti-*` skills and agent definitions; a second run changes nothing (files byte-identical).
- [ ] `init --dry-run` creates nothing and lists the files it would write.
- [ ] `init --type commercial/office` exits 2 and lists `residential/single-family-home`.
- [ ] With a fake `nai` on the path, `init --yes` runs `nai new <project> --template <template>` then `nai check`, in that order, and writes no file under the paths Nai generates; a fake `nai check` failing stops `init` with exit 1 and its message.
- [ ] (integration) `open --no-browser` on a scaffolded project starts the gateway and prints an address whose page answers 200; `gateway stop` leaves no process.
- [ ] (integration) `sources add` of CR-PRT-003's plan, then `sheet calibrate` from its sidecar's dimension lines, then `state --query sources --json` shows the sheet calibrated with its check within tolerance.
- [ ] (integration, the fake CAD session) `model build L0.walls` prints a step record whose checks pass; `model read` then `state --query model --json` lists the level-0 wall objects classified by the rule `L0.walls → structure.wall`.
- [ ] (integration) `declare derive` then `declare confirm` on `one_house()` gives a building revision equal to the G6 oracle.
- [ ] `building import` of `makeFaulty()`'s declaration exits 1 and its `--json` output lists exactly its `breaches`.
- [ ] `command import-building --json '{...}'` prints the `building-revised` event; an unknown command name exits 2.
- [ ] Caller-existence: `parti_axi` calls `parti.schema.validate_message` before sending, `parti.workflow.run_step` in `model build`, and `parti.translators.solidcraft.watch` and `tag` in `model watch`.

## Estimated size

8 points.

## Non-goals

The Pi plugin and agents joining a live session by a wake-up (FR-AXI-8, FR-AXI-9; with the harness, CR-PRT-029); the
catalogue build (CR-PRT-011, 0.2.0); Nai's template itself (Nai's, requested in CR-PRT-031); publishing to PyPI (a
release step).

# CR-PRT-080 — parti-axi: adopting an existing project, and the complete scripts

**Status:** PENDING (spec drafted 2026-11-25; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** CR-PRT-013, CR-PRT-024, CR-PRT-079
**Labels:** parti-axi, scaffold, sdk, axi
**Phase:** 0.1.0 · wave 4
**Design reference:** the AXI standard (https://axi.md/); `docs/research/PRD-parti.md` D16, D27, D39, FR-AXI-2, FR-AXI-4, FR-AXI-6; JohnnyHouse #1690

## Context

JohnnyHouse was made by hand before `parti-axi` existed, and other projects will be too. The owner ruled that such a
project is adopted in place: Parti maps what is there and never moves or overwrites the project's own files (FR-AXI-2).
He also ruled that the SDK reaches a project as complete scripts as well as the library (D27): ready-made AXI tools,
installed into the project, so that the project's own scripts shrink to its data and rules.

## Scope

### §S1 Adoption: `parti-axi init` on a non-empty project

`init --target <dir>` on a folder with content first **surveys** it, read only: drawing sheets and renders (by type,
or `--sources <glob>`), CAD files (`.sc`), data tables valid against `parti.tables/1`, a building declaration valid
against `parti.building/1`, the project's scripts (by folder, or `--scripts <glob>`), its `AGENTS.md` and skills. It
then writes `parti.toml` naming what it found, creates only the missing parts of `<dir>/parti/`, appends Parti's section
to `AGENTS.md`, and installs Parti's skills, agent definitions and scripts beside the project's own. It **moves,
renames and overwrites none of the project's files**: a path Parti would write that the project already holds is
skipped and reported (`--overwrite <path>` to replace it, after a `--dry-run`). The report lists what was **mapped**,
what was **left to migrate** (each of the project's scripts, with the complete script or library function that may
replace it where the name or the tables it reads make it clear), and the next steps (`help[]`: `sources add`, `sheet
calibrate`, `building import`). `--dry-run` reports the survey and writes nothing. The Nai part runs as in CR-PRT-013.

### §S2 The complete scripts (D27)

The library ships `parti.scripts`, AXI tools built on `parti.axi` (CR-PRT-013 §S4), each runnable with the project's
configuration and no gateway (offline, in a batch, in the project's own CI):

- `build_group <group>`: CR-PRT-024's `run_step` for one feature group, headless or connected, writing its checkpoint
  and step record;
- `read_model`: CR-PRT-025's `read`, writing `parti/model/inventory.json` (no domain event: the gateway's `model read`
  does that);
- `check_tables`: the data tables against `parti.tables/1` and their citations;
- `check_human_use`: CR-PRT-079's checks on the last inventory, with the surveys.

`init` installs each as `<dir>/parti/scripts/<name>.py`, a thin launcher whose first line marks it Parti-managed with
its version and hash; a re-run after an upgrade refreshes an unchanged one and keeps, and reports, one the project has
edited (FR-AXI-6). Each script follows the AXI standard: with no arguments it shows what it would act on, it ends every
output with `help[]`, and `--help` is a concise reference.

## Acceptance criteria

- [ ] (integration) `init --dry-run` on a synthetic hand-made project (two sheets, a `.sc` file, a valid declaration, two scripts, an `AGENTS.md`) reports each as mapped or left to migrate and writes nothing (the folder's tree and hashes unchanged).
- [ ] `init` on the same project writes `parti.toml` naming the sheets, the CAD file and the declaration; every file the project had keeps its content and path; its `AGENTS.md` keeps its text with Parti's section appended.
- [ ] A project file at a path Parti would write is skipped and reported; with `--overwrite <path>` it is replaced.
- [ ] `init` installs the four scripts, each marked Parti-managed; after an edit to one, a re-run refreshes the other three and reports the edited one as kept.
- [ ] `parti/scripts/check_human_use.py` with no arguments shows the last inventory's revision and the checks it would run; run, it prints CR-PRT-079's results as TOON ending in `help[]`, and exits 1 on a failure.
- [ ] `build_group L0.walls` with the fake CAD session writes the checkpoint and the step record, as `parti-axi model build` does.
- [ ] Caller-existence: the scripts call `run_step`, `read`, the tables validator and the human-use checks; `init` calls the survey, reviewed at VERIFY.
- [ ] (live, workstation) `init --dry-run --target` JohnnyHouse reports its CAD files, its declaration and its `cad/gen` scripts to migrate, and writes nothing to JohnnyHouse.

## Estimated size

8 points.

## Non-goals

Migrating a project's scripts onto the library (the project's own agent, with the report as its list; JohnnyHouse's
orchestrator for JohnnyHouse); adopting a project's Nai part when it has one of its own (with Nai, CR-PRT-031); removal
(FR-AXI-6, CR-PRT-069).

# CR-PRT-001 — Workspace and toolchain

**Status:** PENDING (spec drafted 2026-11-23; gap analysis 2026-11-24 by Track 1, findings D1–D8 folded in; spec pre-review 2026-11-24, findings P1–P8 folded in; the owner's rulings on D2, D8 and P8)
**Pre-review:** ran — touches another project's surface (Crucible's declaration surfaces: the `test:<tier>` scripts, the per-tier start folder); needed the owner's rulings.
**Type:** feature
**Re-targeted:** 2026-11-24, to the roadmap the owner approved (0.1.0 = the building from CAD); filed on the Crucible board.
**Priority:** High
**Depends on:** —
**Labels:** setup, bun, python, ci
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/Architecture.md` B3 (components), A4 and B2 (R1–R10); `docs/research/DN-test-strategy.md` (tiers, fixtures, CI); `AGENTS.md` (Crucible clients)

## Context

The repository holds only the scaffold: a private root `package.json` with no workspaces, an empty `tests/` package
and two repository guard tests. Every later 0.1.0 CR needs the component layout of Architecture B3, the two stacks
(Bun and Python) wired, and tests run by the Crucible clients and by CI in the tiers of the test strategy.

## Scope

### §S1 Bun workspaces

Root `package.json` declares `"workspaces": ["packages/*"]` and the dev dependency `typescript` (pinned through the
committed `bun.lock`, so `bunx tsc` never fetches an unpinned compiler). Five packages, each with `package.json` (name
`@parti/<name>`, `"private": true`, `"type": "module"`, licence `GPL-3.0-only`), `src/index.ts` and `test/`:
`schema`, `domain`, `gateway`, `adapters-local`, `page` (the `mock-scene` package comes with CR-PRT-016, in 0.4.0).
The dependency direction of Architecture B3 holds: `domain` depends on `@parti/schema` only.

**Type checking:** one root `tsconfig.json` (strict, `noEmit`, `moduleResolution: "bundler"`, `types: ["bun"]`,
including `packages/*/src`, `packages/*/test` and `tests`), with no project references. Nothing is compiled to disk,
so no build output is picked up by the test runner, and `bunx tsc --noEmit -p tsconfig.json` is the same check the
Bun client's gate runs.

Bun links workspaces in isolated mode, so a package that imports another declares it: `domain`, `gateway`,
`adapters-local` and `page` declare `"@parti/schema": "workspace:*"`. `@parti/schema`'s `package.json` has an `exports`
map with `.` and `./test-support`; the test support lives in `packages/schema/src/test-support/` (inside the type
check's `packages/*/src`), where `live(...)` and `isLive` go and CR-PRT-003's generators follow.

### §S2 Python packages

A uv workspace at the root (`pyproject.toml` with `[tool.uv.workspace] members = ["python/*"]`) and two packages,
each built with `uv_build` (a pinned version range) and declaring its licence files:

- `python/parti`, the library (D27; import name `parti`; licence **LGPL-3.0-only**, `license-files` naming `COPYING`
  and `COPYING.LESSER` in the package folder). Empty sub-packages `parti.workflow`, `parti.harness`,
  `parti.catalogue`, `parti.tools`, `parti.translators`, `parti.units`, and `parti.testing`, which holds the live tag
  of §S3 and later the fixture writers of CR-PRT-003; it ships in the wheel, for target projects' own tests.
- `python/parti-axi` (import name `parti_axi`, console script `parti-axi`, GPL-3.0-only with its own `COPYING`,
  depending on `parti`). `parti-axi --version` prints the package version; with no arguments it prints its usage and
  exits 0; an unknown option prints an error and exits 2.

Architecture B3's `parti.converters` and `parti.templates` come with the CRs that need them (the format converters in
0.6.0, templates in 0.5.0). There is no `parti.connectors`: the Nai project writes every connector (PRD-parti D34).

**Python 3.14 only** (owner, 2026-11-24): `.python-version` holds `3.14` and both packages declare
`requires-python = ">=3.14"`; Parti claims only the version it tests.

The root `pyproject.toml` has `[dependency-groups] dev = ["unittest-xml-reporting", "coverage"]`, and `uv.lock` is
committed. `uv sync` removes what it did not install, so the Crucible python client's needs are declared here rather
than installed by hand. CI uses `uv sync --locked` and `uv run --locked`, so a stale lock fails rather than being
rewritten.

### §S3 Test layout and tiers

`<tier>` is one of `unit`, `module`, `integration`. The **e2e tier is not set up yet** (owner, 2026-11-24): the first
CR with an end-to-end test (CR-PRT-017) adds it, with its scripts and CI wiring. The Crucible clients find no tiers in
folders; the verb names the tier.

- **Bun:** tests live in `packages/<name>/test/<tier>/*.test.ts`. The root `package.json` declares three scripts,
  `"test:unit": "bun test test/unit/"` and the same for `module` and `integration` (a path filter, matching
  `packages/*/test/<tier>/`); `bun-crucible.py <tier>` runs `test:<tier>`.
- **Python, tier first** (owner, 2026-11-24): tests live in `tests/<tier>/parti_tests/` and
  `tests/<tier>/parti_axi_tests/`, as `test_*.py`, with an `__init__.py` in every tier folder and every
  `*_tests` folder (without them, discovery skips the tests without an error). Tests import their own helpers by
  relative import only, since the module names differ between the three ways the tests are run.
  `python-crucible.py <tier> --start-dir tests/<tier>` runs one tier. The client puts the start folder on the import
  path, so **no test folder shares an import name with an installed package** (a folder `tests/parti/` would hide the
  library). The repository guard tests stay in `tests/`.
- **Every tier's first tests are real**, each with a production subject:

  | Tier | First tests |
  |---|---|
  | unit | each package's `PACKAGE_NAME`, `parti.__version__`, the live tag (Python and Bun) |
  | module | `checkDomainImports` (§S4), `parti-axi`'s argument handling |
  | integration | `parti-axi --version` as a process; the wheel build (§S2) |

**Live tests** (DN-test-strategy: on a workstation, outside CI) are tagged as live: in Python with the decorator
`parti.testing.live`, in Bun with the helper `live(...)` from `@parti/schema/test-support`, which decides through a
pure predicate `isLive(env)`. A live test runs only when the environment variable `PARTI_LIVE=1` is set, and is skipped
(reported as skipped) otherwise; CI never sets it. Live tests are where the real applications (SolidCraft) and a target
project's own files are used, read in place on the workstation and never committed (NFR-10; the owner's note of
2026-11-24 on borrowing JohnnyHouse's data).

### §S4 Dependency boundary check

A test-support function `checkDomainImports(dir)` (in `packages/domain/test/support/`, not a production export) lists
every import in the script files under a folder that is neither `@parti/schema` (or one of its non-test sub-paths)
nor a relative path that stays inside that folder. `@parti/schema/test-support` is reported, because it brings in the
test runtime. The check reads the specifiers with TypeScript's own pre-processor, covers every import form (static
`import`, side-effect `import "x"`, `import type`, `export … from`, `export * from`, `import x = require("x")`, dynamic
`import()` and `require(…)`) in every script file type (`.ts`, `.tsx`, `.mts`, `.cts`, `.js`), and reports any
specifier that is not a literal string. A module test runs it on `packages/domain/src` (R1: the domain is pure). The
failing cases run on fixtures in a temporary folder, never by writing into `packages/domain/src`; the domain's own
`test/` folder is not scanned, so its tests may use the test-support helpers.

### §S5 CI

`release.yml`'s `test-bun` job runs `bun install --frozen-lockfile`, then `bunx tsc --noEmit -p tsconfig.json`, then
`bun test`. Its `test-python` job installs Python 3.14 and a pinned uv, runs `uv sync --locked`, then
`uv run --locked python -m unittest discover -s tests -t .` (the `-t .` keeps the tier folders importable as
packages). The zizmor audit stays green.

## Acceptance criteria

### §S1
- [ ] `bun install --frozen-lockfile` succeeds at the root and `bun pm ls` lists the five `@parti/*` packages.
- [ ] `bunx tsc --noEmit -p tsconfig.json` exits 0 on the tree and writes no file (reviewed: a planted type error makes it fail).
- [ ] Each package's `src/index.ts` exports a `PACKAGE_NAME` constant equal to its `package.json` name, and a unit test per package asserts it.
- [ ] A unit test in `packages/domain` imports `@parti/schema` and `@parti/schema/test-support` and passes.
- [ ] (reviewed) Each package's `package.json` is private, of type `module` and `GPL-3.0-only`; `domain`'s declares `@parti/schema` as its only dependency.
### §S2
- [ ] `parti-axi --version`, run as a process (the console script beside `sys.executable`, integration tier), prints the version in `python/parti-axi/pyproject.toml` and exits 0; with no arguments it prints its usage and exits 0; with `--nope` it exits 2 with an error (module tier, through its argument parser).
- [ ] `import parti.workflow, parti.harness, parti.catalogue, parti.tools, parti.translators, parti.units, parti.testing` succeeds, and `parti.__version__` equals the version in `python/parti/pyproject.toml`.
- [ ] Building both wheels into a temporary folder (integration tier) yields: for `parti`, metadata `License-Expression: LGPL-3.0-only`, `Requires-Python: >=3.14`, `COPYING` and `COPYING.LESSER` under `dist-info/licenses/`, and `parti/testing` in the wheel; for `parti-axi`, `GPL-3.0-only`, its `COPYING`, and a dependency on `parti`.
- [ ] (reviewed) After `uv sync --locked`, `.venv/bin/python -c "import xmlrunner, coverage"` exits 0.
### §S3
- [ ] Each tier's first tests (the table in §S3) are reported to Crucible under that tier by `bun-crucible.py <tier>` and `python-crucible.py <tier> --start-dir tests/<tier>` (reviewed: the Crucible runs' tier counts).
- [ ] (reviewed) CI's discovery and `python-crucible.py regression` each find every tier test exactly once: their counts equal the three tier runs plus the repository guard tests.
- [ ] (reviewed) No folder under `tests/` has the import name of an installed package (`parti`, `parti_axi`), and every tier and `*_tests` folder has an `__init__.py`.
- [ ] A Python unit test decorates a case with `parti.testing.live` and runs it under a patched environment: skipped when `PARTI_LIVE` is unset or `0`, run when it is `1`.
- [ ] A Bun unit test asserts `isLive` is false for an empty environment and for `PARTI_LIVE=0`, and true for `PARTI_LIVE=1`; (reviewed) `release.yml` sets no `PARTI_LIVE`.
### §S4
- [ ] `checkDomainImports("packages/domain/src")` returns nothing on the tree.
- [ ] On temporary-folder fixtures it reports each of: a static import of `node:fs`, a side-effect `import "node:fs"`, `import type` from `@parti/gateway`, `export … from "node:path"`, `export * from "@parti/gateway"`, `import x = require("fs")`, a dynamic `import("node:fs")`, a `require("fs")`, a non-literal `import(name)`, a relative path leaving the folder (`../../gateway/src/x`), the lookalike `@parti/schemas`, and `@parti/schema/test-support`; in `.tsx`, `.mts`, `.cts` and `.js` files as well as `.ts`.
- [ ] It reports nothing for `@parti/schema`, a non-test sub-path of it, and a relative import inside the folder.
### §S5
- [ ] (reviewed, not tested) A push of the feature branch runs `test-bun` (with the type check), `test-python` (Python 3.14, `--locked`) and the zizmor audit green.

## Estimated size

5 points (re-scored at the gap analysis and the pre-review).

## Follow-up outside this CR

- `AGENTS.md` Setup: the Python test interpreter comes from `uv sync` once this CR merges (Mainline updates it at the
  merge).
- CR-PRT-017 adds the e2e tier (its scripts, its start folder, its CI wiring).

## Non-goals

Any domain code, schema content or user-facing feature; the e2e tier; C++ or Unreal; publishing to PyPI (a release
step); Python versions before 3.14.

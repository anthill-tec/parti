# CR-PRT-001 — Workspace and toolchain

**Status:** PENDING (spec drafted 2026-11-23; gap analysis run 2026-11-24 by Track 1, findings D1–D8 folded in, the owner's rulings on D2 and D8; spec pre-review next)
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
`schema`, `domain`, `gateway`, `adapters-local`, `page` (the `mock-scene` package comes with CR-PRT-016, in 0.4.0). A
root `tsconfig.json` (strict) with project references. The dependency direction of Architecture B3 holds: `domain`
depends on `@parti/schema` only.

Bun links workspaces in isolated mode, so a package that imports another declares it: `domain`, `gateway`,
`adapters-local` and `page` declare `"@parti/schema": "workspace:*"`. `@parti/schema`'s `package.json` has an `exports`
map with `.` and `./test-support`.

### §S2 Python packages

A uv workspace at the root (`pyproject.toml` with `[tool.uv.workspace] members = ["python/*"]`) and two packages:
`python/parti`, the library (D27; import name `parti`; licence **LGPL-3.0-only**, with `COPYING.LESSER` beside the GPL
text in the package; empty sub-packages `parti.workflow`, `parti.harness`, `parti.catalogue`, `parti.tools`,
`parti.translators`, `parti.units`, and `parti.testing`, which holds the live tag of §S3 and later the fixture writers
of CR-PRT-003; it ships in the wheel, for target projects' own tests), and `python/parti-axi` (import name `parti_axi`,
console script `parti-axi`, GPL-3.0-only, depending on `parti`). `parti-axi --version` prints the package version.
Architecture B3's `parti.connectors`, `parti.converters` and `parti.templates` come with the CRs that need them (Nai
integration in 0.1.0, the format converters in 0.6.0, templates in 0.5.0).

**Python 3.14 only** (owner, 2026-11-24): `.python-version` holds `3.14` and both packages declare
`requires-python = ">=3.14"`; Parti claims only the version it tests.

The root `pyproject.toml` has `[dependency-groups] dev = ["unittest-xml-reporting", "coverage"]`, and `uv.lock` is
committed. `uv sync` removes what it did not install, so the Crucible python client's needs are declared here rather
than installed by hand.

### §S3 Test layout and tiers

`<tier>` is one of `unit`, `module`, `integration`, `e2e`. The Crucible clients find no tiers in folders; the verb
names the tier.

- **Bun:** tests live in `packages/<name>/test/<tier>/*.test.ts`. The root `package.json` declares four scripts,
  `"test:unit": "bun test test/unit/"` and the same for `module`, `integration` and `e2e` (a path filter, matching
  `packages/*/test/<tier>/`); `bun-crucible.py <tier>` runs `test:<tier>`.
- **Python, tier first** (owner, 2026-11-24): tests live in `tests/<tier>/parti_tests/` and
  `tests/<tier>/parti_axi_tests/`, as `test_*.py`; `python-crucible.py <tier> --start-dir tests/<tier>` runs one
  tier. The client puts the start folder on the import path, so **no test folder shares an import name with an
  installed package** (a folder `tests/parti/` would hide the library). The repository guard tests stay in `tests/`.

**Live tests** (DN-test-strategy: on a workstation, outside CI) are tagged as live: in Python with the decorator
`parti.testing.live`, in Bun with the helper `live(...)` from `@parti/schema/test-support`. A live test runs only when
the environment variable `PARTI_LIVE=1` is set, and is skipped (reported as skipped) otherwise; CI never sets it. Live
tests are where the real applications (SolidCraft) and a target project's own files are used, read in place on the
workstation and never committed (NFR-10; the owner's note of 2026-11-24 on borrowing JohnnyHouse's data).

### §S4 Dependency boundary check

A function `checkDomainImports(dir)` lists every import in the TypeScript files under a folder that is neither
`@parti/schema` (or a path below it) nor a relative path inside that folder. It reads every import form: static
`import`, `import type`, `export … from`, dynamic `import()` and `require(…)`. A module test runs it on
`packages/domain/src` (R1: the domain is pure). The failing cases run on fixtures in a temporary folder, never by
writing into `packages/domain/src`.

### §S5 CI

`release.yml`'s `test-bun` job runs `bun install --frozen-lockfile` then `bun test`. Its `test-python` job installs
Python 3.14, runs `uv sync --frozen`, then `uv run python -m unittest discover -s tests -t .` (the `-t .` keeps the
tier folders importable as packages). The zizmor audit stays green.

## Acceptance criteria

### §S1
- [ ] `bun install --frozen-lockfile` succeeds at the root and `bun pm ls` lists the five `@parti/*` packages.
- [ ] `bunx tsc -b` exits 0 on the empty packages, using the `typescript` pinned in `bun.lock`.
- [ ] Each package's `src/index.ts` exports a `PACKAGE_NAME` constant equal to its `package.json` name, and a unit test per package asserts it.
- [ ] A unit test in `packages/domain` imports `@parti/schema` and `@parti/schema/test-support` and passes.
### §S2
- [ ] `uv sync --frozen` succeeds; `uv run parti-axi --version` prints the version in `python/parti-axi/pyproject.toml` and exits 0 (tested through `subprocess`).
- [ ] After `uv sync --frozen`, `.venv/bin/python -c "import xmlrunner, coverage"` exits 0.
- [ ] `import parti.workflow, parti.catalogue, parti.testing` succeeds under `uv run python`, and `parti.__version__` equals the version in `python/parti/pyproject.toml`.
- [ ] Building the `parti` wheel (`uv build python/parti`) yields metadata `License-Expression: LGPL-3.0-only` and `Requires-Python: >=3.14`, and the `parti-axi` wheel `GPL-3.0-only` with a dependency on `parti` (read from the built wheels).
### §S3
- [ ] A placeholder test in each tier folder of `packages/domain`, `tests/<tier>/parti_tests` and `tests/<tier>/parti_axi_tests` is reported to Crucible under that tier by `bun-crucible.py <tier>` and `python-crucible.py <tier> --start-dir tests/<tier>` (reviewed, not tested: the Crucible runs' tier counts).
- [ ] A repository test asserts that no folder under `tests/` has the import name of an installed package (`parti`, `parti_axi`).
- [ ] A live-tagged test in each stack is skipped without `PARTI_LIVE` and runs with `PARTI_LIVE=1` (asserted by running the clients both ways on a probe test, then removing the probe; reviewed in VERIFY), and `release.yml` sets no `PARTI_LIVE`.
### §S4
- [ ] `checkDomainImports("packages/domain/src")` returns nothing on the tree.
- [ ] On a temporary-folder fixture, it reports each of: a static import of `node:fs`, `import type` from `@parti/gateway`, `export … from "node:path"`, a dynamic `import("node:fs")` and a `require("fs")`; and it reports nothing for `@parti/schema`, `@parti/schema/test-support` and a relative import inside the folder.
### §S5
- [ ] (reviewed, not tested) A push of the feature branch runs `test-bun`, `test-python` (Python 3.14, inside the synced environment) and the zizmor audit green.

## Estimated size

5 points (re-scored at the gap analysis).

## Risk

- The clients' declaration surfaces (the `test:<tier>` scripts, the per-tier start folder) are read by Crucible; the
  spec pre-review checks them against the clients before RED.

## Follow-up outside this CR

- `AGENTS.md` Setup: the Python test interpreter comes from `uv sync` once this CR merges (Mainline updates it at the
  merge).

## Non-goals

Any domain code, schema content or user-facing feature; C++ or Unreal; publishing to PyPI (a release step); Python
versions before 3.14.

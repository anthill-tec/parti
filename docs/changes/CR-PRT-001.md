# CR-PRT-001 — Workspace and toolchain

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** feature
**Priority:** High
**Depends on:** —
**Labels:** setup, bun, python, ci
**Phase:** 0.1.0 · wave 1
**Design reference:** `docs/Architecture.md` B3 (components), A4 and B2 (R1–R10); `docs/research/DN-test-strategy.md` (tiers, fixtures, CI); `AGENTS.md` (Crucible clients)

## Context

The repository holds only the scaffold: a private root `package.json` with no workspaces, an empty `tests/` package
and two repository guard tests. Every later 0.1.0 CR needs the component layout of Architecture B3, the two stacks
(Bun and Python) wired, and tests discovered by the Crucible clients and by CI in the tiers of the test strategy.

## Scope

### §S1 Bun workspaces

Root `package.json` declares `"workspaces": ["packages/*"]`. Six packages, each with `package.json` (name
`@parti/<name>`, `"private": true`, `"type": "module"`, licence `GPL-3.0-only`), `src/index.ts` and `test/`:
`schema`, `domain`, `gateway`, `adapters-local`, `page`, `mock-scene`. A root `tsconfig.json` (strict) with project
references. The dependency direction of Architecture B3 holds: `domain` depends on `@parti/schema` only.

### §S2 Python packages

A uv workspace at the root (`pyproject.toml` with `[tool.uv.workspace] members = ["python/*"]`) and two packages:
`python/parti`, the library (D27; import name `parti`; licence **LGPL-3.0-only**, with `COPYING.LESSER` beside the GPL
text in the package; empty sub-packages `parti.workflow`, `parti.harness`, `parti.catalogue`, `parti.tools`,
`parti.translators`, `parti.units`), and `python/parti-axi` (import name `parti_axi`, console script `parti-axi`,
GPL-3.0-only, depending on `parti`). Python ≥ 3.12. `parti-axi --version` prints the package version.

### §S3 Test layout and tiers

Bun tests live in `packages/<name>/test/<tier>/*.test.ts`; Python tests in `tests/<package>/<tier>/test_*.py`, with
`<tier>` one of `unit`, `module`, `integration`, `e2e`. Both Crucible clients (`bun-crucible.py test`,
`python-crucible.py test`) discover and report them; the repository guard tests stay where they are.

### §S4 Dependency boundary check

A module test fails when any file under `packages/domain/src` imports anything other than `@parti/schema` or a
relative path inside `packages/domain` (R1: the domain is pure).

### §S5 CI

`release.yml`'s `test-bun` and `test-python` jobs run the new layout: `bun install --frozen-lockfile` then `bun test`;
`uv sync --frozen` then the unittest discovery of `tests/`. The zizmor audit stays green.

## Acceptance criteria

### §S1
- [ ] `bun install --frozen-lockfile` succeeds at the root and `bun pm ls` lists the six `@parti/*` packages.
- [ ] `bunx tsc -b` exits 0 on the empty packages.
- [ ] Each package's `src/index.ts` exports a `PACKAGE_NAME` constant equal to its `package.json` name, and a unit test per package asserts it.
### §S2
- [ ] `uv sync --frozen` succeeds; `uv run parti-axi --version` prints the version in `python/parti-axi/pyproject.toml` and exits 0 (tested through `subprocess`).
- [ ] `import parti.workflow, parti.catalogue` succeeds under `uv run python`, and `parti.__version__` equals the version in `python/parti/pyproject.toml`.
- [ ] Building the `parti` wheel (`uv build python/parti`) yields metadata `License-Expression: LGPL-3.0-only`, and the `parti-axi` wheel `GPL-3.0-only` with a dependency on `parti` (read from the built wheels).
### §S3
- [ ] A placeholder test in each tier folder of `packages/domain`, `tests/parti` and `tests/parti_axi` is reported to Crucible under that tier by the clients (reviewed, not tested: the Crucible run's tier counts).
### §S4
- [ ] The boundary test passes on the tree, and fails (asserted in the same test against a temporary file) when a domain source file imports `node:fs`.
### §S5
- [ ] (reviewed, not tested) A push of the feature branch runs `test-bun`, `test-python` and the zizmor audit green.

## Estimated size

5 points.

## Risk

- The Crucible clients' tier discovery may expect a different folder convention; the gap analysis reads the clients and adjusts §S3 before RED.

## Non-goals

Any domain code, schema content or user-facing feature; C++ or Unreal; publishing to PyPI (a release step).

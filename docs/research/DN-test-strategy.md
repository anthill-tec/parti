# DN — Test strategy

**Date:** 2026-11-23
**Status:** Approved by the owner (23 November 2026). Answers `PRD-parti.md` Q10.
**Author:** Parti orchestrator (vidushi-parti)
**Related:** `PRD-parti.md` (R1–R8 in `../Architecture.md` A4 and B2, NFR-1, NFR-10), `DN-ubiquitous-language.md`

## The rule

Every test runs through the project's Crucible clients and is reported to Crucible (never a test runner invoked
directly). Tests are sorted into Crucible's tiers. **We never mock our own code.** We substitute *fakes* only at a
port, the boundary the architecture already draws (R2), and only in the tiers below integration.

## Tiers

| Tier | What it covers | Real | Faked |
|---|---|---|---|
| **Unit** | The domain's rules: `decide` and `evolve` per context (R1). Translators as plain functions (a maker record in, a product out). | Everything under test | Nothing: the domain is pure, so it needs no fakes |
| **Module** | One package across its own boundary: the gateway's command handling, an adapter against its port, `parti-axi`'s command parsing | The package | At its ports only: an in-memory design store, an in-memory catalogue store |
| **Integration** | The assembled local system: the real gateway, the real JSON event store in a temporary target project, the mock scene over a real WebSocket, `parti-axi` driving it | The gateway, the store, the WebSocket, the processes | No outside application (CAD, Blender, Unreal) |
| **E2E** | `parti-axi init` on a synthetic target project, then the whole release's flow through the page in a real browser and the mock scene | All of Parti | Only the outside applications, which the mock scene stands in for |
| **BDD** | Where useful, the owner's acceptance scenarios as executable specifications | As e2e | As e2e |

## The tools that drive outside applications

Tools whose effect lands inside SolidCraft, Blender or Unreal are tested in two ways:

- **Contract tests (in CI):** the tool generates its batch of commands (or its script calls) from synthetic data
  tables, and the batch is compared with an expected one. This proves our side of the translator (R3) without the
  application.
- **Live tests (on a workstation, outside CI):** a small suite runs against the real application on a machine
  that has it, is tagged as live, and is still reported to Crucible. It proves the application accepts what we send.

## The agent harness (D21, later)

- The workflow graph is tested with a **fake model** that replays recorded answers: the graph's routing, its gates
  (interrupts) and its checkpoints are then deterministic.
- A few **evaluations** run against a live model, measuring task success and cost on fixed tasks, outside CI.

## Fixtures

The repository is public (D20), so fixtures are **synthetic** (NFR-10): generated product records, plain-colour
swatches, small declared buildings (rooms, surfaces, openings) that exercise the rules. Makers' images and the target
project's data are never committed; a test that needs real data reads it in place from a local target project and is
tagged accordingly.

## What CI runs

Unit, module, integration and the contract tests, on every push to `develop` and every pull request (the release
workflow's test jobs). E2E runs in CI once a browser is provisioned there. Live application tests and model
evaluations run on a workstation and report to Crucible.

## Updates (24 November 2026)

- **Layout and runs** (CR-PRT-001, the owner's rulings): Bun tests in `packages/<name>/test/<tier>/`, run per tier by
  the root scripts `test:<tier>`; Python tests **tier first**, `tests/<tier>/{parti_tests,parti_axi_tests}/`, run per tier
  with `python-crucible.py <tier> --start-dir tests/<tier>`; no test folder shares an installed package's import name.
  Python 3.14 only.
- **The e2e tier** is set up by its first CR (CR-PRT-017), not before.
- **Live tests** are tagged in code (`parti.testing.live` in Python, `live(...)` in Bun) and run only with `PARTI_LIVE=1`;
  CI never sets it. They use the real applications (SolidCraft, Blender headless, Unreal) and a target project's files
  read in place (JohnnyHouse, the test bed), never committed.
- **Rust** (from 0.2.0, the SolidCraft plugin, PRD-parti D34): unit and module tests through Crucible's Rust client
  (CR-PRT-073); the plugin against a real SolidCraft is a live test.
- **The router and project pipelines** (D38, D39) are tested with Nai's own `nai check` and `nai test` (scenarios of
  events in and out); reporting them to Crucible is asked of Nai (DN-nai-readiness §5, item 13).
- **The endpoints** (D35): each is contract-tested in CI with CloudEvents in and out against its endpoint definition;
  through a running Nai it is a live test.

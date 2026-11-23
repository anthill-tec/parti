# CR-PRT-018 — Test hygiene for 0.1.0

**Status:** PENDING (spec drafted 2026-11-23; gap analysis not yet run)
**Type:** maintenance
**Priority:** High
**Depends on:** CR-PRT-017
**Labels:** testing, hygiene
**Phase:** 0.1.0 · wave 5
**Design reference:** `docs/research/DN-test-strategy.md`; the `git-workflow` skill §Releases (test hygiene before a release)

## Context

Every release closes with a test-hygiene pass, sequenced last in its final wave, so 0.1.0's suite is lean and
trustworthy before release.

## Scope

- Coverage review of both stacks (Bun and Python clients' coverage), raising each package's domain and adapter code to
  the thresholds below or recording a justified exclusion.
- Remove duplicate and flaky tests (a test that failed and passed on the same commit in Crucible's history), or fix them.
- Retire the placeholder tier tests of CR-PRT-001 now that real tests fill each tier.

## Acceptance criteria

- [ ] (reviewed, not tested) Line coverage at least 90 % for `packages/domain`, 80 % for `gateway`, `adapters-local`, `python/parti-axi` and `python/catalogue-tools`, from the clients' coverage reports, or each exclusion justified in the PR.
- [ ] (reviewed, not tested) Crucible's flaky-test list for the project is empty at the end.
- [ ] (reviewed, not tested) No placeholder test remains.

## Estimated size

2 points.

## Non-goals

New features or behaviour changes.

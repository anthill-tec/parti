---
name: parti-services
description: "Parti's project-specific extension of the `bootstrap` and `shutdown` skills — the service lifecycle of the Mainline (or Solo) orchestrator. At every `/bootstrap mainline` it brings up Parti's own served components and opens Parti's web interface in the user's Chrome through the global `chrome-ui-relay` skill. At every `/shutdown` it closes those tabs and stops EVERY service it started — and only those — from its ledger. It never touches system-level services (Crucible, Sandesh, lean-ctx). Use whenever bootstrapping, shutting down, or after a Pi session restart in ~/Documents/data_projects/parti."
---

# Parti services — bootstrap and shutdown extension

Run **Bring-up** as part of `/bootstrap mainline` (Solo follows Mainline) after the role rules
and the project's `AGENTS.md`/`.env` are loaded and BEFORE the status report to the user — every
run, unconditionally; never wait for the user to ask. Run **Teardown** as part of `/shutdown`
after the active step is closed, and BEFORE the shutdown skill's final watcher stop. A Track runs
neither.

The harness is Pi: a long-running process goes through its `process` tool, never a detached shell
job (`&`, `nohup`, `setsid`). The Sandesh wake watcher is the `bootstrap`/`shutdown` skills' own,
not this skill's.

## Out of scope: system-level services

**This skill manages only Parti's own services** (owner's directive). The system-level services —
the Crucible board, Sandesh, lean-ctx — are not Parti's: it never checks, starts, stops or restarts
them, never opens or closes their pages, and never registers or unregisters on them.

## The ownership rule (owner's directive)

**Every service this skill starts, this skill stops at shutdown. A service it did not start, it
never stops.**

- Before starting anything, check it. A service already up when bootstrap arrives belongs to
  someone else: use it, record it as `preexisting`, and leave it alone at shutdown.
- A service this skill starts is written to the **ledger** at once, in the same turn it is started.
- Shutdown stops exactly the ledger's `started` entries, in reverse order, and verifies each is
  down. It never stops anything the ledger does not name as `started`.

### The ledger

`.run/services.json` at the project root (gitignored; machine-local). It survives a Pi session
restart, which the `process` tool's records and the browser-tab record do not. Shape:

```json
{
  "session": "2026-11-22T12:00:00Z",
  "services": [
    {"name": "parti-gateway", "kind": "process", "state": "started", "processId": "parti-gateway"}
  ],
  "tabs": [{"id": "3", "url": "http://127.0.0.1:<gateway-port>/"}],
  "bridge": "attached"
}
```

`bridge` is `attached`, `not-ready` (bootstrap met `BRIDGE_NOT_READY`), `no-session` (no valid
`PROJECT_TOKEN`) or `none` (no page to open, so no bridge started) — shutdown's browser steps follow
it exactly as `chrome-ui-relay` prescribes.

A ledger already present at bootstrap means the previous run did not shut down cleanly: report it,
run Teardown's service steps for its `started` entries first (a `process` entry from a dead Pi
session is already gone — confirm its port answers nothing), then start a fresh ledger.

## The services

| Service | Kind | Check | Start | Stop (only if `started`) |
| --- | --- | --- | --- | --- |
| Parti's served components (`gateway`, `mock-scene`, …) | `process` tool | none yet: no served component exists | — | — |
| Lavish review session, one per active review artifact | `lavish-axi` session | the artifact is listed in `.run/reviews.json` | `npx -y lavish-axi <file> --no-open` (add `--reopen` only if the owner ended it from the browser and asked for it back); its printed `url:` is the tab to open | `npx -y lavish-axi end <file>` |
| Lavish feedback poll, one per open review session | `process` tool | `pgrep -af 'lavish-axi poll <file>'` shows none | `process start name=lavish-poll-<stem> command="npx -y lavish-axi poll <abs-file>"` | `process kill lavish-poll-<stem>` |

**Lavish review artifacts.** A review surface the orchestrator builds for the owner (for example
`.lavish/architecture.html`) is one of Parti's services while the review is active. The active list is
`.run/reviews.json` (`[{"file": ".lavish/architecture.html", "since": "2026-11-22"}]`): an artifact
is added when the orchestrator opens it and removed when the owner ends it (`Send & End`) or says the
review is done. It persists across shutdowns, so the next bootstrap reopens the same reviews. The
Lavish **server** (`127.0.0.1:4387`) is system-level and shared with other projects: never
`lavish-axi stop`; it stops itself when idle. Exactly one poll per session (never a second listener);
the poll returns on feedback, so after acting on it start the next poll with
`--agent-reply "<message>"`. A poll that returns `browser_disconnected` is not restarted: ask the
owner whether to reopen or end that review.

**Adding a served component.** The CR that introduces a served Parti component (the `gateway` Bun
process serving the page, the `mock-scene`, …) adds its row here in the same change: process name
`parti-<component>`, its start command, its `readyPattern`, its port (bound to `127.0.0.1`,
NFR-8), and its page URL for the Chrome step. Its start is
`process start name=parti-<component> command="…" readyPattern="…"`; its stop is
`process kill parti-<component>` followed by a check that its port answers nothing.

## Bring-up

1. **Ledger.** Read `.run/services.json`; handle a stale one as above. Create a fresh one.
2. **Services, in table order.** For each row: check; if up, record `preexisting`; if down, start
   it, record `started` immediately, then re-check until it answers. A service that will not come
   up is reported to the user with its `process output` lines;
   bootstrap continues and the status report says what is down.
3. **Chrome — Parti's web interface, through `chrome-ui-relay`.** When there is no page to open
   (no served component and no active review), record `bridge: none`, start no bridge, and say so
   in the report.
   Otherwise relay its warning to the user first (Chrome asks to accept the connection; accept
   within about a minute), then its **Open**, with:

   | Input | Value |
   | --- | --- |
   | URLs to open | each served component's page (the `gateway` page first); then each active review's Lavish session `url:` |
   | Our URL patterns | each served component's origin, on `127.0.0.1` and on `localhost`; each review session's exact `http://127.0.0.1:4387/session/<id>` |
   | Protected patterns | none beyond the relay's own rules: it only ever selects, evaluates or closes the tabs it recorded opening |

   Write the returned (id, URL) record and the `bridge` state to the ledger. If the user closes our
   tabs mid-session, run Open again for the missing URLs only.
4. **Report** (folded into the bootstrap status report): each service as `preexisting` /
   `started` / `down`, the tabs with their ids, the bridge state.

## Teardown

1. **Chrome.** Run `chrome-ui-relay` — its warning, then its **Close** and `stop` — from the ledger's
   tab record, following its rules for a restarted bridge, `not-ready` and `no-session`. With
   `bridge: none`, run no browser call at all.
2. **Services — the ledger's `started` entries, in reverse order** (polls before their Lavish
   sessions; `.run/reviews.json` is kept, so the reviews reopen at the next bootstrap). Stop each with its table Stop,
   then verify it is down (its kill line and its port answering nothing). `preexisting` entries are never touched.
3. **Ledger.** Delete `.run/services.json` only when every `started` entry is verified down and the
   tabs are closed (or the relay's rules handed them to the user). Otherwise leave it, naming what
   is still up, so the next bootstrap finishes the job.
4. **Report** (folded into the shutdown report): each service as stopped / left running
   (`preexisting`) / FAILED TO STOP, the tabs closed or left open, with the evidence. A step that
   could not complete is said plainly and handed back to the user, never reported as done.

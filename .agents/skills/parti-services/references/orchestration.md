# Parti — orchestrator reference (services)

Standing rule for `/bootstrap` and `/shutdown` in this project:

- **Bootstrap (Mainline/Solo):** run the `parti-services` skill's **Bring-up**
  (`.agents/skills/parti-services/SKILL.md`) before the status report: bring up Parti's own
  services and open Parti's web interface in Chrome through `chrome-ui-relay`.
  Unconditional, every run.
- **Shutdown (Mainline/Solo):** run its **Teardown** before the final watcher stop: close the tabs
  and stop every service the ledger (`.run/services.json`) records as `started`.
- **Ownership:** every service the orchestrator starts, it stops at shutdown; a service already
  running when it arrived is never stopped.
- **System-level services are out of scope:** Crucible, Sandesh and lean-ctx are never checked,
  started, stopped, opened or registered on by the services extension; it manages Parti's own
  services only.
- **Track:** runs neither.

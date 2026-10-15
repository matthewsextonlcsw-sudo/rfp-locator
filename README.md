# RFP Empire — local foundation

Python application that opens in your browser, with data stored on your computer. This is the first working foundation of the [approved plan](docs/planning/PLAN.md), not a complete nationwide bid service.

## Start

Requirements: Python 3.12 and `uv`. The exact Python version is in `.python-version`; dependencies are pinned in `uv.lock`. From this directory:

```sh
uv sync --locked --group dev
uv run --locked python -m app --demo
```

The browser opens automatically. Demo records are clearly labeled synthetic and use a separate database. To use your own company and client records:

```sh
uv run --locked python -m app
```

After installing dependencies, macOS users can double-click `Launch RFP Empire.command`; Windows users can run `Launch RFP Empire.cmd`. Windows implementation is present but has **not been tested on Windows**. These are developer launchers, not signed installers. No API key is needed for the local foundation.

Reopening the launcher reuses the running process and issues a fresh, one-use browser sign-in link. Closing the browser leaves the service running; use **Settings → Stop local service** or Ctrl+C in the terminal. Launch links expire after 60 seconds; sessions expire after eight hours. Run the launcher again to reopen an expired session.

Optional development controls:

```sh
uv run --locked python -m app --demo --data-dir .local --no-browser
```

`--port 8765` selects a fixed loopback port; otherwise an available port is chosen. `--data-dir` overrides the private data location; `--demo` appends a separate `demo` subdirectory. No remote network interface is enabled.

## Try it

1. In the demo, search `janitorial`; use NAICS `561720`, work location, publisher type, alternatives, exclusions, phrases and deadline filters to narrow records.
2. Open an opportunity. Read its numbered source text and record a review with a line citation. A failed requirement blocks it; a personal “Bid” decision does not remove the blocker.
3. Edit the capability profile. Previous reviews remain stored against their original profile and evidence versions.
4. Create an empty client workspace. Import permitted plain text with a source identifier and, when available, an original publisher link. Reimporting a changed solicitation under the same identifier preserves the old version.
5. Save an opportunity to the watchlist, export a search CSV, or save a verified database backup in Settings.

No automatic qualification, fit score or confidence percentage is shown. Those require the complete source package and the validation work specified in the approved plan. Every imported record starts with unknown package completeness. Company information is self-reported.

## Source access

[Source-access research](docs/SOURCE-ACCESS.md) documents official sources, access requirements, licensing limits and outstanding checks. **Zero live connectors are active.** SAM requires an API key. No mandatory MCP connection has been identified for the researched public sources. HigherGov offers an optional MCP but its standard terms do not establish rights to use its data in this client-facing application.

The Sources screen records these limitations. State/territory placeholders are inventory work, not measured coverage. No live source is contacted at startup. This build never submits bids or purchases access.

## Data and recovery

- macOS: `~/Library/Application Support/RFP Empire/`
- Windows: `%LOCALAPPDATA%\RFP Empire\`
- Demo: the `demo` subdirectory of the selected location.
- `rfp.sqlite3`: all company profiles, supplied source text, revisions, reviews, decisions and search snapshots. SQLite WAL files may exist while running.
- `backup-*.sqlite3`: complete SQLite backups created and integrity-checked by Settings. They contain client data; protect them accordingly.
- `runtime.json`: temporary, private launcher authentication material. Never share this file. It is removed on normal shutdown; a restarted process replaces stale information.

To recover: stop the service, preserve the entire current data directory, and copy a verified backup to `rfp.sqlite3` in a **new, empty** recovery directory. Launch with `--data-dir` pointing there and inspect the recovered records. Do not overwrite a database while the app is running or mix old WAL files with a restored database. A newer schema is rejected rather than automatically downgraded. Automated migration/rollback and restore UI remain planned.

Client workspaces prevent accidental cross-client searches, imports and exports. They are **not separate user accounts or a security boundary against someone with access to your OS account**. The database is not encrypted by this app; use the operating system’s account and disk protections. The service enforces its exact loopback host, browser origin, an HTTP-only session cookie, CSRF checks and a current-workspace binding on saves.

## Tests

```sh
uv sync --locked --group dev
uv run playwright install chromium
uv run pytest -q
```

Tests use temporary data. They cover search semantics, immutable evidence, stale reviews, workspace boundaries, expired deadlines, hostile browser requests, CSV/HTML handling, backups, launcher reuse and a real Chromium workflow. Playwright is a development dependency only; the application uses your installed browser.

[Build status and remaining release gates](docs/BUILD-STATUS.md) separate the working foundation from the full product requirements.

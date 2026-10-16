# RFP Locator — local application preview

RFP Locator (shown as RFP Empire inside the app) opens in your browser and stores data on your computer. This is the first working foundation of the [approved plan](docs/planning/PLAN.md), not a complete nationwide bid service.

## Download and run — no Python setup required

[Download RFP Locator 0.1.1](https://github.com/matthewsextonlcsw-sudo/rfp-locator/releases/download/v0.1.1/rfp-locator-0.1.1.zip) · [Release notes and checksums](https://github.com/matthewsextonlcsw-sudo/rfp-locator/releases/tag/v0.1.1)

1. Download the ZIP and **extract the entire folder** to a writable location, such as Documents. Do not run a file from inside the ZIP.
2. To try synthetic example bids, open **Try Demo.cmd** on Windows or **Try Demo.command** on macOS.
3. To work with your own company and clients, open **Launch RFP Empire.cmd** on Windows or **Launch RFP Empire.command** on macOS.
4. Keep the terminal window open. The app opens in your default browser. Use **Settings → Stop local service** when finished.

Windows uses the x64 uv build. First launch needs an internet connection and may take a few minutes. The launcher installs pinned uv 0.11.6 from Astral into `.bootstrap`, downloads Python 3.12.13 if needed, and installs the locked runtime dependencies into `.venv`. No administrator access, GitHub login, API key, paid subscription or manually installed Python is needed. Windows downloads the official uv ZIP and checks its pinned SHA-256 before extraction; it does not run a downloaded PowerShell installer or change execution policy. Shell profiles and global PATH are not changed. Later launches reuse the installation. Application data stays in the OS user’s data folder, outside the downloaded source folder.

**This is a source-based preview launcher, not a signed installer.** If your operating system or company policy blocks the downloaded script, use an approved development environment or ask your administrator; the app does not disable those protections. Signed/notarized installers remain planned. The app still has zero live bid feeds and does not calculate confidence scores.

Verified: the 19-test browser/API suite and fresh-install check passed on **macOS 14 arm64** and **Windows Server 2025 x64** in [GitHub Actions](https://github.com/matthewsextonlcsw-sudo/rfp-locator/actions/runs/38829517311). Windows 11 desktop acceptance testing and signed installers are still pending.

### If setup does not finish

- Read the message in the terminal. Check your connection and retry; already downloaded packages are reused.
- Keep all files from the ZIP together in a writable folder. Do not move `.venv` between folders or computers.
- If the browser closes, open the same launcher again; it reuses the running service and creates a new local session. Launch links expire after 60 seconds, browser sessions after eight hours.
- For an environment where uv is already approved and installed, open a terminal in the extracted folder and run `uv run --locked --no-dev python -m app --demo` (omit `--demo` for your own data).
- Download updates into a **new folder** after stopping the old service. Your normal data folder stays in place. Back up from Settings before updating. Do not downgrade a database to an older app version.

To uninstall the application, stop it and remove its extracted folder. This leaves company data and backups in the data location listed below. uv’s downloaded Python and shared cache may also remain in your user profile; see the [uv storage documentation](https://docs.astral.sh/uv/reference/storage/) if you want to remove them. Do not delete shared runtimes used by other programs.

### Developer startup

```sh
uv sync --locked --group dev
uv run --locked python -m app --demo
```

`--data-dir PATH` selects a different private data location; `--demo` appends a separate `demo` directory. `--port 8765` sets a fixed loopback port instead of an available one. `--no-browser` supports automated checks. No remote network interface is enabled.

The first-run implementation follows Astral’s official [installation instructions](https://docs.astral.sh/uv/getting-started/installation/) and [custom installation options](https://docs.astral.sh/uv/reference/installer/).

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
uv run python tools/smoke_install.py
```

The fresh-install check downloads its own uv and managed Python into temporary folders, starts the native launcher, verifies sign-in and static assets, reopens the running service, and stops it. GitHub Actions runs the suite on macOS and Windows. Tests use temporary data. They cover search semantics, immutable evidence, stale reviews, workspace boundaries, expired deadlines, hostile browser requests, CSV/HTML handling, backups, launcher reuse and a real Chromium workflow. Playwright is a development dependency only; the application uses your installed browser.

[Build status and remaining release gates](docs/BUILD-STATUS.md) separate the working foundation from the full product requirements.

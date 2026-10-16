# Foundation implementation status

Build: 0.1.1, October 15, 2026. Scope requested for this increment: investigate source access and get the local application foundation working. The approved nationwide product requirements remain unchanged.

## Working foundation

- Python 3.12, FastAPI, server-rendered HTML and a small browser bootstrap script; SQLite FTS5 persistence. No frontend build service or external runtime assets.
- Loopback-only desktop launcher, available-port binding, one-use 60-second bootstrap, eight-hour HTTP-only browser session, authenticated single-instance reopening, exact Host/Origin and CSRF checks.
- Separate demo database, empty real-client workspaces, capability-profile revisions and protection against stale-tab cross-client saves.
- Permission-confirmed plain-text imports, at most 20,000 characters, with source links, immutable SHA-256 evidence versions and transactional FTS publication. Replaying an older version cannot move current evidence backward.
- All-term/phrase, any-term and exclusion search, publisher/location/NAICS/deadline filters, explicit missing-value groups and optional removal of blocked records. No filters silently relaxed.
- Source-line-cited human reviews; cancellation, passed deadline and explicit unmet-requirement blockers. Reviews are valid only for their pinned profile and source versions. Decisions remain separate from qualification.
- Local watchlist, pinned CSV search snapshots with current-status rechecks and spreadsheet-formula escaping, and integrity-checked SQLite backup.
- Source-access/coverage screen, consistent light reading interface, responsive controls and keyboard focus styles.

## Deliberate limits

M0 feasibility and M1 foundation are **partial**, not complete milestone gates. The app reports zero live sources. No automatic extraction, fit scoring, calibrated confidence, complete-package qualification or “Reviewed candidate” promotion is implemented. No external LLM processing is enabled.

The current parser accepts plain text only. PDF/OCR/archive processing must wait for the approved OS isolation proof. Imports carry an operator permission confirmation; connector acquisition grants and machine-enforced provider export policies are not implemented.

Search examines at most 1,001 candidates, returns at most 1,000 and flags possible truncation. It retains at most ten snapshots per workspace for 30 minutes, then asks the operator to clear them or wait. There is no cursor pagination or nationwide-load performance certification. SQLite access is serialized for this local foundation; no persistent background acquisition jobs or scheduling exist.

The company profile is basic and self-reported. Certifications, set-asides, registrations, capacity, geography eligibility and other hard qualification rules remain planned. Reviews are append-only notes; there is no correction/resolution interface or historical-review browser yet. Historical evidence and notes remain in the database. Watchlists do not poll publishers or notify about changes. Form navigation uses the browser’s unsaved-edit warning; crash-resumable drafts and returning to an exact prior search are not implemented.

No signed installer, updater, automatic migrations/rollback, encrypted database, support bundle, source credential storage or Windows execution evidence is provided. Client workspaces are organizational isolation within one OS user’s local app, not independent authenticated client accounts.

## Verification

Run `uv run pytest -q`. Verified on macOS arm64 with Python 3.12.13 and Chromium: **19 tests passed**, including the full local browser workflow, authenticated launcher reuse, rejected incorrect IPC credentials and graceful shutdown. The responsive check passed at 390px; the workflow ran at 1440px. The application was also opened in the Codex in-app browser. Tests use temporary databases; the visible demo uses `.local/demo`.

The test environment emits one upstream Starlette deprecation warning about its current HTTPX test-client integration. It does not affect this passing suite; locked dependency compatibility must be revisited before release. Windows, signed installers, isolated parsers, load benchmarks, calibrated confidence and live-source parity have not been tested. A passing foundation suite is not the approved full product QA/evaluation gate.

## Next required increments

1. Obtain suitable SAM access through a local credential flow; implement and certify listing, description and attachment retrieval with bounded, resumable jobs and contract fixtures.
2. Establish permitted acquisition for representative state, municipal and nonprofit publishers. Expand and audit the nationwide inventory without counting placeholders as coverage.
3. Prove parser isolation on macOS and Windows before enabling binary document processing; add full-package manifests and version-safe extraction.
4. Implement the full capability/eligibility model and evidence-backed fit assessment, then calibrate confidence against labeled data and the approved release gates.
5. Complete snapshot pagination, draft recovery, watch events, recovery/diagnostics, platform testing and signed installers.

These remain requirements, not optional additions. See the [approved task list](planning/IMPLEMENTATION-TASKS.md); none of its cross-cutting tasks is marked wholly complete by this foundation increment.

## Public preview distribution

At the user's request, 0.1.1 adds a downloadable source ZIP with macOS/Windows first-run launchers and separate demo launchers. They fetch pinned uv from the official vendor, install managed Python as needed and sync the locked production dependencies. The app itself remains the local text-only foundation. This is not the M6 signed-installation release or a proof of binary parser isolation.

`tools/smoke_install.py` checks a fresh source copy with spaces in its path, no application virtualenv, a separate managed Python installation and an empty dependency cache. It verifies authenticated demo search, static assets, reopening and graceful shutdown. `.github/workflows/checks.yml` runs that check and the browser/API suite on macOS arm64 and Windows x64. Results are recorded after the checks complete.

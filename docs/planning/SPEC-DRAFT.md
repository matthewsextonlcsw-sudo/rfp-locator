# RFP Empire: nationwide bid discovery and qualification

Status: SPEC APPROVED by the user on October 15, 2026. Autoplan review in progress in PLAN.md.
Research: [source and access findings](RESEARCH.md).
Workflow: user approved this specification and requested `/autoplan`. This file is the approved baseline; review amendments belong in PLAN.md. No application implementation or production data integration is claimed by this document.

## 1. Product outcome

Matthew and his clients can describe work they can perform, tighten a nationwide search, retrieve the solicitation documents, and understand why each opportunity is or is not a practical bidding candidate. The application compares the search and selected company's capabilities with the actual bid requirements, showing an explained match score, evidence completeness, mandatory blockers and, when validated, a calibrated confidence percentage.

User-confirmed requirements: Python; Windows and macOS; browser interface; federal, state, municipal and nonprofit bids throughout the USA; progressively narrower search; full specifications; accurate matching with confidence; useful supporting features selected through research. Nationwide coverage remains the product target throughout delivery. A partial connector release must be labeled partial.

Confirmed deployment decision (user, October 15, 2026): each operator installs the application locally on Windows or macOS and uses its browser interface on the same computer. A consultant can manage multiple client profiles locally; clients install their own copies. Shared hosted access and automatic cross-installation synchronization are outside this delivery. Local workspaces are organizational separation, not protection from another person using the same OS account.

Working scope: procurement contracts and subcontracts, including nonprofit-issued procurements. Grants, nonprofit directories, automatic proposal writing and bid submission are outside this delivery. Early notices and awards are research tabs, never represented as currently bid-able solicitations.

Current pain inferred from the request: fragmented sources and insufficient confidence that a search result is actually actionable. Baseline time spent and business impact are unmeasured; capture task completion time during pilot rather than inventing savings.

## 2. Verified current state

The existing `RFP Empire/tools` directory contains research scripts and generated output, not the requested application. `federal_pull.py:32–41` searches numeric product groups with a page cap; line 73 truncates descriptions. `federal_rank2.py:11–23` filters by historical sample size and sorts a low-competition statistic. Those behaviors are useful for their original research but would omit valid service bids and confuse competition with match confidence if copied into this app.

Create the eventual application under `RFP Empire/bid-discovery-app/`. Keep existing scripts/data intact. Import only reviewed, attributable samples into test fixtures. The parent workspace is not a Git repository; repository creation and issue destination are unresolved, so no GitHub issue has been filed.

## 3. Main user journey

1. Launch installed app; browser opens after local service is healthy. First use shows source setup and an explicit demo/import option if no live sources are connected.
2. Create/select a client capability profile. Enter services/products, codes, geography, capacity, registrations, certifications and constraints. Upload supporting files if desired; unknowns remain unknown.
3. Enter terms or a plain-language description and refine filters. Any interpretation of natural language is shown as editable filters before execution. Exact constraints are never relaxed silently.
4. Browse ranked results with publisher, deadline, source freshness, match score, evidence status and qualification state. Inspect excluded or uncertain results with reasons.
5. Open a bid dossier; retrieve available documents and read the requirement checklist with citations. Missing attachments, conflicts and login requirements remain visible.
6. Compare requirements with the profile; record corrections, evidence and a bid/no-bid decision. Export a source-linked briefing, checklist or spreadsheet.
7. Save the search and watch selected bids. New documents, changed deadlines, cancellations and profile changes invalidate old assessments and trigger reassessment.

## 4. Search requirements

### Search inputs and semantics

- All terms, any terms, exact phrases and excluded terms; match scope selectable across title, description, extracted documents, or all. Default all available text.
- NAICS exact code or explicit descendants, with edition; PSC; source-native commodity codes such as NIGP/UNSPSC when available and permitted. Missing codes remain discoverable through text.
- Publisher type, organization, source, notice type, prime/subcontract, active/open status, posted/updated/due dates and minimum preparation days.
- Place of performance: states, counties, cities, ZIP/radius when geocoded, remote/on-site and service area. Publisher address is not substituted for work location.
- Value range only when source supplies an amount; distinguish estimated value, ceiling, base amount, option-inclusive amount and award amount. “Include unknown value” is explicit and on by default.
- Set-aside/eligibility requirements, licenses, insurance, bonding, site attendance, staffing, clearance, approved-source and contract-vehicle restrictions when stated.
- Minimum match score, evidence completeness, freshness and blocker status. “No known blockers” does not mean “all requirements verified.”

Use OR within a multi-select field and AND across fields. Keep filter chips visible and removable. Excluded terms are hard exclusions in selected text scope. Semantic suggestions expand retrieval only with visible opt-in; they cannot override exact exclusions or mandatory filters. Source-side unsupported filters run locally on retrieved data with retrieval limits disclosed.

Unknown dates, locations and qualifications are a separate result bucket. Provide explicit strict/unknown-inclusive behavior. An ambiguous timezone cannot produce a verified “still open” result near the deadline.

### Search result contract

Show title, publisher, source identifier/link, opportunity type, status, work location, published value or unknown, due time with source timezone and local equivalent, last successful check, fit score, confidence status, evidence coverage, blockers and unread-document count. Support relevance/deadline/newest sorting, saved views, compare up to three bids, and deduplicated results with all source versions available.

The first screen distinguishes no matches, incomplete source scan, offline cached results, missing credentials and provider failure. Pagination and export must use the same filters and assessment versions.

## 5. Client profiles and qualification

Profiles store company name, optional UEI/CAGE and vendor identifiers, capabilities, NAICS/commodity codes, operating areas, remote ability, contract-size preferences, staff/capacity, relevant past performance, certifications/expiration, licenses/jurisdictions, insurance limits, bonding capacity, security clearances, contract vehicles, approved reseller/manufacturer relationships and explicit exclusions.

Every qualification is `verified`, `self_reported`, `unknown`, `expired` or `not_applicable`, with evidence and date. Profile completeness is visible. A user cannot unknowingly treat an expired certificate or unsupported company assertion as verified.

Per requirement, compare as `met`, `not_met`, `unknown`, `not_applicable` or `conflict`; retain whether the requirement itself is mandatory, preferred or unresolved. The overall states are:

- **Potential fit:** no known failure, but checks remain.
- **Needs review:** a mandatory requirement is unknown, a critical document is missing, source freshness is inadequate, or evidence conflicts.
- **Blocked:** a documented mandatory requirement is not met, the opportunity is cancelled, or a confirmed deadline has passed.
- **Reviewed candidate:** a human has reviewed the current complete known document package, resolved mandatory checks and recorded that review. This is a workflow decision, not a guarantee of award or legal eligibility.

Manual overrides preserve the original extraction and reason, author, timestamp and document version. New amendments supersede review status until assessed. Never infer affirmative eligibility merely because restriction words were absent from a summary.

## 6. Full specification and evidence retrieval

Track listing, complete description, known attachments, addenda, questions/answers, drawings, price sheets and forms. Download permitted PDF, HTML, DOCX, XLSX and CSV inputs; extract text with page/section or sheet/cell locations. Scanned PDFs use OCR (text recognition from page images); low-confidence OCR flags affected passages. Unsupported CAD, legacy formats and inaccessible files remain in the manifest as unreviewed.

Each extracted requirement includes source URL, source revision, document hash, page/section/cell, supporting excerpt, extraction method, review status and confidence status. Missing or conflicting values are explicit. A model is prohibited from creating citations or filling missing budget, date, qualification or evaluation-weight fields from general knowledge.

Dossier sections: overview; scope/deliverables; quantities/units; locations and term; milestones; budget type; mandatory qualifications; evaluation criteria; submission instructions; question deadline; site visits; required forms; amendment acknowledgements; client-fit checklist; risks/unknowns; documents; change history; original portal link.

Maintain immutable versions. Changes to the same download URL create a new version by content hash. Known attachment count and retrieval completeness are separated from a claim that the publisher has revealed all documents. Resolve conflicting dates through explicit authoritative addenda or human review; do not use a simplistic “latest fetched page wins” rule.

## 7. Match score, evidence and confidence

### Explained match score

Initial proposed weighting: capability/scope 45, geography/work mode 15, size/capacity 15, experience/preferences 15, classification alignment 10. These are tunable product assumptions, not measured probabilities. Each criterion stores a normalized 0–1 score, its weight and evidence. The score is 100 × the weighted mean over evaluated applicable criteria. Show evaluated weight coverage separately and mark the score provisional when evaluated coverage is below 80%. No evaluated criteria means no score, not zero.

Missing facts never become positive matches. A missing criterion cannot inflate a result into a “strong match” badge: that badge requires score ≥80, evaluated weight coverage ≥80%, no mandatory unknown/conflict/failure, and current required documents. Recompute under a versioned scoring policy. Mandatory requirements and lifecycle status remain separate hard gates regardless of score.

### Evidence completeness

Show concrete counts: known documents retrieved/known documents, requirements evaluated/extracted requirements, profile facts verified, date of source check. If the manifest itself is incomplete, display “package completeness unknown”; do not label it 100% complete. A missing critical document forces “Needs review” even when other documents are present.

### Calibrated match confidence

The requested percentage estimates: “Given this query/profile and the available evidence, a qualified reviewer will judge this result relevant and worth further bid qualification.” It is not win probability and does not supersede qualification blockers.

Build a labeled dataset of real permitted opportunities spanning federal, state, municipal and nonprofit sources and multiple industries. At least 500 labeled query/profile/opportunity examples are an initial experiment floor, not proof of adequacy. Keep solicitation families, near duplicates and revisions in the same split. Separate model fitting, calibration and a time-separated test set. Two reviewers independently label at least 20%; adjudicate disagreements.

Report precision/recall, precision at 10, calibration reliability plots, Brier score, uncertainty intervals, sample counts and per-source/sector failure rates. Proposed gate: precision at 10 ≥90% on adjudicated relevance labels; calibration error ≤0.05 overall; no published confidence bin with fewer than 50 held-out examples; supported source/sector group calibration error ≤0.10. Increase the sample if groups or intervals are too small to justify the claim. These thresholds are release targets, not observed results.

Display confidence only for validated model/version/cohorts, with sample/date and limitations available. Otherwise return null and show “Confidence not yet validated” or “Insufficient evidence.” Stale documents, profile changes, unsupported sectors or drift can suppress a previous percentage. A model's self-reported confidence is not calibration. User feedback queues labeled review; it never directly rewrites the production probability model.

## 8. Nationwide coverage and source operations

Maintain a source registry with publisher hierarchy, geographic coverage, source URL, record types, access method, credentials requirement, usage/redistribution rights, document rights, rate budget, schema version, last successful scan, cursor/watermark, completeness and error state. States, DC and territories are separate coverage entries. Counties, municipalities, school districts, utilities and nonprofits require their own publisher inventory; a state connector does not imply coverage of all of them.

Access priority: documented public API/export; appropriately licensed feed; permitted publisher page retrieval; user-assisted download/import. A portal is activated only after permission/access, pagination, amendments, document retrieval and deletion/cancellation behavior are tested. Unsupported source means unsupported, not a zero-result success.

Initial candidates: SAM, NYC, California, Texas, permitted nonprofit publisher pages, SUBNet and DIBBS discovery. All other states and local sources remain required coverage work tracked in the registry. A licensed nationwide feed may accelerate coverage, but does not replace publisher-level auditing. HigherGov is blocked pending a specific agreement suitable for this competing/client-facing use; standard subscriber access is insufficient based on its current terms. No purchase is authorized by this draft.

Workers use resumable incremental retrieval, overlapping update windows, full reconciliation where needed, stable source identifiers, duplicate detection, and atomic writes so a repeated page does not create repeated records. Record incomplete scans. Respect provider retry windows and quotas; pause repeated failures without affecting other sources. Fetch documents on demand and for watched results to control cost/storage.

Default local refresh proposal: when running, check watched bids every 6 hours and saved searches daily, subject to source limits. Laptop sleep or closed app pauses work; show missed runs and catch up on launch. Do not promise alerts while the local app is stopped. Catch-up queues prioritize deadline changes and cancellations. Explicitly record source-reported update time versus retrieval time.

## 9. Workspace, watchlist and exports

Consultant client switcher; separate profile, notes, saved searches, watchlists, review decisions and exports per workspace. Duplicate public records may be shared internally only if the license permits; private profile data and annotations cannot leak across clients.

Bid pipeline: New → Reviewing → Bid / No bid → Submitted → Awarded / Lost / Withdrawn. Submitted is a user record, not an automated submission. Tasks include document retrieval, qualification gaps, questions, site visits and acknowledgements. Calendar export supports confirmed dates; ambiguous dates are blocked from automatic scheduling.

Exports: CSV/XLSX results, requirement checklist, printable HTML/PDF briefing and document manifest with permitted files. Include original links, timestamps, versions, score/confidence labels and unresolved blockers. Respect source-specific redistribution restrictions, exclude credentials, prevent spreadsheet formula execution, and show workspace/client name before export. Email delivery, CRM integrations and automatic outbound messages are deferred; in-app alerts are included.

## 10. Proposed technical plan

This section is a draft architecture for review, based on the confirmed local-install deployment.

Python FastAPI service, server-rendered HTML with small progressive JavaScript interactions, SQLite full-text search, durable local job table and filesystem document store. Use one local database writer to simplify concurrent work. Search works on an incrementally refreshed local index; external data fetches and document extraction run outside request handling. Native browser opening comes from the launcher. No Electron shell or separate frontend runtime is required for the initial local build.

```text
Desktop launcher -> loopback web service -> browser screens
                            |
              profile / search / dossier / review services
                            |
                  SQLite index + job queue
                            |
            source adapters -> normalized source versions
                            |
               document store -> extraction worker
                            |
                   cited requirements -> assessment
```

Optional semantic extraction uses a configured provider behind a small interface; deterministic search and manual evidence review continue if it is unavailable. Client documents stay local by default. External processing requires explicit in-app opt-in naming provider, data sent and cost limit; no model key is assumed available. Parser-only output never claims full qualification.

Use platform-native user-data directories. Package separately on Windows and macOS; include migrations, offline fixtures and a visible stop/restart control. Check for an existing instance before allocating a new local port. Browser close is not service shutdown. Backup before migrations; rollback restores both database and document references. Signing/notarization and Windows installer verification require their respective platform access.

### Core data records

| Record | Required identity and data |
|---|---|
| Workspace/ProfileRevision | workspace UUID, immutable profile revision, capability facts with status/evidence/expiry |
| Source/SourceRun | source UUID, publisher/access/rights, run start/end/status, watermark, completeness/error |
| Opportunity/SourceVersion | canonical UUID; unique source + external ID + revision hash; raw record reference, lifecycle, timestamps and provenance |
| Classification | opportunity version, system, code, edition, stated/inferred flag |
| DocumentVersion | UUID, source version, URL, SHA-256, media type, retrieval/extraction/access status, parent amendment |
| Requirement/Evidence | UUID, document version, kind, mandatory state, typed value/unit, location, quote, parser/model version |
| Assessment | opportunity/profile/query/policy/model revisions, score, coverage, nullable probability, qualification state, reasons |
| SavedSearch/Watch/Decision | workspace scoped IDs, query revision, user decisions, tasks, timestamps |
| Job/AuditEvent | stable operation key, status/retry/cursor, object IDs, redacted outcome |

Core constraints: enforce foreign keys, unique version keys, enum/check constraints and no silent null-to-false conversion. Amounts use integer minor currency units or exact decimals; codes are strings preserving leading zeros. Dates preserve original text, parsed timezone and certainty. Queries bind parameters rather than concatenate user strings. Evidence cannot point at a deleted document version. Search assessment caching keys include profile, document, query and model/policy revisions.

### Local interface contract

```json
POST /api/search
{
  "workspace_id": "uuid",
  "profile_revision_id": "uuid",
  "query": {"all_terms": ["janitorial"], "any_terms": [], "phrases": [], "exclude_terms": ["residential"]},
  "filters": {"states": ["NY"], "notice_types": ["solicitation"], "include_unknowns": true},
  "sort": "match",
  "cursor": null
}
```

Response includes results, next cursor, source coverage, pending jobs, query revision and last successful checks. Each result includes `match_score`, `evaluated_weight_percent`, `match_confidence_percent` (nullable), `confidence_status`, `qualification_state`, `blockers`, `unknowns` and cited assessment links. `/api/opportunities/{id}`, `/api/jobs/{id}`, `/api/workspaces/{id}/profiles`, `/api/watches`, `/api/exports` and `/api/sources` provide the matching operations. All private operations require the current workspace/session scope; caller-supplied IDs alone never authorize access.

## 11. Security and failure handling

Bind only loopback; validate Host and Origin; require a random local session and protect state-changing requests from cross-site request forgery (another website triggering local actions). Keep API keys in OS credential storage, never browser storage, exported files or logs. Restrict allowed document hosts and validate redirects/DNS resolution to stop downloaded URLs reaching private/internal services. User imports are explicit local file selections, not unrestricted filesystem reads.

Treat documents as data, including any embedded instructions aimed at the AI. Extraction has no shell, account access or arbitrary network tools. Sanitize displayed text, disable active HTML/scripts/macros, cap downloads/archive expansion/OCR time, and parse in restricted worker processes. A malformed file cannot crash the server. Keep provider credentials out of request URLs in diagnostics.

| Failure | User-visible result and recovery |
|---|---|
| Missing/expired key | Source needs connection; actionable setup link; other sources remain searchable. |
| Provider quota/outage | Cached results labeled stale/partial; retry time and resumable run. |
| Missing/login-only attachment | Manifest entry remains; dossier needs review; open original or import file. |
| Conflicting deadline/addendum | Both citations visible; no verified-open eligibility or automatic calendar date. |
| Scan/OCR/parser failure | File remains unreviewed; retry/manual review; reduced evidence coverage. |
| Cancelled/expired notice | Removed from open results; watchlist receives lifecycle change; history retained. |
| Client profile changes | Prior assessment marked outdated; recompute without copying old confidence. |
| Duplicate cross-source notices | Preserve versions/provenance; uncertain merges need review and can be undone. |
| Disk full/interrupted write | Transaction rollback, intact previous data, resumable jobs and clear storage action. |
| App stopped/asleep | Display last run/missed checks; catch up on launch. |
| Unavailable AI provider | Text search/manual review remain; extraction marked partial, no fabricated output. |

## 12. Delivery sequence and measurable gates

| Milestone | Deliverable | Gate |
|---|---|---|
| M0 Access and source inventory | Confirmed local deployment; nationwide publisher registry; provider rights; labeled example plan. | Unverified rows explicitly marked; no nationwide completeness claim. |
| M1 Usable local application | Launcher, profiles, source setup, import, search, dossiers, notes and export. | End-to-end fixture workflow on macOS and Windows; no user-installed Python needed in packaged build. |
| M2 Live source ingestion | SAM and verified direct adapters; amendments, documents, retries, provenance. | Per-source replay/live checks; all incomplete scans and blocked documents surfaced. |
| M3 Qualification and evidence | Full extraction, citations, hard requirements, profile comparison, version invalidation. | Adversarial qualification fixtures and real-document review pass. |
| M4 Confidence validation | Labeled corpus, separated splits, calibration report, cohort suppression. | Section 7 empirical gates; otherwise percentage remains unavailable. |
| M5 Nationwide coverage expansion | All-state/DC/territory inventory and verified local/nonprofit acquisition routes. | Publisher-level audit; no claiming a statewide feed covers every municipality. |
| M6 Client release | Cross-platform packaging, backups, onboarding, update/rollback, support diagnostics. | Tested installers and client workflow; remaining coverage/credential dependencies plainly documented. |

M1 is an internal pilot, not completion of the full request. M5 and M4 remain required work even if a pilot is useful. No fabricated live results: demo fixtures are labeled and segregated from live data.

### Acceptance criteria

1. Exact filters apply consistently to search, pagination, saved searches and exports; unknown values follow the selected policy.
2. A service bid with no historical award statistics remains discoverable. Code-less records remain searchable by text.
3. Every extraction used for qualification links to an existing document version and verifiable location/excerpt; unsupported claims are rejected.
4. A mandatory failure remains blocked at any match score; a mandatory unknown or missing critical attachment remains needs review.
5. Past deadlines, cancellation and non-solicitation notices cannot appear as verified open bids. Date/time uncertainty is visible.
6. Amendment ingestion invalidates stale assessments and emits one watch event per material change, despite retries.
7. Source failure and incomplete pagination never display as a successful exhaustive zero-result search.
8. Same-source repeated fetches do not duplicate records; cross-source merge preserves separate evidence and can be reversed.
9. Match score and historical competition are distinct; unvalidated cohorts never receive a numerical probability.
10. Calibration report satisfies Section 7 before confidence percentages are enabled; report includes exclusions and sample limits.
11. Client workspace switching cannot expose another client's annotations/files through UI, export, cache or direct API IDs.
12. Live integration requires appropriate credentials and usage rights. Missing credentials produce setup, not disguised sample results.
13. Local search p95 ≤2 seconds for the defined benchmark of 100,000 notices plus 1 million text chunks on a specified 16-GB reference machine; record corpus and hardware. Source fetch and OCR run asynchronously with progress/cancel.
14. Each supported OS passes install → launch → profile → search → dossier → export → stop → reopen → backup/restore. Upgrade preserves records and can roll back a failed migration.
15. Keyboard navigation, labeled forms, visible focus, non-color status labels and readable zoom at 200% work on primary screens.
16. Coverage page reports connected/degraded/unsupported publishers and checked dates; claims do not exceed measured coverage.

### Test plan

| Layer | Required coverage |
|---|---|
| Unit | Filter precedence/exclusion, missing fields, code edition/hierarchy, timezone/DST/date-only cases, scoring weights/coverage, hard gates, invalidation, normalization/dedup keys. |
| Adapter contract | Pagination, boundary overlap, repeated pages, deletion/cancellation, expired document links, auth errors, quotas, schema drift and incomplete scans for every enabled source. |
| Integration | Ingest → document manifest → extraction → citation → profile comparison; addendum changes; source conflicts; worker restart; export rights; migration restore; workspace isolation. |
| Browser end-to-end | First run without key, source setup, profile editing, narrow search, unread-document recovery, comparison, decision, watch change, export and offline restart. |
| Security | Cross-site local requests, private-network URL redirects, malicious files/archive paths, document instruction attacks, stored HTML, leaked secrets, spreadsheet formulas and cross-workspace IDs. |
| Evaluation | Human relevance/qualification labels, citation accuracy, false mandatory-pass rate, OCR failures, negation and exceptions, probability calibration and drift. |
| Platform/manual | Windows and macOS packaging, port conflict, sleep/resume, browser default, clean stop, update/rollback, 200% zoom and keyboard workflow. |

Critical blocker fixtures require zero false “met” decisions. Real-document false-pass rate and uncertainty must be reported; passing synthetic tests alone does not establish qualification accuracy. Initial fixture set covers explicit negatives, brand-name-or-equal versus brand-only, optional versus mandatory attendance, expired credentials, missing budget, date-only deadline, conflicting addendum, stale API record and inaccessible attachment.

## 13. Planned file map and effort

Paths below are relative to proposed `RFP Empire/bid-discovery-app/`; these files do not exist yet.

| Area | Files/modules | Human effort estimate | AI-assisted engineering estimate |
|---|---|---|---|
| Shell/storage | `app/launcher.py`, `app/web.py`, `app/db/`, `app/templates/` | 4–6 days | 2–4 focused days |
| Search/profiles | `app/search/`, `app/profiles/`, `app/workspaces/` | 4–7 days | 2–4 days |
| Source ingestion | `app/sources/`, `app/jobs/`, `data/source_registry.json` | 5–10 days for first verified sources | 3–6 days plus external access delays |
| Document/evidence | `app/documents/`, `app/requirements/` | 6–10 days | 3–6 days |
| Matching/evaluation | `app/matching/`, `evals/`, `tests/fixtures/` | 5–10 days plus human labels | 3–6 days plus human labels |
| Watch/export/release | `app/watch/`, `app/exports/`, `packaging/`, `tests/e2e/` | 5–8 days | 3–5 days |

Ranges are planning estimates, not delivery commitments. Nationwide long-tail adapters and commercial access have unknown effort until the inventory and permission checks are complete. Human labeling, credential setup and platform testing cannot be compressed into an unverified “finished in minutes” claim.

## 14. Decisions needed and next workflow

1. Settled: local installations on Windows/macOS, each opening in the browser. The user subsequently approved the complete specification and requested autoplan.
2. Confirm this product boundary and proposed confidence semantics. Nationwide remains a target, with honest partial-source labels until coverage is proven.
3. Paid data, external AI and licensing are optional gated dependencies; no spending or provider account creation has been authorized. Provide supported public/import workflows while those are unresolved.

Next: execute `/spec` quality/file/archive workflow where a repository destination exists, then requested `/autoplan` CEO → Design → applicable DX → Engineering reviews. The specification is approved; the amended implementation plan requires the autoplan final review gate. Build work follows that reviewed implementation plan.

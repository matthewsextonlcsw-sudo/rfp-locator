**APPROVED — user selected A, approve as-is, October 15, 2026.** See the final approval record below; historical pending statements describe the pre-approval review.

<!-- /autoplan restore point: "/Users/matthewsexton/.gstack/projects/rfp-bid-discovery/approved-autoplan-restore-20261015-164855.md" -->
## Implementation plan
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

<!-- autoplan-accepted:ceo -->
- C1: Source setup must distinguish API key, portal account, manual import, licensed feed and optional MCP. HigherGov offers an MCP endpoint at https://www.highergov.com/mcp/ (https://www.highergov.com/gov-mcp/ checked October 15, 2026); its existence does not grant permission for competing services or client redistribution. Keep disabled until explicit applicable written authorization and connector tests. No verified source requires MCP for the base app. Test each setup status and disabled-source search behavior.
- C2: Every source coverage claim must carry a versioned publisher inventory denominator, verified/unsupported/unknown counts and audit date. Never describe an unknown denominator as 100%. A registry completeness audit and independent sample comparison of known live notices must precede each expansion claim; universal 'all bids' cannot be a release assertion unless proven. Full nationwide discovery remains required; unresolved inaccessible/private solicitations are reported gaps, not silently removed scope.
- C3: First-run guided sample uses isolated demo data and persistent Demo label. A five-step guided path gets users from client profile to search to cited requirement to qualification decision to export. Record elapsed time and success/failure locally with opt-in pilot reporting; do not collect telemetry by default.
- C4: Search must explain exclusions, and zero results must offer editable filter relaxation suggestions without executing them. Show amendment differences and an exact reason a candidate became Needs review. Test excluded terms remain hard constraints after all suggestions.
- C5: Confidence stays disabled by default until the held-out evaluation passes. Before enabling a cohort, the evaluation owner records label definition, sampling frame, split family IDs, model/policy hashes, uncertainty method, bin boundaries and exclusions. A coverage or cohort change triggers revalidation before confidence is restored. Human approval cannot override a failed numerical-confidence gate.
- C6: A document is critical when needed to resolve a mandatory qualification, submission condition, price schedule, statement of work or controlling amendment. Criticality unknown or manifest completeness unknown prevents Reviewed candidate and strong-match badges. Store criticality reason, reviewer and document/manifest revision. New files or changed criticality invalidate the review; test missing and unknown critical files as Needs review.
- C7: Calibration uses predeclared equal-width probability bins [0,.1), …, [.9,1]. ECE = sum over bins of n_bin/N times absolute(mean predicted probability minus observed positive fraction). Evaluate unweighted held-out examples under a documented sampling frame; never rebalance test data after seeing outcomes. Activation requires ECE point estimate <=.05 overall and <=.10 in each published cohort, plus the existing precision and >=50 test examples in every published bin. Publish 95% percentile intervals from 2,000 solicitation-family cluster bootstrap replicates with saved seed. Empty/small bins cannot publish percentages; collect more labels instead of changing bins post hoc. Cohorts are source class (federal/state/local/nonprofit) crossed with NAICS two-digit sector, with unknown sector separate; suppress unsupported intersections. Record precision@10 by held-out query/profile group and its interval; threshold applies to its mean point estimate. This defines the initial reproducible protocol; later changes need a new protocol and untouched test data.
- C8: M0 produces a versioned coverage acceptance matrix for every US state, DC and territory and federal/state/local/nonprofit publisher classes. Each identified publisher has discovery route, acquisition rights, document path, freshness budget, test status and owner. M5 completion requires every publisher in the audited inventory to have a working permitted acquisition route meeting its budget and full-spec manifest tests, zero unresolved required-source gaps, and a separate audit of inventory completeness. Unknown inventory completeness prevents 'all bids' completion. Missing/inaccessible sources remain unresolved work; displaying them is not completion. Any proposal to accept a lesser scope must return to the user explicitly; do not silently reduce the approved nationwide objective.
- C9: Section 14.2 is a historical stale confirmation request: the user approved the product boundary and confidence semantics on October 15, 2026. Only actual source permissions, validation results and the autoplan final gate remain unresolved; do not ask to reapprove the specification.
- C10: M0 is a feasibility checkpoint owned by the product lead, with an initial 10 working-day research budget (planning assumption, not spending authorization). Produce the inventory completeness method, scored direct/feed/import alternatives on the same representative notices and full-document/amendment tests, recurring per-install API/storage/OCR/support costs, rights blockers and ownership. If universal completeness cannot be established, return concrete evidence and options to the user; M5 stays open. Do not infer that nationwide geographic reach equals exhaustive publisher coverage.
- C11: Before M4 development, evaluation owner estimates supported source/sector cohorts, held-out bin sample needs, human labeling hours and permitted data cost. M4 is only fully complete for all supported product cohorts; unknown/unvalidated cohorts remain explicit incomplete work. Pilot 12 real qualification tasks (at least three per publisher class) with two operators using current tools and app on matched tasks; predeclare target median decision-time reduction >=25%, no additional missed viable bids against adjudication, and zero material mandatory false-pass in the pilot. Record all manual work and confidence's incremental benefit. Small pilot is a usability signal, not population accuracy proof. Failed targets reopen design, not waive scope.
- C12: Before M6 assign a maintainer for every adapter, evaluation release and platform package. Support current and prior app release for 90 days; publish compatibility/rights status and signed updates. Clients approve installation and optional redacted diagnostic export. Test at least two clean installs with differing credentials and update states. Budget estimates include source-change response and local storage; disable incompatible connectors visibly without losing cached evidence.
- C13: Planned document acquisition stages temp files then atomically renames by hash and commits database references through the single writer. After crash, reconcile orphan temp/blob files without deleting referenced evidence. Assessment publish uses compare-and-swap on profile/query/opportunity/manifest/policy/model revision tuple; a changed tuple yields outdated state and requeue. Profile save, amendment ingestion, export and assessment jobs must test both completion orders with controlled barriers.
- C14: Use typed errors for network timeout/auth/rate-limit/schema, parser/unsupported/limit, citation validation, provider refusal/empty/malformed response, disk-full/DB-busy and migration failure. All routes return stable error codes, redacted operation IDs and recovery text. Never convert failures to successful empty results or mandatory met. Enforce workspace scope in service and repository calls; validate query lengths, enum values, media types and IDs. No evaluation/model tools or document-originated instruction can invoke shell/network or grant access.
- C15: Bound initial work: page size100, query length4,000 chars, 50 terms, document download100MB, extracted archive500MB with 1,000 members, OCR500 pages/10 minutes, two fetch jobs and one parser job per install; all configurable policy caps with explicit incomplete status, not truncation hidden as success. Profile/source IDs and status/date filters need indexes; batch assessment joins. Store job payloads as IDs, not blobs. Cache keyed by complete revision tuple. Test caps at boundary and excess, cancellation and retry after process termination.
- C16: Redacted local diagnostics record operation/source/run/job/version IDs, elapsed time, stage, retry count and error code, never API keys or document bodies. Source-health UI shows last success, coverage completeness, queue age and next retry; users can pause/retry a source and export diagnostics by consent. Migration sequence stops worker/writer, verifies a DB+document-manifest backup, migrates, checks integrity and launches. Failure restores backup and previous package; no simultaneous old/new writers. Smoke tests inspect first5minutes and firsthour, including source freshness, search, evidence retrieval, workspace isolation and watch invalidation. Confidence and each connector activate independently only after their gates.
- C17: Duplicate mutations reuse operation IDs; stale forms reject with conflict and preserve drafts; navigation must not silently lose unsaved input. Exports pin a labeled immutable assessment snapshot and never mix revisions. Test both profile-save/export completion orders and duplicate clicks/retries. Dependency lockfiles, package audit and signed-release verification are required before client release. Time rollback on fixture corpus against a 15-minute recovery target; report actual timing and failures. UI recovery paths include auth reconnect, quota retry, parser manual review, disk remediation and schema-update advice. Local health surfaces these states; no stopped-app alert promise.
<!-- /autoplan-accepted:ceo -->

<!-- autoplan-accepted:design -->
- D2.1: Search uses a readable row layout, not metric cards. Row primary: title, publisher, qualification label, next actionable deadline. Secondary: place of performance, short scope, top blocker/unknown. Tertiary: Fit n/100, evaluated coverage, document counts and source freshness. Expand details for all remaining section4 contract fields. Relevance confidence is subordinate, with accessible definition/sample/version disclosure. No percent gauge. Examples must cover high-fit blocked, unknown deadline, provisional score and null confidence; comparison and export preserve this precedence.
- D2.2: Dossier review lists mandatory unresolved requirements first, mandatory resolved second, preferred third. Selection shows cited excerpt/location beside corresponding profile fact and evidence. Separate actions record met/not_met/unknown/conflict/not_applicable, correct extraction, attach evidence, resolve conflict and classify document criticality; changes require reason and retain history. A checklist names every remaining Reviewed candidate gate. Desktop two-column requirement/evidence workspace becomes sequential panels at narrow widths/200% zoom, preserving selection and return position. Manual assessment cannot override lifecycle, missing manifest or mandatory blockers.
- D2.3: Always distinguish Publisher status, Current qualification and Your decision. Preserve Submitted/Bid history through amendments/cancellation; show current assessment Outdated/Needs review/Blocked and changed citations. Business decisions never promote qualification. Decision changes require reason; Submitted requires user-entered submission date/reference, not a remote submission. Test Submitted -> amendment -> Needs review with historical Submitted intact; cancellation forces current Blocked.
- D2.4: First use offers Connect a source, Import a solicitation, Try guided sample as three direct actions. Draft real profile needs company name, capability description and work area only; optional facts stay unknown and are requested in context. Guided milestones: profile, search, source evidence, review decision, export; progress resumes. Exit demo selects/creates real workspace and never copies sample evidence or decisions. First useful cited requirement precedes exhaustive credential intake.
- D2.5: Primary search has query plus location, deadline and notice type. Advanced groups are classifications, qualifications, value, evidence and sources. Natural language opens editable filter preview before Search. One query-level Include unknowns toggle governs all applicable missing-field filters; default on, persists per saved query and matches API include_unknowns. Known matches and uncertain matches have separate labeled counts/views with reasons; excluded records are a separate inspection view and never silently join active results. Each proposed relaxation names old/new filter and requires Apply; exclusions remain hard until explicitly edited.
- D2.6: Search initial loading shows stage and Cancel; no sources shows the three setup choices; success shows count and coverage; cached+refreshing keeps rows/selection fixed with last-check label and Update results action; partial/error shows per-source failures and retry; cancellation preserves completed evidence and marks incomplete. Dossier loading shows manifest/extraction stage; empty package shows original link/import; partial shows missing critical files and Needs review; error retains last readable version; success shows citations and remaining checks. Export loading shows processed count when known; empty scope shows revise filters; partial shows omitted items/reasons and explicit partial-export choice; error retains retryable job; success shows filename, download/destination and pinned snapshot time. Never reorder a viewed list on background completion. Old scores remain labeled Outdated with assessment time, separated from current pending state. Unknown progress totals show stage rather than a fake percent.
- D2.7: Use distinct terms Closing browser, Stopping service and Computer asleep. Browser close leaves service running; Stop service or sleep pauses checks. Launcher has starting/running/stopped/error states, Open browser, Start and Stop service controls; stop explains paused monitoring. Browser persistent service indicator shows last/next check; disconnected screen instructs Launch RFP Empire to restart. Test close-browser/reopen and stop-service/relaunch separately.
- D2.8: Persistent navigation: Search, Watchlist, Profile, Sources/Coverage, Settings; Watchlist contains pipeline, tasks and changes. Client/workspace name remains visible beside decisions and exports. Dossier Back restores query/filter/page/scroll. Workspace switch with unsaved edits asks Save draft, Discard or Stay; never silent discard. A running export stays bound to its original workspace and labels the originating client even after switch; its download cannot appear in the new client's list.
- D2.9: Keyboard-only path must cover query -> filter disclosure -> result -> citation -> recorded review -> export; real table headers, visible labels, skip link, nav/main landmarks, accessible status names and non-hover critical content. Dialogs/citation views restore focus; submit errors focus error summary and preserve fields. Live regions announce major completion/error once, not every OCR page. Target44px controls, body>=16px, body contrast>=4.5:1 and UI/focus>=3:1; visible 2px focus ring. At>=1200px use list+dossier split,768–1199px list or full dossier with Back,below768px use labeled result rows and one evidence pane; comparison becomes one bid at a time with a selector preserving compared fields. Test1280x800 at200% plus keyboard/screen reader and long titles without hidden status.
- D2.10: Provisional visual taste T1 for final gate: office-light reading surface, IBM Plex Sans bundled locally with license, 16px/1.5 body, 24px page headings, tabular deadline numerals. CSS tokens: canvas #F4F6F8, surface #FFFFFF, text #17283B, secondary #465668, accent #006B67; verified contrast required before release. 4/8/12/16/24/32 spacing,4px control radius, no decorative shadows/gradients/card mosaics. Theme focus, selection, caret, link/visited distinction and scrollbar with forced-color fallback. Motion limited to a120ms visible-default evidence-pane emphasis on selection; reduced-motion disables it. No motion-dependent content or polling animation.
<!-- /autoplan-accepted:design -->

<!-- autoplan-accepted:dx -->
- X1: Developer quickstart documents macOS shell and Windows PowerShell from the downloaded source bundle, with pinned tested Python3.12 patch and uv version in toolchain metadata, pyproject.toml and committed uv.lock. From app root: `uv sync --locked --group dev`, then `uv run --locked python -m app --demo`. Demo command initializes isolated demo storage, seeds the fixture adapter through the real ingestion/extraction pipeline and opens the browser after health readiness. Expected UI: Demo workspace, sample opportunity, a verifiable requirement citation and Confidence not validated. Commands are planned contracts until implemented/tested. Target<=5minutes from source+declared toolchain to understood citation including dependency download; report clean-machine toolchain setup separately. Packaged clients need neither Python nor uv. No hosted playground/public SDK added.
- X2: Local API is internal, authenticated, same-version browser/server only. Use typed request/response schemas and protected OpenAPI docs. Canonical sorts match,deadline,newest; UI relevance maps to match, Fit is the explained score. Search defaults match,page size50(max100),include_unknowns=true; cursor binds workspace/profile/query/index-generation/sort snapshot and expires after30minutes, returning409 CURSOR_EXPIRED with rerun action rather than silently mixing pages. POST workspace/profile/search/export/watch operations, GET dossier/job/source status, POST job cancel/retry are documented with concrete schemas; no route inferred from names alone. Accepted background mutation returns202/job_id; completed search returns200 with completeness/errors/pending_jobs; failure returns appropriate4xx/5xx, never disguised empty. Idempotency-Key header scopes mutations to workspace+operation, body hash mismatch409; retain24h. Revision conflicts409 with current IDs. Supply local authenticated TestClient workflow workspace->profile->search->evidence->export without production credentials.
- X3: Adapter protocol has describe_capabilities()->SourceCapabilities, fetch_page(window,cursor,cancel_token)->SourcePage, and fetch_manifest(source_version)->Manifest. SourcePage includes source/external IDs, raw provenance, normalized records, next_cursor, window bounds, provider watermark, completeness and typed errors; only the job coordinator commits cursor after durable page writes. Manifest includes discovered file IDs/URLs/rights/criticality and completeness_known. Adapters declare incremental/full reconciliation, cancellation/deletion and auth/rate-limit support; unsupported capabilities remain explicit. A credential-free fixture adapter exercises duplicate/interrupted pages, amendments and inaccessible attachments. `uv run --locked pytest tests/contracts -k fixture_adapter` is the planned reusable suite entry point; guide plus passing fixture precedes added live adapters.
- X4: Shared error envelope contains code, problem, known cause or 'cause unknown', recovery action, bundled help anchor, operation_id and optional retry_at/field. Map to launcher, API, job and browser. Include auth, quota, parser, schema, disk/busy, migration, session-expiry, stale-cursor and invalid-config catalog entries. Example SOURCE_AUTH: 'This source could not connect; the provider rejected its credential; reconnect in Sources; help/sources#authentication'. DOC_PARSE: 'This file could not be read; cause unknown; open original or import a readable copy; help/documents#unreadable'. STORAGE_FULL: 'Changes could not be saved; the data volume is full; free space then Retry; help/recovery#storage'. Examples are required future outputs, not observed runtime. Contract tests verify fields and redact credentials/doc bodies.
- X5: Documentation ships with the app version: README quickstart, bundled operator guide, developer run/test/architecture guide, adapter guide, configuration reference, generated internal API/error reference, changelog and update/restore runbook. Include executable complete examples with expected200/202/409 and null-confidence/partial-source responses. Links from setup and errors work offline. Verify getting-started commands on both OS and help lookup<=2minutes for setup/auth/restore using task-based trials. Maintainer support instructions and a local diagnostic/issue template name the configured support destination; do not invent a live community or publish private data.
- X6: Typed effective-settings view shows defaults, values, units, scope, restart needs and validation errors with secrets redacted. Precedence: packaged defaults < installation settings < workspace search/profile settings; explicit dev CLI overrides only the declared port/data-dir/demo flags and appear in effective settings. Refresh6h/watch and24h/search allowed15min–7days subject to provider minimum; worker count1–2 fetch and1 parser; resource limits may be lowered, increases require maintained policy revision and benchmark. AI provider opt-in per workspace; scoring policy weights are maintainer versioned, not ad hoc user sliders. Port0(auto) or1024–65535 loopback only; changing port/data directory requires stopped service and validated restart/migration. Search defaults hot-apply only to new query revisions. Licensing, isolation, loopback, blockers and confidence validation cannot be disabled by settings.
- X7: App releases use semantic versions, schema versions and connector compatibility metadata. Breaking changes include migration guide, preflight incompatibility warning and tested backup/restore; downgrades reject newer DB schemas unless restoring matching backup. Maintain current/prior90-day support from C12. Local dev supports hot reload in dev mode only; fake clocks, isolated temp directories and fixture transports enable offline CI on Windows/macOS with pinned toolchain. No TypeScript SDK/Linux-client promise added. Post-build DX check uses clean caches and human-readable instructions, records dependency/toolchain time, errors and successful cited result, with opt-in local notes and no automatic telemetry or recurring external task.
<!-- /autoplan-accepted:dx -->

<!-- autoplan-accepted:eng -->
- E1: Assessments include evaluated_at and valid_until, the earliest applicable deadline, credential expiry and source freshness boundary. Recheck temporal gates at search/dossier read, assessment publication and export completion even without revision changes. Expired deadlines force Blocked; expired credentials/freshness force Needs review and suppress current probability/badges. Historical exports retain as-of labels plus current-at-export warning. Use UTC instants, preserve source timezone/uncertainty, monotonic elapsed time within a run; detect wall-clock rollback or unexplained large jump, invalidate temporal assurances and request clock correction/recheck. Never reactivate expired confidence solely because the clock moved backward. Fake-clock tests cross each boundary, sleep/resume and export completion.
- E2: Define immutable AssessmentInputRevision combining the C13 tuple with requirement-set, extraction, human correction/evidence-review and acquisition-grant revisions. Every correction, attachment, conflict resolution or rights change creates a new aggregate input revision. Publish/cache/review/export bind to that aggregate, temporal validity and workspace. CAS rejects stale attempts and retains the historical record; both completion orders of correction/assessment, attachment/assessment and conflict/export are mandatory integration cases.
- E3: Before untrusted document extraction ships, prove OS-enforced parser isolation in packaged Windows and macOS builds. Candidate mechanisms: Windows AppContainer with no network capabilities plus process/job restrictions; macOS signed sandboxed XPC helper with no network or broad file entitlements. Native glue is confined to the helper boundary; core application remains Python. Only staged input, private scratch and bounded output are exposed; no DB, credentials, other workspace files or arbitrary process launch. Broker validates output. Initial per-parser policy: 1GiB memory,120s CPU,10min wall time,20MiB extracted text, in addition to C15 download/archive/page caps; supervisor terminates on any exceeded limit, records partial/error and preserves original. Verify actual enforcement and dependency compatibility during M0/M1 platform spike; no claim that subprocess alone is a sandbox. If a supported OS cannot enforce the contract, automatic parsing is disabled visibly there and M3/M6 remain incomplete until repaired; manual review is an interim path, not completion. Tests attempt network, sibling-file reads, child execution, memory growth and non-OCR hangs. Signed platform isolation is a release prerequisite, not a waived risk.
- E4: Durable jobs use queued -> running -> succeeded, retry_wait, failed_terminal or cancelled. Atomic claim assigns attempt_id and fencing token through the single writer; heartbeat15s, lease60s while awake, coordinator fences pre-suspend attempts on resume/restart. Only current attempt may commit a result or renew. Cancellation is persisted and checked before network/parser starts, between chunks and before commit; already committed results remain historical. Retry transient failures at most5attempts with full jitter exponential delay base2s cap15min, respecting larger provider retry_at; auth/schema/permanent failures pause with action. Exhausted jobs are visible failed_terminal and manual Retry makes a new linked attempt. Commit source page, cursor, material change and unique watch-event/outbox key in one transaction; outbox delivery is idempotent by workspace/watch/material-revision/type. Kill/replay every boundary and resume a fenced worker; never claim external exactly-once delivery.
- E5: Search materializes ordered result IDs and assessment-input revisions in bounded SearchSnapshot rows; deterministic final tie-breaker opportunity UUID. Build under a short consistent read, finish within2s target or cancel at5s with explicit QUERY_LIMIT and refinement action, never hold a read transaction across browser pages. Snapshot TTL30minutes, at most100,000 result rows/snapshot,10active snapshots/workspace and1million snapshot rows/install; beyond caps return explicit partial/limit with counts and refinement, never exhaustive success. Completed snapshots supply pages and exports; no long-lived SQLite read transaction. Rights and temporal gates are rechecked on every access; changed current facts are overlaid as outdated/blocked without silent reordering. Expired snapshots return409; exports pin their snapshot until job completion within bounded retention and retain client/as-of labels. Expiration cleanup respects active export references; admission rejects new snapshots when storage cap is reached. Benchmark baseline100knotices/1mchunks with two fetch jobs, parser and10snapshots, plus10x stress reporting latency/RSS/disk/WAL/queue growth. The10x run diagnoses scale; it does not invent a2s guarantee at that scale.
- E6: Launcher creates/validates the service through an OS-user-restricted local IPC identity handshake, not a response on a remembered TCP port. Bind random available127.0.0.1 port and validate exact Host/origin. A256-bit one-use bootstrap token expires60s and is delivered in URL fragment, consumed by same-origin POST, removed immediately with history.replaceState before other navigation; no third-party assets, no referrer, no token logging/caching. Exchange establishes host-only HttpOnly SameSite=Strict session cookie with8h absolute lifetime; rotate bootstrap/session signing secrets on service restart. Session cannot be reused across restart, bootstrap replay fails. Use plain loopback HTTP only after testing browser cookie behavior; do not falsely promise Secure-cookie protection over HTTP. CSRF tokens and exact Origin/Host enforce mutations; minimal unauthenticated readiness returns no private data. CSP/default self, frame-ancestors none and Referrer-Policy no-referrer. Packaged tests cover wrong process/port, replay/expiry/restart, missing/forged origins, hostile external page and URL/log leakage. Same-OS-account malware is outside this session boundary, consistent with baseline.
- E7: Separate Blob(hash,bytes) from AcquisitionGrant(workspace,source/acquisition route,license/document rights,private/public,revision,revocation) and DocumentVersion provenance. Identical hashes do not grant access. Every citation, file route, export, cache and optional provider-processing job resolves a current authorized grant plus pinned provenance; no direct hash-only retrieval. Revocation prevents new viewing/export/external processing even for a historical assessment; retain a tombstone/audit reason where permitted. Previously downloaded external copies cannot be recalled and this is stated. Do not reveal existence across workspaces; dedup storage sharing is allowed only under applicable rights. Test identical bytes acquired with different rights, revocation during export/provider job and old cached links.
- E8: Use SQLite WAL on local disk only, foreign keys enabled, bounded5s busy timeout and single writer ownership. Maintain FTS5 and normalized content in the same transaction; migration/backfill explicitly rebuilds and validates the index. Search quote/escape rules generate FTS expressions from validated term structure, not raw user query operators; parameter binding alone does not validate FTS grammar. Test literal punctuation, negation, Unicode, empty/all-stopword queries, SQL/FTS operators, index rebuild consistency and disk-full rollback. Backup uses quiescence plus SQLite backup API/integrity validation, never copies live DB alone without WAL. Document blob collection deletes only unreferenced, unpinned blobs after reconciliation and a7day grace period, with rights retention constraints and dry-run manifest; referenced evidence is never garbage-collected.
- E9: Build on each supported OS: initial target Windows11 x64 and macOS14+ arm64/x86_64, verify dependency/support compatibility during M0 and record exact tested OS/browser versions at release. Broader Windows/macOS requests remain coverage work if target customers need other architectures; never imply untested compatibility. Package Python dependencies and OCR assets separately per target, signed/notarized installer/app with SBOM and checksums; private artifact download channel configured before client release, no website publication/purchase authorized by this plan. CI runs locked unit/contract/integration/eval fixtures and browser tests on both OS; protected release jobs use signing secrets from platform stores, never repo. Run clean-machine install/update/restore/isolation tests before release. Select final bundler only after E3 spike; PyInstaller is a candidate, not proof of sandbox compatibility. Automatic parsing/release blocked if isolation proof fails. All benchmark/calibration/platform results are future measurements.
- E10: Implement the complete codepath and user-flow test matrix in the engineering QA artifact. Use pytest for pure/contracts/integration, Playwright Python for browser flows, packaged OS tests for native isolation/install/lifecycle, and versioned offline evals for extraction/citations/qualification/relevance/calibration. Existing app coverage is zero because app does not exist. Test through real service/repository/worker boundaries with fixture transports, fake clocks and controlled barriers; do not add production-only test endpoints. New live adapters require rights-qualified fixture replay and bounded live parity checks. No tests of untouched research scripts are required; existing behavior there remains unchanged. M0 precedes source commitments; foundation/schema contracts precede parallel adapters/UI/evaluation; integrate all before M3/M6 gates.
<!-- /autoplan-accepted:eng -->
## Review record

### Autoplan execution provenance
User approved baseline October 15, 2026 and requested autoplan. Restore bytes are immutable. Primary/native host Codex; external provider Claude Code unavailable because project is not a Git repository. No external agreement is implied. CEO methodology read ranges 1–600, 601–1200, 1201–1800, 1801–2400, 2401–2457 (truncated spans reread). No applicable design doc. DX scope helper returned 34 matches, so DX required. No unrelated VibeCheck learnings imported. Aside unavailable; authoritative web research used. No brain trust gate established, so no brain writeback.

### CEO Step 0 analysis
Problem: scattered bid discovery and expensive qualification. Buyers are local-install consultants and their clients, not procurement publishers. The scarce resource is a defensible bid/no-bid decision, not the count of search hits. Pilot measures manual baseline and assisted time; claimed savings remain unmeasured.

Reuse map: federal_pull.py and federal_rank2.py provide attributable fixture candidates and historical research ideas, not production ingestion/scoring. Research manifests' dated sources and explicit unknowns are good patterns; avoid hard-coded dates/page caps and description truncation. Git log/diff/stash unavailable (nonrepo); no revision history assertions. No existing app migrations or tests to reuse.

Landscape: tried-and-true SAM filters/saved searches plus direct portal documents; current HigherGov aggregates state/local procurement and offers API/MCP, but coverage numbers are vendor claims and terms block competing/client reuse absent agreement. First principles: licensed/public retrieval + local evidence provenance + hard qualification gates is the differentiated product. Buying a feed is an optional speedup, not authorization or a substitute for document verification. Sources: https://alpha.sam.gov/find-contract-opportunities ; https://docs.highergov.com/find-opportunities/state-and-local-contracts ; https://www.highergov.com/gov-mcp/ ; https://www.highergov.com/tos/ .

Current -> this delivery -> 12-month ideal:
research scripts -> local traceable qualification across audited sources -> sustained nationwide publisher coverage and validated industry cohorts.
The 10x ambition is fewer wasted bid hours through evidence-based qualification. Do not promise 10x measured performance. Platform potential is additional permitted adapters and models behind narrow contracts, not a hosted platform or plugin marketplace in this delivery.

At least five delight candidates: guided first dossier (accept C3); explain why excluded (accept C4); amendment changes (accept C4); comparison of three bids (already approved, reject duplicate); confidence provenance drawer (already approved, reject duplicate); automatic CRM sync (defer D1, outside local workflow). All accepted additions use existing screens/services, estimated <1 focused AI day each and no new infrastructure. Borderline look/feel remains for design review. No User Challenge to local installs. Universal completeness is a verification risk, not permission to change the nationwide objective.

### CEO decision ledger
| ID | Decision | Alternatives | Choice | Authority | Reason / verification |
|---|---|---|---|---|---|
| U1 | Product/deployment | local / hosted | local, nationwide | explicit user approval | Preserve approved scope |
| C1 | Integration disclosure | API only / typed setup | typed setup | autoplan P1/P5 | Correct MCP evidence and licensing visibility; setup tests |
| C2 | Coverage denominator | geography badge / inventory audit | inventory audit | autoplan P1 | Prevent unsupported exhaustive claims; sample check |
| C3 | First-run help | empty screen / guided fixture | guided fixture | autoplan P2 | Small addition to existing flow; timed pilot |
| C4 | Tightening search | silent expansion / explanations | explanations | autoplan P1/P2 | No broken hard filters; regression |
| C5 | Calibration activation | informal approval / versioned gate | versioned gate | autoplan P1 | Prevent invalid percentages; held-out audit |
| D1 | Automatic CRM sync | add / defer | defer | autoplan P3 | New external integration beyond local scope |
| S1 | Three-way compare | add / duplicate | skip duplicate | autoplan P4 | Already section 4 |
| S2 | Confidence evidence | add / duplicate | skip duplicate | autoplan P4 | Already section 7 |

<!-- autoplan-accepted:ceo -->
- C1: Source setup must distinguish API key, portal account, manual import, licensed feed and optional MCP. HigherGov offers an MCP endpoint at https://www.highergov.com/mcp/ (https://www.highergov.com/gov-mcp/ checked October 15, 2026); its existence does not grant permission for competing services or client redistribution. Keep disabled until explicit applicable written authorization and connector tests. No verified source requires MCP for the base app. Test each setup status and disabled-source search behavior.
- C2: Every source coverage claim must carry a versioned publisher inventory denominator, verified/unsupported/unknown counts and audit date. Never describe an unknown denominator as 100%. A registry completeness audit and independent sample comparison of known live notices must precede each expansion claim; universal 'all bids' cannot be a release assertion unless proven. Full nationwide discovery remains required; unresolved inaccessible/private solicitations are reported gaps, not silently removed scope.
- C3: First-run guided sample uses isolated demo data and persistent Demo label. A five-step guided path gets users from client profile to search to cited requirement to qualification decision to export. Record elapsed time and success/failure locally with opt-in pilot reporting; do not collect telemetry by default.
- C4: Search must explain exclusions, and zero results must offer editable filter relaxation suggestions without executing them. Show amendment differences and an exact reason a candidate became Needs review. Test excluded terms remain hard constraints after all suggestions.
- C5: Confidence stays disabled by default until the held-out evaluation passes. Before enabling a cohort, the evaluation owner records label definition, sampling frame, split family IDs, model/policy hashes, uncertainty method, bin boundaries and exclusions. A coverage or cohort change triggers revalidation before confidence is restored. Human approval cannot override a failed numerical-confidence gate.
- C6: A document is critical when needed to resolve a mandatory qualification, submission condition, price schedule, statement of work or controlling amendment. Criticality unknown or manifest completeness unknown prevents Reviewed candidate and strong-match badges. Store criticality reason, reviewer and document/manifest revision. New files or changed criticality invalidate the review; test missing and unknown critical files as Needs review.
- C7: Calibration uses predeclared equal-width probability bins [0,.1), …, [.9,1]. ECE = sum over bins of n_bin/N times absolute(mean predicted probability minus observed positive fraction). Evaluate unweighted held-out examples under a documented sampling frame; never rebalance test data after seeing outcomes. Activation requires ECE point estimate <=.05 overall and <=.10 in each published cohort, plus the existing precision and >=50 test examples in every published bin. Publish 95% percentile intervals from 2,000 solicitation-family cluster bootstrap replicates with saved seed. Empty/small bins cannot publish percentages; collect more labels instead of changing bins post hoc. Cohorts are source class (federal/state/local/nonprofit) crossed with NAICS two-digit sector, with unknown sector separate; suppress unsupported intersections. Record precision@10 by held-out query/profile group and its interval; threshold applies to its mean point estimate. This defines the initial reproducible protocol; later changes need a new protocol and untouched test data.
- C8: M0 produces a versioned coverage acceptance matrix for every US state, DC and territory and federal/state/local/nonprofit publisher classes. Each identified publisher has discovery route, acquisition rights, document path, freshness budget, test status and owner. M5 completion requires every publisher in the audited inventory to have a working permitted acquisition route meeting its budget and full-spec manifest tests, zero unresolved required-source gaps, and a separate audit of inventory completeness. Unknown inventory completeness prevents 'all bids' completion. Missing/inaccessible sources remain unresolved work; displaying them is not completion. Any proposal to accept a lesser scope must return to the user explicitly; do not silently reduce the approved nationwide objective.
- C9: Section 14.2 is a historical stale confirmation request: the user approved the product boundary and confidence semantics on October 15, 2026. Only actual source permissions, validation results and the autoplan final gate remain unresolved; do not ask to reapprove the specification.
- C10: M0 is a feasibility checkpoint owned by the product lead, with an initial 10 working-day research budget (planning assumption, not spending authorization). Produce the inventory completeness method, scored direct/feed/import alternatives on the same representative notices and full-document/amendment tests, recurring per-install API/storage/OCR/support costs, rights blockers and ownership. If universal completeness cannot be established, return concrete evidence and options to the user; M5 stays open. Do not infer that nationwide geographic reach equals exhaustive publisher coverage.
- C11: Before M4 development, evaluation owner estimates supported source/sector cohorts, held-out bin sample needs, human labeling hours and permitted data cost. M4 is only fully complete for all supported product cohorts; unknown/unvalidated cohorts remain explicit incomplete work. Pilot 12 real qualification tasks (at least three per publisher class) with two operators using current tools and app on matched tasks; predeclare target median decision-time reduction >=25%, no additional missed viable bids against adjudication, and zero material mandatory false-pass in the pilot. Record all manual work and confidence's incremental benefit. Small pilot is a usability signal, not population accuracy proof. Failed targets reopen design, not waive scope.
- C12: Before M6 assign a maintainer for every adapter, evaluation release and platform package. Support current and prior app release for 90 days; publish compatibility/rights status and signed updates. Clients approve installation and optional redacted diagnostic export. Test at least two clean installs with differing credentials and update states. Budget estimates include source-change response and local storage; disable incompatible connectors visibly without losing cached evidence.
- C13: Planned document acquisition stages temp files then atomically renames by hash and commits database references through the single writer. After crash, reconcile orphan temp/blob files without deleting referenced evidence. Assessment publish uses compare-and-swap on profile/query/opportunity/manifest/policy/model revision tuple; a changed tuple yields outdated state and requeue. Profile save, amendment ingestion, export and assessment jobs must test both completion orders with controlled barriers.
- C14: Use typed errors for network timeout/auth/rate-limit/schema, parser/unsupported/limit, citation validation, provider refusal/empty/malformed response, disk-full/DB-busy and migration failure. All routes return stable error codes, redacted operation IDs and recovery text. Never convert failures to successful empty results or mandatory met. Enforce workspace scope in service and repository calls; validate query lengths, enum values, media types and IDs. No evaluation/model tools or document-originated instruction can invoke shell/network or grant access.
- C15: Bound initial work: page size100, query length4,000 chars, 50 terms, document download100MB, extracted archive500MB with 1,000 members, OCR500 pages/10 minutes, two fetch jobs and one parser job per install; all configurable policy caps with explicit incomplete status, not truncation hidden as success. Profile/source IDs and status/date filters need indexes; batch assessment joins. Store job payloads as IDs, not blobs. Cache keyed by complete revision tuple. Test caps at boundary and excess, cancellation and retry after process termination.
- C16: Redacted local diagnostics record operation/source/run/job/version IDs, elapsed time, stage, retry count and error code, never API keys or document bodies. Source-health UI shows last success, coverage completeness, queue age and next retry; users can pause/retry a source and export diagnostics by consent. Migration sequence stops worker/writer, verifies a DB+document-manifest backup, migrates, checks integrity and launches. Failure restores backup and previous package; no simultaneous old/new writers. Smoke tests inspect first5minutes and firsthour, including source freshness, search, evidence retrieval, workspace isolation and watch invalidation. Confidence and each connector activate independently only after their gates.
- C17: Duplicate mutations reuse operation IDs; stale forms reject with conflict and preserve drafts; navigation must not silently lose unsaved input. Exports pin a labeled immutable assessment snapshot and never mix revisions. Test both profile-save/export completion orders and duplicate clicks/retries. Dependency lockfiles, package audit and signed-release verification are required before client release. Time rollback on fixture corpus against a 15-minute recovery target; report actual timing and failures. UI recovery paths include auth reconnect, quota retry, parser manual review, disk remediation and schema-update advice. Local health surfaces these states; no stopped-app alert promise.
<!-- /autoplan-accepted:ceo -->

### CEO spec review iteration 1
Read both inputs fully; score 8/10; four issues: criticality, stale approval text, calibration definition, coverage completion. C6–C9 auto-accepted under P1, highest completeness; no user-scope change. Applied for review iteration 2.

### CEO Step 0 completion and temporal interrogation
Separate spec reviews: iteration 1 score8/10 four issues; iteration2 score9/10 PASS all dimensions and confirmed four fixes. Required metrics persisted. Scope documents accepted under autoplan authority, subject to final gate, not implementation approval.
Foundation M0/M1: source-access proof and local schema/launcher, human 4–6 days / assisted 2–4 plus external waiting. Core M2/M3: source/doc/evidence contracts, human 11–20 days / assisted 6–12. Integration M4/M5: evaluation and nationwide acquisition on parallel tracks after schema; labels/access are critical path with unknown duration. Polish M6: platform validation, human5–8/assisted3–5 days. Do not spend months polishing before proving source rights and full-document access. Stop shipping claims when M4/M5 gates fail; retain required work. Critical dependencies: verified source routes, labeled examples, Windows runner and signing credentials. No completed build or empirical accuracy claimed.

### CEO dual voices and disposition
Native completed, INPUT e04401bc26c100ed34a4375bc47c152401418beeaddd01e0f1f8bd2410feba25 matches immutable snapshot. Six findings (1 critical,4 high,1 medium). Outside preflight failed with ERROR: not in a git repo; no process or completed external review. No cross-model credit.
| Dimension | Native | Outside | Consensus |
|---|---|---|---|
| Premises | Feasibility unresolved | unavailable | N/A |
| Right problem | Qualification value needs pilot | unavailable | N/A |
| Scope | Preserve objective; prove access | unavailable | N/A |
| Alternatives | Need comparative acquisition costs | unavailable | N/A |
| Competition | Test against current workflow | unavailable | N/A |
| Six-month path | Operating/evaluation model missing | unavailable | N/A |
C10 accepts findings1/5; C11 accepts2/3/6; C12 accepts4 under P1 highest completeness. User Challenge UC1: literal all-bids completeness may be impossible to prove given private/inaccessible sources. Preserve objective and require M0 evidence; final gate offers informed handling, not a silent scope cut. Cost of proceeding without evidence: unbounded adapter/label/support work.

### CEO Sections 1–11
1. Architecture: one loopback service/writer with parser processes fits local installs. Database is single failure point, so verified backup/restore is mandatory. At10x data storage/OCR dominate; at100x a local full corpus may exceed disk. C13/15 bound work without hiding incomplete retrieval. Existing scripts remain separate fixture sources; no runtime coupling. Every private API requires local session plus workspace context; source setup changes only authorized source config. Elegant extension is a typed adapter contract, not a framework or microservice fleet.
2. Errors: mapped ten groups below. C14 rejects silent empty successes and separates AI refusal from invalid evidence. No actual methods exist; proposed service boundaries below define implementation contracts, not audited code. Every mapped error has a planned visible rescue/test; none proven implemented.
3. Security: SSRF and malicious files likelihood medium/impact high mitigated by destination revalidation and isolated bounded parsers; local cross-site access medium/high mitigated by session/Host/Origin/CSRF; cross-client IDs medium/high by service/repository scoping; secrets/log leakage medium/high by keyring/redaction; prompt injection high/high by no tool authority and cited schema validation. Package dependency compromise medium/high remains release verification: pinned locked builds and dependency audit, not unexamined latest packages. C14/16 accepted. Nil/type/length/unicode inputs explicitly rejected or normalized; data display escaped; parameterized SQL; no shell interpolation.
4. Data/interaction: C13 resolves amendment/profile races, export snapshot isolation and crash consistency. Double-click mutations require operation IDs; stale forms return conflict without clobbering; navigation preserves drafts; retry reuses IDs; zero results distinguish partial/offline; large lists paginate stable revision snapshots; queued jobs show status/cancel and backpressure. Nine interaction cases mapped, no intentionally silent case.
5. Quality: proposed modules fit Python service boundaries. Do not transplant historical ranking into fit. No production implementation exists to measure cyclomatic complexity or duplicated code. Keep adapter interface and typed schema narrow; shared score/filter policy must drive UI/export. Review actual functions with >5 decision branches when implemented; no speculative generic plugin platform.
6. Tests: acceptance1–16 map to unit/adapter/integration/browser/platform/evaluation suites. Critical assertions are no false met, exact filter parity, one watch event per revision, no cross-client access and no percentage outside validated cohort. C13–16 add crash/order/boundary proof; Friday confidence is complete install-to-amendment-and-restore E2E; hostile QA changes profile during export; chaos kills parser/writer between blob staging and commit. Offline fixtures/fake clock/controlled barriers reduce flakes; live contracts are separate gated smoke checks.
7. Performance: three slow paths estimated, not observed: broad local search p99 target3s; large OCR up to10min cap; source scan unbounded provider latency, page checkpointed. p95 benchmark remains2s on specified 16GB machine. C15 sets memory/work caps; export streams rows, no all-corpus list; indexes on workspace/profile/revision/status/date and FTS; batch joins avoid N+1. No global cache without workspace/revision keys. Benchmark before increasing limits.
8. Observability: C16 closes diagnosis gap with correlated run/job/version IDs and local health controls. Source failures appear in-app; no background alerts while stopped. Runbooks: auth->reconnect; quota->scheduled retry; parse->manual import/review; storage->free space and resume; stale schema->disable adapter and update; calibration drift->suppress and revalidate. Three-week diagnosis limited by retained redacted metadata; evidence versions preserved, no secret-bearing support upload.
9. Deployment: C16 requires quiescence and verified backup before migration, package rollback with data snapshot, and smoke checks. Platform signing/access still dependencies. M1 pilot is not M6 release. Activation flags for connectors/probabilities prevent unverified features. Old/new writers never coexist. Recovery-time target15minutes on fixture corpus is unmeasured and must be timed during platform gate.
10. Trajectory: reversibility4/5 for local service/modules,2/5 for acquired dataset/labels/rights. Debt: long-tail adapters, document format handling, cohort label coverage and installer matrix. C10–12 give these owners/decision points. Documentation must explain source contract, evidence lineage and recovery. None of the deferred CRM work is load-bearing for accepted features.
11. Design: prioritize client context, actionable candidate list and evidence over large confidence gauges. Journey uncertainty->narrowing->cited review->decision->amendment follow-up. All screens need partial/error/empty paths; laptop and 200% zoom are primary responsive goals. No existing DESIGN.md; dedicated design phase must specify hierarchy/focus/contrast and anti-generic layout.

### Error & Rescue Registry / Failure Modes
All rows are planned, require tests before shipping; no implemented rescue is claimed.
| Codepath | Exception / failure | Planned rescue | User sees | Test | Logged |
|---|---|---|---|---|---|
| source.fetch | TimeoutError / RateLimitError | checkpoint, bounded retry/backoff | stale/partial + retry time | adapter timeout/429 | Y |
| source.auth | CredentialError | pause source | Connect source | expired key | Y |
| source.normalize | SchemaError / missing IDs | quarantine record, incomplete run | schema changed | malformed page | Y |
| document.fetch | AccessDenied / UnsafeURL / SizeLimit | retain manifest, no unsafe fetch | login/import or blocked | redirect/private IP/limit | Y |
| document.extract | ParseError / UnsupportedFormat / OCRTimeout | retain file unreviewed | retry/manual review | corrupt/empty/oversize | Y |
| model.extract | Refusal / EmptyResponse / JSONDecodeError | typed incomplete output | provider refused/empty/invalid | separate fixtures each | Y |
| evidence.validate | CitationError / invented location | reject claim | needs review | nonexistent quote/page | Y |
| assessment.publish | RevisionConflict | discard stale publish,requeue | outdated assessment | both race orders | Y |
| storage.commit | DiskFull / DatabaseBusy | rollback,bounded retry,reconcile | storage action | kill/full/lock | Y |
| migration.apply | MigrationError / IntegrityError | restore verified backup | recovery mode | injected failure | Y |
No row has an intentionally silent/unrescued design; execution coverage remains unimplemented.

### Diagrams and shadow paths
Architecture (existing research scripts are fixture-only, outside runtime):
```text
Launcher -> browser -> loopback API/session -> scoped services -> single SQLite writer
                                         |                    |-> FTS/profile/version DB
                                         -> job coordinator -> adapters -> hash blobs
                                                            -> bounded parser -> citations
                                                            -> assessment CAS -> watch/export
```
Data flow for queries/profiles, source records, documents and exports:
```text
input -> type/length/rights validation -> normalize/extract -> staged blob + DB txn -> cited result
 nil -> explicit unknown/reject       empty -> zero/invalid  conflict -> rollback/retry
 type/size/encoding -> field error    timeout/OOM -> partial stale -> invalidate
 duplicate -> idempotent existing     private URL -> reject export -> pinned snapshot
```
State transitions:
```text
Job: queued -> leased -> succeeded | failed-retry -> queued | cancelled
Source: unconfigured -> checking -> healthy | partial | needs-auth | unsupported
Document: discovered -> fetched -> parsed | unreadable/access-blocked -> manual-review
Assessment: potential-fit -> needs-review | blocked -> reviewed-candidate (human+all gates)
Any governing version change -> outdated -> recompute; cannot jump unknown -> reviewed
Pipeline: New -> Reviewing -> Bid/No bid -> Submitted -> Awarded/Lost/Withdrawn (user event)
```
Error flow:
```text
failure -> typed stage/error+ID -> rollback/preserve last good -> UI action + durable retry
                              -> no fabricated empty success / no affirmative eligibility
```
Async schedules (publication boundary invariant: current tuple must equal computation tuple):
```text
assessment A reads v1 | amendment B commits v2 | state v2 | A CAS(v1) rejected
assessment A CAS v1   | amendment B commits v2 | state v2 | old assessment invalidated
profile save B v2     | export A pinned v1     | export labeled v1 historical, UI current v2
export A pins v1      | profile save B v2      | same: immutable snapshot, no mixed records
```
Deployment/rollback:
```text
verify package -> stop workers -> verified backup -> migrate -> integrity -> launch -> smoke
                                                  failure -> stop -> restore DB+manifest
                                                                       -> previous package -> smoke
```
Test map:
```text
launch/profile/search/dossier/decision/watch/export -> browser E2E + service integration
source pages/attachments/amendments -> adapter replay + permitted live smoke
parse/citation/match/cohort -> unit + labeled eval + failure fixtures
writer/job/migration -> crash+barrier integration; platform packaging -> both OS manual+E2E
```
Stale diagram audit: original architecture in section10 remains accurate; no code diagrams edited. Seven new diagram blocks above.

### NOT in scope
Deferred D1 automatic CRM integration in TODOS.md; baseline email/remote hosting/grants/bid submission remain excluded. Duplicate proposals S1/S2 rejected as already required; no reduction of M4/M5.
### What already exists
Research scripts and dated source research only; fixture candidates reused after attribution/access review. No application to refactor or existing tests to claim passed.
### Dream state delta
This plan establishes auditable local workflows. The12-month ideal requires sustained publisher access, ongoing evidence updates and validated cohorts; none are delivered by writing the plan.
### CEO approval readiness
U1 explicit user; C1–C16 accepted under autoplan P1/P2/P5; D1 under P3; S1/S2 P4. UC1 is a feasibility challenge retained for the final gate. No permission to spend, publish or change deployment. Approval readiness: PASS for recorded provisional amendments, UC1 pending final gate.

### CEO completion summary
| Item | Actual outcome |
|---|---|
| Mode | SELECTIVE EXPANSION |
| System audit | Nonrepo research scripts, no app; fixed filters cannot be reused as match engine |
| Step0 | 8 proposals:5 accepted,1 deferred,2 duplicate skips; 4 spec issues resolved in2 reviews,9/10 |
| Arch | 2 risks handled by C13/15 |
| Errors |10 groups mapped;0 silent design gaps;runtime unverified |
| Security |5 high-impact paths mapped; release dependency audit required |
| Data/UX |9 interaction edge cases;2 race pairs with both orders |
| Quality |1 prototype-reuse hazard;runtime metrics unavailable |
| Tests |Diagram and assertions added;all implementation tests pending |
| Performance |3 slow paths/caps;unmeasured |
| Observability |1 correlated diagnosis gap addressed |
| Deploy |3 risks: concurrent writers, failed migration, missing OS verification |
| Future |Reversibility4/5 code,2/5 data;4 debt areas |
| Design |Hierarchy/state needs handed to design phase |
| NOT scope / reuse / dream delta |Written |
| Error/failure registries |10 rows,0 intentionally silent paths |
| TODO |1 deferred integration |
| CEO plan |Saved in ceo-plans/2026-10-15-rfp-bid-discovery.md |
| Outside |Claude Code unavailable: nonrepo;native6 concerns |
| Lake score |N/A, no numerical option scoring |
| Diagrams/stale |7 new blocks;0 stale |
| Unresolved |UC1 at final gate; implementation/evaluation/access gates pending |

### Implementation Tasks: CEO
Estimates adjust automation ratios for empirical access, labeling and platform work. All files to be determined within proposed app modules.
- [ ] **C-T1 (P1, human 5–10 days / AI-assisted 3–5 days plus external waits)** — Prove acquisition and evaluation feasibility. Finding: C10–C11: unbounded access and label costs. Files: to be determined. Verify: Review completed M0 matrix, costs and unresolved-source report.
- [ ] **C-T2 (P1, human 3 days / AI-assisted 1–2 days)** — Implement revision-safe evidence publication. Finding: C13: stale results and crash consistency. Files: to be determined. Verify: Barrier tests both orders and crash staging/commit.
- [ ] **C-T3 (P1, human 4 days / AI-assisted 2 days)** — Implement typed failures and bounded jobs. Finding: C14–C15: silent failures and memory limits. Files: to be determined. Verify: Registry fixtures and cap boundaries.
- [ ] **C-T4 (P1, human 4 days / AI-assisted 2 days plus both OS testing)** — Implement support diagnostics and backup rollback. Finding: C12/C16: local installation operations. Files: to be determined. Verify: Two-install smoke, recovery and redaction checks.

### Design review provenance and scope
Full methodology read1–600,601–1200,1201–1800,1801–1931, truncated preamble span reread260–285. Target approved PLAN.md, UI yes, no DESIGN.md or app components to reuse. Nonrepo history unavailable. Step0 impression6/10: strong evidence semantics but missing layout/tokens/state combinations. A10 would specify each screen and interaction with validated pixels; all relevant dimensions reviewed. Designer version probe passed; variants failed before generating any image with No OpenAI API key found. Requested/saved0; no mockup approval or visual verification. No fabricated substitute. Native INPUT design4fa133925bf9609314a276f2149181d235d2a266ba4d3bdb36d6a4b7526aeb51 matched snapshot;9 findings,6 high and3 medium. External unavailable from retained nonrepo preflight; no outside review credited.

<!-- autoplan-accepted:design -->
- D2.1: Search uses a readable row layout, not metric cards. Row primary: title, publisher, qualification label, next actionable deadline. Secondary: place of performance, short scope, top blocker/unknown. Tertiary: Fit n/100, evaluated coverage, document counts and source freshness. Expand details for all remaining section4 contract fields. Relevance confidence is subordinate, with accessible definition/sample/version disclosure. No percent gauge. Examples must cover high-fit blocked, unknown deadline, provisional score and null confidence; comparison and export preserve this precedence.
- D2.2: Dossier review lists mandatory unresolved requirements first, mandatory resolved second, preferred third. Selection shows cited excerpt/location beside corresponding profile fact and evidence. Separate actions record met/not_met/unknown/conflict/not_applicable, correct extraction, attach evidence, resolve conflict and classify document criticality; changes require reason and retain history. A checklist names every remaining Reviewed candidate gate. Desktop two-column requirement/evidence workspace becomes sequential panels at narrow widths/200% zoom, preserving selection and return position. Manual assessment cannot override lifecycle, missing manifest or mandatory blockers.
- D2.3: Always distinguish Publisher status, Current qualification and Your decision. Preserve Submitted/Bid history through amendments/cancellation; show current assessment Outdated/Needs review/Blocked and changed citations. Business decisions never promote qualification. Decision changes require reason; Submitted requires user-entered submission date/reference, not a remote submission. Test Submitted -> amendment -> Needs review with historical Submitted intact; cancellation forces current Blocked.
- D2.4: First use offers Connect a source, Import a solicitation, Try guided sample as three direct actions. Draft real profile needs company name, capability description and work area only; optional facts stay unknown and are requested in context. Guided milestones: profile, search, source evidence, review decision, export; progress resumes. Exit demo selects/creates real workspace and never copies sample evidence or decisions. First useful cited requirement precedes exhaustive credential intake.
- D2.5: Primary search has query plus location, deadline and notice type. Advanced groups are classifications, qualifications, value, evidence and sources. Natural language opens editable filter preview before Search. One query-level Include unknowns toggle governs all applicable missing-field filters; default on, persists per saved query and matches API include_unknowns. Known matches and uncertain matches have separate labeled counts/views with reasons; excluded records are a separate inspection view and never silently join active results. Each proposed relaxation names old/new filter and requires Apply; exclusions remain hard until explicitly edited.
- D2.6: Search initial loading shows stage and Cancel; no sources shows the three setup choices; success shows count and coverage; cached+refreshing keeps rows/selection fixed with last-check label and Update results action; partial/error shows per-source failures and retry; cancellation preserves completed evidence and marks incomplete. Dossier loading shows manifest/extraction stage; empty package shows original link/import; partial shows missing critical files and Needs review; error retains last readable version; success shows citations and remaining checks. Export loading shows processed count when known; empty scope shows revise filters; partial shows omitted items/reasons and explicit partial-export choice; error retains retryable job; success shows filename, download/destination and pinned snapshot time. Never reorder a viewed list on background completion. Old scores remain labeled Outdated with assessment time, separated from current pending state. Unknown progress totals show stage rather than a fake percent.
- D2.7: Use distinct terms Closing browser, Stopping service and Computer asleep. Browser close leaves service running; Stop service or sleep pauses checks. Launcher has starting/running/stopped/error states, Open browser, Start and Stop service controls; stop explains paused monitoring. Browser persistent service indicator shows last/next check; disconnected screen instructs Launch RFP Empire to restart. Test close-browser/reopen and stop-service/relaunch separately.
- D2.8: Persistent navigation: Search, Watchlist, Profile, Sources/Coverage, Settings; Watchlist contains pipeline, tasks and changes. Client/workspace name remains visible beside decisions and exports. Dossier Back restores query/filter/page/scroll. Workspace switch with unsaved edits asks Save draft, Discard or Stay; never silent discard. A running export stays bound to its original workspace and labels the originating client even after switch; its download cannot appear in the new client's list.
- D2.9: Keyboard-only path must cover query -> filter disclosure -> result -> citation -> recorded review -> export; real table headers, visible labels, skip link, nav/main landmarks, accessible status names and non-hover critical content. Dialogs/citation views restore focus; submit errors focus error summary and preserve fields. Live regions announce major completion/error once, not every OCR page. Target44px controls, body>=16px, body contrast>=4.5:1 and UI/focus>=3:1; visible 2px focus ring. At>=1200px use list+dossier split,768–1199px list or full dossier with Back,below768px use labeled result rows and one evidence pane; comparison becomes one bid at a time with a selector preserving compared fields. Test1280x800 at200% plus keyboard/screen reader and long titles without hidden status.
- D2.10: Provisional visual taste T1 for final gate: office-light reading surface, IBM Plex Sans bundled locally with license, 16px/1.5 body, 24px page headings, tabular deadline numerals. CSS tokens: canvas #F4F6F8, surface #FFFFFF, text #17283B, secondary #465668, accent #006B67; verified contrast required before release. 4/8/12/16/24/32 spacing,4px control radius, no decorative shadows/gradients/card mosaics. Theme focus, selection, caret, link/visited distinction and scrollbar with forced-color fallback. Motion limited to a120ms visible-default evidence-pane emphasis on selection; reduced-motion disables it. No motion-dependent content or polling animation.
<!-- /autoplan-accepted:design -->

### Design decision ledger and seven passes
Each D2.1–D2.9 accepts the matching native finding under P1/P5 (complete specified behavior instead of implementation guesswork); D2.10 is TASTE T1, provisional under autoplan until final gate. No issue treated as approved by scope selection alone.

Pass1 Information architecture:5->9. Sixteen competing result fields risk hiding blockers. D2.1/2/8 choose hierarchy and navigation over equal-weight cards; comparison/export reuse it. A10 still needs rendered scan testing. No mandatory field removed.
```text
RFP Empire | Client: [name] | service/check status
Search | Watchlist | Profile | Sources/Coverage | Settings
Search -> query/common filters -> advanced groups/chips -> known/uncertain counts
       -> result rows -> dossier -> requirement list | source excerpt + profile evidence
Watchlist -> pipeline + tasks + changes -> same dossier -> reasoned decision/export
```
Pass2 State coverage:6->9. D2.6/7 provide combined states and stable refresh; D2.8 protects drafts and workspace switching. A10 requires actual live-region/focus and long-running job QA.
| Feature | Loading | Empty | Error | Success | Partial |
|---|---|---|---|---|---|
| Launch | Starting service | First-run actions | Retry/diagnostic ID | Open browser | running but source unhealthy |
| Profile | Loading saved draft | Minimal draft fields | Field errors+preserved draft | Saved revision | Unknown facts named |
| Sources | Checking credentials | Connect/import | Specific auth/quota action | Last success+coverage | Unsupported publishers counted |
| Search | stage+cancel | No matches+proposed filter edit | source list+retry | fixed result rows | cached+refreshing banner |
| Dossier | manifest stage | original/import | old version+retry | cited checklist | missing critical items |
| Review | saving decision | no decision yet | preserve reason/retry | recorded revision | outdated after amendment |
| Watchlist | loading changes | Save a bid | retain prior list | tasks/pipeline/changes | missed checks visible |
| Compare | loading chosen bids | Select up to3 | retry failed bid | same field hierarchy | per-bid unknowns |
| Export | count/stage | revise scope | retry job | file+client+snapshot | omissions preview |
Pass3 Journey:8->9. D2.4 makes value precede exhaustive setup; D2.3 preserves trust after amendments. A10 requires real pilot observation; inferred emotions are hypotheses.
| Step | User action | Likely feeling | Support |
|---|---|---|---|
| First5sec | choose import/live/demo | uncertainty | three concrete entry actions |
| First5min | open cited requirement | comprehension | minimal profile and source evidence |
| Narrow | inspect matches/exclusions | control | visible filters and unknown counts |
| Qualify | compare company evidence | cautious confidence | mandatory gates and reasons |
| Decide/export | record candidate | accountability | client+snapshot+blockers |
| Return months later | inspect amendment | regained context | immutable history and exact changes |
Pass4 Specificity/AI slop:4->8. OPERATE mode; no existing hard rejection can be proven from pixels, but layout/tokens were unspecified. D2.1 and T1 prohibit dashboard-card mosaics, hero copy and percent gauges. Primary litmus after proposed fixes: brand YES(name/client), anchor YES(result/evidence workspace), headings YES(utility nav), one-job YES, cards necessary NO(no cards), motion useful YES(selection cue), shadows unnecessary YES. These are plan judgments, not outside consensus or rendered validation. A10 needs approved/rendered visual tests; no forced decorative motion.
Pass5 Design system:3->8. No DESIGN.md; explicit D2.10 supplies provisional fonts/tokens/components. Choices are tied to office reading, not generic procurement branding. A10 needs taste decision and measured contrast/type/forced-color validation. Controls share field/error/focus states; tokens are reusable specification, not implemented CSS.
Pass6 Responsive/accessibility:5->9. D2.9 assigns concrete viewport behavior and full keyboard path; no accessibility debt deferred. A10 requires screen reader and both-platform browser proof.
Pass7 unscored:9 structural issues resolved in plan; T1 palette/type/layout detail pending final taste gate. UC1 from CEO remains separate. No new TODO deferrals; original CRM deferral untouched. No marketing site, mobile-native application or shared hosting added.

### Design litmus dual-voice scorecard
| Check | Native evidence | Outside | Consensus |
|---|---|---|---|
| Brand unmistakable | not specified in input | unavailable | N/A |
| Visual anchor | hierarchy missing | unavailable | N/A |
| Scannable | hierarchy missing | unavailable | N/A |
| One job per section | navigation unresolved | unavailable | N/A |
| Cards necessary | not specified | unavailable | N/A |
| Motion useful | not specified | unavailable | N/A |
| Without shadows | not specified | unavailable | N/A |
No cross-model hard-rejection agreement claimed.

### Design required outputs and summary
NOT in scope: marketing/native-mobile/hosting; no in-scope a11y/states deferred. What exists: research HTML is not a reusable product system; no app components or DESIGN.md. Mockups generated0,approved0 (missing key). Decisions9 structural plus1 provisional taste. Overall lowest-pass score3->8; Step0 impression6 separate. All seven passes executed; no claim of pixel QA. T1 remains unresolved, so status issues_open despite planned score8. No new TODOS. Required visual review after implementation remains mandatory before polished client release.

### Implementation Tasks: Design
- [ ] **D-T1 (P1, human 4 days / AI-assisted 2 days)** — Build search and evidence-review layout. Finding: D2.1/2/5/8 hierarchy and narrowing. Files: to be determined within app/templates and browser tests. Verify: Keyboard search-to-citation flow and preserved back navigation.
- [ ] **D-T2 (P1, human 3 days / AI-assisted 1–2 days)** — Implement state transitions and recovery screens. Finding: D2.3/4/6/7 combined states and lifecycle. Files: to be determined within app/templates and browser tests. Verify: Submitted amendment, demo isolation, offline refresh and stopped-service tests.
- [ ] **D-T3 (P1, human 3 days / AI-assisted 1–2 days)** — Apply responsive accessible controls and provisional tokens. Finding: D2.9/10 no concrete a11y/token contract. Files: to be determined within app/templates and browser tests. Verify: 200% zoom, screen reader, contrast and long-title checks.

### DX Step0 evidence (before scoring)
Methodology read1–600,601–1200,1201–1800,1801–2107 fully. Primary product is local end-user application; developer surface is internal API/service, Python maintainers and source adapters. Autoplan scope helper requires DX. DX POLISH, no public SDK/platform added. Persona inferred under P6: Python maintainer adding permitted adapters and debugging local client installs, expects reproducible fixtures and typed contracts, tolerance5min to first useful fixture. End clients remain no-Python GUI users. No README/app package/changelog exists yet; planned file map is not runnable code. Nonrepo history unavailable; prior generic AIProjects reviews are not this project.

Developer perspective (predicted, no runtime observation): I maintain Python applications and have been asked to add a source for a client. I can read the specification and understand why source provenance, mandatory requirements and unknowns matter. I cannot yet clone an application repository or run a documented development command, because this is a new build. I would first want a small fixture that travels through the same source normalization, document and assessment path as real data. Seeing a requirement tied to an actual page would tell me I am testing the useful behavior. I do not want a live provider key just to learn the architecture. When I change a field, I need a typed schema and a test that tells me whether I broke citations, pagination or client separation. If a source refuses access, I need an actionable error and a replay fixture, not a misleading empty list. Before changing the database I need the migration and rollback contract. These are predicted needs from the declared architecture, not claims about current error messages or measured onboarding.

Competitive benchmark (October15 official docs; times unknown, no human timing collected):
| Tool | Start -> useful result | Time/evidence | DX choice | Source |
|---|---|---|---|---|
| Datasette | local installation -> fixture database browser | unknown; documented | fixture exploration, desktop option | https://docs.datasette.io/en/stable/installation.html |
| Streamlit | Python environment/install -> hello browser app | unknown; documented | one visible demo command after install | https://docs.streamlit.io/develop/api-reference/cli/hello |
| RFP Empire | source bundle+declared toolchain -> cited fixture requirement | unknown; plan only | same-path offline fixture |
Peer boundaries differ; compare choices, not fabricated speed ranks. Target auto-selected under P1/P5: competitive <=5minutes for a Python maintainer from source bundle and declared toolchain with no dependencies cached to an understood fixture requirement, including instructions/dependency installation. Internet download time recorded, no warm-timer substitution. Clean-machine toolchain installation separately timed and reported, not hidden. Client packaged path separately <=5minutes from downloaded installer to cited demo requirement. Magic moment: same-path fixture with a verifiable citation; simplest existing demo capability, no hosted playground.

| Stage | Developer does | Friction / disposition | Status |
|---|---|---|---|
| Discover | reads audience/architecture | README not yet exists; specify both audiences | required build work |
| Install | resolves locked Python deps | no command/toolchain contract yet | required build work |
| Hello World | launches offline fixture | chosen existing demo, exact path missing | required build work |
| Real usage | adds permitted adapter | tests/schema/checkpoint contract needed | required build work |
| Debug | replays failed page | typed errors defined, examples absent | required build work |
| Upgrade | migrates local data | recovery defined, release docs absent | required build work |
First-time report: T+0 sees specification; T+0:30 looks for app README (not present); T+1 cannot run non-existent app; T+2/3 timing unknown because implementation has not started. These are documentary availability observations, not simulated executed errors. Improvements are in-scope completion of declared implementation.

<!-- autoplan-accepted:dx -->
- X1: Developer quickstart documents macOS shell and Windows PowerShell from the downloaded source bundle, with pinned tested Python3.12 patch and uv version in toolchain metadata, pyproject.toml and committed uv.lock. From app root: `uv sync --locked --group dev`, then `uv run --locked python -m app --demo`. Demo command initializes isolated demo storage, seeds the fixture adapter through the real ingestion/extraction pipeline and opens the browser after health readiness. Expected UI: Demo workspace, sample opportunity, a verifiable requirement citation and Confidence not validated. Commands are planned contracts until implemented/tested. Target<=5minutes from source+declared toolchain to understood citation including dependency download; report clean-machine toolchain setup separately. Packaged clients need neither Python nor uv. No hosted playground/public SDK added.
- X2: Local API is internal, authenticated, same-version browser/server only. Use typed request/response schemas and protected OpenAPI docs. Canonical sorts match,deadline,newest; UI relevance maps to match, Fit is the explained score. Search defaults match,page size50(max100),include_unknowns=true; cursor binds workspace/profile/query/index-generation/sort snapshot and expires after30minutes, returning409 CURSOR_EXPIRED with rerun action rather than silently mixing pages. POST workspace/profile/search/export/watch operations, GET dossier/job/source status, POST job cancel/retry are documented with concrete schemas; no route inferred from names alone. Accepted background mutation returns202/job_id; completed search returns200 with completeness/errors/pending_jobs; failure returns appropriate4xx/5xx, never disguised empty. Idempotency-Key header scopes mutations to workspace+operation, body hash mismatch409; retain24h. Revision conflicts409 with current IDs. Supply local authenticated TestClient workflow workspace->profile->search->evidence->export without production credentials.
- X3: Adapter protocol has describe_capabilities()->SourceCapabilities, fetch_page(window,cursor,cancel_token)->SourcePage, and fetch_manifest(source_version)->Manifest. SourcePage includes source/external IDs, raw provenance, normalized records, next_cursor, window bounds, provider watermark, completeness and typed errors; only the job coordinator commits cursor after durable page writes. Manifest includes discovered file IDs/URLs/rights/criticality and completeness_known. Adapters declare incremental/full reconciliation, cancellation/deletion and auth/rate-limit support; unsupported capabilities remain explicit. A credential-free fixture adapter exercises duplicate/interrupted pages, amendments and inaccessible attachments. `uv run --locked pytest tests/contracts -k fixture_adapter` is the planned reusable suite entry point; guide plus passing fixture precedes added live adapters.
- X4: Shared error envelope contains code, problem, known cause or 'cause unknown', recovery action, bundled help anchor, operation_id and optional retry_at/field. Map to launcher, API, job and browser. Include auth, quota, parser, schema, disk/busy, migration, session-expiry, stale-cursor and invalid-config catalog entries. Example SOURCE_AUTH: 'This source could not connect; the provider rejected its credential; reconnect in Sources; help/sources#authentication'. DOC_PARSE: 'This file could not be read; cause unknown; open original or import a readable copy; help/documents#unreadable'. STORAGE_FULL: 'Changes could not be saved; the data volume is full; free space then Retry; help/recovery#storage'. Examples are required future outputs, not observed runtime. Contract tests verify fields and redact credentials/doc bodies.
- X5: Documentation ships with the app version: README quickstart, bundled operator guide, developer run/test/architecture guide, adapter guide, configuration reference, generated internal API/error reference, changelog and update/restore runbook. Include executable complete examples with expected200/202/409 and null-confidence/partial-source responses. Links from setup and errors work offline. Verify getting-started commands on both OS and help lookup<=2minutes for setup/auth/restore using task-based trials. Maintainer support instructions and a local diagnostic/issue template name the configured support destination; do not invent a live community or publish private data.
- X6: Typed effective-settings view shows defaults, values, units, scope, restart needs and validation errors with secrets redacted. Precedence: packaged defaults < installation settings < workspace search/profile settings; explicit dev CLI overrides only the declared port/data-dir/demo flags and appear in effective settings. Refresh6h/watch and24h/search allowed15min–7days subject to provider minimum; worker count1–2 fetch and1 parser; resource limits may be lowered, increases require maintained policy revision and benchmark. AI provider opt-in per workspace; scoring policy weights are maintainer versioned, not ad hoc user sliders. Port0(auto) or1024–65535 loopback only; changing port/data directory requires stopped service and validated restart/migration. Search defaults hot-apply only to new query revisions. Licensing, isolation, loopback, blockers and confidence validation cannot be disabled by settings.
- X7: App releases use semantic versions, schema versions and connector compatibility metadata. Breaking changes include migration guide, preflight incompatibility warning and tested backup/restore; downgrades reject newer DB schemas unless restoring matching backup. Maintain current/prior90-day support from C12. Local dev supports hot reload in dev mode only; fake clocks, isolated temp directories and fixture transports enable offline CI on Windows/macOS with pinned toolchain. No TypeScript SDK/Linux-client promise added. Post-build DX check uses clean caches and human-readable instructions, records dependency/toolchain time, errors and successful cited result, with opt-in local notes and no automatic telemetry or recurring external task.
<!-- /autoplan-accepted:dx -->

### DX independent voice and decisions
Native INPUT dx4762412cfd9ff119ed8c3bbd2097ec16cbaee21455f1fe6ea98e2bd236536fe9 matches snapshot.6 findings (3 high,3 medium), no critical. Outside unavailable due retained nonrepo error, no new completed external attempt. X1 accepts reproducible startup but retains already selected5minute target instead of reviewer's suggested10; target is unmeasured. X2/X3/X4/X5/X6 accept findings2–6 under P1/P5. X7 follows required upgrade/platform proof. All scoped to internal/local product, no public SDK or hosted demo. No DX taste decision added.

### DX eight passes (references read separately per pass)
1 Getting Started:3->8. No executable dev path existed in plan; X1 defines2commands plus open sample, locked deps and isolated demo. Fixture citation is meaningful, but clean-system timing unmeasured;10 would require repeated successful human trials under5min.
2 API/CLI/SDK:5->8. Internal API had inconsistent vocabulary and unspecified pagination/job contracts; X2/3 define schema/cursor/idempotency/adapter boundaries. No public API promised.10 requires example contract execution and zero undocumented routes.
3 Errors:7->9. C14 covered failure types; X4 closes message/cause/fix/help gap. Current runtime text unavailable. Three traces: rejected credential->SOURCE_AUTH/reconnect; corrupt file->DOC_PARSE/original/manual; disk full->STORAGE_FULL/free space+retry. Cause unknown is honest; no guessed diagnosis.10 requires field/redaction/help-link proof in actual surfaces.
4 Docs:2->8. X5 makes examples and offline help release deliverables. Tutorial (guided demo), task guides (adapter/restore), reference (schema/settings) are distinct; no docs-site infrastructure required.10 requires both-OS paste tests and timed findability.
5 Upgrade:7->9. Existing backup design retained; X7 adds schema compatibility, release notes and rejection of unsafe downgrade. Automated codemods are unnecessary for internal APIs but data migrations must be tested.10 requires actual failed-upgrade recovery proof.
6 Dev environment:3->8. X1/7 supply pinned Python/uv, hot reload and offline fixture CI. Python type annotations replace irrelevant TS-SDK demand. No Docker required for local workflow.10 requires both architecture/OS build matrix evidence and measured edit/test loop.
7 Community/ecosystem:6->8. This is a client application, not an OSS community launch. X5 provides operator/maintainer help and private diagnostic template; licensing costs disclosed per source. No new external channel, plugin marketplace or open-source license chosen.10 would require demonstrated support responsiveness, not fake community links.
8 Measurement:5->8. X7 measures the declared cold-start clock, local-only human observations, separate client/contributor journeys and accurate success endpoint. No adoption percentages borrowed from generic references.10 requires actual onboarding observations; no telemetry/recurring process authorized.

### DX Scorecard
| Dimension | Pre-fix | Post-plan | Evidence limit |
|---|---|---|---|
| Getting started |3|8|not measured |
| API/CLI/SDK |5|8|schemas/tests to build |
| Errors |7|9|examples proposed |
| Documentation |2|8|docs to build |
| Upgrade |7|9|restore test pending |
| Environment |3|8|OS matrix pending |
| Community/support |6|8|support destination configured at release |
| Measurement |5|8|human trials pending |
Overall arithmetic mean4.75->8.25 (all dimensions>=8 after specification); this is plan completeness, not observed DX quality. No prior RFP review trend. TTHW unknown -> target<=5minutes, competitive target not earned rank. Magic moment designed via existing isolated demo. Product internal API/local Python app; mode DX POLISH. Principles covered in plan: zero-friction X1, learn-by-doing X1/3/5, uncertainty X4, defaults/escape X6, code-in-context X2/5, useful result X1.

### DX consensus
| Dimension | Native | Outside | Consensus |
|---|---|---|---|
| Startup<5min | unmeasured path | unavailable | N/A |
| Naming | contracts missing | unavailable | N/A |
| Errors | diagnostic fields missing | unavailable | N/A |
| Docs | deliverable missing | unavailable | N/A |
| Upgrade | no separate issue beyond docs | unavailable | N/A |
| Environment | reproducibility missing | unavailable | N/A |

### DX implementation checklist
- [ ] Cold-start cited fixture under5min; report toolchain install separately.
- [ ] Locked install and first-run command produce meaningful isolated demo, no credentials.
- [ ] Error code/problem/cause/fix/help/operation ID works on all surfaces.
- [ ] Typed internal API, defaults, revisions, cursor and adapter contracts exercised.
- [ ] Both-OS copy-paste docs, real partial/conflict examples and offline help search.
- [ ] Changelog/migration/restore/version compatibility and fixture CI pass.
- [ ] Private support route configured and diagnostics require user consent.
TypeScript SDK/free-tier service/public community not applicable; no such product commitment introduced. NOT in scope: public SDK, hosted playground, new community infrastructure. What exists: planned API and error taxonomy, research scripts only. No new TODO deferrals; all fixes are implementation work, not proven code.

### Implementation Tasks: DX
- [ ] **X-T1 (P1, human 2 days / AI-assisted 1 day)** — Build reproducible developer and operator quickstarts. Finding: X1/X5 onboarding/docs gaps. Files: to be determined within app/docs/tests. Verify: Clean-cache both-OS cited demo and doc example tests.
- [ ] **X-T2 (P1, human 3 days / AI-assisted 1–2 days)** — Define typed API and adapter contracts. Finding: X2/X3 incomplete interfaces. Files: to be determined within app/docs/tests. Verify: Authenticated TestClient scenario and fixture adapter contract suite.
- [ ] **X-T3 (P1, human 2 days / AI-assisted 1 day)** — Build error catalog and effective configuration. Finding: X4/X6 recovery and overrides. Files: to be determined within app/docs/tests. Verify: Error schema/redaction/settings invalidation tests.
- [ ] **X-T4 (P1, human 2 days / AI-assisted 1 day plus OS runs)** — Document and verify release/dev compatibility. Finding: X7 upgrade/toolchain gaps. Files: to be determined within app/docs/tests. Verify: Old schema, downgrade rejection and restore tests.

### Engineering provenance and scope
Methodology KFuvMy SHA de048c9230e9842fd1c8a0d4d13499afe4128eeeb3dd684c58b60340d51017bc read ranges1–600,601–1200,1201–1800,1801–2208 through EOF; truncated portions repaired190–360,700–870,1480–1570. Fixed ENG_INPUT mFpqjb/eng-implementation.md SHA513ddfcc8645ba2214b86489e829943ccb51d337b2de80d1a7226a4263242fe3. Native eng_voice terminal INPUT matches,7issues(4high/3medium). Outside unavailable: git guard exit128/not a repository at /Volumes; no external process completed. Native model identity unreported. No claim of cross-model agreement.

Step0 scope accepted as-is, FULL_REVIEW. Existing authored code freshly read: tools/federal_pull.py1–122, tools/federal_rank2.py1–29. Relevant history unavailable (nonrepo); future app paths and tests absent. No AGENTS testing rules/framework detected. Approved plan targets Python; pytest+Playwright selected under autoplanP1/P5. Scope structure auto-decision E0: original functional modules estimated20–30production files/12service responsibilities plus tests/docs vs smaller single-file web+jobs+parsing arrangement3–5files; retain functional modules because mixing privilege and storage boundaries raises risk. Neither arrangement changes features; no scope cuts. No new service infrastructure/Celery/Redis/Electron. Core process + supervisor/workers + native sandbox helpers is the minimum proven boundary candidate. Count is estimate, not an existing diff. Source access/coverage, search, document extraction, qualification, confidence and release each map to the corresponding planned module; research scripts contribute reviewed fixtures only. Product is innovating, not a migration of those scripts.

Search check (official docs,2026-10-15): [Layer1] SQLite WAL permits concurrent readers but long read transactions can obstruct checkpointing; choose short reads/materialized results (https://www.sqlite.org/wal.html). FTS requires synchronized content/index maintenance and explicit initial rebuild (https://www.sqlite.org/fts5.html). FastAPI BackgroundTasks is not the selected durable queue; heavy work stays supervised outside request lifecycle (https://fastapi.tiangolo.com/tutorial/background-tasks/). Platform packaging builds on each OS (https://pyinstaller.org/en/stable/usage.html). Windows AppContainer provides capability isolation (https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation); Apple warns child processes do not provide XPC isolation (https://developer.apple.com/library/archive/documentation/Miscellaneous/Reference/EntitlementKeyReference/Chapters/EnablingAppSandbox.html). E3 choices require packaged proof; docs are not runtime validation. No unfamiliar distributed concurrency introduced.

### Engineering dual voices
CLAUDE CODE SAYS (eng architecture challenge): unavailable; no review output.
CODEX (in-host) SUBAGENT:7 findings, all plan risks: time-only invalidation,E1; missing review revision,E2; parser isolation,E3; durable leases/events,E4; pagination persistence,E5; bootstrap,E6; blob rights,E7. All accepted under P1/P5. Full reviewer result retained in conversation; these are not observed defects in running app.
| Dimension | Native | Claude Code | Consensus |
|---|---|---|---|
| Architecture | E1/E2/E4 changes needed | unavailable | N/A |
| Tests | seven regression groups missing | unavailable | N/A |
| Performance | snapshot/WAL risk | unavailable | N/A |
| Security | isolation/bootstrap/grants | unavailable | N/A |
| Error paths | worker recovery underspecified | unavailable | N/A |
| Deployment | isolation must be proven | unavailable | N/A |
Single-voice high risks retained; no consensus credit. UC1 is a single-voice/parent feasibility concern, not a both-model User Challenge. Original nationwide requirement stands.

<!-- autoplan-accepted:eng -->
- E1: Assessments include evaluated_at and valid_until, the earliest applicable deadline, credential expiry and source freshness boundary. Recheck temporal gates at search/dossier read, assessment publication and export completion even without revision changes. Expired deadlines force Blocked; expired credentials/freshness force Needs review and suppress current probability/badges. Historical exports retain as-of labels plus current-at-export warning. Use UTC instants, preserve source timezone/uncertainty, monotonic elapsed time within a run; detect wall-clock rollback or unexplained large jump, invalidate temporal assurances and request clock correction/recheck. Never reactivate expired confidence solely because the clock moved backward. Fake-clock tests cross each boundary, sleep/resume and export completion.
- E2: Define immutable AssessmentInputRevision combining the C13 tuple with requirement-set, extraction, human correction/evidence-review and acquisition-grant revisions. Every correction, attachment, conflict resolution or rights change creates a new aggregate input revision. Publish/cache/review/export bind to that aggregate, temporal validity and workspace. CAS rejects stale attempts and retains the historical record; both completion orders of correction/assessment, attachment/assessment and conflict/export are mandatory integration cases.
- E3: Before untrusted document extraction ships, prove OS-enforced parser isolation in packaged Windows and macOS builds. Candidate mechanisms: Windows AppContainer with no network capabilities plus process/job restrictions; macOS signed sandboxed XPC helper with no network or broad file entitlements. Native glue is confined to the helper boundary; core application remains Python. Only staged input, private scratch and bounded output are exposed; no DB, credentials, other workspace files or arbitrary process launch. Broker validates output. Initial per-parser policy: 1GiB memory,120s CPU,10min wall time,20MiB extracted text, in addition to C15 download/archive/page caps; supervisor terminates on any exceeded limit, records partial/error and preserves original. Verify actual enforcement and dependency compatibility during M0/M1 platform spike; no claim that subprocess alone is a sandbox. If a supported OS cannot enforce the contract, automatic parsing is disabled visibly there and M3/M6 remain incomplete until repaired; manual review is an interim path, not completion. Tests attempt network, sibling-file reads, child execution, memory growth and non-OCR hangs. Signed platform isolation is a release prerequisite, not a waived risk.
- E4: Durable jobs use queued -> running -> succeeded, retry_wait, failed_terminal or cancelled. Atomic claim assigns attempt_id and fencing token through the single writer; heartbeat15s, lease60s while awake, coordinator fences pre-suspend attempts on resume/restart. Only current attempt may commit a result or renew. Cancellation is persisted and checked before network/parser starts, between chunks and before commit; already committed results remain historical. Retry transient failures at most5attempts with full jitter exponential delay base2s cap15min, respecting larger provider retry_at; auth/schema/permanent failures pause with action. Exhausted jobs are visible failed_terminal and manual Retry makes a new linked attempt. Commit source page, cursor, material change and unique watch-event/outbox key in one transaction; outbox delivery is idempotent by workspace/watch/material-revision/type. Kill/replay every boundary and resume a fenced worker; never claim external exactly-once delivery.
- E5: Search materializes ordered result IDs and assessment-input revisions in bounded SearchSnapshot rows; deterministic final tie-breaker opportunity UUID. Build under a short consistent read, finish within2s target or cancel at5s with explicit QUERY_LIMIT and refinement action, never hold a read transaction across browser pages. Snapshot TTL30minutes, at most100,000 result rows/snapshot,10active snapshots/workspace and1million snapshot rows/install; beyond caps return explicit partial/limit with counts and refinement, never exhaustive success. Completed snapshots supply pages and exports; no long-lived SQLite read transaction. Rights and temporal gates are rechecked on every access; changed current facts are overlaid as outdated/blocked without silent reordering. Expired snapshots return409; exports pin their snapshot until job completion within bounded retention and retain client/as-of labels. Expiration cleanup respects active export references; admission rejects new snapshots when storage cap is reached. Benchmark baseline100knotices/1mchunks with two fetch jobs, parser and10snapshots, plus10x stress reporting latency/RSS/disk/WAL/queue growth. The10x run diagnoses scale; it does not invent a2s guarantee at that scale.
- E6: Launcher creates/validates the service through an OS-user-restricted local IPC identity handshake, not a response on a remembered TCP port. Bind random available127.0.0.1 port and validate exact Host/origin. A256-bit one-use bootstrap token expires60s and is delivered in URL fragment, consumed by same-origin POST, removed immediately with history.replaceState before other navigation; no third-party assets, no referrer, no token logging/caching. Exchange establishes host-only HttpOnly SameSite=Strict session cookie with8h absolute lifetime; rotate bootstrap/session signing secrets on service restart. Session cannot be reused across restart, bootstrap replay fails. Use plain loopback HTTP only after testing browser cookie behavior; do not falsely promise Secure-cookie protection over HTTP. CSRF tokens and exact Origin/Host enforce mutations; minimal unauthenticated readiness returns no private data. CSP/default self, frame-ancestors none and Referrer-Policy no-referrer. Packaged tests cover wrong process/port, replay/expiry/restart, missing/forged origins, hostile external page and URL/log leakage. Same-OS-account malware is outside this session boundary, consistent with baseline.
- E7: Separate Blob(hash,bytes) from AcquisitionGrant(workspace,source/acquisition route,license/document rights,private/public,revision,revocation) and DocumentVersion provenance. Identical hashes do not grant access. Every citation, file route, export, cache and optional provider-processing job resolves a current authorized grant plus pinned provenance; no direct hash-only retrieval. Revocation prevents new viewing/export/external processing even for a historical assessment; retain a tombstone/audit reason where permitted. Previously downloaded external copies cannot be recalled and this is stated. Do not reveal existence across workspaces; dedup storage sharing is allowed only under applicable rights. Test identical bytes acquired with different rights, revocation during export/provider job and old cached links.
- E8: Use SQLite WAL on local disk only, foreign keys enabled, bounded5s busy timeout and single writer ownership. Maintain FTS5 and normalized content in the same transaction; migration/backfill explicitly rebuilds and validates the index. Search quote/escape rules generate FTS expressions from validated term structure, not raw user query operators; parameter binding alone does not validate FTS grammar. Test literal punctuation, negation, Unicode, empty/all-stopword queries, SQL/FTS operators, index rebuild consistency and disk-full rollback. Backup uses quiescence plus SQLite backup API/integrity validation, never copies live DB alone without WAL. Document blob collection deletes only unreferenced, unpinned blobs after reconciliation and a7day grace period, with rights retention constraints and dry-run manifest; referenced evidence is never garbage-collected.
- E9: Build on each supported OS: initial target Windows11 x64 and macOS14+ arm64/x86_64, verify dependency/support compatibility during M0 and record exact tested OS/browser versions at release. Broader Windows/macOS requests remain coverage work if target customers need other architectures; never imply untested compatibility. Package Python dependencies and OCR assets separately per target, signed/notarized installer/app with SBOM and checksums; private artifact download channel configured before client release, no website publication/purchase authorized by this plan. CI runs locked unit/contract/integration/eval fixtures and browser tests on both OS; protected release jobs use signing secrets from platform stores, never repo. Run clean-machine install/update/restore/isolation tests before release. Select final bundler only after E3 spike; PyInstaller is a candidate, not proof of sandbox compatibility. Automatic parsing/release blocked if isolation proof fails. All benchmark/calibration/platform results are future measurements.
- E10: Implement the complete codepath and user-flow test matrix in the engineering QA artifact. Use pytest for pure/contracts/integration, Playwright Python for browser flows, packaged OS tests for native isolation/install/lifecycle, and versioned offline evals for extraction/citations/qualification/relevance/calibration. Existing app coverage is zero because app does not exist. Test through real service/repository/worker boundaries with fixture transports, fake clocks and controlled barriers; do not add production-only test endpoints. New live adapters require rights-qualified fixture replay and bounded live parity checks. No tests of untouched research scripts are required; existing behavior there remains unchanged. M0 precedes source commitments; foundation/schema contracts precede parallel adapters/UI/evaluation; integrate all before M3/M6 gates.
<!-- /autoplan-accepted:eng -->

### Engineering decision audit
| ID | Phase | Decision | Classification | Principle | Rationale | Rejected |
|---|---|---|---|---|---|---|
| E0 | Eng scope | preserve functional modules/full scope | auto | P2/P5 | separate privileges, no new server infrastructure | monolith file or scope cut |
| E1 | Eng architecture | temporal validity | auto | P1 | revision alone misses expired bid | revision-only cache |
| E2 | Eng architecture | aggregate input revision | auto | P1 | human corrections cannot be overwritten | incomplete CAS |
| E3 | Eng architecture | prove native parser isolation | auto | P1/P5 | process separation is insufficient | unsandboxed fallback as complete |
| E4 | Eng architecture | fenced jobs + transactional events | auto | P1/P5 | retry/crash/sleep recovery | in-memory tasks |
| E5 | Eng performance | bounded materialized results | auto | P1/P5 | stable pages without long read lock | persistent read transaction |
| E6 | Eng architecture | one-use local bootstrap | auto | P1 | reject forged/stale/replayed authority | reusable URL secret |
| E7 | Eng architecture | grants separate from blobs | auto | P1 | equal bytes do not imply equal rights | hash-only authorization |
| E8 | Eng quality | transactional FTS/backup/GC | auto | P1/P5 | consistency and recovery | raw FTS strings/live file copy |
| E9 | Eng architecture | OS build and isolation release gate | auto | P1 | platform evidence before client release | cross-compile assumption |
| E10 | Eng tests | full behavior matrix | auto | P1 | approved requirements need regression proof | smoke-only suite |
Approval readiness: PASS for auto-decisions E0–E10 under user's explicit autoplan request; T1 visual taste remains provisional at driver final gate. No changes to approved scope. Runtime correctness unverified.

### Engineering Section1: Architecture
[P1] (confidence8/10) PLAN.md:160 “Assessment | opportunity/profile/query/policy/model revisions” omits time and human-review changes; planned races, not reproduced bugs. Accepted E1/E2.
[P1] (confidence8/10) PLAN.md:186 “parse in restricted worker processes” lacks OS mechanism; accepted E3 with release proof, not an assurance subprocess is safe.
[P1] (confidence8/10) PLAN.md:162 “Job/AuditEvent | stable operation key, status/retry/cursor” lacks fencing/state recovery; accepted E4.
[P2] (confidence8/10) PLAN.md:184 “require a random local session” lacks bootstrap protocol; accepted E6.
[P2] (confidence8/10) PLAN.md:120 “Duplicate public records may be shared internally only if the license permits” needs acquisition authorization distinct from byte identity; accepted E7.
[P2] (confidence8/10) PLAN.md:148 “Package separately on Windows and macOS” needs packaging/isolation compatibility spike and release channel; accepted E9. Seven architecture issues counting E1/E2 separately. Blast radius: false bid readiness, leaked client evidence, lost jobs; local disk is single point of failure, addressed backups, not HA. No direct reuse of data-pull logic. Source adapters share normalized contracts but retain distinct provider rights/errors.
```text
Existing research scripts -- reviewed fixtures only --> fixture adapter
(no runtime import)                                     |
Launcher -- restricted IPC --> local service <--- authenticated browser
                                | validate/session/workspace
                  search/profile/dossier/review/export
                                | aggregate revisions + grants
                     single writer / SQLite WAL + FTS
                       |        |             |
                    jobs     snapshots     outbox/watch
                       |                      |
                fenced supervisor      local UI events
                  /          
          source adapters    sandbox broker -> native parser helper
               |                   |              |
            permitted URLs     staged blob    bounded output
                                   \---- citation validation
                                             |
                                   assessment CAS + temporal gate
```
Coupling rule: adapters never write DB/cursors; parsers never receive DB/keys; web requests never wait for OCR. Planned inline diagrams in jobs, matching, documents broker and db transaction modules explain ownership/CAS/recovery. Distribution: native builds+signing+private installer channel; signing accounts/channel remain release dependencies, not permission to publish.
Dispositions: E1/2/3/4/6/7/9 accepted;0 rejected/0 deferred architecture changes.

### Engineering Section2: Code quality
[P2] (confidence8/10) PLAN.md:164 “Queries bind parameters rather than concatenate user strings” is insufficient to define FTS-language escaping; E8 owns query compiler and index consistency. One code-quality issue.
Existing federal_pull.py:41 “pages = min(...,100)” and:73 “[:600]” would violate completeness if transplanted; federal_rank2.py:11–12 excludes low-history codes and:23 sorts thin_pct. Preserve untouched; no speculative shared extraction into production. Proposed callers only: search page and export use one query service; dossier and assessment use one evidence/grant validator; source retries and manual retry use job coordinator. No verified production duplicates exist; no claimed line savings. New common modules grow total code but enforce one security/meaning contract; tests at both caller boundaries. Naming match vs confidence vs qualification follows X2; no generic mega-helper. Error handling uses X4 typed envelope and C14 registry. No touched existing diagrams or obsolete tests.
Dispositions: E8 accepted; no refactor of existing research files.

### Engineering Section3: Test review
Actual source read in dedicated call before diagram; future app and tests absent. Existing quality coverage0, not a failed test run. Chosen frameworks pytest/Playwright Python; native packaged probes for sandbox/installer. Unit boundaries enforce deterministic semantics; integration at transactions/jobs; E2E for client journey; eval for extraction and calibration. Every row below is GAP with planned behavioral/edge/error assertions, not TESTED. Twenty coverage groups,0/20 currently protected; future quality goal★★★ for each, not a test-count quota.
```text
ENTRY / CODE PATH                                      USER FLOW + COVERAGE
launcher -> IPC -> bootstrap -> cookie                 [GAP T01 ->E2E] start/replay/port/restart
profile input -> validate -> immutable revision        [GAP T02 ->E2E] draft/edit/switch/stale submit
search terms -> typed filters -> FTS -> snapshot       [GAP T03 unit+integration] narrow/unknown/exclude
snapshot -> grant/time checks -> row/page/export       [GAP T04 ->E2E] page while updates happen
source setup -> rights/key -> fetch -> normalized page [GAP T05 contract] no-key/auth/429/schema/partial
page -> writer txn -> cursor/change/outbox             [GAP T06 integration] crash/replay/cancel
job claim -> heartbeat -> attempt commit               [GAP T07 integration] dead worker/sleep/retry
manifest -> fetch allowlist -> staged blob/grant        [GAP T08 security] redirects/limits/private host
sandbox input -> parse/OCR -> output -> validate        [GAP T09 native+integration] hang/bomb/escape
excerpt -> requirement -> evidence/correction revision [GAP T10 ->EVAL] citation/manual correction
profile+requirement -> rules -> score+hard gate         [GAP T11 unit+eval] high-fit blocked/unknown
input revision + time -> assessment CAS                [GAP T12 integration] race/time-only expiry
labeled corpus -> splits -> calibration -> activation  [GAP T13 ->EVAL] supported/unsupported/drift
workspace grant -> file/cache/provider/export          [GAP T14 security ->E2E] same bytes/different rights
watch -> material event -> business/history state      [GAP T15 ->E2E] Submitted -> amended/cancelled
export scope -> pinned snapshot -> rights -> output    [GAP T16 ->E2E] partial/formula/stale/duplicate
DB/blob -> quiesce -> backup/migrate/restore/GC          [GAP T17 native+integration] disk-full/crash/downgrade
all screens -> loading/empty/error/success/partial      [GAP T18 ->E2E] keyboard/zoom/drafts/back/compare
installer -> signed assets -> launch/update/stop        [GAP T19 platform] clean install both architectures
registry -> publisher inventory -> coverage audit      [GAP T20 contract+manual] known/unknown/missing source
```
For each transform, null/empty/invalid/limit input is either schema rejection with preserved UI fields, explicit unknown/partial, or empty success only for a complete scan. None become eligibility met. All branches shown have matching assertions/value cards in saved QA artifact. Existing coverage cannot catch regressions because there is no app suite. No production seam added solely for tests; clock/transport boundaries are operational interfaces, controlled barriers use worker/coordinator test harness only. Existing research scripts are not changed, so no regression contract for them needed.
LLM/eval suites: extraction structure/negation/optional-vs-mandatory; citation exact-location validity; qualification critical blockers zero false-met fixtures; source/sector relevance and fixed C7 calibration; prompt-injection/tool-denial; OCR uncertainty; provider refusal/empty/malformed outputs. Compare parser-only and current approved model/prompt baselines on same held-out families; never tune on activation test. Model changes rerun affected quality and full activation gates. No API/key presumed. Tests to retire:none. Dispositions:20groups of required proof accepted E10,0 optional deferrals.

### Engineering Section4: Performance
[P2] (confidence8/10) PLAN.md:307 “cursor binds...index-generation...expires after30minutes” specifies identity but not persistence; E5 materializes bounded results. One performance issue. Query plans/actual timings unknown. Fetch/parser budgets C15 bound work; server uses batched assessment/grant joins to avoid per-row queries, FK/filter indexes and FTS.20MiB text/1GiB parser caps and streamed downloads prevent whole-archive memory loads. Search snapshot creation has5s cancellation, p95target2s at100k/1m corpus, no fabricated measurements. Long read transactions removed; WAL size/checkpoint latency recorded under concurrent ingestion. Source catch-up may grow queue: prioritize watched/deadline work, retain durable cursors and expose backlog. Cache uses full input revision+valid_until+grant revision; TTL alone cannot authorize. Disposition E5 accepted; baseline and10x stress documented in QA plan.

### Engineering failure modes registry
| Path | Failure | Error/recovery | Proof | Critical silent gap |
|---|---|---|---|---|
| Launch/auth | wrong server/token replay | reject,relaunch;no private health data | T01 | no,planned |
| Profile/search | stale revision/invalid FTS |409/422,retain draft/rerun | T02/03 | no,planned |
| Snapshot | timeout/cap/expiry | explicit limit/409 | T04 | no,planned |
| Adapter | key/quota/schema/deletion | pause/backoff/partial/cancel | T05 | no,planned |
| Commit/outbox | crash after data before notice | atomic txn/idempotent consumer | T06 | no,planned |
| Job | dead or obsolete worker | lease/fence/terminal retry | T07 | no,planned |
| Download | malicious URL/oversize | deny,manifest remains missing | T08 | no,planned |
| Parser | escape/hang/OOM | OS deny/terminate,Needs review | T09 | no,platform proof required |
| Evidence | fabricated citation/correction race | reject/CAS,outdated | T10/12 | no,planned |
| Qualification | unknown requirement/expired facts | Needs review/Blocked | T11/12 | no,planned |
| Probability | small unsupported cohort/drift | null/suppress | T13 | no,planned |
| Blob/grant | identical bytes cross-client | deny current grant,log redacted | T14 | no,planned |
| Watch/decision | amendment after Submitted | retain history,reset qualification | T15 | no,planned |
| Export | rights/time changed/partial | recheck,explicit omissions/no mixedversions | T16 | no,planned |
| Storage/update | disk full/failed migration | rollback/verified restore | T17/19 | no,planned |
| UI | lost draft/hidden status | preserve draft/focus/state feedback | T18 | no,planned |
| Coverage | absent publisher/unknown denominator | gap stays unresolved | T20 | no,feasibility unknown |
Zero remaining design gaps with neither handling nor test. All runtime proofs pending; this is not a claim of secure or reliable implementation.

### NOT in scope / What already exists
Deferred CRM sync remains the sole TODO; no new deferred expansion. Shared hosted service, cross-install sync, automatic proposal submission, grants and public SDK remain outside approved boundary. Nationwide sources and calibrated confidence remain in scope. Existing research scripts/output are intact; use only permitted attributable samples. Standard SQLite/FTS/OS keyring/HTTP libraries are reuse targets, native helpers require platform validation. No existing production code rebuilt; diagrams describe future code.

### Engineering dependency and parallelization strategy
| Step | Modules | Depends on |
|---|---|---|
| M0 | source inventory, rights, platform isolation proof | user-approved plan |
| Foundation | app/db,jobs,session,workspaces,types | M0 architecture proof |
| A acquisition | app/sources,documents broker,platform helpers | foundation contracts |
| B experience | app/templates,search,dossier,profile,watch,exports | foundation contracts; fixture adapter |
| C evaluation | evals,permitted labeled fixtures | M0 rights+label protocol |
| Integration | matching,shared schemas,all flows | A+B+C |
| Release | packaging,docs,signed updates | integration/platform/eval/coverage gates |
Parallel lanes A+B+C after foundation. Shared schemas/db changes stay on foundation/integration lane, never concurrent independent migrations. Merge/wait A+B+C before final qualification/release verification.3parallel lanes,3shared sequential stages after M0; worktrees only after repository exists, none created by review. Unknown source access can block affected adapters while offline foundation work proceeds; exhaustive completion cannot be declared.

### Engineering completion summary
Step0 scope accepted as-is (FULL_REVIEW). Architecture7issues; codequality1; test diagram produced20gapgroups; performance1; four-section total29. Native7 concerns are overlapping, not added again. NOT in scope/reuse written; TODO1retained,0new; failure registry17rows,0unmapped silent critical gaps, platform isolation proof is critical implementation gate. Unresolved engineering choices0; inheritedT1andUC1disclosure remain final gate. OutsideClaudeCodeunavailable/nonrepo; nativecompleted. Parallelization3lanes/3parallel/3sharedsequential stages afterM0. LakeScoreN/A,no scored user options. Suppressed findings:none. No tests executed or app code created; QA artifact is proposed verification, not pass evidence.

### Engineering QA artifact
Saved full planned assertions and value cards: /Users/matthewsexton/.gstack/projects/AIProjects/matthewsexton-unknown-eng-review-test-plan-20261015-132343.md
Task JSONL: /Users/matthewsexton/.gstack/projects/AIProjects/tasks-eng-review-20261015-132343.jsonl

### Implementation Tasks: Engineering
- [ ] **E-T1 (P1,human:3days/AI-assisted:1–2days)** — Enforce time and complete evidence revisions. Surfaced by:E1/E2 temporal and correction races. Modules:assessment;exact files future. Verify:corresponding QA matrix groups and native platform runs.
- [ ] **E-T2 (P1,human:5–8days/AI-assisted:3–5days plus OS access)** — Prove parser isolation and package per OS. Surfaced by:E3/E9 security and distribution proof. Modules:platform;exact files future. Verify:corresponding QA matrix groups and native platform runs.
- [ ] **E-T3 (P1,human:3days/AI-assisted:1–2days)** — Implement fenced jobs and transactional watch events. Surfaced by:E4 crash/replay/cancel boundaries. Modules:jobs;exact files future. Verify:corresponding QA matrix groups and native platform runs.
- [ ] **E-T4 (P1,human:3days/AI-assisted:1–2days)** — Build bounded snapshots and transactional FTS. Surfaced by:E5/E8 pagination,WAL,index consistency. Modules:search;exact files future. Verify:corresponding QA matrix groups and native platform runs.
- [ ] **E-T5 (P1,human:3–4days/AI-assisted:2days)** — Implement local bootstrap and acquisition grants. Surfaced by:E6/E7 browser authority and document rights. Modules:security;exact files future. Verify:corresponding QA matrix groups and native platform runs.
- [ ] **E-T6 (P1,human:5–8days plus labels/AI-assisted:3–5days plus labels)** — Implement full QA/eval matrix and recovery benchmark. Surfaced by:E10 twenty gapgroups and platform evidence. Modules:validation;exact files future. Verify:corresponding QA matrix groups and native platform runs.

### Decision Audit Trail (consolidated pre-gate verification)
48 independently tracked choices:47auto-decisions,1provisional taste,0both-model User Challenges. UC1 remains a feasibility concern,not claimed cross-model consensus. Original user-approved deployment/scope is baseline,not counted again.

| ID | Phase | Decision | Classification | Principle | Rationale | Rejected |
|---|---|---|---|---|---|---|
| C1 | CEO | Source setup must distinguish API key, portal account, manual import, licensed feed and optional MCP | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C1 | Unspecified implementation or weaker verification |
| C2 | CEO | Every source coverage claim must carry a versioned publisher inventory denominator, verified/unsupported/unknown counts and a | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C2 | Unspecified implementation or weaker verification |
| C3 | CEO | First-run guided sample uses isolated demo data and persistent Demo label | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C3 | Unspecified implementation or weaker verification |
| C4 | CEO | Search must explain exclusions, and zero results must offer editable filter relaxation suggestions without executing them | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C4 | Unspecified implementation or weaker verification |
| C5 | CEO | Confidence stays disabled by default until the held-out evaluation passes | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C5 | Unspecified implementation or weaker verification |
| C6 | CEO | A document is critical when needed to resolve a mandatory qualification, submission condition, price schedule, statement of w | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C6 | Unspecified implementation or weaker verification |
| C7 | CEO | Calibration uses predeclared equal-width probability bins [0,.1), …, [.9,1] | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C7 | Unspecified implementation or weaker verification |
| C8 | CEO | M0 produces a versioned coverage acceptance matrix for every US state, DC and territory and federal/state/local/nonprofit pub | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C8 | Unspecified implementation or weaker verification |
| C9 | CEO | Section 14.2 is a historical stale confirmation request: the user approved the product boundary and confidence semantics on O | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C9 | Unspecified implementation or weaker verification |
| C10 | CEO | M0 is a feasibility checkpoint owned by the product lead, with an initial 10 working-day research budget (planning assumption | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C10 | Unspecified implementation or weaker verification |
| C11 | CEO | Before M4 development, evaluation owner estimates supported source/sector cohorts, held-out bin sample needs, human labeling  | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C11 | Unspecified implementation or weaker verification |
| C12 | CEO | Before M6 assign a maintainer for every adapter, evaluation release and platform package | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C12 | Unspecified implementation or weaker verification |
| C13 | CEO | Planned document acquisition stages temp files then atomically renames by hash and commits database references through the si | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C13 | Unspecified implementation or weaker verification |
| C14 | CEO | Use typed errors for network timeout/auth/rate-limit/schema, parser/unsupported/limit, citation validation, provider refusal/ | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C14 | Unspecified implementation or weaker verification |
| C15 | CEO | Bound initial work: page size100, query length4,000 chars, 50 terms, document download100MB, extracted archive500MB with 1,00 | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C15 | Unspecified implementation or weaker verification |
| C16 | CEO | Redacted local diagnostics record operation/source/run/job/version IDs, elapsed time, stage, retry count and error code, neve | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C16 | Unspecified implementation or weaker verification |
| C17 | CEO | Duplicate mutations reuse operation IDs; stale forms reject with conflict and preserve drafts; navigation must not silently l | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement C17 | Unspecified implementation or weaker verification |
| D2.1 | Design | Search uses a readable row layout, not metric cards | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.1 | Unspecified implementation or weaker verification |
| D2.2 | Design | Dossier review lists mandatory unresolved requirements first, mandatory resolved second, preferred third | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.2 | Unspecified implementation or weaker verification |
| D2.3 | Design | Always distinguish Publisher status, Current qualification and Your decision | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.3 | Unspecified implementation or weaker verification |
| D2.4 | Design | First use offers Connect a source, Import a solicitation, Try guided sample as three direct actions | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.4 | Unspecified implementation or weaker verification |
| D2.5 | Design | Primary search has query plus location, deadline and notice type | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.5 | Unspecified implementation or weaker verification |
| D2.6 | Design | Search initial loading shows stage and Cancel; no sources shows the three setup choices; success shows count and coverage; ca | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.6 | Unspecified implementation or weaker verification |
| D2.7 | Design | Use distinct terms Closing browser, Stopping service and Computer asleep | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.7 | Unspecified implementation or weaker verification |
| D2.8 | Design | Persistent navigation: Search, Watchlist, Profile, Sources/Coverage, Settings; Watchlist contains pipeline, tasks and changes | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.8 | Unspecified implementation or weaker verification |
| D2.9 | Design | Keyboard-only path must cover query -> filter disclosure -> result -> citation -> recorded review -> export; real table heade | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement D2.9 | Unspecified implementation or weaker verification |
| D2.10 | Design | Provisional visual taste T1 for final gate: office-light reading surface, IBM Plex Sans bundled locally with license, 16px/1. | provisional taste | P6 | Preserve full behavior with explicit gates; see accepted requirement D2.10 | Unspecified implementation or weaker verification |
| X1 | DX | Developer quickstart documents macOS shell and Windows PowerShell from the downloaded source bundle, with pinned tested Pytho | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement X1 | Unspecified implementation or weaker verification |
| X2 | DX | Local API is internal, authenticated, same-version browser/server only | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement X2 | Unspecified implementation or weaker verification |
| X3 | DX | Adapter protocol has describe_capabilities()->SourceCapabilities, fetch_page(window,cursor,cancel_token)->SourcePage, and fet | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement X3 | Unspecified implementation or weaker verification |
| X4 | DX | Shared error envelope contains code, problem, known cause or 'cause unknown', recovery action, bundled help anchor, operation | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement X4 | Unspecified implementation or weaker verification |
| X5 | DX | Documentation ships with the app version: README quickstart, bundled operator guide, developer run/test/architecture guide, a | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement X5 | Unspecified implementation or weaker verification |
| X6 | DX | Typed effective-settings view shows defaults, values, units, scope, restart needs and validation errors with secrets redacted | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement X6 | Unspecified implementation or weaker verification |
| X7 | DX | App releases use semantic versions, schema versions and connector compatibility metadata | auto | P1/P5 | Preserve full behavior with explicit gates; see accepted requirement X7 | Unspecified implementation or weaker verification |
| D1 | CEO | Defer automatic CRM sync | auto | P3 | Outside local approved workflow | Duplicate/new integration |
| S1 | CEO | Skip duplicate compare proposal | auto | P4 | Already in approved spec | Duplicate/new integration |
| S2 | CEO | Skip duplicate confidence provenance proposal | auto | P4 | Already in approved spec | Duplicate/new integration |
| E0 | Eng scope | preserve functional modules/full scope | auto | P2/P5 | separate privileges, no new server infrastructure | monolith file or scope cut |
| E1 | Eng architecture | temporal validity | auto | P1 | revision alone misses expired bid | revision-only cache |
| E2 | Eng architecture | aggregate input revision | auto | P1 | human corrections cannot be overwritten | incomplete CAS |
| E3 | Eng architecture | prove native parser isolation | auto | P1/P5 | process separation is insufficient | unsandboxed fallback as complete |
| E4 | Eng architecture | fenced jobs + transactional events | auto | P1/P5 | retry/crash/sleep recovery | in-memory tasks |
| E5 | Eng performance | bounded materialized results | auto | P1/P5 | stable pages without long read lock | persistent read transaction |
| E6 | Eng architecture | one-use local bootstrap | auto | P1 | reject forged/stale/replayed authority | reusable URL secret |
| E7 | Eng architecture | grants separate from blobs | auto | P1 | equal bytes do not imply equal rights | hash-only authorization |
| E8 | Eng quality | transactional FTS/backup/GC | auto | P1/P5 | consistency and recovery | raw FTS strings/live file copy |
| E9 | Eng architecture | OS build and isolation release gate | auto | P1 | platform evidence before client release | cross-compile assumption |
| E10 | Eng tests | full behavior matrix | auto | P1 | approved requirements need regression proof | smoke-only suite |

### Final pre-gate verification
CEO: eleven sections, named premises, error/rescue/failure registries, reuse/exclusions/dream delta, completion summary and consensus present. Design: all seven passes complete; first six numeric scores5->9,6->9,8->9,4->8,3->8,5->9; seventh unresolved-decisions dimension scored8/10 for review completeness (nine structural issues resolved,T1pending), supplemental plan score only. No rendered visual verification because image generation had no configured key. DX:eight scores,journey,empathy,benchmark/TTHW,checklist,consensus present. Engineering: fresh source read,scope challenge,architecture and20group coverage diagrams,QA artifact/value cards,17failure paths,reuse/exclusions,completion summary and consensus present. Native terminal results verified for every phase;outside unavailable for each. Two independent CEO spec reviews8->9 completed. All accepted behaviors retained in implementation projection; review-only appendices do not change that projection. Engineering is last substantive review.
Cross-phase themes: coverage/access truthfulness(CEO/Eng),confidence distinct from qualification(CEO/Design/Eng),revision and time freshness(CEO/Design/Eng),recoverable local operation(CEO/DX/Eng),minimal useful onboarding(CEO/Design/DX),client context and rights(Design/Eng).
No substantive scope reductions. M0 feasibility and isolation proof precede related commitments; inaccessible sources and unvalidated confidence remain required work. All scores assess plan completeness only. Final approval,then review-log persistence and end-of-skill bookkeeping remain pending under driver. No build,test execution,purchase,publishing or external message has occurred.

### Aggregated implementation tasks
Saved17tasks:/Volumes/AI Projects/RFP Empire/specs/bid-discovery/IMPLEMENTATION-TASKS.md. Standard Git-window aggregation unavailable/nonrepo; exact current-run fallback manifest checked. No task dropped.

### Final approval record
User answer: “A — Approve as-is (recommended)” to the final autoplan gate. The complete amended implementation plan is APPROVED. T1 light reading interface is accepted. UC1 is acknowledged as an unresolved implementation feasibility risk; the nationwide requirement remains intact and has not been reduced. No further product or architecture choice is pending from this review. Source permissions, calibration evidence, platform isolation, signing and tested installers remain implementation/release gates, not completed work.
Approval changes disposition only; the reviewed implementation projection and all C/D2/X/E obligations remain byte-for-byte unchanged. No rerun required for this unchanged choice. The 17 aggregated tasks and engineering QA artifact remain the approved build handoff. No application code has been created or tests executed in this planning workflow.
Status: DONE_WITH_CONCERNS. All four planning reviews completed with native reviewers; outside Claude Code coverage unavailable in every phase because this is not a Git repository. No cross-model agreement claimed. Design rendering and real onboarding timings remain unverified. Engineering issues_open means mapped implementation/test obligations, not rejected user approval or proof of shipping readiness.

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|---|---|---|---|---|---|
| CEO | /autoplan | Scope and feasibility | 1 | APPROVED; implementation risks retained | 6 native concerns; no scope reduction |
| Design | /autoplan | UI and accessibility | 1 | APPROVED | 9 native issues mapped; plan score 8/10; T1 accepted |
| DX | /autoplan | Setup and maintenance | 1 | APPROVED | 6 native issues mapped; plan score 8.25/10; timings unmeasured |
| Engineering | /autoplan | Architecture and tests | 1 | ISSUES OPEN; plan APPROVED | 7 native findings; 29 section issues/test-gap groups mapped; 0 unmapped silent gaps |
| Outside | Claude Code | Independent provider review | 4 phases attempted/unavailable | UNAVAILABLE | Nonrepo guard; no completed external review |

OUTSIDE COVERAGE: Codex host; native CEO/design/DX/engineering completed, respectively 6/9/6/7 findings. Claude Code unavailable in every phase; all have partial voice coverage. Cross-model consensus N/A.
VERDICT: User approved the full amended implementation plan. Autoplan complete with concerns. This is planning approval, not a clean implementation review or release authorization. Run /ship after implementation and required checks, when ready for a PR.
NO UNRESOLVED DECISIONS

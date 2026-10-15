# Bid discovery: source and product research

Research date: October 15, 2026. Status: requirements research, not connector certification. Public documentation was inspected; no customer account, paid subscription, authenticated feed, or exhaustive nationwide crawl was tested.

## Findings that change the product

1. The user wants purchasable work: federal, state, municipal and nonprofit solicitations. Nonprofit directories and grant applications are different record types. Neither can be counted as open bids.
2. Nationwide is the target geographic scope. No source inspected establishes exhaustive access to every US bid. The product must show which publishers, documents, dates and jurisdictions are actually covered. It must never convert missing coverage into “no opportunities.”
3. Search relevance, ability to meet requirements, document completeness and estimated probability of a useful match are different measurements. They need separate labels and evidence. A high relevance score cannot remove a mandatory qualification failure.
4. A downloadable Python program can launch a browser interface locally. The user confirmed local Windows/macOS installations, each opening in the browser, on October 15, 2026.
5. Existing RFP Empire scripts provide useful source samples, but their fixed-date product filtering and historical competition ranking do not implement the requested qualification system.

## Source access matrix

“Documented” means the linked primary source supports the access description. It does not mean this application has a working connector. No MCP requirement was found in the documentation inspected. An MCP server would be an optional wrapper, not a substitute for permission, credentials or a data license.

| Source | Role and documented access | Credentials/cost/rights | Implementation disposition |
|---|---|---|---|
| [SAM public Opportunities API](https://open.gsa.gov/api/get-opportunities-public-api/) | Federal notices; filters include NAICS, classification, dates, organization and set-aside. Description and attachment links are separate from the listing. | Public API key required; role-dependent request limits. | Primary federal connector. Handle pagination and date-window limits. Verify current source status and attachments before qualification. |
| [DLA DIBBS](https://www.dla.mil/Acquisition/) | DLA supply RFQs, search/view and secure quoting. | Public information and secured actions differ; technical-data access must be tested separately. | Federal coverage candidate, not assumed included by SAM. Discovery/document adapter only; no quote submission. |
| [SBA SUBNet](https://www.sba.gov/counseling/prime-and-subcontracting/) | Prime contractors publish subcontracting opportunities. | Public listings; automated retrieval route not verified here. | Separate subcontracting record type and coverage row. |
| [NASPO state directory](https://www.naspo.org/states/) | Starting point for procurement offices and state profiles. | Public directory, not a national live-bid feed. | Build the 50-state, DC and territory source inventory from verified publisher links. |
| [California Cal eProcure](https://www.dgs.ca.gov/en/PD/Resources/Page-Content/Procurement-Division-Resources-List-Folder/Cal-eProcure-Portal-to-Access-Bid-Opportunities) | State opportunities in the California State Contracts Register. | API, document permissions and automation access not established by this page. | Direct state adapter feasibility probe; visible manual fallback until verified. |
| [Texas procurement resources](https://comptroller.texas.gov/purchasing/publications/) and [NIGP guide](https://comptroller.texas.gov/purchasing/nigp/nigp-code-help-guide.pdf) | Procurement publications/downloads and commodity-code search guidance. | No nationwide API established; taxonomy permissions separate from portal viewing. | Texas source discovery and classification compatibility. Verify active ESBD endpoints during adapter implementation. |
| [NYC PASSPort](https://www.nyc.gov/site/mocs/passport/about-passport.page) | Procurement Navigator and PASSPort Public can be browsed without an account; response requires a PASSPort account. | Browsing access does not establish bulk API or unrestricted attachment access. | Municipal adapter feasibility probe; preserve publisher link and login-required states. |
| [BidNet participating buyers](https://www.bidnetdirect.com/participating-buyers/changePage?innerTabId=private&isListView=false&purchasingGroupContext=true) | Agencies publish through participating purchasing groups. | API, subscriptions, document rights and client distribution need verification. | Portal-family candidate, not a promised free national feed. |
| [DemandStar / Euna supplier registration](https://openbids-help.eunasolutions.com/hc/en-us/articles/48369406019219-How-to-Register-as-a-Supplier-Vendor-with-Euna-OpenBids-Demandstar) | Supplier registration and subscription selection. | Access differs by agency/subscription. Automated ingestion and reuse remain unverified. | Portal-family candidate; source-specific account/access status. |
| [OpenGov API catalog](https://developer.opengov.com/catalog/public-service-platform-procurement-contract-management) | APIs describe records from a customer's OpenGov account. | Account API availability is not evidence of a public nationwide solicitation feed. | Do not infer supplier-wide API access. Probe public publisher pages separately. |
| [HigherGov API](https://docs.highergov.com/import-and-export/highergov-api.md) | Documented consolidated API; opportunity records can lead to document downloads. | Subscription/API key. Documentation currently lists 10,000 records/month; custom volume pricing. Download URLs expire. | Candidate only, blocked for this product pending written rights suitable for client-facing use. |
| [HigherGov terms](https://www.highergov.com/tos/) | Standard terms restrict sharing, scraping, and competing services. | An ordinary subscription does not establish permission to power this client app. | Do not purchase, trial, scrape or activate on the assumption that API access grants redistribution rights. A negotiated agreement or another permitted feed is needed. |
| [American Red Cross suppliers](https://www.redcross.org/about-us/supplier-partnership-program.html) | Example of a nonprofit's own supplier program. | This page alone does not establish a complete public RFP feed. | Nonprofit publisher discovery; verify each actual solicitation source. |
| [USAspending API](https://api.usaspending.gov/docs/) | Historical federal spending and awards. | Public API documentation; endpoint quotas and data freshness must be tested. | Award context only, never evidence that an open solicitation exists. |
| [IRS EO master file](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf) | Nonprofit organization records. | Public downloads. | Optional publisher enrichment, not procurement opportunity coverage. |
| [Grants.gov APIs](https://www.grants.gov/api/applicant) | Grant opportunities. | Operation-specific API access. | Separate future grant mode; exclude from default bid search. |

## Classification and search research

[Census NAICS](https://www.census.gov/naics/) publishes industry definitions, historical editions and revision information. Store code system and edition together. Support exact codes and explicit descendant search; never silently rewrite old codes to a newer edition.

SAM supports NAICS and classification codes. State/local sources may use NIGP and other source-specific commodity systems. [NIGP's own documentation](https://support.nigp.com/hc/en-us/articles/115000077032-NIGP-Code-Structure-and-Subscriptions) describes hierarchy and subscriptions. Preserve codes appearing in a permitted record; require appropriate rights before bundling a full proprietary taxonomy or crosswalk. Suggested mappings are search aids, not proof of eligibility.

Recommended search controls: exact phrases; all/any/excluded terms; agency; publisher type; posted/updated/deadline ranges; place of performance; remote/on-site; industry and commodity codes; notice type; contract value if published; set-asides; registration/contract-vehicle restrictions; mandatory attendance; bonding/insurance/licenses; delivery capacity; prime/subcontract status; evidence completeness; freshness; known blockers. Unknown values remain selectable instead of being silently discarded.

## What a usable bid dossier needs

The following is a product synthesis from the different source fields and the user's qualification goal, not a claim that every publisher exposes these fields:

- Original solicitation identifier, publisher, original URL, status, last successful retrieval and revision history.
- Statement of work, deliverables, quantities, units, locations, contract term and delivery milestones.
- Bid due date/time/timezone, question cutoff, mandatory site visits/conferences, submission portal and instructions.
- Published budget/ceiling/estimate, with those amount types kept distinct; missing values stay unknown.
- Mandatory registrations, certifications, licenses, insurance, bonds, experience, staffing, clearances, approved sources and contract vehicles when specified.
- Evaluation factors and weights when stated; required forms, signatures, attachments and acknowledgements.
- Amendment history, changed requirements, contradictions, unread documents and access restrictions.
- Requirement-by-requirement comparison against the chosen client profile, with document/page/section evidence.
- Bid/no-bid notes, ownership, tasks, saved searches, alerts and exportable source-linked evidence.

## Confidence research and recommendation

[Scikit-learn's calibration documentation](https://scikit-learn.org/stable/modules/calibration.html) describes checking whether predicted probabilities agree with observed outcomes. This supports evaluating a confidence percentage on held-out human-reviewed matches; it does not supply a ready-made procurement confidence model.

Start with an explained 0–100 match score and separate evidence/eligibility indicators. Build the labeled evaluation set and calibrated probability feature into the delivery plan. Until validated for the relevant source and sector, show “confidence not validated” rather than an invented percentage. The predicted event is that a reviewer finds a result relevant and worth qualification for this profile/query, never winning the contract or being legally eligible.

## Desktop/browser delivery research

[FastAPI deployment guidance](https://fastapi.tiangolo.com/deployment/concepts/) supports the Python web-service route. The proposed local product launches that service on loopback and opens the default browser. Background document work must not block search.

[PyInstaller documentation](https://pyinstaller.org/en/stable/usage.html) requires platform-specific packaging work for distributing on multiple operating systems. A successful macOS run is not Windows verification. The delivery plan needs Windows and macOS installer, update, uninstall and data-preservation checks.

## Verified reuse inventory

| Existing file | Evidence | Reuse decision |
|---|---|---|
| `../../tools/federal_pull.py:11` | Fixed October 16, 2026 cutoff. | Reference only; replace fixed date with runtime filters. |
| `../../tools/federal_pull.py:32` | Iterates numeric product groups; uses website search route. | Do not copy as all-sector federal coverage; use documented adapter and completeness tests. |
| `../../tools/federal_pull.py:41` | Caps each group at 100 pages. | New connector must report incomplete traversal and resume. |
| `../../tools/federal_pull.py:73` | Keeps only first 600 characters of description. | Cannot support full requirement extraction; retain complete source documents. |
| `../../tools/federal_rank2.py:7` | Restriction keyword pattern and fixed due-date cutoff. | Reuse terms as test cases, not authoritative eligibility rules. |
| `../../tools/federal_rank2.py:11` | Drops opportunities without 30 historical competed awards. | Do not apply to match search; history availability must not exclude an otherwise useful bid. |
| `../../tools/federal_rank2.py:23` | Sorts historical low-competition percentage. | Keep separate from relevance/confidence and future win predictions. |
| `../../tools/nyc_bidders.py` | Text regex for historical vendor counts. | Candidate historical fixtures after provenance verification; not live opportunity discovery. |
| `../../tools/parse_nassau.py` | HTML table-to-CSV script. | Candidate input sample and parser test material, not certified adapter. |

No application server, client account system, persistent search schema or qualification test suite was found in the inspected RFP Empire files. Existing research files were not executed or changed.

## Outstanding evidence

- Actual provider credentials, allowed quotas and any paid-feed agreement.
- A publisher inventory and measured recall covering the nationwide target, not just a few example portals.
- Representative nonprofit procurement sources, verified separately from grants.
- Permission and working fetch tests for each adapter and document host.
- Representative client capability profiles and adjudicated bid matches for calibration.
- Windows/macOS release environments and signing credentials.

These are recorded dependencies, not implied approvals or completed integrations.

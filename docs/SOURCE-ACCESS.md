# Source access investigation

Checked October 15, 2026. Documentation research and a limited unauthenticated SAM probe; no paid accounts, credentials, source downloads or source connectors were activated. Public documentation is evidence of an offered interface, not proof of ingestion rights or successful retrieval.

| Source | Verified route | Requirements and current disposition |
|---|---|---|
| Federal — SAM.gov | [Official opportunities API documentation](https://open.gsa.gov/api/get-opportunities-public-api/) | API key required. Role-dependent request limits. First candidate for an official API adapter; live contract and attachment checks still outstanding. No MCP required by this API. |
| State — California | [DGS Cal eProcure entry point](https://www.dgs.ca.gov/PD/Resources/Page-Content/Procurement-Division-Resources-List-Folder/Cal-eProcure-Portal-to-Access-Bid-Opportunities) | Public State Contracts Register discovery. No supported bulk API or automated attachment/reuse rights established by this investigation. Manual source link only. |
| State — Texas | [ESBD portal](https://www.txsmartbuy.gov/esbd), [official procurement guidance](https://spdedu.cpa.texas.gov/wp-content/uploads/2022/02/Advertising-Procurments-inTexas-.pdf) | Public solicitation browsing. API access, rate limits, amendment parity and attachment rights remain unverified. A third-party scraper listing is not an official access agreement. |
| Municipal — New York City | [Official PASSPort overview](https://www.nyc.gov/site/mocs/passport/about-passport.page) | Public opportunity browsing; vendor account needed for participation/response. Separate document access, automation and redistribution checks remain. No mandatory MCP identified. |
| Nonprofit — Urban Institute | [Vendor RFP page](https://www.urban.org/projects/request-proposals-award-lifecycle-assessment), [linked RFP PDF](https://www.urban.org/sites/default/files/2024-03/Award%20Lifecycle%20RFP.pdf) | Historical 2024 procurement example for award-lifecycle assessment, demonstrating an actual nonprofit vendor RFP rather than grant discovery. Not an active bid or a general nonprofit feed. No app ingestion performed. |
| Cross-source — HigherGov | [MCP offering](https://www.highergov.com/gov-mcp/), [terms](https://www.highergov.com/tos/) | Optional MCP endpoint advertised at `https://www.highergov.com/mcp/`. Standard terms include restrictions on scraping, programmatic access, sharing and competing services. Blocked pending applicable written commercial rights; no subscription purchased. |
| Discovery — NASPO | [State procurement directory](https://www.naspo.org/states/) | Useful inventory seed. Not a bid feed and not evidence of local/nonprofit completeness. |

## SAM adapter contract to implement next

Based on the [official API documentation](https://open.gsa.gov/api/get-opportunities-public-api/):

- Production endpoint: `https://api.sam.gov/opportunities/v2/search`.
- `api_key` is required. Never log request query strings containing it. A future settings flow must store it in the OS credential store; do not put it in chat, repository files or exports.
- `postedFrom` and `postedTo` are required, use `MM/dd/yyyy`, and permit at most a one-year window. Date windows must be checkpointed and resumable.
- `offset` is a **page index**, not a record offset. `limit` defaults to 1 and permits up to 1,000. Page-count and total-record consistency must be tested against live responses before certification.
- `ncode` selects NAICS and `ccode` selects classification/PSC. Do not reuse the old project script’s numeric-only PSC loop as nationwide coverage. `state` concerns place of performance, not necessarily the buying office’s address.
- Opportunity types distinguish solicitations/combined notices from awards and other informational records. Do not present an award as an open bid.
- The documented feed returns the latest active version, with active data refreshed daily and archived data weekly. Preserve local immutable observations; do not imply that the API supplies a complete historical amendment ledger.
- Description retrieval and resource links are separate from listing discovery. A successful listing search does not prove access to every attachment or the complete bid package.
- Do not invent support for an updated-since or status filter where the documentation does not establish it. Reconciliation and freshness require explicit, tested policy.

One bounded GET without a key, using a valid-looking date window and limit 1, returned **HTTP 404 with an empty body** from this environment. This is an inconclusive probe, not a successful API contract test and not proof of the API’s expected authentication-error behavior. The requirement for a key comes from the documentation. A keyed test must check success, paging, descriptions, attachments, rate limiting and source parity.

## Coverage and permission gates

The app contains 57 jurisdiction placeholders: 50 states, DC, five inhabited territories and UM. Those are not 57 working sources. The municipal and nonprofit publisher universe has not been enumerated; the federal feed also does not establish all subthreshold or agency-local opportunities. Nationwide coverage remains required work under the approved plan.

Before activating each connector, record the publisher and canonical URL, supported access mechanism, permission/licensing basis, login or API requirements, permitted storage/export scope, rate limits, pagination, stable identity, deadline/timezone semantics, cancellation/amendment behavior, expected attachment manifest and inaccessible-document states. Compare sampled normalized results with the publisher and retain redacted contract fixtures.

M0 is **not passed**: no keyed SAM sample or permitted automated state/local/nonprofit acquisition is certified; cross-platform isolated PDF/OCR execution is also not proven. Text-only imports allow the foundation to operate while those prerequisites are resolved. Unknown access and missing documents must remain visible and must never produce a high-confidence qualification.

The original [research](planning/RESEARCH.md) and [approved implementation plan](planning/PLAN.md) remain the broader product scope. This investigation does not authorize a source integration or reduce that scope.

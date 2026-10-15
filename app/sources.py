"""Access findings are not connector certification. No network access at startup."""
from datetime import timedelta
from .store import now

SOURCES = [
    dict(id='sam', name='SAM.gov', kind='Federal', access='API key required', status='Not connected', url='https://open.gsa.gov/api/get-opportunities-public-api/', mcp='Not required', detail='Documented public API. Date windows and pagination required; descriptions and attachments are separate. Latest active version only. A key and live contract checks are still needed.'),
    dict(id='nyc', name='NYC PASSPort', kind='Local', access='Public browsing / portal account to respond', status='Manual source', url='https://www.nyc.gov/site/mocs/passport/about-passport.page', mcp='Not established / not needed for browsing', detail='Browse publicly. Bulk automation, document retrieval and reuse rights have not been certified.'),
    dict(id='ca', name='California Cal eProcure', kind='State', access='Public portal', status='Manual source', url='https://www.dgs.ca.gov/PD/Resources/Page-Content/Procurement-Division-Resources-List-Folder/Cal-eProcure-Portal-to-Access-Bid-Opportunities', mcp='No requirement found', detail='State Contracts Register discovery. Public API and document automation remain unverified.'),
    dict(id='tx', name='Texas ESBD', kind='State', access='Public browsing', status='Manual source', url='https://www.txsmartbuy.gov/esbd', mcp='No requirement found', detail='Public solicitation search. No bulk connector activated; attachments, amendment parity and rights need verification.'),
    dict(id='urban', name='Urban Institute', kind='Nonprofit', access='Publisher page and linked RFP', status='Historical example', url='https://www.urban.org/projects/request-proposals-award-lifecycle-assessment', mcp='Not required for public page', detail='A real vendor procurement example, not a grant or live nationwide feed. The linked 2024 RFP is historical; never label it an open bid.'),
    dict(id='highergov', name='HigherGov', kind='Federal / state / local', access='Negotiated data rights + paid access', status='Blocked: licensing', url='https://www.highergov.com/tos/', mcp='Optional: https://www.highergov.com/mcp/', detail='Standard terms restrict competing services and sharing. Do not activate API/MCP without applicable written rights. No account or purchase made.'),
    dict(id='naspo', name='NASPO state directory', kind='Discovery directory', access='Public directory', status='Inventory aid only', url='https://www.naspo.org/states/', mcp='Not required', detail='Starting point for state procurement offices. Not a live bid feed and not evidence of municipal or nonprofit coverage.'),
]
JURISDICTIONS = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC AS GU MP PR VI UM'.split()


def seed_demo(store, wid):
    """Synthetic, explicitly labeled fixtures use the same ingest path as imports."""
    specs = [
        ('demo-federal','Federal building janitorial services','Example Federal Office','Federal','NY','561720','active',21,
         'SYNTHETIC DEMO — not a real solicitation.\nProvide janitorial cleaning for a federal office building.\nProof of general liability insurance is required.\nA mandatory site visit must be attended before submitting.\nSubmit the price schedule and acknowledge every amendment.'),
        ('demo-state','Facilities cleaning and floor care','Example State Purchasing Office','State','CA','561720','active',14,
         'SYNTHETIC DEMO — not a real solicitation.\nProvide cleaning and floor care at two public facilities.\nContractor must hold applicable local licenses.\nStaffing and insurance documentation must accompany the bid.'),
        ('demo-local','Municipal website accessibility review','Example City','Local','NY','541519','active',None,
         'SYNTHETIC DEMO — not a real solicitation.\nAudit the municipal website for accessibility barriers.\nInclude keyboard and screen reader testing.\nThe submission deadline and complete attachment list are not supplied.'),
        ('demo-nonprofit','Nonprofit procurement process assessment','Example Community Organization','Nonprofit',None,None,'active',30,
         'SYNTHETIC DEMO — not a real solicitation.\nAssess purchasing processes and recommend improvements.\nProvide two examples of comparable nonprofit work.\nThe complete document package has not been verified.'),
        ('demo-cancelled','Cancelled custodial contract','Example City Facilities','Local','NY','561720','cancelled',10,
         'SYNTHETIC DEMO — not a real solicitation.\nJanitorial and custodial cleaning services.\nThis solicitation has been cancelled. Do not prepare a bid.'),
    ]
    with store.db() as db:
        existing=db.execute('SELECT count(*) FROM notices WHERE workspace=?',(wid,)).fetchone()[0]
    if existing:
        return
    profile=store.profile(wid)
    store.save_profile(wid,profile['id'],dict(company='Demo Facilities Company',capabilities='Janitorial cleaning and floor care',states='NY',naics='561720'))
    for key,title,publisher,kind,state,naics,status,days,text in specs:
        store.ingest(wid,dict(source_key=key,title=title,publisher=publisher,kind=kind,state=state,naics=naics,naics_edition='2022',status=status,due=(now()+timedelta(days=days)).isoformat() if days else None,url='',origin='Synthetic demo',package_complete=False),text)

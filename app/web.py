from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import csv
import io
import secrets
import sqlite3
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError, field_validator

from .store import Store, Problem, now
from .sources import SOURCES, JURISDICTIONS, seed_demo

ROOT=Path(__file__).parent


class ImportRecord(BaseModel):
    source_key: str = Field(min_length=1,max_length=160)
    title: str = Field(min_length=1,max_length=250)
    publisher: str = Field(min_length=1,max_length=200)
    kind: str
    state: str = Field(max_length=2)
    naics: str = Field(max_length=6)
    due: str = Field(max_length=40)
    url: str = Field(max_length=2000)
    text: str = Field(min_length=1,max_length=20000)
    rights: str
    status: str = 'active'

    @field_validator('kind')
    @classmethod
    def kind_valid(cls,v):
        if v not in ('Federal','State','Local','Nonprofit'): raise ValueError('Select a publisher type.')
        return v

    @field_validator('state')
    @classmethod
    def state_valid(cls,v):
        v=v.upper()
        if v and v not in JURISDICTIONS: raise ValueError('Use a US state or territory code.')
        return v

    @field_validator('naics')
    @classmethod
    def naics_valid(cls,v):
        if v and (not v.isascii() or not v.isdigit() or not 2<=len(v)<=6): raise ValueError('NAICS must contain 2–6 digits.')
        return v

    @field_validator('due')
    @classmethod
    def due_valid(cls,v):
        if not v: return v
        d=datetime.fromisoformat(v)
        if d.tzinfo is None: raise ValueError('Include a timezone offset, for example 2026-12-01T17:00:00-05:00, or leave unknown.')
        return d.astimezone(timezone.utc).isoformat()

    @field_validator('url')
    @classmethod
    def url_valid(cls,v):
        if not v: return v
        parsed=urlsplit(v)
        if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password: raise ValueError('Use a public HTTP(S) source link without credentials.')
        return v

    @field_validator('rights')
    @classmethod
    def rights_valid(cls,v):
        if v!='on': raise ValueError('Confirm permission to store and export this text.')
        return v

    @field_validator('status')
    @classmethod
    def status_valid(cls,v):
        if v not in ('active','cancelled'): raise ValueError('Select active or cancelled.')
        return v


def create_app(data_dir, origin, demo=False):
    app=FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
    store=Store(Path(data_dir)/'rfp.sqlite3')
    spaces=store.workspaces()
    if not spaces:
        store.create_workspace('My company')
    if demo and not any(w['demo'] for w in store.workspaces()):
        wid=store.create_workspace('Demo workspace',True)
        seed_demo(store,wid)
    app.state.store=store
    app.state.origin=origin
    app.state.sessions={}
    app.state.bootstrap={}
    app.state.stop=lambda:None
    template=Jinja2Templates(directory=ROOT/'templates')
    app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')

    def token():
        for old,expiry in list(app.state.bootstrap.items()):
            if expiry<time.monotonic(): app.state.bootstrap.pop(old,None)
        key=secrets.token_urlsafe(32)
        app.state.bootstrap[key]=time.monotonic()+60
        return key
    app.state.new_bootstrap=token

    def error(request,code,message,status):
        if request.url.path.startswith('/api/'):
            return JSONResponse(dict(code=code,problem=message,cause='See problem description',recovery='Correct the input or reload the current screen.',help='/settings',operation_id=str(uuid.uuid4())),status_code=status)
        return template.TemplateResponse(request=request,name='page.html',context=dict(page='error',error=message,code=code,workspace=None,spaces=[],csrf='',origin=origin),status_code=status)

    @app.middleware('http')
    async def local_boundary(request,call_next):
        if request.headers.get('host') != urlsplit(origin).netloc:
            return error(request,'HOST_REJECTED','Open the app using its desktop launcher.',403)
        if request.headers.get('origin') not in (None,origin):
            return error(request,'ORIGIN_REJECTED','Requests from other websites are not allowed.',403)
        if request.headers.get('sec-fetch-site')=='cross-site':
            return error(request,'ORIGIN_REJECTED','Open the app from its launcher.',403)
        public=request.url.path in ('/','/healthz','/api/bootstrap') or request.url.path.startswith('/static/')
        session=app.state.sessions.get(request.cookies.get('rfp_session',''))
        if session and time.monotonic()>session['expires']:
            session=None
        if not public and not session:
            return error(request,'SESSION_EXPIRED','Launch RFP Empire again to open a new local session.',401)
        request.state.session=session
        if request.method not in ('GET','HEAD','OPTIONS'):
            if request.headers.get('origin')!=origin:
                return error(request,'ORIGIN_REQUIRED','Reload the local app before saving.',403)
            body=bytearray()
            async for chunk in request.stream():
                body.extend(chunk)
                if len(body)>100000:
                    return error(request,'INPUT_LIMIT','This foundation accepts at most 20,000 characters of source text. Use a smaller excerpt.',413)
            request._body=bytes(body)
            if request.url.path!='/api/bootstrap':
                data=parse_qs(request._body.decode('utf-8',errors='replace'))
                supplied=request.headers.get('x-csrf-token') or data.get('csrf',[''])[0]
                if not session or not secrets.compare_digest(supplied,session['csrf']):
                    return error(request,'CSRF_REJECTED','Reload the local app before saving.',403)
                workspace_id=request.headers.get('x-workspace-id') or data.get('workspace_id',[''])[0]
                if request.url.path!='/workspace' and workspace_id!=session['workspace']:
                    return error(request,'WORKSPACE_CHANGED','The selected client changed in another tab. Reload before saving; copy your edits first.',409)
        response=await call_next(request)
        response.headers.update({'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'; form-action 'self'; base-uri 'none'",'Referrer-Policy':'same-origin','X-Content-Type-Options':'nosniff','Cache-Control':'no-store'})
        return response

    @app.exception_handler(Problem)
    async def handle_problem(request,exc): return error(request,exc.code,exc.message,exc.status)

    @app.exception_handler(sqlite3.Error)
    async def handle_storage(request,exc): return error(request,'STORAGE_ERROR','Storage could not complete this operation. Check free disk space and retry; existing committed data is retained.',503)

    @app.exception_handler(RequestValidationError)
    async def handle_validation(request,exc): return error(request,'INPUT_INVALID','Check the input fields and try again.',422)

    def ctx(request,page,**extra):
        session=request.state.session
        spaces=store.workspaces()
        workspace=next((w for w in spaces if w['id']==session['workspace']),None)
        return dict(page=page,workspace=workspace,spaces=spaces,csrf=session['csrf'],profile=store.profile(workspace['id']),origin=origin,**extra)

    def render(request,page,status_code=200,**extra):
        return template.TemplateResponse(request=request,name='page.html',context=ctx(request,page,**extra),status_code=status_code)

    async def form(request):
        try:body=(await request.body()).decode('utf-8')
        except UnicodeDecodeError:raise Problem('INPUT_INVALID','Form data must be valid UTF-8 text.',422)
        return {k:v[-1].strip() for k,v in parse_qs(body,keep_blank_values=True).items()}

    def bounded(value,label,limit=200,required=True):
        if (required and not value.strip()) or len(value)>limit:
            raise Problem('INPUT_INVALID',f'{label} must contain '+('1–' if required else 'at most ')+f'{limit} characters.',422)
        return value.strip()

    @app.get('/healthz')
    def health():return {'ready':True}

    @app.get('/')
    def home(request:Request):
        if request.state.session and request.query_params.get('launch')!='1':return RedirectResponse('/search',303)
        return template.TemplateResponse(request=request,name='page.html',context=dict(page='bootstrap',workspace=None,spaces=[],csrf='',origin=origin))

    @app.post('/api/bootstrap')
    async def bootstrap(request:Request):
        try:data=await request.json()
        except ValueError:raise Problem('INPUT_INVALID','Invalid sign-in request.',422)
        key=data.get('token') if isinstance(data,dict) else None
        if not isinstance(key,str):raise Problem('TOKEN_INVALID','Launch the app again.',401)
        expiry=app.state.bootstrap.pop(key,0)
        if time.monotonic()>expiry:raise Problem('TOKEN_EXPIRED','The one-use launch link expired. Launch the app again.',401)
        spaces=store.workspaces()
        wid=next((w['id'] for w in spaces if w['demo']),spaces[0]['id']) if demo else next(w['id'] for w in spaces if not w['demo'])
        if request.state.session:wid=request.state.session['workspace']
        sid=secrets.token_urlsafe(32)
        app.state.sessions[sid]=dict(workspace=wid,csrf=secrets.token_urlsafe(32),expires=time.monotonic()+8*3600)
        response=JSONResponse({'next':'/search'})
        response.set_cookie('rfp_session',sid,httponly=True,samesite='strict',max_age=8*3600)
        return response

    @app.post('/workspace')
    async def workspace(request:Request):
        f=await form(request)
        if f.get('name'):
            wid=store.create_workspace(bounded(f['name'],'Workspace name',100))
        else:
            wid=f.get('workspace')
            if wid not in [w['id'] for w in store.workspaces()]:raise Problem('NOT_FOUND','Workspace not found.',404)
        request.state.session['workspace']=wid
        return RedirectResponse('/search',303)

    @app.get('/search')
    def search(request:Request):
        query=dict(request.query_params)
        if not query: query={'unknowns':'on','open':'on'}
        for name in ('q','any','exclude'):
            bounded(query.get(name,''),name,4000,False)
        if query.get('state') and query['state'] not in JURISDICTIONS: raise Problem('INPUT_INVALID','Choose a valid state.',422)
        if query.get('kind') and query['kind'] not in ('Federal','State','Local','Nonprofit'):raise Problem('INPUT_INVALID','Choose a valid publisher type.',422)
        if query.get('sort') and query['sort'] not in ('deadline','newest'):raise Problem('INPUT_INVALID','Choose deadline or newest order.',422)
        if query.get('naics') and (not query['naics'].isascii() or not query['naics'].isdigit() or not 2<=len(query['naics'])<=6):raise Problem('INPUT_INVALID','NAICS must have 2–6 digits.',422)
        if query.get('due_before'):
            try:datetime.strptime(query['due_before'],'%Y-%m-%d')
            except ValueError:raise Problem('INPUT_INVALID','Use a valid deadline date.',422)
        rows,sid,partial=store.search(request.state.session['workspace'],query)
        return render(request,'search',query=query,rows=rows,snapshot=sid,partial=partial,states=JURISDICTIONS)

    @app.get('/profile')
    def profile(request:Request):return render(request,'profile',saved=request.query_params.get('saved'))

    @app.post('/profile')
    async def save_profile(request:Request):
        f=await form(request)
        data={k:bounded(f.get(k,''),k,limit,k=='company') for k,limit in [('company',200),('capabilities',4000),('states',200),('naics',200)]}
        store.save_profile(request.state.session['workspace'],f.get('revision'),data)
        return RedirectResponse('/profile?saved=1',303)

    @app.get('/import')
    def import_page(request:Request):return render(request,'import',fields={},errors=[],states=JURISDICTIONS)

    @app.post('/import')
    async def import_text(request:Request):
        fields=await form(request)
        try:r=ImportRecord.model_validate(fields)
        except ValidationError as e:
            return render(request,'import',status_code=422,fields=fields,errors=[str(x['loc'][0])+': '+x['msg'] for x in e.errors(include_input=False)],states=JURISDICTIONS)
        record=r.model_dump(exclude={'text','rights'})
        record.update(due=r.due or None,state=r.state or None,naics=r.naics or None,naics_edition='unspecified',origin='Operator text import',package_complete=False)
        nid=store.ingest(request.state.session['workspace'],record,r.text)
        return RedirectResponse('/opportunities/'+nid,303)

    @app.get('/opportunities/{nid}')
    def dossier(request:Request,nid:str):
        wid=request.state.session['workspace']
        row=store.notice(wid,nid)
        return render(request,'dossier',row=row,assessment=store.assessment(wid,row),lines=row['text'].splitlines(),history=store.history(wid,nid))

    @app.post('/opportunities/{nid}/review')
    async def review(request:Request,nid:str):
        f=await form(request)
        try:start,end=int(f.get('start','')),int(f.get('end',''))
        except ValueError:raise Problem('CITATION_INVALID','Enter valid line numbers.',422)
        if f.get('status') not in ('met','not_met','unknown','conflict'):raise Problem('INPUT_INVALID','Select a review status.',422)
        store.review(request.state.session['workspace'],nid,f.get('version'),f.get('profile'),start,end,f['status'],bounded(f.get('reason',''),'Review reason',2000))
        return RedirectResponse('/opportunities/'+nid,303)

    @app.post('/opportunities/{nid}/decision')
    async def decision(request:Request,nid:str):
        f=await form(request)
        if f.get('decision') not in ('Reviewing','Bid','No bid'):raise Problem('INPUT_INVALID','Select a decision.',422)
        store.decide(request.state.session['workspace'],nid,f.get('version'),f.get('profile'),f['decision'],bounded(f.get('reason',''),'Decision reason',2000))
        return RedirectResponse('/opportunities/'+nid,303)

    @app.post('/opportunities/{nid}/watch')
    def watch(request:Request,nid:str):
        store.watch(request.state.session['workspace'],nid)
        return RedirectResponse('/watchlist',303)

    @app.get('/watchlist')
    def watchlist(request:Request):return render(request,'watchlist',rows=store.watchlist(request.state.session['workspace']))

    @app.get('/sources')
    def sources(request:Request):return render(request,'sources',sources=SOURCES,jurisdictions=JURISDICTIONS)

    @app.get('/settings')
    def settings(request:Request):return render(request,'settings',storage=str(store.path.parent),backup=request.query_params.get('backup'))

    @app.post('/settings/clear')
    def clear(request:Request):
        store.clear_snapshots(request.state.session['workspace'])
        return RedirectResponse('/search',303)

    @app.post('/settings/backup')
    def backup(request:Request):return RedirectResponse('/settings?backup='+store.backup(),303)

    @app.post('/settings/stop')
    def stop(request:Request):
        app.state.stop()
        return HTMLResponse('<h1>Local service stopping</h1><p>Launch RFP Empire to reopen it. Closing the browser alone does not stop the service.</p>')

    @app.get('/exports/{sid}.csv')
    def export(request:Request,sid:str):
        wid=request.state.session['workspace']
        snap=store.snapshot(wid,sid)
        output=io.StringIO(newline='')
        writer=csv.writer(output)
        writer.writerow(['Client','Title','Publisher','Type','State','NAICS','Deadline UTC','Qualification at search','Current qualification','Evidence version','Snapshot time','Profile revision','Confidence','Source link','Snapshot status'])
        client=next(w['name'] for w in store.workspaces() if w['id']==wid)
        for r in snap['rows']:
            current=store.notice(wid,r['id'])
            a=store.assessment(wid,current)
            current_status=a['qualification']
            if current['version']!=r['version'] or store.profile(wid)['id']!=snap['profile']:
                current_status='Changed since search; '+current_status
            cells=[client,r['title'],r['publisher'],r['kind'],r['state'] or 'Unknown',r['naics'] or 'Unknown',r['due'] or 'Unknown',r['qualification'],current_status,r['version'],snap['as_of'],snap['profile'],'Not validated',r['url'],'Partial' if snap['partial'] else 'Local snapshot only; nationwide coverage unknown']
            writer.writerow(["'"+str(c) if str(c).lstrip().startswith(('=','+','-','@','\t','\r','\n')) else c for c in cells])
        return Response(output.getvalue(),media_type='text/csv; charset=utf-8',headers={'Content-Disposition':'attachment; filename="rfp-search.csv"'})

    @app.get('/api/opportunities/{nid}')
    def opportunity_api(request:Request,nid:str):
        wid=request.state.session['workspace']; row=store.notice(wid,nid)
        return row | store.assessment(wid,row)

    @app.get('/api/sources')
    def source_api():return dict(sources=SOURCES,connected=0,inventory_complete=False)

    return app

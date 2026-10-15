"""SQLite owns persistence; all private records belong to a workspace."""
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import shlex
import sqlite3
import threading
import uuid


def uid():
    return str(uuid.uuid4())


def now():
    return datetime.now(timezone.utc)


def stamp():
    return now().isoformat()


class Problem(Exception):
    def __init__(self, code, message, status=400):
        self.code, self.message, self.status = code, message, status


def terms(value):
    if len(value) > 4000:
        raise Problem('QUERY_LIMIT', 'Use at most 4,000 characters.', 422)
    try:
        result = shlex.split(value)
    except ValueError:
        raise Problem('QUERY_INVALID', 'Close each quoted phrase, then search again.', 422)
    if len(result) > 50:
        raise Problem('QUERY_LIMIT', 'Use at most 50 terms.', 422)
    if any(not re.search(r'\w', t) for t in result):
        raise Problem('QUERY_INVALID', 'Each search term must contain a letter or number. No filters were relaxed.', 422)
    return result


def fts_query(value, join=' AND '):
    return join.join('"' + t.replace('"', '""') + '"' for t in terms(value))


SCHEMA = '''
CREATE TABLE IF NOT EXISTS workspaces(id TEXT PRIMARY KEY,name TEXT NOT NULL,demo INTEGER NOT NULL CHECK(demo IN(0,1)));
CREATE TABLE IF NOT EXISTS profiles(id TEXT PRIMARY KEY,workspace TEXT NOT NULL REFERENCES workspaces(id),data TEXT NOT NULL,created TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS profile_workspace ON profiles(workspace,created);
CREATE TABLE IF NOT EXISTS notices(id TEXT PRIMARY KEY,workspace TEXT NOT NULL REFERENCES workspaces(id),source_key TEXT NOT NULL,current_version TEXT,UNIQUE(workspace,source_key));
CREATE TABLE IF NOT EXISTS versions(id TEXT PRIMARY KEY,notice TEXT NOT NULL REFERENCES notices(id),hash TEXT NOT NULL,data TEXT NOT NULL,text TEXT NOT NULL,created TEXT NOT NULL,UNIQUE(notice,hash));
CREATE VIRTUAL TABLE IF NOT EXISTS evidence_fts USING fts5(version UNINDEXED,title,text);
CREATE TABLE IF NOT EXISTS reviews(id TEXT PRIMARY KEY,workspace TEXT NOT NULL REFERENCES workspaces(id),version TEXT NOT NULL REFERENCES versions(id),profile TEXT NOT NULL REFERENCES profiles(id),line_start INTEGER NOT NULL,line_end INTEGER NOT NULL,status TEXT NOT NULL CHECK(status IN('met','not_met','unknown','conflict')),reason TEXT NOT NULL,created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS watches(workspace TEXT NOT NULL REFERENCES workspaces(id),notice TEXT NOT NULL REFERENCES notices(id),PRIMARY KEY(workspace,notice));
CREATE TABLE IF NOT EXISTS decisions(id TEXT PRIMARY KEY,workspace TEXT NOT NULL REFERENCES workspaces(id),notice TEXT NOT NULL REFERENCES notices(id),version TEXT NOT NULL REFERENCES versions(id),profile TEXT NOT NULL REFERENCES profiles(id),decision TEXT NOT NULL CHECK(decision IN('Reviewing','Bid','No bid')),reason TEXT NOT NULL,created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS snapshots(id TEXT PRIMARY KEY,workspace TEXT NOT NULL REFERENCES workspaces(id),profile TEXT NOT NULL REFERENCES profiles(id),data TEXT NOT NULL,created REAL NOT NULL);
CREATE INDEX IF NOT EXISTS snapshot_workspace ON snapshots(workspace,created);
'''


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        with self.db() as db:
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version not in (0, 1):
                raise Problem('SCHEMA_NEWER', 'This database needs a newer app. Do not downgrade.', 409)
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript(SCHEMA)
            db.execute('PRAGMA user_version=1')

    @contextmanager
    def db(self):
        # ponytail: serialize this local foundation; separate readers after load measurements.
        with self.lock:
            db = sqlite3.connect(self.path, timeout=5)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA foreign_keys=ON')
            try:
                with db:
                    yield db
            finally:
                db.close()

    def workspaces(self):
        with self.db() as db:
            return [dict(r) for r in db.execute('SELECT * FROM workspaces ORDER BY name')]

    def create_workspace(self, name, demo=False):
        wid = uid()
        with self.db() as db:
            db.execute('INSERT INTO workspaces VALUES(?,?,?)', (wid, name, int(demo)))
            self._profile(db, wid, dict(company=name, capabilities='', states='', naics=''))
        return wid

    def _profile(self, db, wid, data):
        pid = uid()
        db.execute('INSERT INTO profiles VALUES(?,?,?,?)', (pid, wid, json.dumps(data), stamp()))
        return pid

    def profile(self, wid):
        with self.db() as db:
            r = db.execute('SELECT * FROM profiles WHERE workspace=? ORDER BY rowid DESC LIMIT 1', (wid,)).fetchone()
            if not r:
                raise Problem('NOT_FOUND', 'Select an existing client workspace.', 404)
            return dict(id=r['id'], **json.loads(r['data']))

    def save_profile(self, wid, expected, data):
        with self.db() as db:
            current = self.profile(wid)
            if current['id'] != expected:
                raise Problem('REVISION_CONFLICT', 'The profile changed in another tab. Reload before saving; copy your edits first.', 409)
            return self._profile(db, wid, data)

    def ingest(self, wid, record, text):
        """Same path for synthetic fixtures and operator-provided plain text. No binary parsing."""
        self.profile(wid)
        data = json.dumps(record, sort_keys=True)
        digest = hashlib.sha256((data + '\n' + text).encode()).hexdigest()
        with self.db() as db:
            r = db.execute('SELECT id FROM notices WHERE workspace=? AND source_key=?', (wid, record['source_key'])).fetchone()
            nid = r['id'] if r else uid()
            if not r:
                db.execute('INSERT INTO notices VALUES(?,?,?,NULL)', (nid, wid, record['source_key']))
            old = db.execute('SELECT id FROM versions WHERE notice=? AND hash=?', (nid, digest)).fetchone()
            if old:
                # A replay of an old version must not undo a newer amendment.
                return nid
            vid = uid()
            db.execute('INSERT INTO versions VALUES(?,?,?,?,?,?)', (vid, nid, digest, data, text, stamp()))
            db.execute('INSERT INTO evidence_fts VALUES(?,?,?)', (vid, record['title'], text))
            db.execute('UPDATE notices SET current_version=? WHERE id=?', (vid, nid))
        return nid

    def notice(self, wid, nid, version=None):
        with self.db() as db:
            r = db.execute('''SELECT n.id,n.workspace,n.current_version,v.id version,v.hash,v.data,v.text,v.created
              FROM notices n JOIN versions v ON v.notice=n.id AND v.id=COALESCE(?,n.current_version)
              WHERE n.id=? AND n.workspace=?''', (version, nid, wid)).fetchone()
            if not r:
                raise Problem('NOT_FOUND', 'This opportunity is not in the selected workspace.', 404)
            return dict(r) | json.loads(r['data'])

    def assessment(self, wid, row, profile=None, at=None):
        profile = profile or self.profile(wid)
        at = at or now()
        reasons = ['Full document package and mandatory qualification have not been verified.']
        state = 'Needs review'
        if row['status'] == 'cancelled':
            state, reasons = 'Blocked', ['Publisher status recorded as cancelled.']
        due = row.get('due')
        if due and datetime.fromisoformat(due) <= at:
            state, reasons = 'Blocked', ['The recorded deadline has passed.']
        if not due:
            reasons.append('Deadline is unknown.')
        with self.db() as db:
            checks = [dict(r) for r in db.execute('SELECT * FROM reviews WHERE workspace=? AND version=? AND profile=? ORDER BY rowid', (wid, row['version'], profile['id']))]
        # Human notes are evidence review, never automatic certification of the full package.
        if any(r['status'] == 'not_met' for r in checks):
            state, reasons = 'Blocked', ['A reviewed requirement is marked not met.']
        counts = dict(met=0, not_met=0, unknown=0, conflict=0)
        for check in checks:
            counts[check['status']] += 1
        return dict(qualification=state, reasons=reasons, match_score=None,
                    match_confidence_percent=None, confidence_status='Confidence not yet validated',
                    fit_status='Fit scoring not implemented in this foundation', reviews=checks,
                    review_counts=counts, profile_revision=profile['id'], evaluated_at=at.isoformat())

    def search(self, wid, query):
        with self.lock:
            clauses, args = ['n.workspace=?'], [wid]
            for field, join, exclude in [('q',' AND ',False),('any',' OR ',False),('exclude',' OR ',True)]:
                expression = fts_query(query.get(field, ''), join)
                if expression:
                    clauses.append('v.id '+('NOT IN' if exclude else 'IN')+' (SELECT version FROM evidence_fts WHERE evidence_fts MATCH ?)')
                    args.append(expression)
            include_unknowns = query.get('unknowns') == 'on'
            for field in ['state','kind','naics']:
                value = query.get(field, '').strip()
                if value:
                    column = "json_extract(v.data,'$."+field+"')"
                    if field == 'naics' and query.get('descendants') == 'on':
                        match = column + ' LIKE ?'
                        value += '%'
                    else:
                        match = column + '=?'
                    if include_unknowns:
                        match = '('+match+' OR '+column+" IS NULL OR "+column+"='')"
                    clauses.append(match)
                    args.append(value)
            with self.db() as db:
                rows = db.execute('''SELECT n.id,v.id version,v.data,v.text,v.hash,v.created,n.current_version
                  FROM notices n JOIN versions v ON v.id=n.current_version WHERE '''+' AND '.join(clauses)+' ORDER BY n.id LIMIT 1001', args).fetchall()
            result = []
            profile = self.profile(wid)
            for r in rows:
                item = dict(r) | json.loads(r['data'])
                item.update(self.assessment(wid, item, profile))
                if query.get('open') == 'on' and item['qualification'] == 'Blocked':
                    continue
                if query.get('due_before'):
                    if not item.get('due') and not include_unknowns:
                        continue
                    if item.get('due') and item['due'][:10] > query['due_before']:
                        continue
                item['uncertain'] = any(query.get(f) and not item.get(f) for f in ('state','kind','naics')) or bool(query.get('due_before') and not item.get('due'))
                result.append(item)
            result.sort(key=lambda r: ((r.get('due') or '9999'),r['id']) if query.get('sort')=='deadline' else (r['created'],r['id']), reverse=query.get('sort')!='deadline')
            partial = len(rows) > 1000
            result = result[:1000]
            sid = uid()
            snapshot = dict(query=query, rows=[dict(id=r['id'],version=r['version'],title=r['title'],publisher=r['publisher'],kind=r['kind'],state=r['state'],naics=r['naics'],due=r['due'],qualification=r['qualification'],url=r['url']) for r in result],partial=partial,as_of=stamp())
            with self.db() as db:
                db.execute('DELETE FROM snapshots WHERE created<?', (now().timestamp()-1800,))
                count = db.execute('SELECT count(*) FROM snapshots WHERE workspace=?',(wid,)).fetchone()[0]
                if count >= 10:
                    raise Problem('SNAPSHOT_LIMIT','Ten searches are retained for 30 minutes. Clear snapshots in Settings or wait before searching again.',409)
                db.execute('INSERT INTO snapshots VALUES(?,?,?,?,?)', (sid,wid,profile['id'],json.dumps(snapshot),now().timestamp()))
            return result, sid, partial

    def snapshot(self, wid, sid):
        with self.db() as db:
            r = db.execute('SELECT * FROM snapshots WHERE id=? AND workspace=?',(sid,wid)).fetchone()
        if not r or now().timestamp()-r['created']>1800:
            raise Problem('CURSOR_EXPIRED','This search snapshot expired. Run the search again.',409)
        return json.loads(r['data']) | dict(profile=r['profile'])

    def review(self, wid, nid, version, profile, start, end, status, reason):
        with self.lock:
            row = self.notice(wid,nid)
            if row['version'] != version or self.profile(wid)['id'] != profile:
                raise Problem('REVISION_CONFLICT','The profile or solicitation changed. Reload before recording review.',409)
            if not 1 <= start <= end <= len(row['text'].splitlines()):
                raise Problem('CITATION_INVALID','Select valid source line numbers.',422)
            with self.db() as db:
                db.execute('INSERT INTO reviews VALUES(?,?,?,?,?,?,?,?,?)',(uid(),wid,version,profile,start,end,status,reason,stamp()))

    def watch(self,wid,nid):
        self.notice(wid,nid)
        with self.db() as db:
            db.execute('INSERT OR IGNORE INTO watches VALUES(?,?)',(wid,nid))

    def watchlist(self,wid):
        with self.db() as db:
            ids=[r[0] for r in db.execute('SELECT notice FROM watches WHERE workspace=?',(wid,))]
        return [self.notice(wid,nid) for nid in ids]

    def decide(self,wid,nid,version,profile,decision,reason):
        with self.lock:
            row=self.notice(wid,nid)
            if row['version'] != version or self.profile(wid)['id'] != profile:
                raise Problem('REVISION_CONFLICT','Reload the current dossier before saving a decision.',409)
            with self.db() as db:
                db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?,?,?)',(uid(),wid,nid,version,profile,decision,reason,stamp()))

    def history(self,wid,nid):
        self.notice(wid,nid)
        with self.db() as db:
            return [dict(r) for r in db.execute('SELECT * FROM decisions WHERE workspace=? AND notice=? ORDER BY rowid DESC',(wid,nid))]

    def clear_snapshots(self,wid):
        with self.db() as db:
            db.execute('DELETE FROM snapshots WHERE workspace=?',(wid,))

    def backup(self):
        with self.db() as db:
            name='backup-'+now().strftime('%Y%m%d-%H%M%S')+'-'+uid()[:8]+'.sqlite3'
            target=self.path.parent/name
            with sqlite3.connect(target) as dest:
                db.backup(dest)
                if dest.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
                    raise Problem('BACKUP_FAILED','Backup integrity check failed. Original data is unchanged.',500)
            return name

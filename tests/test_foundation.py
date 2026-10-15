import csv
from datetime import timedelta
import io
import sqlite3
import time

from fastapi.testclient import TestClient
import pytest

from app.store import Problem, Store, now
from app.web import create_app

ORIGIN = 'http://127.0.0.1:8765'


@pytest.fixture
def local(tmp_path):
    app = create_app(tmp_path, ORIGIN, demo=True)
    client = TestClient(app, base_url=ORIGIN)
    token = app.state.new_bootstrap()
    response = client.post('/api/bootstrap', json={'token': token}, headers={'Origin': ORIGIN})
    assert response.status_code == 200
    session = app.state.sessions[client.cookies['rfp_session']]
    yield app, client, session
    client.close()


def post(local, path, **data):
    app, client, session = local
    return client.post(path, data={'csrf': session['csrf'], 'workspace_id': session['workspace'], **data}, headers={'Origin': ORIGIN}, follow_redirects=False)


def record(**changes):
    return dict(source_key='test:001', title='Janitorial cleaning', publisher='Test publisher', kind='Local', state='NY', naics='561720', naics_edition='2022', status='active', due=(now()+timedelta(days=10)).isoformat(), url='https://example.org/bid', origin='Test fixture', package_complete=False) | changes


def first(local):
    app, _, session = local
    store = app.state.store
    with store.db() as db:
        nid = db.execute('SELECT id FROM notices WHERE workspace=? AND source_key=?', (session['workspace'], 'demo-federal')).fetchone()[0]
    return store.notice(session['workspace'], nid)


def test_launch_token_one_use_expiry_and_restart(local, tmp_path):
    app, client, _ = local
    token = app.state.new_bootstrap()
    assert client.post('/api/bootstrap', json={'token': token}, headers={'Origin': ORIGIN}).status_code == 200
    assert client.post('/api/bootstrap', json={'token': token}, headers={'Origin': ORIGIN}).status_code == 401
    token = app.state.new_bootstrap()
    app.state.bootstrap[token] = time.monotonic()-1
    assert client.post('/api/bootstrap', json={'token': token}, headers={'Origin': ORIGIN}).status_code == 401
    restarted = TestClient(create_app(tmp_path, ORIGIN), base_url=ORIGIN, cookies=client.cookies)
    assert restarted.get('/api/sources').status_code == 401


@pytest.mark.parametrize('headers', [{'Host': 'evil.example'}, {'Origin': 'https://evil.example'}, {'Sec-Fetch-Site': 'cross-site'}])
def test_local_boundary(local, headers):
    assert local[1].get('/search', headers=headers).status_code == 403


def test_csrf_body_limit_and_security_headers(local):
    app, client, session = local
    assert client.post('/settings/backup', headers={'Origin': ORIGIN}).status_code == 403
    assert client.post('/settings/backup', data={'csrf': session['csrf']}).status_code == 403
    assert client.post('/import', content=b'x'*100001, headers={'Origin': ORIGIN}).status_code == 413
    response = client.get('/profile')
    assert "frame-ancestors 'none'" in response.headers['content-security-policy']
    assert response.headers['cache-control'] == 'no-store'
    assert response.headers['referrer-policy'] == 'same-origin'
    assert client.post('/import', content=b'text=\xff', headers={'Origin': ORIGIN, 'x-csrf-token': session['csrf'], 'x-workspace-id': session['workspace']}).status_code == 422
    assert client.get('/search', params={'kind':'Made up'}).status_code == 422
    assert client.get('/search', params={'sort':'Made up'}).status_code == 422


def test_search_phrases_exclusions_and_code_descendants(local):
    app, _, session = local
    store = app.state.store
    rows, _, _ = store.search(session['workspace'], {'q': 'cleaning', 'naics': '561', 'descendants': 'on', 'exclude': 'cancelled', 'open': 'on'})
    assert {r['source_key'] for r in rows} == {'demo-federal', 'demo-state'}
    rows, _, _ = store.search(session['workspace'], {'q': '"floor care"'})
    assert [r['source_key'] for r in rows] == ['demo-state']
    rows, _, _ = store.search(session['workspace'], {'naics': '561'})
    assert rows == []
    rows, _, _ = store.search(session['workspace'], {'q': 'cleaning OR accessibility'})
    assert rows == []  # OR is a literal term; user input cannot become an FTS operator.
    rows, _, _ = store.search(session['workspace'], {'any': 'accessibility custodial', 'open': 'on'})
    assert [r['source_key'] for r in rows] == ['demo-local']


@pytest.mark.parametrize('query', ['"unclosed', '***', 'a '*51])
def test_invalid_query_never_silently_relaxes(local, query):
    assert local[1].get('/search', params={'q': query}).status_code == 422


def test_unknown_filter_group_and_no_fake_confidence(local):
    app, _, session = local
    rows, _, _ = app.state.store.search(session['workspace'], {'state': 'NY', 'unknowns': 'on', 'open': 'on'})
    assert [r['source_key'] for r in rows if r['uncertain']] == ['demo-nonprofit']
    assert all(r['match_confidence_percent'] is None and r['match_score'] is None for r in rows)
    assert all(r['qualification'] == 'Needs review' for r in rows)


def test_immutable_ingest_replay_cannot_revert_amendment(local):
    app, _, session = local
    store, wid = app.state.store, session['workspace']
    nid = store.ingest(wid, record(), 'Original scope\nInsurance required')
    original = store.notice(wid, nid)
    assert store.ingest(wid, record(due=original['due']), original['text']) == nid
    amended = record(due=original['due'], title='Amended scope')
    store.ingest(wid, amended, 'Amended evidence')
    current = store.notice(wid, nid)
    store.ingest(wid, record(due=original['due']), original['text'])
    assert store.notice(wid, nid)['version'] == current['version']
    assert store.notice(wid, nid, original['version'])['text'] == original['text']
    with store.db() as db:
        assert db.execute('SELECT count(*) FROM versions WHERE notice=?', (nid,)).fetchone()[0] == 2
    rows, _, _ = store.search(wid, {'q': '"Original scope"'})
    assert rows == []  # Historical FTS rows must not appear as current results.


def test_reviews_pin_versions_and_bid_decision_does_not_remove_blocker(local):
    app, client, session = local
    row = first(local)
    profile = app.state.store.profile(session['workspace'])
    data = dict(version=row['version'], profile=profile['id'], start=3, end=3, status='not_met', reason='Insurance is not held.')
    assert post(local, '/opportunities/'+row['id']+'/review', **data).status_code == 303
    assert post(local, '/opportunities/'+row['id']+'/decision', version=row['version'], profile=profile['id'], decision='Bid', reason='Management review').status_code == 303
    response = client.get('/api/opportunities/'+row['id']).json()
    assert response['qualification'] == 'Blocked'
    assert response['reviews'][0]['line_start'] == 3
    assert post(local, '/profile', revision=profile['id'], company='Changed company', capabilities='', states='', naics='').status_code == 303
    response = client.get('/api/opportunities/'+row['id']).json()
    assert response['reviews'] == []
    assert response['qualification'] == 'Needs review'
    assert post(local, '/opportunities/'+row['id']+'/review', **data).status_code == 409
    assert post(local, '/profile', revision=profile['id'], company='Stale company').status_code == 409


def test_expired_deadline_and_invalid_citation(local):
    app, _, session = local
    row = first(local)
    store, wid = app.state.store, session['workspace']
    assert store.assessment(wid, row, at=now()+timedelta(days=100))['qualification'] == 'Blocked'
    with pytest.raises(Problem) as caught:
        store.review(wid, row['id'], row['version'], store.profile(wid)['id'], 0, 1000, 'met', 'Invalid excerpt')
    assert caught.value.code == 'CITATION_INVALID'


def test_workspace_boundary_and_stale_tab_import(local):
    app, client, session = local
    row = first(local)
    original_wid = session['workspace']
    _, sid, _ = app.state.store.search(original_wid, {})
    assert post(local, '/workspace', name='Client B').status_code == 303
    assert session['workspace'] != original_wid
    assert client.get('/api/opportunities/'+row['id']).status_code == 404
    assert client.get('/exports/'+sid+'.csv').status_code == 409
    assert post(local, '/opportunities/'+row['id']+'/watch').status_code == 404
    assert post(local, '/import', workspace_id=original_wid).status_code == 409
    assert app.state.store.watchlist(session['workspace']) == []
    assert '0 local results' in client.get('/search').text


def test_text_import_validation_html_escape_and_snapshot_export(local):
    app, client, session = local
    fields = dict(source_key='manual:1', title='=dangerous()', publisher='<script>alert(1)</script>', kind='Local', state='NY', naics='561720', due='', url='https://example.org/bid', text='<script>alert(2)</script>\nInsurance required', rights='on', status='active')
    response = post(local, '/import', **fields)
    assert response.status_code == 303
    dossier = client.get(response.headers['location'])
    assert '<script>alert(' not in dossier.text
    assert '&lt;script&gt;alert(2)&lt;/script&gt;' in dossier.text
    rows, sid, _ = app.state.store.search(session['workspace'], {'q': 'dangerous'})
    assert len(rows) == 1
    assert post(local, '/import', **(fields | {'title': 'Amended title'})).status_code == 303
    exported = list(csv.reader(io.StringIO(client.get('/exports/'+sid+'.csv').text)))
    assert exported[1][1] == "'=dangerous()"
    assert exported[1][8].startswith('Changed since search;')
    assert exported[1][12] == 'Not validated'
    for change in [{'url': 'javascript:alert(1)'}, {'due': '2026-12-01T12:00:00'}, {'rights': ''}, {'text': 'x'*20001}]:
        invalid = post(local, '/import', **(fields | change))
        assert invalid.status_code == 422 and 'Check these fields:' in invalid.text


def test_snapshot_expiry_limit_and_persistence(local, tmp_path):
    app, _, session = local
    store, wid = app.state.store, session['workspace']
    _, sid, _ = store.search(wid, {})
    with store.db() as db:
        db.execute('UPDATE snapshots SET created=0 WHERE id=?', (sid,))
    with pytest.raises(Problem) as caught:
        store.snapshot(wid, sid)
    assert caught.value.code == 'CURSOR_EXPIRED'
    for _ in range(10):
        store.search(wid, {})
    with pytest.raises(Problem) as caught:
        store.search(wid, {})
    assert caught.value.code == 'SNAPSHOT_LIMIT'
    store.clear_snapshots(wid)
    store.search(wid, {})
    restored = Store(tmp_path/'rfp.sqlite3')
    assert restored.profile(wid) == store.profile(wid)
    assert restored.notice(wid, first(local)['id'])['hash'] == first(local)['hash']


def test_backup_is_consistent_and_includes_evidence(local, tmp_path):
    app, client, session = local
    row = first(local)
    assert post(local, '/opportunities/'+row['id']+'/watch').status_code == 303
    assert 'Federal building janitorial' in client.get('/watchlist').text
    name = app.state.store.backup()
    with sqlite3.connect(tmp_path/name) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert db.execute('SELECT count(*) FROM versions').fetchone()[0] == 5
        assert db.execute('SELECT count(*) FROM watches').fetchone()[0] == 1


def test_sources_are_honest_about_access(local):
    data = local[1].get('/api/sources').json()
    assert data['connected'] == 0 and data['inventory_complete'] is False
    assert next(s for s in data['sources'] if s['id'] == 'sam')['access'] == 'API key required'
    assert 'Blocked' in next(s for s in data['sources'] if s['id'] == 'highergov')['status']

"""A real browser checks the operator workflow against a temporary local service."""
from pathlib import Path
import subprocess
import sys
import time
from multiprocessing import AuthenticationError
from multiprocessing.connection import Client
import json

import pytest

from playwright.sync_api import sync_playwright, expect

from app.__main__ import request_launch


def test_browser_workflow_and_launcher(tmp_path):
    directory = tmp_path/'demo'
    process = subprocess.Popen([sys.executable, '-m', 'app', '--demo', '--no-browser', '--data-dir', str(tmp_path)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    try:
        for _ in range(100):
            if (directory/'runtime.json').exists():
                break
            assert process.poll() is None, process.stderr.read()
            time.sleep(0.1)
        else:
            raise AssertionError('Launcher did not become ready within 10 seconds')
        url = request_launch(directory)
        info = json.loads((directory/'runtime.json').read_text())
        with pytest.raises(AuthenticationError):
            Client(info['address'], family=info['family'], authkey=b'wrong key')
        repeated = subprocess.run([sys.executable, '-m', 'app', '--demo', '--no-browser', '--data-dir', str(tmp_path)], capture_output=True, text=True, timeout=10)
        assert repeated.returncode == 0 and 'already running' in repeated.stdout
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1440, 'height': 1100})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(url)
            expect(page.get_by_role('heading', name='Search opportunities')).to_be_visible()
            assert '#token=' not in page.url
            expect(page.get_by_role('heading', name='4 local results')).to_be_visible()
            old_cookie = page.context.cookies()[0]['value']
            page.goto(request_launch(directory))
            expect(page.get_by_role('heading', name='Search opportunities')).to_be_visible()
            assert '#token=' not in page.url
            assert page.context.cookies()[0]['value'] != old_cookie
            page.get_by_label('All terms or exact phrases').fill('janitorial')
            page.get_by_role('button', name='Search local records').click()
            expect(page.get_by_role('heading', name='1 local result', exact=True)).to_be_visible()
            with page.expect_download() as download:
                page.get_by_role('link', name='Export this snapshot (CSV)').click()
            assert 'Federal building janitorial' in Path(download.value.path()).read_text()
            page.get_by_role('link', name='Federal building janitorial services').click()
            expect(page.get_by_role('heading', name='Source evidence')).to_be_visible()
            page.get_by_label('From line').fill('3')
            page.get_by_label('To line').fill('3')
            page.get_by_label('Requirement review', exact=True).select_option('not_met')
            page.get_by_label('Reason and supporting company evidence').fill('Insurance evidence is missing.')
            page.get_by_role('button', name='Record cited review').click()
            expect(page.locator('.notice .status')).to_have_text('Blocked')
            page.get_by_label('Decision', exact=True).select_option('Bid')
            page.get_by_label('Reason', exact=True).fill('Owner reviewing the blocker.')
            page.get_by_role('button', name='Save decision for Demo workspace').click()
            expect(page.locator('.notice .status')).to_have_text('Blocked')
            page.get_by_role('button', name='Add to watchlist').click()
            expect(page.get_by_role('link', name='Federal building janitorial services')).to_be_visible()
            page.get_by_role('link', name='Profile', exact=True).click()
            page.get_by_label('Company name', exact=True).fill('Updated demo company')
            page.get_by_role('button', name='Save new revision').click()
            expect(page.get_by_role('status')).to_have_text('New profile revision saved.')
            page.get_by_text('New client', exact=True).click()
            page.get_by_label('Client name', exact=True).fill('Browser Test Client')
            page.get_by_role('button', name='Create empty workspace').click()
            expect(page.get_by_role('heading', name='0 local results')).to_be_visible()
            page.get_by_role('link', name='Import solicitation text').click()
            page.get_by_label('Solicitation identifier').fill('test:browser')
            page.get_by_label('Title', exact=True).fill('Browser test procurement')
            page.get_by_label('Publisher', exact=True).fill('Test nonprofit')
            page.get_by_label('Publisher type').select_option('Nonprofit')
            page.get_by_label('Source text').fill('A permitted test excerpt.\nInsurance evidence is required.')
            page.get_by_label('I have permission').check()
            page.get_by_role('button', name='Import and open evidence').click()
            expect(page.get_by_role('heading', name='Browser test procurement')).to_be_visible()
            page.get_by_role('link', name='Sources / Coverage').click()
            expect(page.get_by_role('heading', name='Sources and coverage')).to_be_visible()
            page.get_by_role('link', name='Settings', exact=True).click()
            page.get_by_role('button', name='Save verified database backup').click()
            expect(page.get_by_role('status')).to_contain_text('Backup saved')
            assert len(list(directory.glob('backup-*.sqlite3'))) == 1
            page.set_viewport_size({'width': 390, 'height': 844})
            page.get_by_role('link', name='Search', exact=True).click()
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
            assert errors == []
            page.get_by_role('link', name='Settings', exact=True).click()
            page.get_by_role('button', name='Stop local service').click()
            expect(page.get_by_role('heading', name='Local service stopping')).to_be_visible()
            browser.close()
        assert process.wait(timeout=10) == 0
        assert not (directory/'runtime.json').exists()
        assert not (tmp_path/'rfp.sqlite3').exists()  # Demo must not create a real-data database.
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=10)

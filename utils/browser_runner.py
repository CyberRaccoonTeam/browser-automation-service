"""
Browser Runner - Execute browser automation tasks with Playwright
"""
import os
import sys
import json
import base64
import sqlite3
from datetime import datetime
import asyncio

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tasks.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def update_task(task_id, status, result=None, error=None):
    """Update task status and result"""
    conn = get_db()
    now = datetime.utcnow().isoformat()
    
    if status == 'running':
        conn.execute(
            'UPDATE tasks SET status = ?, started_at = ? WHERE id = ?',
            (status, now, task_id)
        )
    elif status in ('completed', 'failed'):
        conn.execute(
            'UPDATE tasks SET status = ?, completed_at = ?, result = ?, error = ? WHERE id = ?',
            (status, now, json.dumps(result) if result else None, error, task_id)
        )
    else:
        conn.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (status, task_id)
        )
    
    conn.commit()
    conn.close()


async def run_task(task_id):
    """Execute a browser automation task"""
    conn = get_db()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if not task:
        return
    
    task_data = dict(task)
    actions = json.loads(task_data['actions']) if task_data['actions'] else []
    url = task_data['url']
    task_type = task_data['type']
    webhook = task_data['webhook']
    
    update_task(task_id, 'running')
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            results = []
            
            # Navigate to URL
            await page.goto(url, wait_until='networkidle')
            results.append({'action': 'navigate', 'url': url, 'status': 'success'})
            
            # Execute actions
            for action in actions:
                action_type = action.get('type')
                
                if action_type == 'wait':
                    selector = action.get('selector')
                    timeout = action.get('timeout', 5000)
                    await page.wait_for_selector(selector, timeout=timeout)
                    results.append({'action': 'wait', 'selector': selector, 'status': 'success'})
                
                elif action_type == 'click':
                    selector = action.get('selector')
                    await page.click(selector)
                    results.append({'action': 'click', 'selector': selector, 'status': 'success'})
                
                elif action_type == 'fill':
                    selector = action.get('selector')
                    value = action.get('value')
                    await page.fill(selector, value)
                    results.append({'action': 'fill', 'selector': selector, 'status': 'success'})
                
                elif action_type == 'screenshot':
                    full_page = action.get('full_page', False)
                    screenshot_bytes = await page.screenshot(full_page=full_page)
                    screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
                    results.append({
                        'action': 'screenshot',
                        'status': 'success',
                        'data': screenshot_b64[:100] + '...',  # Truncated for JSON
                        'size_bytes': len(screenshot_bytes)
                    })
                
                elif action_type == 'extract':
                    selector = action.get('selector')
                    elements = await page.query_selector_all(selector)
                    texts = []
                    for el in elements:
                        text = await el.text_content()
                        texts.append(text.strip() if text else '')
                    results.append({'action': 'extract', 'selector': selector, 'data': texts})
            
            # Default screenshot for screenshot tasks
            if task_type == 'screenshot' and not any(a.get('type') == 'screenshot' for a in actions):
                screenshot_bytes = await page.screenshot(full_page=True)
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
                results.append({
                    'action': 'screenshot',
                    'status': 'success',
                    'size_bytes': len(screenshot_bytes)
                })
            
            await browser.close()
            
            update_task(task_id, 'completed', result={'actions': results})
            
            # Send webhook notification
            if webhook:
                import requests
                try:
                    requests.post(webhook, json={
                        'task_id': task_id,
                        'status': 'completed',
                        'result': {'actions': results}
                    }, timeout=5)
                except:
                    pass
    
    except Exception as e:
        update_task(task_id, 'failed', error=str(e))


def run_task_sync(task_id):
    """Synchronous wrapper for run_task"""
    asyncio.run(run_task(task_id))
"""
Task Routes - Browser automation task management
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Blueprint, jsonify, request
import sqlite3
from datetime import datetime
import uuid
import asyncio
import json

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api')

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tasks.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            url TEXT,
            actions TEXT,
            status TEXT DEFAULT 'pending',
            result TEXT,
            webhook TEXT,
            created_at TEXT,
            started_at TEXT,
            completed_at TEXT,
            error TEXT
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """List all tasks"""
    status = request.args.get('status')
    limit = request.args.get('limit', 50, type=int)
    
    conn = get_db()
    if status:
        tasks = conn.execute(
            'SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?',
            (status, limit)
        ).fetchall()
    else:
        tasks = conn.execute(
            'SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?',
            (limit,)
        ).fetchall()
    conn.close()
    
    return jsonify([dict(t) for t in tasks])


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new browser automation task"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    task_type = data.get('type', 'screenshot')
    url = data.get('url')
    actions = data.get('actions', [])
    webhook = data.get('webhook')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    task_id = str(uuid.uuid4())[:8]
    
    conn = get_db()
    conn.execute(
        'INSERT INTO tasks (id, type, url, actions, webhook, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (task_id, task_type, url, json.dumps(actions), webhook, 'pending', datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    
    # Execute task asynchronously
    from utils.browser_runner import run_task
    asyncio.run(run_task(task_id))
    
    return jsonify({
        'task_id': task_id,
        'status': 'pending',
        'url': url,
        'type': task_type
    }), 201


@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get task status and result"""
    conn = get_db()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    result = dict(task)
    if result.get('actions'):
        result['actions'] = json.loads(result['actions'])
    if result.get('result'):
        try:
            result['result'] = json.loads(result['result'])
        except:
            pass
    
    return jsonify(result)


@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    conn = get_db()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if not task:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task deleted'})
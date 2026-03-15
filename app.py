"""
Browser Automation Service - Scheduled browser tasks via API
Main Flask Application
"""
import os
import asyncio
import uuid
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'tasks.db')
    
    # Register routes
    from routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    
    # Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'Browser Automation Service'})
    
    # Landing page
    @app.route('/landing')
    def landing():
        return render_template('landing.html')
    
    # Home
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Browser Automation Service',
            'version': '1.0.0',
            'endpoints': {
                'tasks': 'GET/POST /api/tasks',
                'task': 'GET/DELETE /api/tasks/<id>',
                'health': 'GET /health'
            }
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5557))
    
    # Send startup notification to Discord
    from utils.discord_notify import notify_startup
    notify_startup(port)
    
    app.run(host='0.0.0.0', port=port, debug=True)
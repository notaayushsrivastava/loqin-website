import hmac
import json
import os
from pathlib import Path
from datetime import datetime

from flask import Flask, abort, jsonify, redirect, render_template, request

# Vercel serves public/ from its CDN. Flask exposes the same directory locally,
# so template asset URLs work the same in development and production.
app = Flask(__name__, static_folder='public', static_url_path='')

INSTALLER_URL = (
    'https://github.com/notaayushsrivastava/Loqin/releases/latest/download/'
    'Install_loqin.exe'
)
NOTIFICATION_FILE = Path(app.static_folder) / 'notification.json'


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/download')
def download():
    return render_template('thank-you.html')


@app.get('/installer')
def installer():
    return redirect(INSTALLER_URL)

@app.get('/privacy')
def privacy():
    return render_template('privacy.html')

@app.get('/license')
def license_page():
    return render_template('license.html')

@app.post('/push-notifications')
def push_notifications():
    payload = request.get_json(silent=True)
    password = payload.get('password') if isinstance(payload, dict) else None
    expected_password = "asjkdhiwuasdiwuahisdbjiwg8u1872y3iqujwe72yqwjbd278etwdb"
    # Return a 404 rather than exposing whether this endpoint exists or why
    # authentication was rejected.
    if (
        not isinstance(password, str)
        or len(expected_password) != len(password)
        or not hmac.compare_digest(password, expected_password)
    ):
        abort(404)

    required_fields = ('title', 'body')
    if not all(field in payload for field in required_fields):
        return jsonify(error='title, and body are required.'), 400

    notification = {field: payload[field] for field in required_fields}
    NOTIFICATION_FILE.write_text(
        json.dumps(notification.update({'created_at':datetime.now().isoformat()}), ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    return jsonify(notification), 200

@app.get('/push-notifications')
def get_notif():
    return jsonify(json.loads(NOTIFICATION_FILE.read_text('utf-8')))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

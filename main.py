import hmac
import json
import os
import re
from pathlib import Path
from datetime import datetime

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

# Vercel serves public/ from its CDN. Flask exposes the same directory locally,
# so template asset URLs work the same in development and production.
app = Flask(__name__, static_folder='public', static_url_path='')

INSTALLER_URL = (
    'https://github.com/notaayushsrivastava/Loqin/releases/latest/download/'
    'Install_Loqin.exe'
)
MAC_OS_INSTALLER_URL = (
    'https://github.com/notaayushsrivastava/Loqin/releases/latest/download/'
    'Install_Loqin_macOS.dmg'
)
NOTIFICATION_FILE = Path(app.static_folder) / 'notification.json'


def detect_client_os(user_agent: str) -> str:
    ua = (user_agent or '').lower()
    if 'android' in ua:
        return 'android'
    if 'mac os x' in ua or 'macintosh' in ua:
        return 'mac'
    if 'windows' in ua:
        return 'windows'
    return 'unknown'


@app.get('/')
def index():
    return render_template(
        'index.html',
        windows_installer_url=INSTALLER_URL,
        mac_installer_url=MAC_OS_INSTALLER_URL,
    )


@app.get('/download')
def download():
    client_os = detect_client_os(request.user_agent.string)
    if client_os == 'android':
        return render_template(
            'android.html',
            windows_installer_url=INSTALLER_URL,
            mac_installer_url=MAC_OS_INSTALLER_URL,
        )

    return render_template(
        'download.html',
        windows_installer_url=INSTALLER_URL,
        mac_installer_url=MAC_OS_INSTALLER_URL,
        client_os=client_os,
    )


@app.get('/download/thanks')
def download_thanks():
    client_os = detect_client_os(request.user_agent.string)
    requested_os = (request.args.get('os') or '').lower()
    selected_os = requested_os if requested_os in ('windows', 'mac') else (client_os if client_os in ('windows', 'mac') else None)

    return render_template(
        'thank-you.html',
        windows_installer_url=INSTALLER_URL,
        mac_installer_url=MAC_OS_INSTALLER_URL,
        selected_os=selected_os,
    )


# Backward-compatibility alias for /thank-you if anyone visited previously
@app.get('/thank-you')
def thank_you_legacy():
    return redirect(url_for('download_thanks', **request.args))


@app.get('/windows')
def windows_guide():
    return render_template(
        'windows.html',
        windows_installer_url=INSTALLER_URL,
        mac_installer_url=MAC_OS_INSTALLER_URL,
    )


@app.get('/macos')
def macos_guide():
    return render_template(
        'macos.html',
        windows_installer_url=INSTALLER_URL,
        mac_installer_url=MAC_OS_INSTALLER_URL,
    )


@app.get('/troubleshooting')
def troubleshooting():
    return render_template('troubleshooting.html')


@app.get('/faq')
def faq():
    return render_template('faq.html')


@app.get('/installer')
def installer():
    forced_os = (request.args.get('os') or '').lower()
    if forced_os == 'mac':
        return redirect(MAC_OS_INSTALLER_URL)
    if forced_os == 'windows':
        return redirect(INSTALLER_URL)

    client_os = detect_client_os(request.user_agent.string)
    if client_os == 'android':
        return redirect('/download')
    if client_os == 'mac':
        return redirect(MAC_OS_INSTALLER_URL)
    return redirect(INSTALLER_URL)


VERSION_PATTERN = re.compile(r'^[0-9A-Za-z\.\-]+$')
ALLOWED_DOWNLOAD_FILES = {
    'Loqin_Store.msi': 'application/x-msi',
    'Loqin_Store.msix': 'application/msix',
    'Install_Loqin_WinGet.exe': 'application/vnd.microsoft.portable-executable',
}


@app.get('/downloads/<version>/Loqin_Store.msi')
@app.get('/downloads/<version>/Loqin_Store.msix')
@app.get('/downloads/<version>/Install_Loqin_WinGet.exe')
def download_versioned_installer(version: str):
    if not VERSION_PATTERN.match(version):
        abort(404)

    filename = request.path.rsplit('/', 1)[-1]
    mimetype = ALLOWED_DOWNLOAD_FILES.get(filename, 'application/octet-stream')

    downloads_dir = Path(app.static_folder) / 'downloads' / version
    file_path = downloads_dir / filename
    if not file_path.is_file():
        abort(404)

    response = send_from_directory(
        downloads_dir,
        filename,
        as_attachment=True,
        mimetype=mimetype,
    )
    response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response


@app.get('/privacy')
def privacy():
    return render_template('privacy.html')


@app.get('/license')
def license_page():
    return render_template('license.html')


@app.get('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt', mimetype='text/plain')


@app.get('/sitemap.xml')
def sitemap_xml():
    return send_from_directory(app.static_folder, 'sitemap.xml', mimetype='application/xml')


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
    notification['created_at'] = datetime.now().isoformat()
    NOTIFICATION_FILE.write_text(
        json.dumps(notification, ensure_ascii=False, indent=2) + '\n',
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

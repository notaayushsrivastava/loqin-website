from flask import Flask, redirect, render_template

# Vercel serves public/ from its CDN. Flask exposes the same directory locally,
# so template asset URLs work the same in development and production.
app = Flask(__name__, static_folder='public', static_url_path='')

INSTALLER_URL = (
    'https://github.com/notaayushsrivastava/Loqin/releases/latest/download/'
    'Install_loqin.exe'
)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/download')
def download():
    return render_template('thank-you.html')


@app.get('/installer')
def installer():
    return redirect(INSTALLER_URL)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)

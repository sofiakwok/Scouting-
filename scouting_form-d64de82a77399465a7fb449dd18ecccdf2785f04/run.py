import argparse, os, random, subprocess, sys, threading, time, webbrowser
if sys.version[0] == '2':
    from urllib2 import urlopen
    from urllib import urlretrieve
else:
    from urllib.request import urlopen, urlretrieve

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-?', '--help', action='help')
parser.add_argument('-h', '--host', default='0.0.0.0')
parser.add_argument('-p', '--port', type=int, default=8000)
parser.add_argument('-n', '--no-open', action='store_true', help="Don't open a web browser")
parser.add_argument('-r', '--reload', action='store_true', help="Reload changed files automatically")
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

import util
util.logging_init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
util.cwd = os.getcwd()
abspath = util.abspath

sk_path = '.secret_key.data'
if not os.path.isfile(sk_path):
    with open(sk_path, 'wb') as f:
        f.write(str(random.getrandbits(2000)).encode())

sys.path.append(abspath('packages.zip'))
try:
    import flask
except ImportError:
    try:
        urlretrieve('https://github.com/FRC830/scouting_form/releases/download/0.1/packages.zip', abspath('packages.zip'))
        import flask
    except ImportError:
        print('Module Flask not found... installing with pip')
        import pip
        pip.main(['install', '-r', 'requirements.txt', '--user'])
        import flask

import jinja2
app = flask.Flask("Scouting Form",
    static_folder=abspath('static'),
    static_url_path='/static'
)
# Load templates from scouting_form/web and scouting_form/../web
# http://stackoverflow.com/questions/13598363
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader([
        abspath('web'),
        abspath('..', 'web'),
    ]),
])
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

with open(sk_path, 'rb') as f:
    app.secret_key = f.read()
flask.current_app = app
import server

if not os.path.isdir('backups'):
    os.mkdir('backups')

def server_running():
    try:
        c = urlopen('http://localhost:%i/test' % (args.port)).read()
        if c == '1' or c == b'1':
            return True
    except Exception:
        pass
    return False

def open_page():
    if args.no_open:
        return
    if not os.environ.get('_SF_OPENED'):
        webbrowser.open('http://localhost:%i' % (args.port))
    os.environ['_SF_OPENED'] = '1'

def main(*_):
    # with the reloader active, this will run multiple times
    if not args.reload:
        OpenThread().start()
    elif not args.no_open:
        print('Web browser support disabled with --reload')
    print('Starting server')
    app.run(host=args.host, port=args.port, use_reloader=args.reload, debug=args.debug,
        threaded=False)

class OpenThread(threading.Thread):
    # If the main thread fails, this should stop waiting for the server to appear
    daemon = True
    def run(self):
        timeout = 10
        end_time = time.time() + timeout
        while time.time() < end_time:
            if server_running():
                print('Found server')
                open_page()
                return
            time.sleep(1)
        print('Could not find server')

if __name__ == '__main__':
    main()

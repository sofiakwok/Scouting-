import flask
import json
import os
import shutil
import subprocess
import sys
import time

import config
import exporter
import schedule_fetcher
import form_helper
import util
conf = config.config

app = flask.current_app
request = flask.request

custom = flask.Blueprint('custom', 'custom', static_url_path='/static/custom', static_folder=os.path.join('..', 'web'))
app.register_blueprint(custom)

def csv_filename(use_id=False):
    return conf.get('computer_name', '') + \
        ('_' + conf.get('export_id', '1') if use_id else '') + \
        "_scouting_data.csv"
def csv_path():
    return util.abspath('..',csv_filename())

@app.route('/')
def root():
    return flask.redirect(flask.url_for('form'))

@app.route('/test')
def test():
    return '1'

@app.route('/form', methods=('GET', 'POST'))
def form():
    if not conf.get('computer_name', ''):
        return flask.redirect(flask.url_for('config_form', return_to='/form'))
    f = form_helper.load_form(os.path.join(os.getcwd(), '..', 'web', 'fields.py'))()
    if f.validate_on_submit():
    	# this will save data entered on the form to a new line in the csv file
    	# Ex: Red1_scouting_data.csv (if running on computer Red1)
        fieldnames = []
        for field in f:
            if field.type != "CSRFTokenField":
                fieldnames.append(field.name)
        exporter.save_data(fieldnames, f.data, csv_path())
        return flask.redirect('/form')
    return flask.render_template('form.html', form=f, conf=conf)

@app.route('/config', methods=('GET', 'POST'))
def config_form(return_to=None):
    return_to = return_to or request.args.get('return_to', None)
    f = config.ConfigForm()
    success = False
    if f.validate_on_submit():
        for field in f:
            if field.type != "CSRFTokenField":
                conf.set(field.name, f.data[field.name])
        conf.save()
        if return_to:
            return flask.redirect(return_to)
        else:
            success = True
    return flask.render_template('config_form.html', form=f, success=success)

def get_export_path():
    path = conf.get('export_path', '')
    if not path:
        path = {'darwin': '/Volumes/SCOUTING', 'win32': 'E:\\'}.get(sys.platform, '')
    return path

@app.route('/export')
def export_form():
    return flask.render_template('export.html', default_path=get_export_path())

@app.route('/schedule')
def load_schedule():
    return flask.render_template('schedule_loader.html')

@app.route('/export/<command>')
def export_handler(command):
    def path_ok(path):
        return os.path.isdir(path) and not os.path.exists(os.path.join(path, csv_filename(use_id=True)))
    path = os.path.expanduser(request.args.get('path', get_export_path()))
    if command == 'info':
        return flask.jsonify(
            filename=csv_filename(use_id=True),
            path=path,
            default_path=get_export_path(),
            ok=path_ok(path),
            stats=stats(callback=dict),
        )
    elif command == 'check_path':
        ok = path_ok(path)
        if ok:
            conf.set('export_path', path)
            conf.save()
        return flask.jsonify(ok=ok)
    elif command == 'do_export':
        if not path_ok(path):
            return flask.jsonify(ok=False, error="Invalid path: %s" % path)
        try:
            shutil.copyfile(csv_path(), os.path.join(path, csv_filename(use_id=True)))
            shutil.move(csv_path(), util.abspath('backups', '%s-%s' % (csv_filename(), time.strftime('%d-%b-%Y-%H-%M-%S-%p'))))
            conf.set('export_id', conf.get('export_id', '1', type=int) + 1)
            return flask.jsonify(ok=True)
        except Exception as e:
            return flask.jsonify(ok=False, error=str(e))
    else:
        flask.abort(404)

@app.route('/schedule/load')
def schedule_handler():
    source = request.args.get('source')
    filename = request.args.get('filename')
    success = False
    result = schedule_fetcher.fetch(source, filename)
    if isinstance(result, tuple):
        message, success = result
    return flask.jsonify(res=message, success=success)

@app.route('/schedule/select')
def schedule_select():
	return flask.jsonify(file=subprocess.check_output([sys.executable, util.abspath('filedialog.py')]).strip())

@app.route('/schedule/current')
def match_data():
    if conf.get('station', 'none') == 'none':
        return flask.jsonify(error='No station specified')
    event_name = conf.get('event_name', '')
    if not event_name:
        return flask.jsonify(error='No match specified')
    path = util.abspath('match_schedules', event_name + '.json')
    try:
        with open(path) as f:
            raw_data = json.load(f)
    except (IOError, ValueError) as e:
        return flask.jsonify(error='Could not load match data: %s' % e)
    data = {}
    station = conf.get('station')
    for k, v in raw_data.items():
        if not isinstance(v, dict):
            return flask.jsonify(error='Bad match entry (%s)' % k)
        elif station not in raw_data[k]:
            return flask.jsonify(error='Match %s missing team ID for %s' % (k, station))
        else:
            data[k] = raw_data[k][station]
    return flask.jsonify(data)

@app.route('/stats')
def stats(callback=None):
    lines = 0
    if os.path.isfile(csv_path()):
        with open(csv_path()) as f:
            lines = max(0, len(f.readlines()) - 1)
    return (callback or flask.jsonify)(
        lines=lines
    )

@app.route('/shutdown')
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()
    return 'shutdown'


import flask_wtf
import itertools
import os
import wtforms.fields as fields
from wtforms.validators import DataRequired

import util

try:
    import ConfigParser as configparser
    from ConfigParser import SafeConfigParser
except ImportError:
    import configparser
    from configparser import SafeConfigParser

_none = object()
_pass_thru = lambda x: x
class ConfigFile:
    _section = 'config'
    def __init__(self, path):
        self.path = path
        self.parser = SafeConfigParser()
        self.parser.read(path)

    def has(self, key):
        return self.parser.has_option(self._section, key)

    def get(self, key, default=_none, type=_pass_thru):
        try:
            return type(self.parser.get(self._section, key))
        except configparser.Error:
            if default is _none:
                raise
            else:
                return type(default)

    def set(self, key, value):
        if self._section not in self.parser.sections():
            self.parser.add_section(self._section)
        self.parser.set(self._section, key, str(value))

    def save(self):
        with open(self.path, 'w') as f:
            self.parser.write(f)

config = ConfigFile('config.txt')

class ConfigForm(flask_wtf.Form):
    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        event_names = [('', '')]
        for f in os.listdir(util.abspath('match_schedules')):
            name, ext = os.path.splitext(f)
            if ext == '.json':
                event_names.append((name, name))
        self.event_name.choices = event_names

    computer_name = fields.StringField('Computer name',
        default=lambda: config.get('computer_name', None) or os.environ.get('COMPUTERNAME', None),
        validators=[DataRequired()])
    export_id = fields.IntegerField('Export ID',
        default=lambda: config.get('export_id', '1'),
        validators=[DataRequired()])
    station = fields.SelectField('Station',
        choices=[(name, name) for name in
            ['None'] + list(map(lambda item: ' '.join(map(str, item)),
                itertools.product(['Red', 'Blue'], [1, 2, 3])))],
        default=lambda: config.get('station', None))
    event_name = fields.SelectField('Event schedule',
        choices=[], default=lambda: config.get('event_name', ''))

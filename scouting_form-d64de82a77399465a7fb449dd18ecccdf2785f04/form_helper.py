import os
import sys

import util

def load_form(path):
    env = {}
    util.exec_file(path, env)
    form = env['Form']
    return form

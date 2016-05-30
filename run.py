#!/usr/bin/env python
import os, sys
os.execl(sys.executable, sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scouting_form', 'run.py'), *sys.argv[1:])

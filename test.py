#!/usr/bin/env python3

import os
from pprint import pprint
from shotgun_api3 import Shotgun
from collections import defaultdict

def pp(data):
    """debug output printing"""
    pprint(data, indent=2)

def dd(obj):
    """inspect available property and method names"""
    pp([symbol for symbol in sorted(dir(obj)) if not symbol.startswith('_')])

SERVER_PATH = os.environ['SG_SERVER_PATH']
SCRIPT_NAME = os.environ['SG_SCRIPT_NAME']
SCRIPT_KEY  = os.environ['SG_SCRIPT_KEY']


# instantiate a Shotgrid object
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)


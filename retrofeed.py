import argparse
import datetime as dt
import importlib.util
import os
import sys
import textwrap as tw
import time
import tomllib

from display import Display

VERSION = '1.0.0'
COPYRIGHT_YEAR = '2023'
CONFIG_FILENAME = 'config.toml'
EXPECTED_TABLES = ['display', 'segments', 'playlist']

def check_config_tables(config):
missing_tables = []
for table in EXPECTED_TABLES:
if table not in config:
missing_tables.append(table)
if len(missing_tables) > 0:
raise RuntimeError('Table(s) missing in config: ' + ', '.join(missing_tables))
bad_segments = []
for key in config['segments']:
if 'module' not in config['segments'][key]:
bad_segments.append(key)
if len(bad_segments) > 0:
raise RuntimeError('No module defined for segment(s) in config: ' + ', '.join(bad_segments))

def override_timings(config):
config['display']['cps'] = 1000
config['display']['newline_cps'] = 1000
config['display']['beat_seconds'] = 0.1
config['playlist']['segment_pause'] = 1
return config

def instantiate_segments(config, d):
segments = {}
shown_intros = []
for key in config['segments']:
mod_name = config['segments'][key]['module']
# Just in case the user put the .py on the end...
if mod_name.endswith('.py'):
mod_name = mod_name[0:-3]
# Import, instantiate, and add to segments dictionary
# using the specified key (which will match in playlist)
module = importlib.import_module('segments.' + mod_name)
segments[key] = module.Segment(d, config['segments'][key])
# If we haven't heard it already, give the module
# a chance to introduce itself...
intro = segments[key].intro
if intro is not None:
intro = intro.strip()
if intro != '' and intro not in shown_intros:
d.print(intro)
shown_intros.append(intro)
return segments

def parse_seg_key_and_fmt(seg):
seg_key = ''
seg_fmt = {}
if isinstance(seg, str):
seg_key = seg
elif isinstance(seg, list):
seg_key = seg[0]
if len(seg) > 1:
seg_fmt = seg[1]
return (seg_key, seg_fmt)

def show_title(d):
os.system('clear')  # Use 'clear' for UNIX systems like Raspberry Pi
for i in range(24):
print()
d.print('HELLO SEAN')
d.newline()

def get_args():
parser = argparse.ArgumentParser(description='Send a retro-style newsfeed to stdout.')
parser.add_argument('-f', '--fast', action='store_true', dest='fast_mode',
help='Use fast display speed, overriding config file settings')
parser.add_argument('-v', '--version', action='version', version='RetroFeed ' + VERSION)
parser.add_argument('filename', nargs='?', default=CONFIG_FILENAME,
help='Specify TOML configuration file. If omitted, defaults to config.toml')
return parser.parse_args()

###############################################################################

def main():
args = get_args()

if name == "main":
main()

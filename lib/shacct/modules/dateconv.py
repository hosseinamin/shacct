
from __future__ import print_function
from . import *
from time import gmtime, strftime, strptime
import re

def dateconv(date):
  date = date.strip()
  time = None
  pttrn = re.compile("^([0-9]{2})\s+([a-z]{3}),\s+([0-9]{4})$", re.I)
  match = pttrn.match(date)
  if match is not None:
    time = strptime(date, "%d %b, %Y")
  pttrn = re.compile("^([0-9]{2})/([0-9]{2})/([0-9]{4})$")
  match = pttrn.match(date)
  if match is not None:
    time = strptime(date, "%m/%d/%Y")
  if time is None:
    pttrn = re.compile("^([0-9]{2})\s+([a-z]{3})\s+([0-9]{4})\s+([0-9]{2}):([0-9]{2})$", re.I)
    match = pttrn.match(date)
    if match is not None:
      time = strptime(date, "%d %b %Y %H:%M")
  if time is None:
    pttrn = re.compile("^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})\\+([0-9]{2}):([0-9]{2})$")
    match = pttrn.match(date)
    if match is not None:
      time = strptime(date[:-6], "%Y-%m-%dT%H:%M:%S")
  if time is None:
    pttrn = re.compile("^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})$")
    match = pttrn.match(date)
    if match is not None:
      time = strptime(date, "%Y-%m-%dT%H:%M:%S")
  print(strftime("%a, %d %b %Y %H:%M:%S %Z", time() if time is None else time))

commands = {}
default_command = dateconv

def main(args):
  eval_command_type_a(commands, default_command, args)

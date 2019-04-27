from __future__ import print_function
from . import *
from shacct import config
from decimal import Decimal
import csv
import os.path
from time import gmtime, strftime, strptime
from util import moneyfmt

def centerify(s, n, c=" "):
  sl = len(s)
  while sl < n:
    if n - sl > 1:
      s = c + s + c
    else:
      s = c + s
    sl = len(s)
  return s
  
def prependn(s, n, c=" "):
  while len(s) < n:
    s = c + s
  return s
  
def upgrade01(filename="history", section='DEFAULT'):  
  with open(os.path.join(config.evalpath(config[section]['path']), filename), 'r') as f:
    with open(os.path.join(config.evalpath(config[section]['path']), filename+".new"), "w") as wf:
      writer = csv.writer(wf, delimiter="|")
      for row in csv.reader(f, delimiter="|"):
        if len(row) < 9 or row[0].startswith("#"):
          writer.writerow(row)
          continue
        row = map(lambda a:a.strip(), row)
        rtime = strptime(row[0].split(",")[1].strip(), "%d %b %Y %H:%M:%S")
        if row[2] == "conv":
          newrow = [ strftime("%Y-%m-%d %H:%M", rtime), centerify(row[1], 9), centerify(row[2], 8),
                     prependn(moneyfmt(Decimal(row[5]), 8 if row[4].lower() == "btc" else 2), 12),
                     prependn(moneyfmt(Decimal(row[8]), 8 if row[7].lower() == "btc" else 2), 12),
                     centerify(row[3], 9), centerify(row[6], 9), "  " + row[9] ]
        else:
          newrow = [ strftime("%Y-%m-%d %H:%M", rtime), centerify(row[1], 9), centerify(row[2], 8),
                     prependn(moneyfmt(Decimal(row[8]), 8 if row[7].lower() == "btc" else 2), 12),
                     prependn("", 12),
                     centerify(row[6], 9), centerify("", 9), "  " + (row[3] + " " + row[9]).strip() ]
        newrow = map(lambda a: a, newrow)
        writer.writerow(newrow)

commands = { }
default_command = upgrade01

def main(args):
  init_module(args)
  eval_command_type_a(commands, default_command, args)
